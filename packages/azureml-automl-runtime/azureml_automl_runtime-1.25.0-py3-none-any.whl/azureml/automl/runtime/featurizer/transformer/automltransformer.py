# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base logger class for all the transformers."""
from typing import List, Optional, Dict, Any
import logging

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from azureml.automl.runtime.column_purpose_detection.types import StatsAndColumnPurposeType
from azureml.automl.runtime.shared.types import DataSingleColumnInputType, DataInputType


class AutoMLTransformer(BaseEstimator, TransformerMixin):
    """Base logger class for all the transformers."""
    is_distributable = False
    is_separable = False

    @property
    def operator_name(self) -> Optional[str]:
        """Operator name for the engineering feature names."""
        return self._get_operator_name()

    def _get_operator_name(self) -> Optional[str]:
        return None

    @property
    def transformer_name(self) -> str:
        """Transform function name for the engineering feature names."""
        return self._get_transformer_name()

    def _get_transformer_name(self) -> str:
        # TODO Remove this and make it abstract
        return self.__class__.__name__

    def __getstate__(self):
        """
        Overridden to remove logger object when pickling.

        :return: this object's state as a dictionary
        """
        state = super(AutoMLTransformer, self).__getstate__()
        newstate = {**state, **self.__dict__}
        newstate["logger"] = None
        return newstate

    def _to_dict(self):
        """
        Create dict from transformer for serialization usage.

        :return: a dictionary
        """
        dct = {"args": [], "kwargs": {}}  # type: Dict[str, Any]
        return dct

    def get_memory_footprint(self, X: DataInputType, y: DataSingleColumnInputType) -> int:
        """
        Obtain memory footprint by adding this featurizer.

        :param X: Input data.
        :param y: Input label.
        :return: Amount of memory taken in bytes.
        """
        # TODO Make this method abstract once we have all featurizers implementing this method.
        return 0

    def transform(self, X: DataInputType) -> np.ndarray:
        raise NotImplementedError()
