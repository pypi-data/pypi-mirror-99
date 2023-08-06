# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Validation for AutoML metrics."""
import logging
import numpy as np
import sklearn.utils
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import AutoMLInternal
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.reference_codes import ReferenceCodes

from sklearn.base import TransformerMixin
from typing import Dict, List, Optional

from azureml.automl.runtime.shared.score import constants, utilities
from azureml.automl.runtime.shared.score._metric_base import NonScalarMetric
from azureml.automl.core.shared.exceptions import ValidationException


logger = logging.getLogger(__name__)


def validate_classification(y_test: np.ndarray,
                            y_pred_probs: np.ndarray,
                            metrics: List[str],
                            class_labels: np.ndarray,
                            train_labels: np.ndarray,
                            sample_weight: Optional[np.ndarray],
                            y_transformer: Optional[TransformerMixin]) -> None:
    """
    Validate the inputs for scoring classification.

    :param y_test: Target values.
    :param y_pred_probs: The predicted probabilities for all classes.
    :param metrics: Metrics to compute.
    :param class_labels: All classes found in the full dataset.
    :param train_labels: Classes as seen (trained on) by the trained model.
    :param sample_weight: Weights for the samples.
    :param y_transformer: Used to inverse transform labels.
    """
    for metric in metrics:
        Contract.assert_true(
            metric in constants.CLASSIFICATION_SET, "Metric {} not a valid classification metric".format(metric),
            target="metric", reference_code=ReferenceCodes._METRIC_INVALID_CLASSIFICATION_METRIC
        )

    Contract.assert_value(class_labels, "class_labels")
    Contract.assert_value(train_labels, "train_labels")

    _check_array_shapes_1d(y_test, y_pred_probs, 'y_test', 'y_pred_probs')

    array_dict = {
        'class_labels': class_labels,
        'train_labels': train_labels,
        'y_test': y_test,
    }
    _check_arrays_same_type(array_dict, check_numeric_type=False)

    _check_dim(y_test, 'y_test', 1)
    _check_dim(y_pred_probs, 'y_pred_probs', 2)

    _check_array(class_labels, 'class_labels', ensure_2d=False)
    _check_array(train_labels, 'train_labels', ensure_2d=False)
    _check_array(y_test, 'y_test', ensure_2d=False)
    _check_array(y_pred_probs, 'y_pred_probs')
    if sample_weight is not None:
        _check_array(sample_weight, 'sample_weight', ensure_2d=False)

    unique_classes = np.unique(class_labels)
    Contract.assert_true(unique_classes.shape[0] >= 2,
                         message="Number of classes must be at least 2 for classification (got {})".format(
                             unique_classes.shape[0]),
                         target="num_unique_classes", log_safe=True)

    if sample_weight is not None:
        Contract.assert_true(sample_weight.dtype.kind in set('fiu'),
                             message="Type of sample_weight must be numeric (got type {})".format(sample_weight.dtype),
                             target="sample_weight", log_safe=True)

        Contract.assert_true(y_test.shape[0] == sample_weight.shape[0],
                             message="Number of samples does not match in y_test ({}) and sample_weight ({})".format(
                                 y_test.shape[0], sample_weight.shape[0]),
                             target="sample_weight", log_safe=True)

    Contract.assert_true(train_labels.shape[0] == y_pred_probs.shape[1],
                         message="train_labels.shape[0] ({}) does not match y_pred_probs.shape[1] ({}).".format(
                             train_labels.shape[0], y_pred_probs.shape[1]), log_safe=True)

    set_diff = np.setdiff1d(train_labels, class_labels)
    if set_diff.shape[0] != 0:
        logger.error("train_labels contains values not present in class_labels")
        message = "Labels {} found in train_labels are missing from class_labels.".format(set_diff)
        raise ValidationException._with_error(
            AzureMLError.create(
                AutoMLInternal, target="train_labels",
                reference_code=ReferenceCodes._METRIC_VALIDATION_EXTRANEOUS_TRAIN_LABELS, error_details=message)
        )

    set_diff = np.setdiff1d(np.unique(y_test), class_labels)
    if set_diff.shape[0] != 0:
        logger.error("y_test contains values not present in class_labels")
        message = "Labels {} found in y_test are missing from class_labels.".format(set_diff)
        raise ValidationException._with_error(
            AzureMLError.create(
                AutoMLInternal, target="y_test",
                reference_code=ReferenceCodes._METRIC_VALIDATION_EXTRANEOUS_YTEST_LABELS, error_details=message)
        )


def log_classification_debug(y_test: np.ndarray,
                             y_pred_probs: np.ndarray,
                             class_labels: np.ndarray,
                             train_labels: np.ndarray,
                             sample_weight: Optional[np.ndarray] = None) -> None:
    """
    Log shapes of classification inputs for debugging.

    :param y_pred_probs: The predicted probabilities for all classes.
    :param class_labels: All classes found in the full dataset.
    :param train_labels: Classes as seen (trained on) by the trained model.
    :param sample_weight: Weights for the samples.
    """
    unique_y_test = np.unique(y_test)
    debug_data = {
        'y_test': y_test.shape,
        'y_pred_probs': y_pred_probs.shape,
        'unique_y_test': unique_y_test.shape,
        'class_labels': class_labels.shape,
        'train_labels': train_labels.shape,
        'n_missing_train': np.setdiff1d(class_labels, train_labels).shape[0],
        'n_missing_valid': np.setdiff1d(class_labels, unique_y_test).shape[0],
        'sample_weight': None if sample_weight is None else sample_weight.shape
    }

    logger.info("Classification metrics debug: {}".format(debug_data))


def validate_regression(y_test: np.ndarray,
                        y_pred: np.ndarray,
                        metrics: List[str]) -> None:
    """
    Validate the inputs for scoring regression.

    :param y_test: Target values.
    :param y_pred: Target predictions.
    :param metrics: Metrics to compute.
    """
    for metric in metrics:
        Contract.assert_true(
            metric in constants.REGRESSION_SET, "Metric {} not a valid regression metric".format(metric),
            target="metric", reference_code=ReferenceCodes._METRIC_INVALID_REGRESSION_METRIC
        )

    _check_array_shapes_1d(y_test, y_pred, 'y_test', 'y_pred')
    _check_array(y_test, 'y_test', ensure_2d=False)
    _check_array(y_pred, 'y_pred', ensure_2d=False)


def log_regression_debug(y_test: np.ndarray,
                         y_pred: np.ndarray,
                         y_min: Optional[float],
                         y_max: Optional[float],
                         sample_weight: Optional[np.ndarray] = None) -> None:
    """
    Log shapes of regression inputs for debugging.

    :param y_test: Target values.
    :param y_pred: Predicted values.
    :param y_min: Minimum target value.
    :param y_max: Maximum target value.
    :param sample_weight: Weights for the samples.
    """
    min_max_equal = None if None in [y_min, y_max] else y_min == y_max
    debug_data = {
        'y_test': y_test.shape,
        'y_pred': y_pred.shape,
        'y_test_unique': np.unique(y_test).shape[0],
        'y_pred_unique': np.unique(y_pred).shape[0],
        'y_test_has_negative': (y_test < 0).sum() > 0,
        'y_pred_has_negative': (y_pred < 0).sum() > 0,
        'min_max_equal': min_max_equal,
        'sample_weight': None if sample_weight is None else sample_weight.shape
    }

    logger.info("Regression metrics debug: {}".format(debug_data))


def validate_forecasting(y_test: np.ndarray,
                         y_pred: np.ndarray,
                         horizons: np.ndarray,
                         metrics: List[str]) -> None:
    """
    Validate the inputs for scoring forecasting.

    :param y_test: Target values.
    :param y_pred: Target predictions.
    :param horizons: Forecast horizons per sample.
    :param metrics: Metrics to compute.
    """
    for metric in metrics:
        Contract.assert_true(
            metric in constants.FORECASTING_SET, "Metric {} not a valid forecasting metric".format(metric),
            target="metric", reference_code=ReferenceCodes._METRIC_INVALID_FORECASTING_METRIC
        )

    _check_array_shapes_1d(y_test, y_pred, 'y_test', 'y_pred')
    _check_array_shapes_1d(y_test, horizons, 'y_test', 'horizons')
    _check_array(y_test, 'y_test', ensure_2d=False)
    _check_array(y_pred, 'y_pred', ensure_2d=False)
    _check_array(horizons, 'horizons', ensure_2d=False, allow_none=True)


def log_forecasting_debug(y_test: np.ndarray,
                          y_pred: np.ndarray,
                          horizons: np.ndarray,
                          y_min: Optional[float],
                          y_max: Optional[float],
                          sample_weight: Optional[np.ndarray] = None) -> None:
    """
    Log shapes of forecasting inputs for debugging.

    :param y_test: Target values.
    :param y_pred: Predicted values.
    :param horizons: Forecast horizons per sample.
    :param y_min: Minimum target value.
    :param y_max: Maximum target value.
    :param sample_weight: Weights for the samples.
    """
    min_max_equal = None if None in [y_min, y_max] else y_min == y_max
    debug_data = {
        'y_test': y_test.shape,
        'y_pred': y_pred.shape,
        'horizons': horizons.shape,
        'y_test_unique': np.unique(y_test).shape[0],
        'y_pred_unique': np.unique(y_pred).shape[0],
        'y_test_has_negative': (y_test < 0).sum() > 0,
        'y_pred_has_negative': (y_pred < 0).sum() > 0,
        'min_max_equal': min_max_equal,
        'sample_weight': None if sample_weight is None else sample_weight.shape
    }

    logger.info("Forecasting metrics debug: {}".format(debug_data))


def _check_array_shapes_1d(array_a: np.ndarray,
                           array_b: np.ndarray,
                           array_a_name: str,
                           array_b_name: str) -> None:
    """
    Validate that two arrays have the same shape in the first dimension.

    :array_a: First array.
    :array_b: Second array.
    :array_a_name: First array name.
    :array_b_name: Second array name.
    """
    Contract.assert_value(array_a, array_a_name)
    Contract.assert_value(array_b, array_b_name)
    message = "Number of samples does not match in {} ({}) and {} ({})".format(
        array_a_name, array_a.shape[0], array_b_name, array_b.shape[0])
    Contract.assert_true(array_a.shape[0] == array_b.shape[0], message=message, log_safe=True)


def _check_array(arr: np.ndarray,
                 name: str,
                 ensure_2d: bool = True,
                 allow_none: bool = False) -> None:
    """
    Check the array for reasonable values.

    :param arr: Array to check.
    :param name: Array name.
    :param ensure_2d: Extra check to ensure 2 dimensional.
    """
    if arr.dtype.kind in set('bcfiu'):
        Contract.assert_true(~np.isnan(arr).any(), message="Elements of {} cannot be NaN".format(name),
                             log_safe=True)
        Contract.assert_true(np.isfinite(arr).all(), message="Elements of {} cannot be infinite".format(name),
                             log_safe=True)

    if not np.issubdtype(arr.dtype, np.str_) and not allow_none:
        try:
            sklearn.utils.check_array(arr, ensure_2d=ensure_2d)
        except ValueError:
            raise ValidationException._with_error(
                AzureMLError.create(
                    AutoMLInternal, target=name, error_details="{} failed sklearn.utils.check_array().".format(name)
                )
            )


def _check_arrays_same_type(array_dict: Dict[str, np.ndarray], check_numeric_type: bool = True) -> None:
    """
    Check that multiple arrays have the same types.

    :param array_dict: Dictionary from array name to array.
    :param check_numeric_type: whether to compare numeric arrays
    """
    items = list(array_dict.items())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            i_type, j_type = items[i][1].dtype, items[j][1].dtype
            i_name, j_name = items[i][0], items[j][0]

            # Handle equivalent types like int32/int64 integers, U1/U2 strings
            if check_numeric_type:
                # check if two numeric types are equivalent types
                if np.issubdtype(i_type, np.integer) and np.issubdtype(j_type, np.integer):
                    continue
                if np.issubdtype(i_type, np.floating) and np.issubdtype(j_type, np.floating):
                    continue
            else:
                # if they are both numeric, then continue
                if np.issubdtype(i_type, np.number) and np.issubdtype(j_type, np.number):
                    continue
            if np.issubdtype(i_type, np.str_) and np.issubdtype(j_type, np.str_):
                continue

            # Handle all other types
            Contract.assert_true(i_type == j_type,
                                 message="{} ({}) does not have the same type as {} ({})".format(
                                     i_name, i_type, j_name, j_type),
                                 log_safe=True)


def _check_dim(arr: np.ndarray,
               name: str,
               n_dim: int) -> None:
    """
    Check the number of dimensions for the given array.

    :param arr: Array to check.
    :param name: Array name.
    :param n_dim: Expected number of dimensions.
    """
    Contract.assert_true(arr.ndim == n_dim, message="{} must be an ndarray with {} dimensions, found {}".format(
        name, n_dim, arr.ndim), target=name, log_safe=True)


def format_1d(arr: np.ndarray) -> np.ndarray:
    """
    Format an array as 1d if possible.

    :param arr: The array to reshape.
    :return: Array of shape (x,).
    """
    if arr is None:
        return arr
    if arr.ndim == 2 and (arr.shape[0] == 1 or arr.shape[1] == 1):
        arr = np.ravel(arr)
    return arr


def log_failed_splits(scores, metric):
    """
    Log if a metric could not be computed for some splits.

    :scores: The scores over all splits for one metric.
    :metric: Name of the metric.
    """
    n_splits = len(scores)

    failed_splits = []
    for score_index, score in enumerate(scores):
        if utilities.is_scalar(metric):
            if np.isnan(score):
                failed_splits.append(score_index)
        else:
            if NonScalarMetric.is_error_metric(score):
                failed_splits.append(score_index)
    n_failures = len(failed_splits)
    failed_splits_str = ', '.join([str(idx) for idx in failed_splits])

    if n_failures > 0:
        warn_args = metric, n_failures, n_splits, failed_splits_str
        warn_msg = "Could not compute {} for {}/{} validation splits: {}"
        logger.warning(warn_msg.format(*warn_args))
