import numpy as np
from mindsdb_native.libs.constants.mindsdb import *


def clean_df(df, target, transaction, is_classification, extra_params):
    """ Returns cleaned DF for nonconformist calibration """
    output_columns = transaction.lmd['predict_columns']
    ignored_columns = extra_params['columns_to_ignore']
    enc = transaction.hmd['label_encoders'].get(target, None)
    stats = transaction.lmd['stats_v2']

    y = df.pop(target).values

    if is_classification:
        if enc and isinstance(enc.categories_[0][0], str):
            cats = enc.categories_[0].tolist()
            y = np.array([cats.index(i) for i in y])
        y = y.astype(int)

    for key, value in stats.items():
        if key in df.columns and key in output_columns:
            df.pop(key)
    for col in ignored_columns:
        if col in df.columns:
            df.pop(col)
    return df, y


def set_conf_range(X, icp, target, typing_info, lmd, std_tol=1, group='__default'):
    """ Sets confidence level and returns it plus predictions regions """
    # numerical
    if typing_info['data_type'] == DATA_TYPES.NUMERIC or (typing_info['data_type'] == DATA_TYPES.SEQUENTIAL and
                                                          DATA_TYPES.NUMERIC in typing_info['data_type_dist'].keys()):
        # ICP gets all possible bounds (shape: (B, 2, 99))
        all_ranges = icp.predict(X.values)

        # iterate over confidence levels until spread >= a multiplier of the dataset stddev
        for tol in [std_tol, std_tol + 1, std_tol + 2]:
            for significance in range(99):
                ranges = all_ranges[:, :, significance]
                spread = np.mean(ranges[:, 1] - ranges[:, 0])
                tolerance = lmd['stats_v2'][target]['train_std_dev'][group] * tol

                if spread <= tolerance:
                    confidence = (99 - significance) / 100
                    if lmd['stats_v2'][target].get('positive_domain', False):
                        ranges[ranges < 0] = 0
                    return confidence, ranges
        else:
            ranges = all_ranges[:, :, 0]
            if lmd['stats_v2'][target].get('positive_domain', False):
                ranges[ranges < 0] = 0
            return 0.9901, ranges

    # categorical
    elif (typing_info['data_type'] == DATA_TYPES.CATEGORICAL or  # categorical
          (typing_info['data_type'] == DATA_TYPES.SEQUENTIAL and  # time-series w/ cat target
           DATA_TYPES.CATEGORICAL in typing_info['data_type_dist'].keys())) and \
            lmd['stats_v2'][target]['typing']['data_subtype'] != DATA_SUBTYPES.TAGS:  # no tag support yet

        pvals = icp.predict(X.values)
        conf = np.subtract(1, pvals.min(axis=1)).mean()
        return conf, pvals

    # default
    return 0.005, np.zeros((X.shape[0], 2))


def get_numerical_conf_range(all_confs, predicted_col, stats, std_tol=1, group='__default', error_rate=None):
    """ Gets prediction bounds for numerical targets, based on ICP estimation and width tolerance
        error_rate: pre-determined error rate for the ICP, used in anomaly detection tasks to adjust the
        threshold sensitivity.

        :param all_confs: numpy.ndarray, all possible bounds depending on confidence level
        :param predicted_col: str
        :param stats: dict
        :param std_tol: int
        :param group: str
        :param error_rate: float (1 >= , can be specified to bypass automatic confidence/bound detection
    """
    if not isinstance(error_rate, float):
        error_rate = None

    if error_rate is None:
        significances = []
        conf_ranges = []
        std_dev = stats[predicted_col]['train_std_dev'][group]

        tolerance = std_dev * std_tol

        for sample_idx in range(all_confs.shape[0]):
            sample = all_confs[sample_idx, :, :]
            for idx in range(sample.shape[1]):
                significance = (99 - idx) / 100
                diff = sample[1, idx] - sample[0, idx]
                if diff <= tolerance:
                    conf_range = list(sample[:, idx])
                    significances.append(significance)
                    conf_ranges.append(conf_range)
                    break
            else:
                significances.append(0.9991)  # default: confident that value falls inside big bounds
                bounds = sample[:, 0]
                sigma = (bounds[1] - bounds[0]) / 4
                conf_range = [bounds[0] - sigma, bounds[1] + sigma]
                conf_ranges.append(conf_range)

        conf_ranges = np.array(conf_ranges)
    else:
        # fixed error rate
        error_rate = max(0.01, min(1.0, error_rate))
        conf = 1 - error_rate
        conf_idx = int(100*error_rate) - 1
        conf_ranges = all_confs[:, :, conf_idx]
        significances = [conf for _ in range(conf_ranges.shape[0])]

    if stats[predicted_col].get('positive_domain', False):
        conf_ranges[conf_ranges < 0] = 0
    return significances, conf_ranges


def get_categorical_conf(all_confs, conf_candidates):
    """ Gets ICP confidence estimation for categorical targets.
    Prediction set is always unitary and includes only the predicted label.
    :param all_confs: numpy.ndarray, all possible label sets depending on confidence level
    :param conf_candidates: list, includes preset confidence levels to check
    """
    significances = []
    for sample_idx in range(all_confs.shape[0]):
        sample = all_confs[sample_idx, :, :]
        for idx in range(sample.shape[1]):
            conf = (99 - conf_candidates[idx]) / 100
            if np.sum(sample[:, idx]) == 1:
                significances.append(conf)
                break
        else:
            significances.append(0.005)  # default: not confident label is the predicted one
    return significances


def get_anomalies(bounds, observed_series, cooldown=1):
    anomalies = []
    counter = 0

    for (l, u), t in zip(bounds, observed_series):
        if t is not None:
            anomaly = not (l <= t <= u)

            if anomaly and (counter == 0 or counter >= cooldown):
                anomalies.append(anomaly)  # new anomaly event triggers, reset counter
                counter = 1
            elif anomaly and counter < cooldown:
                anomalies.append(False)  # overwrite as not anomalous if still in cooldown
                counter += 1
            else:
                anomalies.append(anomaly)
                counter = 0
        else:
            anomalies.append(None)
            counter += 1

    return anomalies
