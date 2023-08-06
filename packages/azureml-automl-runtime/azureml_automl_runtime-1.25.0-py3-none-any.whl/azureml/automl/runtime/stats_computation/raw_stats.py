# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for computing feature stats_computation from raw features."""
from typing import DefaultDict, Optional
import copy
import json
from collections import defaultdict

import numpy as np
import pandas


from azureml.automl.core.constants import FeatureType as _FeatureType
from azureml.automl.runtime.shared.utilities import _get_num_unique
from azureml.automl.core.shared.utilities import _check_if_column_data_type_is_datetime,\
    _check_if_column_data_type_is_numerical, is_known_date_time_format
from azureml.automl.runtime.shared import utilities as runtime_utilities


class RawFeatureStats:
    """
    Class for computing feature stats_computation from raw features.

    :param raw_column: Column having raw data.
    :type raw_column: pandas.core.series.Series
    """

    # max size in characters for ngram
    _max_ngram = 3
    # Hashing seed value for murmurhash
    _hashing_seed_value = 314489979

    def __init__(self, raw_column: pandas.core.series.Series):
        """
        Calculate stats_computation for the input column.

        These stats_computation are needed for deciding the data type of the column.

        :param raw_column: Column having raw data.
        :type raw_column: numpy.ndarray
        """
        # --- Common stats for all data types --- #
        # Drop all invalid entries from the column
        non_na_raw_column = raw_column.dropna()
        # Get the column type
        self.column_type = runtime_utilities._get_column_data_type_as_str(non_na_raw_column.values)
        if self.column_type == "string":
            # remove empty string
            non_na_raw_column = non_na_raw_column[non_na_raw_column.astype(bool)]
        # Number of unique values in the column
        self.num_unique_vals = _get_num_unique(non_na_raw_column)
        # Total number of non nan values in the column
        self.total_number_vals = non_na_raw_column.shape[0]
        # Total number of values in the column including nans
        self.total_number_vals_including_nans = raw_column.shape[0]
        # Number of missing values in the column
        self.num_na = raw_column.shape[0] - non_na_raw_column.shape[0]
        # Create a series having lengths of the entries in the column
        # Convert values in the column to strings
        non_na_raw_column_str = non_na_raw_column.apply(str)
        self.lengths = non_na_raw_column_str.apply(len)
        # Calculate the number of lengths of the entries in the column
        self.num_unique_lens = 0
        # Average lengths of an entry in the column
        self.average_entry_length = 0
        # Average number of spaces in an entry in the column
        self.average_number_spaces = 0
        # Ratio of number of unique value to total number of values
        self.cardinality_ratio = 0
        # Check if the column is of type datetime
        self.is_datetime = False
        # Check if the column has all nan values
        self.is_all_nan = False
        # Median of unicode values to detemine language
        self.unicode_median_value = 0

        # Get stats based on the type of data
        if self.total_number_vals == 0:
            self.is_all_nan = True
        elif _check_if_column_data_type_is_numerical(self.column_type):
            self._fill_stats_if_numeric_feature(raw_column)
        elif _check_if_column_data_type_is_datetime(self.column_type):
            self.is_datetime = is_known_date_time_format(
                str(raw_column[raw_column.first_valid_index()]))
        elif self._check_if_column_is_datetime(non_na_raw_column):
            self.is_datetime = True
        else:
            self._fill_stats_if_text_or_categorical_feature(non_na_raw_column_str)

    def _fill_stats_if_numeric_feature(self, raw_column: pandas.Series) -> None:
        """
        Get the stats applicable to numeric types.

        :param raw_column: Column having raw data.
        :type raw_column: pandas.core.series.Series
        """
        # TODO: Maybe add max/min value from the data set
        pass

    def _fill_stats_if_text_or_categorical_feature(self, raw_column_str: pandas.Series) -> None:
        """
        Get the stats applicable to text or categorical types.

        :param raw_column_str: raw column converted to string type.
        :type raw_column_str: pandas.core.series.Series
        """
        self.num_unique_lens = self.lengths.unique().shape[0]

        for column_entry in raw_column_str:
            self.average_number_spaces += column_entry.count(' ')

        if self.total_number_vals > 0:
            self.average_entry_length = 1.0 * (sum(self.lengths) / self.total_number_vals)
            self.average_number_spaces /= 1.0 * self.total_number_vals
            self.cardinality_ratio = (1.0 * self.num_unique_vals) / self.total_number_vals
            self.unicode_median_value = np.median(np.array([ord(c) for c in raw_column_str.str.cat(sep='\n')]))

    def _check_if_column_is_datetime(self, raw_column: pandas.Series) -> bool:
        """
        Take a raw column and return 'True' if this is detected as datetime and 'False' otherwise.

        :param raw_column: Column having raw data.
        :type raw_column: pandas.core.series.Series
        :return: True is detected type is datetime and False otherwise
        """
        # If the first valid entry is not datetime format, then return False
        if not is_known_date_time_format(
                str(raw_column[raw_column.first_valid_index()])):
            return False

        # Convert non_na to strings
        raw_column_str = raw_column.apply(str)

        # Detect if the column has date time data in a known format
        num_dates = np.sum(raw_column_str.apply(is_known_date_time_format))

        # Check if all the valid strings match the date time format
        if num_dates != raw_column_str.shape[0]:
            return False

        # Try inferring dates
        try:
            actual_dates = pandas.to_datetime(raw_column_str, infer_datetime_format=True)
        except BaseException:
            # If dates cannot be inferred, then return False
            return False

        # Check if all the valid entries pass by pandas date time function
        if actual_dates.shape[0] == raw_column_str.shape[0] and raw_column_str.shape[0] > 0:
            return True

        # date time not detected case
        return False

    def __str__(self):
        dct = copy.deepcopy(self.__dict__)
        dct.pop('lengths')
        return json.dumps(dct)


class PreprocessingStatistics:
    """
    Keeps statistics about the pre-processing stage in AutoML.

    Records the number of various feature types detected from
    the raw data
    """

    def __init__(self):
        """Initialize all statistics about the raw data."""
        # Dictionary to capture all raw feature stats_computation
        self.num_raw_feature_type_detected = defaultdict(int)   # type: DefaultDict[str, int]

    def update_raw_feature_stats(self, feature_type: str, column_count: int = 1) -> None:
        """Increment the counters for different types of features."""
        if feature_type in _FeatureType.FULL_SET:
            self.num_raw_feature_type_detected[feature_type] += column_count

    def get_raw_data_stats(self) -> str:
        """Return the string for overall raw feature stats_computation."""
        str_overall_raw_stats = 'The stats_computation for raw data are following:-'
        for feature_type in _FeatureType.FULL_SET:
            str_overall_raw_stats += \
                '\n\tNumber of ' + feature_type + ' features: ' + \
                str(self.num_raw_feature_type_detected[feature_type])

        return str_overall_raw_stats
