# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Wrapper over pandas.cut for binning the train data into intervals and then applying them to test data."""
from typing import Optional
import logging

import pandas as pd

from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.shared.transformer_runtime_exceptions import (
    BinTransformerRuntimeNotCalledException)
from ..automltransformer import AutoMLTransformer
from azureml.automl.core.constants import SupportedTransformersInternal as _SupportedTransformersInternal


class BinTransformer(AutoMLTransformer):
    """
    Wrapper over pandas.cut for binning the train data into intervals and then applying them to test data.

    :param num_bins: Number of bins for binning the values into discrete
    intervals.
    :type num_bins: int
    """

    def __init__(self, num_bins: int = 5):
        """
        Construct the BinTransformer.

        :param num_bins: Number of bins for binning the values into discrete intervals.
        """
        super().__init__()
        self._num_bins = num_bins
        self._bins = None
        self._transformer_name = _SupportedTransformersInternal.BinTransformer

    def _get_transformer_name(self) -> str:
        return self._transformer_name

    def _to_dict(self):
        """
        Create dict from transformer for  serialization usage.

        :return: a dictionary
        """
        dct = super(BinTransformer, self)._to_dict()
        dct['id'] = "bin_transformer"
        dct['type'] = "numeric"
        dct['kwargs']['num_bins'] = self._num_bins

        return dct

    @function_debug_log_wrapped()
    def fit(self, x, y=None):
        """
        Identify the distribution of values with repect to the number of specified bins.

        :param x: The data to transform.
        :type x: numpy.ndarray or pandas.core.series.Series
        :param y: Target values.
        :type y: numpy.ndarray
        :return: The instance object: self.
        """
        _, self._bins = pd.cut(x, self._num_bins, retbins=True)
        return self

    @function_debug_log_wrapped()
    def transform(self, x):
        """
        Return the bins identified for the input values.

        :param x: The data to transform.
        :type x: numpy.ndarray or pandas.core.series.Series
        :return: The transformed data.
        """
        if self._bins is None:
            raise BinTransformerRuntimeNotCalledException("BinTransformer not fit", has_pii=False)
        return pd.cut(x, bins=self._bins, labels=False)
