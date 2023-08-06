from mindsdb_native.libs.constants.mindsdb import *
from mindsdb_native.libs.helpers.general_helpers import get_value_bucket

from sklearn.metrics import confusion_matrix
import random


class AccStats:
    """
    Computes accuracy stats and a confusion matrix for the validation dataset
    """

    def __init__(self, col_stats, col_name, input_columns):
        """
        Chose the algorithm to use for the rest of the model
        As of right now we go with BernoulliNB
        """
        self.col_stats = col_stats
        self.col_name = col_name
        self.input_columns = input_columns

        if 'percentage_buckets' in col_stats:
            self.buckets = col_stats['percentage_buckets']

    def fit(self, real_df, predictions_arr, missing_col_arr, hmd=None):
        """
        :param real_df: A dataframe with the real inputs and outputs for every row
        :param predictions_arr: An array containing arrays of predictions, one containing the "normal" predictions and the rest containing predictions with various missing column
        :param missing_col_arr: The missing columns for each of the prediction arrays, same order as the arrays in `predictions_arr`, starting from the second element of `predictions_arr` (The first is assumed to have no missing columns)
        """
        self.real_values_bucketized = []
        self.normal_predictions_bucketized = []
        self.numerical_samples_arr = []

        column_indexes = {}
        for i, col in enumerate(self.input_columns):
            column_indexes[col] = i

        real_present_inputs_arr = []
        for _, row in real_df.iterrows():
            present_inputs = [1] * len(self.input_columns)
            for i, col in enumerate(self.input_columns):
                if str(row[col]) in ('None', 'nan', '', 'Nan', 'NAN', 'NaN'):
                    present_inputs[i] = 0
            real_present_inputs_arr.append(present_inputs)

        for n in range(len(predictions_arr)):
            for m in range(len(predictions_arr[n][self.col_name])):
                row = real_df.iloc[m]

                real_value = row[self.col_name]
                predicted_value = predictions_arr[n][self.col_name][m]

                try:
                    predicted_value = predicted_value if self.col_stats['typing']['data_type'] != DATA_TYPES.NUMERIC else float(predicted_value)
                except Exception:
                    predicted_value = None

                try:
                    real_value = real_value if self.col_stats['typing']['data_type'] != DATA_TYPES.NUMERIC else float(real_value)
                except Exception:
                    real_value = None

                if self.buckets is not None:
                    predicted_value_b = get_value_bucket(predicted_value, self.buckets, self.col_stats, hmd)
                    real_value_b = get_value_bucket(real_value, self.buckets, self.col_stats, hmd)
                else:
                    predicted_value_b = predicted_value
                    real_value_b = real_value

                has_confidence_range = self.col_stats['typing']['data_type'] == DATA_TYPES.NUMERIC and f'{self.col_name}_confidence_range' in predictions_arr[n]

                predicted_range = predictions_arr[n][f'{self.col_name}_confidence_range'][m] if has_confidence_range else (None, None)

                if n == 0:
                    self.real_values_bucketized.append(real_value_b)
                    self.normal_predictions_bucketized.append(predicted_value_b)
                    if has_confidence_range:
                        self.numerical_samples_arr.append((real_value,predicted_range))

                feature_existance = real_present_inputs_arr[m]
                if n > 0:
                    for missing_col in missing_col_arr[n - 1]:
                        feature_existance[self.input_columns.index(missing_col)] = 0

    def get_accuracy_stats(self):
        bucket_accuracy = {}
        bucket_acc_counts = {}
        for i, bucket in enumerate(self.normal_predictions_bucketized):
            if bucket not in bucket_acc_counts:
                bucket_acc_counts[bucket] = []

            if len(self.numerical_samples_arr) != 0:
                bucket_acc_counts[bucket].append(self.numerical_samples_arr[i][1][0] < self.numerical_samples_arr[i][0] < self.numerical_samples_arr[i][1][1])
            else:
                bucket_acc_counts[bucket].append(1 if bucket == self.real_values_bucketized[i] else 0)

        for bucket in bucket_acc_counts:
            bucket_accuracy[bucket] = sum(bucket_acc_counts[bucket])/len(bucket_acc_counts[bucket])

        accuracy_count = []
        for counts in list(bucket_acc_counts.values()):
            accuracy_count += counts

        overall_accuracy = sum(accuracy_count) / len(accuracy_count)

        for bucket in range(len(self.buckets)):
            if bucket not in bucket_accuracy:
                if bucket in self.real_values_bucketized:
                    # If it was never predicted, but it did exist as a real value, then assume 0% confidence when it does get predicted
                    bucket_accuracy[bucket] = 0

        for bucket in range(len(self.buckets)):
            if bucket not in bucket_accuracy:
                # If it wasn't seen either in the real values or in the predicted values, assume average confidence (maybe should be 0 instead ?)
                bucket_accuracy[bucket] = overall_accuracy

        accuracy_histogram = {
            'buckets': list(bucket_accuracy.keys())
            ,'accuracies': list(bucket_accuracy.values())
        }

        labels= list(set([*self.real_values_bucketized, *self.normal_predictions_bucketized]))
        matrix = confusion_matrix(self.real_values_bucketized, self.normal_predictions_bucketized, labels=labels)
        matrix = [[int(y) if str(y) != 'nan' else 0 for y in x] for x in matrix]

        bucket_values = [self.buckets[i] if i < len(self.buckets) else None for i in labels]

        cm = {
            'matrix': matrix,
            'predicted': bucket_values,
            'real': bucket_values
        }

        accuracy_samples = None
        if len(self.numerical_samples_arr) > 0:
            nr_samples = min(400,len(self.numerical_samples_arr))
            sampled_numerical_samples_arr = random.sample(self.numerical_samples_arr, nr_samples)
            accuracy_samples = {
                'y': [x[0] for x in sampled_numerical_samples_arr]
                ,'x': [x[1] for x in sampled_numerical_samples_arr]
            }

        return overall_accuracy, accuracy_histogram, cm, accuracy_samples
