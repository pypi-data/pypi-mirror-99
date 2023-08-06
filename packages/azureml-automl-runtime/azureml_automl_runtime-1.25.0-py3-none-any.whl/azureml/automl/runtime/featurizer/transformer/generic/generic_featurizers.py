# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Container for generic featurizers."""
from typing import Any

from nimbusml.preprocessing.missing_values import Handler as NimbusMLMissingValuesHandler
from nimbusml.preprocessing.schema import ColumnSelector as NimbusMLColumnSelector
from sklearn.cluster import MiniBatchKMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MaxAbsScaler

from azureml.automl.core.shared import constants
from .imputation_marker import ImputationMarker
from .lambda_transformer import LambdaTransformer


class GenericFeaturizers:
    """Container for generic featurizers."""

    @classmethod
    def imputation_marker(cls, *args: Any, **kwargs: Any) -> ImputationMarker:
        """Create imputation marker."""
        return ImputationMarker()

    @classmethod
    def lambda_featurizer(cls, *args: Any, **kwargs: Any) -> LambdaTransformer:
        """Create lambda featurizer."""
        return LambdaTransformer(*args, **kwargs)

    @classmethod
    def imputer(cls, *args: Any, **kwargs: Any) -> SimpleImputer:
        """Create Imputer."""
        imputer = SimpleImputer(*args, **kwargs)
        # Workaround to ensure featurization setting maps to object
        setattr(imputer, '_transformer_name', 'Imputer')
        return imputer

    @classmethod
    def minibatchkmeans_featurizer(cls, *args: Any, **kwargs: Any) -> MiniBatchKMeans:
        """Create mini batch k means featurizer."""
        return MiniBatchKMeans(*args, **kwargs)

    @classmethod
    def maxabsscaler(cls, *args: Any, **kwargs: Any) -> MaxAbsScaler:
        """Create maxabsscaler featurizer."""
        return MaxAbsScaler(*args, **kwargs)

    @classmethod
    def nimbus_missing_values_handler(cls, *args: Any, **kwargs: Any) -> NimbusMLMissingValuesHandler:
        """Create Imputer."""
        return NimbusMLMissingValuesHandler(*args, **kwargs)

    @classmethod
    def nimbus_column_selector(cls, *args: Any, **kwargs: Any) -> NimbusMLColumnSelector:
        """Create Column Selector transform."""
        return NimbusMLColumnSelector(*args, **kwargs)
