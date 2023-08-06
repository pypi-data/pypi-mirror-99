# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Cast input to string."""
from typing import Optional, List
import logging

import numpy as np

from azureml.automl.core.constants import SupportedTransformersInternal as _SupportedTransformersInternal
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from ..automltransformer import AutoMLTransformer


class StringCastTransformer(AutoMLTransformer):
    """
    Cast input to string and lower case it if needed.

    The input and output type is same for this transformer.
    """

    def __init__(self) -> None:
        """Initialize the StringCastTransformer object."""
        super().__init__()
        self._transformer_name = _SupportedTransformersInternal.StringCast  # type: str
        self._operator_name = None  # type: Optional[str]

    def _get_operator_name(self) -> Optional[str]:
        return self._operator_name

    def _get_transformer_name(self) -> str:
        return self._transformer_name

    def _to_dict(self):
        """
        Create dict from transformer for  serialization usage.

        :return: a dictionary
        """
        dct = super(StringCastTransformer, self)._to_dict()
        dct['id'] = "string_cast"
        dct['type'] = 'text'

        return dct

    @function_debug_log_wrapped()
    def fit(self, x: np.ndarray, y: Optional[np.ndarray] = None) -> "StringCastTransformer":
        """
        Fit function for string cast transform.

        :param x: Input array.
        :param y: Target values.
        :return: The instance object: self.
        """
        return self

    @function_debug_log_wrapped()
    def transform(self, x: np.ndarray) -> np.ndarray:
        """
        Transform data x into array of strings.

        :param x: The data to transform.
        :return: The transformed data as array of strings.
        """
        return x.astype(str)

    def get_memory_footprint(self, X: DataInputType, y: DataSingleColumnInputType) -> int:
        """
        Obtain memory footprint estimate for this transformer.

        :param X: Input data.
        :param y: Input label.
        :return: Amount of memory taken.
        """
        # Note: This transformer won't be last transformer in featurization pipeline hence return # 0
        return 0
