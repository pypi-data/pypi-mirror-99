# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilities used during AutoML training."""
import ast
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

import azureml.dataprep as dprep
import numpy as np
import pandas as pd
from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import ArgumentBlankOrEmpty, ArgumentOutOfRange
from azureml._tracing._tracer_factory import get_tracer

from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.shared import constants, utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (ConflictingValueForArguments,
                                                                              DataShapeMismatch,
                                                                              InvalidArgumentWithSupportedValues,
                                                                              InvalidValuesInCVSplitColumn,
                                                                              MissingColumnsInData)
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.automl.core.shared.constants import TelemetryConstants
from azureml.automl.core.shared.exceptions import ConfigException, DataException, UserException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime import _data_splitting_utilities, _data_transformation_utilities
from azureml.automl.runtime import _ml_engine as ml_engine
from azureml.automl.runtime import _time_series_training_utilities, dataprep_utilities
from azureml.automl.runtime._data_definition.raw_experiment_data import RawExperimentData
from azureml.automl.runtime._ml_engine.validation import common_data_validations, RawExperimentDataValidatorSettings
from azureml.automl.runtime._runtime_params import ExperimentControlSettings, ExperimentDataSettings
from azureml.automl.runtime.data_context import TransformedDataContext
from azureml.automl.runtime.featurizer.transformer.timeseries import forecasting_heuristic_utils
from azureml.automl.runtime.shared._cv_splits import _CVSplits
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.datasets import ClientDatasets, DatasetBase, SubsampleCacheStrategy
from azureml.automl.runtime.shared.streaming_dataset import DatasetMetadataKeys, StreamingDataset
from azureml.automl.runtime.shared.types import CoreDataInputType, DataInputType, DataSingleColumnInputType
from azureml.automl.runtime.streaming_data_context import StreamingTransformedDataContext
from azureml.dataprep.api.dataflow import DataflowValidationError
from scipy import sparse
from sklearn.base import TransformerMixin

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)


class LargeDatasetLimit:
    """Constants for limiting large datasets."""

    MAX_ROWS_TO_SUBSAMPLE = 100000

    # Number of rows to  use for doing validations on the data
    VALIDATION_SUBSAMPLE_SIZE = 5000


MASKED = '[Masked]'


def auto_block_models(
        raw_experiment_data: RawExperimentData, automl_settings: AutoMLBaseSettings
) -> None:
    """
    Add appropriate files to blocked_models automatically.

    :param raw_experiment_data: An instance of RawExperimentData which has data objects such as 'X' and 'y'
    :param automl_settings: The settings used for this current run.
    :return: None
    """
    # Only enable auto-block if user didn't add any models to the allowed list
    if automl_settings.auto_blacklist and not automl_settings.whitelist_models:
        Contract.assert_type(raw_experiment_data, "raw_experiment_data", expected_types=RawExperimentData)
        X = raw_experiment_data.X
        if X is not None and (sparse.issparse(X) or X.shape[0] > constants.MAX_SAMPLES_AUTOBLOCK):
            if automl_settings.blacklist_algos is None:
                automl_settings.blacklist_algos = \
                    constants.MAX_SAMPLES_AUTOBLOCKED_ALGOS
            else:
                for blacklist_algo in constants.MAX_SAMPLES_AUTOBLOCKED_ALGOS:
                    if blacklist_algo not in automl_settings.blacklist_algos:
                        automl_settings.blacklist_algos.append(blacklist_algo)
            automl_settings.blacklist_samples_reached = True
            automl_settings._validate_model_filter_lists()


def prepare_raw_experiment_data(
        X=None, y=None, sample_weight=None, X_valid=None, y_valid=None, sample_weight_valid=None,
        cv_splits_indices=None, user_script=None,
        training_data=None, validation_data=None, label_column_name=None, weight_column_name=None,
        cv_split_column_names=None, automl_settings=None, verifier=None):
    """
    Prepare raw experiment data from all supported input formats.

    Note that this method also splits the training dataset into train/valid datasets, if there is no user defined
    rule for validating the model.

    :param X: Training features.
    :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param y: Training labels.
    :type y: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param sample_weight: Sample weights for training data.
    :type sample_weight: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param X_valid: validation features.
    :type X_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param y_valid: validation labels.
    :type y_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param sample_weight_valid: validation set sample weights.
    :type sample_weight_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param cv_splits_indices:
        Indices where to split training data for cross validation.
        Each row is a separate cross fold and within each crossfold, provide 2 arrays,
        the first with the indices for samples to use for training data and the second
        with the indices to use for validation data. i.e [[t1, v1], [t2, v2], ...]
        where t1 is the training indices for the first cross fold and v1 is the validation
        indices for the first cross fold.
    :type cv_splits_indices: numpy.ndarray
    :param training_data: The training data to be used within the experiment.
    :type training_data: typing.Union[pandas.DataFrame, azureml.core.Dataset,
        azureml.data.dataset_definition.DatasetDefinition, azureml.data.TabularDataset]
    :param validation_data: The validation data to be used within the experiment.
    :type validation_data: typing.Union[pandas.DataFrame, azureml.core.Dataset,
        azureml.data.dataset_definition.DatasetDefinition, azureml.data.TabularDataset]
    :param label_column_name: The name of the label column.
    :type label_column_name: str
    :param weight_column_name: The name of the sample weight column.
    :type weight_column_name: str
    :param cv_split_column_names: List of names for columns that contain custom cross validation split.
    :type cv_split_column_names: list(str)
    :param user_script: File path to script containing get_data()
    :param automl_settings: automl settings
    :param verifier: Verifier Manager instance.
    :type verifier: azureml.automl.runtime.faults_verifier.VerifierManager
    :return: RawExperimentData
    """
    Contract.assert_value(automl_settings, "automl_settings")

    x_raw_column_names = None
    reset_index_msg = ("Reset dataframe index to avoid potential conflicts "
                       "if time/time_series_id_column_names column is part of an index.")

    if X is None and y is None and training_data is None:
        data_dict = _extract_user_data(user_script)
        X = data_dict.get('X')
        y = data_dict.get('y')
        sample_weight = data_dict.get('sample_weight')
        X_valid = data_dict.get('X_valid')
        y_valid = data_dict.get('y_valid')
        sample_weight_valid = data_dict.get('sample_weight_valid')
        cv_splits_indices = data_dict.get("cv_splits_indices")
        x_raw_column_names = data_dict.get("x_raw_column_names")
    elif training_data is not None and label_column_name is not None:
        logger.info("Received training_data and label.")
        if isinstance(training_data, pd.DataFrame):
            X, y, sample_weight, cv_splits_indices = _extract_data_from_combined_dataframe(
                training_data=training_data, label_column_name=label_column_name,
                sample_weight_column_name=weight_column_name, cv_split_column_names=cv_split_column_names
            )

            if validation_data is not None:
                X_valid, y_valid, sample_weight_valid, _ = _extract_data_from_combined_dataframe(
                    training_data=validation_data, label_column_name=label_column_name,
                    sample_weight_column_name=weight_column_name
                )
        elif isinstance(training_data, dprep.Dataflow):
            X, y, sample_weight, cv_splits_indices = _extract_data_from_combined_dataflow(
                training_data=training_data, label_column_name=label_column_name,
                sample_weight_column_name=weight_column_name, cv_split_column_names=cv_split_column_names
            )

            if validation_data is not None:
                X_valid, y_valid, sample_weight_valid, _ = _extract_data_from_combined_dataflow(
                    training_data=validation_data, label_column_name=label_column_name,
                    sample_weight_column_name=weight_column_name
                )
            x_raw_column_names = X.head(1).columns.values

    X = dataprep_utilities.materialize_dataflow(X)
    if X_valid is not None:
        X_valid = dataprep_utilities.materialize_dataflow(X_valid)

    y = dataprep_utilities.materialize_dataflow(y, as_numpy=True)
    if y_valid is not None:
        y_valid = dataprep_utilities.materialize_dataflow(y_valid, as_numpy=True)

    if sample_weight is not None:
        sample_weight = dataprep_utilities.materialize_dataflow(sample_weight, as_numpy=True)
    if sample_weight_valid is not None:
        sample_weight_valid = dataprep_utilities.materialize_dataflow(sample_weight_valid, as_numpy=True)

    if cv_splits_indices is not None and cv_split_column_names is None:
        # cv_splits_indices NOT derived from cv_split_column_names so it still needs to resolve
        cv_splits_indices = dataprep_utilities.resolve_cv_splits_indices(cv_splits_indices)

    # Get the raw column names
    if isinstance(X, pd.DataFrame):
        # reset index in case a customer's df contains index column(s)
        X.reset_index(inplace=True, drop=True)
        forecasting_heuristic_utils._log_warn_maybe(reset_index_msg)
        # Cache the raw column names if available
        x_raw_column_names = X.columns.values

        # reset index in case a customer's df contains index column(s)
        if X_valid is not None:
            X_valid.reset_index(inplace=True, drop=True)
            forecasting_heuristic_utils._log_warn_maybe(reset_index_msg)
    else:
        X = _data_transformation_utilities._add_raw_column_names_to_X(X)
        if X_valid is not None:
            X_valid = _data_transformation_utilities._add_raw_column_names_to_X(X_valid)

    y = _convert_to_numpy_maybe(y, 'y')
    y_valid = _convert_to_numpy_maybe(y_valid, 'y_valid')

    if isinstance(sample_weight, pd.DataFrame):
        sample_weight = sample_weight.values
    if isinstance(sample_weight_valid, pd.DataFrame):
        sample_weight_valid = sample_weight_valid.values
    data_dict = {
        'X': X,
        'y': y,
        'X_valid': X_valid,
        'y_valid': y_valid,
        'cv_splits_indices': cv_splits_indices,
        'x_raw_column_names': x_raw_column_names,
        'sample_weight': sample_weight,
        'sample_weight_valid': sample_weight_valid}

    raw_experiment_data = RawExperimentData.create(
        data_dict,
        automl_settings.label_column_name,
        automl_settings.weight_column_name,
        automl_settings.validation_size,
        automl_settings.n_cross_validations)

    try:
        # Update the original training data / settings, if test or validation size was provided, or we needed to
        # apply a manual validation strategy
        _data_splitting_utilities.update_training_data_splits(raw_experiment_data, automl_settings, verifier)
    except Exception as e:
        # At this point, user datasets are not validated. Hence, known errors during splitting should be raised with
        # user error codes.
        common_data_validations.materialized_tabular_data_user_error_handler(e)

    if automl_settings.is_timeseries:
        raw_experiment_data = _time_series_training_utilities.preprocess_timeseries_data(
            raw_experiment_data, automl_settings, False, verifier)
    return raw_experiment_data


def _convert_to_numpy_maybe(
        y: Optional[Union[np.ndarray, pd.DataFrame, pd.Series]],
        ds_name: str) -> Optional[np.ndarray]:
    """
    Try to convert y to numpy array.

    If y can not be converted to np.ndarray or has wrong shape the DataException is raised.
    :param y: The data set to be converted.
    :param ds_name: The name of the data set to convert.
    :raises: DataException
    """
    if y is None:
        return y
    if isinstance(y, pd.DataFrame):
        _check_y_shape(y, 'y')
        return cast(np.ndarray, y[y.columns[0]].values)
    if isinstance(y, pd.Series):
        return cast(np.ndarray, y.values)
    return y


def _check_y_shape(y: pd.DataFrame, ds_name: str) -> None:
    """
    Check if y data frame has only one column.

    :param y: The y dataframe.
    :param name: The name of a data set.
    :raises: DataException
    """
    if y.shape[1] > 1:
        raise DataException._with_error(AzureMLError.create(
            DataShapeMismatch, target=ds_name, reference_code=ReferenceCodes._Y_SHAPE_MISMATCH)
        )


def validate_training_data_dict(raw_experiment_data: RawExperimentData,
                                automl_settings: AutoMLBaseSettings) -> None:
    """
    Validate that training data and parameters have been correctly provided.

    :param raw_experiment_data: User provided data inputs for the experiment
    :param automl_settings: AutoML configuration
    :return:
    """
    logger.info("Start data validation.")
    Contract.assert_value(raw_experiment_data, "raw_experiment_data")

    with tracer.start_as_current_span(
            TelemetryConstants.SPAN_FORMATTING.format(
                TelemetryConstants.COMPONENT_NAME, TelemetryConstants.DATA_VALIDATION
            ),
            user_facing_name=TelemetryConstants.DATA_VALIDATION_USER_FACING
    ):
        Validation.validate_value(raw_experiment_data.X, "X")
        Validation.validate_value(raw_experiment_data.y, "y")

        # Handling for legacy code paths, where in the inputs may not be a pandas DataFrame
        if not automl_settings.enable_streaming:
            raw_experiment_data.X = _data_transformation_utilities._add_raw_column_names_to_X(
                raw_experiment_data.X, raw_experiment_data.feature_column_names)
            if raw_experiment_data.X_valid is not None:
                raw_experiment_data.X_valid = _data_transformation_utilities._add_raw_column_names_to_X(
                    raw_experiment_data.X_valid, raw_experiment_data.feature_column_names)

        if automl_settings.is_timeseries:
            ml_engine.validate_timeseries(raw_experiment_data, automl_settings)
        else:
            ml_engine.validate(raw_experiment_data, RawExperimentDataValidatorSettings(automl_settings),
                               ExperimentDataSettings(automl_settings))


def _construct_coord_indices_str(data_indices: np.ndarray, n_top_indices: int = 20) -> str:
    """Contruct a string with top 20 indices."""
    if data_indices.ndim == 1 or data_indices.shape[1] == 1:
        indices = sorted(data_indices)
    else:
        indices = sorted(data_indices, key=lambda x: (x[1], x[0]))
    if len(indices) <= n_top_indices:
        print_indices = data_indices  # type: Union[np.ndarray, List[List[int]]]
        return ", ".join([str(idx) for idx in print_indices])
    else:
        if data_indices.ndim == 1:
            print_indices = data_indices[:n_top_indices]
        else:
            col_idx_dict = {}  # type: Dict[int, List[List[int]]]
            for idx in indices:
                if idx[1] not in col_idx_dict:
                    col_idx_dict[idx[1]] = [idx]
                else:
                    col_idx_dict[idx[1]].append(idx)
            top_indices = sorted(col_idx_dict.keys(), key=lambda x: len(col_idx_dict[x]))
            if len(top_indices) > n_top_indices:
                print_indices = [col_idx_dict[idx][0] for idx in top_indices[:n_top_indices]]
            else:
                print_indices = [col_idx_dict[idx][0] for idx in top_indices]
        return ", ".join([str(idx) for idx in print_indices]) + "..."


def _get_data_indices_by_mask_function(data: CoreDataInputType,
                                       mask_function: 'Callable[..., Optional[Any]]') -> np.ndarray:
    """Obtain the indices list where the data entry in data has the mask function evaluated as True."""
    if isinstance(data, np.ndarray) or isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
        return np.argwhere(mask_function(data))
    elif sparse.issparse(data):
        coo_data = sparse.coo_matrix(data)
        return np.array(
            [(coo_data.row[i], coo_data.col[i]) for i in np.argwhere(mask_function(coo_data.data)).ravel()])
    else:
        return np.array([])


def _is_sparse_matrix_int_type(sparse_matrix: DataInputType) -> bool:
    """
    Check if a sparse matrix is in integer format.

    :param sparse_matrix:
    :return:
    """
    if sparse_matrix is not None and sparse.issparse(sparse_matrix):
        numpy_int_types = [np.int32, np.int64, np.int16, np.int8,
                           np.uint32, np.uint64, np.uint16, np.uint8]

        if sparse_matrix.dtype in numpy_int_types:
            return True

    return False


def _upgrade_sparse_matrix_type(sparse_matrix: DataInputType) -> DataInputType:
    """
    Convert sparse matrix in integer format into floating point format.

    This function will create a copy of the sparse matrix in when the conversion happens.
    :param sparse_matrix:
    :return:
    """
    if sparse_matrix is not None and sparse.issparse(sparse_matrix):
        if sparse_matrix.dtype == np.int32 or sparse_matrix.dtype == np.int16 or \
                sparse_matrix.dtype == np.int8 or sparse_matrix.dtype == np.uint32 or \
                sparse_matrix.dtype == np.uint16 or sparse_matrix.dtype == np.uint8 or \
                sparse_matrix.dtype == np.bool:
            return sparse_matrix.astype(np.float32)
        elif sparse_matrix.dtype == np.int64 or sparse_matrix.dtype == np.uint64:
            return sparse_matrix.astype(np.float64)
        else:
            return sparse_matrix

    return sparse_matrix


def init_client_dataset_from_fit_iteration_params(fit_iteration_parameters_dict: Dict[str, Any],
                                                  experiment_control_settings: ExperimentControlSettings,
                                                  experiment_data_settings: ExperimentDataSettings,
                                                  cache_store: Optional[CacheStore] = None,
                                                  subsample_cache_strategy: str = SubsampleCacheStrategy.Preshuffle,
                                                  init_all_stats: bool = False,
                                                  keep_in_memory: bool = False) -> ClientDatasets:
    """
    Get a ClientDatasets object from fit_iteration_parameters

    TODO: This method needs to be deprecated. ClientDatasets should be consolidated to only use transformed data ctx

    :param fit_iteration_parameters_dict: Dictionary that contains input data
    :param automl_settings:  AutoML settings config
    :param cache_store: Underlying cache store to use, will default to local FileStore
    :param subsample_cache_strategy: the subsampling strategy to use
    :param init_all_stats: Initialize all the stats
    :param keep_in_memory: Whether to flush the data to the cache store or keep it in-memory
    :return: ClientDatasets
    """
    cv_splits = _CVSplits(X=fit_iteration_parameters_dict.get('X'),
                          y=fit_iteration_parameters_dict.get('y'),
                          frac_valid=experiment_data_settings.validation_size,
                          cv_splits_indices=fit_iteration_parameters_dict.get('cv_splits_indices'),
                          is_time_series=experiment_control_settings.is_timeseries,
                          timeseries_param_dict=experiment_control_settings.timeseries_param_dict,
                          task=experiment_control_settings.task_type)

    dataset = _get_client_dataset(fit_iteration_parameters_dict.get('X'),
                                  fit_iteration_parameters_dict.get('y'),
                                  cache_store=cache_store,
                                  sample_weight=fit_iteration_parameters_dict.get('sample_weight'),
                                  X_valid=fit_iteration_parameters_dict.get('X_valid'),
                                  y_valid=fit_iteration_parameters_dict.get('y_valid'),
                                  sample_weight_valid=fit_iteration_parameters_dict.get('sample_weight_valid'),
                                  cv_splits=cv_splits,
                                  num_classes=experiment_data_settings.num_classes,
                                  task_type=experiment_control_settings.task_type,
                                  y_min=experiment_data_settings.y_min,
                                  y_max=experiment_data_settings.y_max,
                                  init_all_stats=init_all_stats,
                                  subsample_cache_strategy=subsample_cache_strategy)

    dataset.x_raw_column_names = fit_iteration_parameters_dict.get('x_raw_column_names')

    if not keep_in_memory:
        dataset.cache_dataset(keep_in_memory)

    return dataset


def init_dataset(
        transformed_data_context: Union[TransformedDataContext, StreamingTransformedDataContext],
        cache_store: CacheStore,
        task_type: str,
        experiment_data_settings: ExperimentDataSettings,
        subsample_cache_strategy: str = SubsampleCacheStrategy.Preshuffle,
        init_all_stats: bool = False,
        keep_in_memory: bool = False
) -> DatasetBase:
    """
    Initialize the dataset.

    :param transformed_data_context: Featurized dataset.
    :param cache_store: cache store
    :param automl_settings: automl settings
    :param subsample_cache_strategy: the subsampling strategy to use
    :param init_all_stats: init all stats
    :param keep_in_memory: Whether to flush the data to the cache store or keep it in-memory
    :return: DatasetBase
    """
    if isinstance(transformed_data_context, StreamingTransformedDataContext):
        return init_streaming_dataset(
            transformed_data_context=transformed_data_context,
            task_type=task_type,
            experiment_data_settings=experiment_data_settings
        )

    elif isinstance(transformed_data_context, TransformedDataContext):
        return init_client_dataset(
            transformed_data_context=transformed_data_context,
            cache_store=cache_store,
            task_type=task_type,
            experiment_data_settings=experiment_data_settings,
            subsample_cache_strategy=subsample_cache_strategy,
            init_all_stats=init_all_stats,
            keep_in_memory=keep_in_memory)


def init_client_dataset(transformed_data_context: TransformedDataContext,
                        cache_store: CacheStore,
                        task_type: str,
                        experiment_data_settings: ExperimentDataSettings,
                        subsample_cache_strategy: str = SubsampleCacheStrategy.Preshuffle,
                        init_all_stats: bool = False,
                        keep_in_memory: bool = False) -> ClientDatasets:
    """
    Get the client dataset.

    :param transformed_data_context: Transformed_data_context contains X,y & other data's.
    :param cache_store: Cache store object.
    :param task_type: task type
    :param num_classes: number of classes
    :param n_cross_validations: number of cross validations to use
    :param y_min: min value for y
    :param y_max: max value for y
    :param subsample_cache_strategy: the subsampling strategy to use
    :param init_all_stats: Initialize all the statistics.
    :param keep_in_memory: Whether to flush the data to the cache store or keep it in-memory.
    :return: ClientDatasets object.
    """
    dataset = _get_client_dataset(transformed_data_context.X,
                                  transformed_data_context.y,
                                  cache_store=cache_store,
                                  sample_weight=transformed_data_context.sample_weight,
                                  X_valid=transformed_data_context.X_valid,
                                  y_valid=transformed_data_context.y_valid,
                                  sample_weight_valid=transformed_data_context.sample_weight_valid,
                                  cv_splits=transformed_data_context.cv_splits,
                                  num_classes=experiment_data_settings.num_classes,
                                  task_type=task_type,
                                  y_min=experiment_data_settings.y_min,
                                  y_max=experiment_data_settings.y_max,
                                  init_all_stats=init_all_stats,
                                  subsample_cache_strategy=subsample_cache_strategy,
                                  transformers=transformed_data_context.transformers,
                                  X_raw=transformed_data_context.X_raw_cleaned,
                                  y_raw=transformed_data_context.y_raw_cleaned,
                                  X_valid_raw=transformed_data_context.X_valid_raw_cleaned,
                                  y_valid_raw=transformed_data_context.y_valid_raw_cleaned)

    dataset.timeseries = transformed_data_context.timeseries
    # If dataset was initialized via parse_data the timeseries key is set correctly on the _dataset dict
    # otherwise we need to add it manually. This ensures the key is always properly set to the value
    # when retrieving from the cache.
    dataset._dataset["timeseries"] = dataset.timeseries
    dataset.timeseries_param_dict = transformed_data_context.timeseries_param_dict
    dataset.x_raw_column_names = transformed_data_context.x_raw_column_names
    dataset.raw_data_type = transformed_data_context._get_raw_data_type()
    dataset.raw_data_snapshot_str = transformed_data_context._get_raw_data_snapshot_str()

    if experiment_data_settings.n_cross_validations is None and transformed_data_context.X_valid is None:
        # set the value for num_auto_cv_splits if no other mode of Validation is specified
        n_cv = transformed_data_context._get_num_cv_splits()
        dataset.num_auto_cv_splits = None if n_cv == 0 else n_cv

    if not keep_in_memory:
        dataset.cache_dataset(keep_in_memory)

    return dataset


def _get_client_dataset(X: DataInputType,
                        y: DataSingleColumnInputType,
                        cache_store: Optional[CacheStore] = None,
                        sample_weight: Optional[DataInputType] = None,
                        X_valid: Optional[DataInputType] = None,
                        y_valid: Optional[DataSingleColumnInputType] = None,
                        sample_weight_valid: Optional[DataInputType] = None,
                        cv_splits: Optional[_CVSplits] = None,
                        num_classes: Optional[int] = None,
                        task_type: str = constants.Tasks.CLASSIFICATION,
                        y_min: Optional[float] = None,
                        y_max: Optional[float] = None,
                        init_all_stats: bool = False,
                        subsample_cache_strategy: str = SubsampleCacheStrategy.Preshuffle,
                        transformers: Optional[Dict[str, TransformerMixin]] = None,
                        X_raw: Optional[DataInputType] = None,
                        y_raw: Optional[DataSingleColumnInputType] = None,
                        X_valid_raw: Optional[DataInputType] = None,
                        y_valid_raw: Optional[DataSingleColumnInputType] = None) -> ClientDatasets:
    default_dataset_name = 'NoName'

    if cv_splits:
        frac_valid = cv_splits.get_fraction_validation_size()
        cv_splits_indices = cv_splits.get_custom_split_indices()
        num_cv_folds = cv_splits.get_num_k_folds()
    else:
        frac_valid = None
        cv_splits_indices = None
        num_cv_folds = None

    dataset = ClientDatasets(subsample_cache_strategy=subsample_cache_strategy, cache_store=cache_store)
    logger.info('Created ClientDataset.')

    if X_valid is not None:
        training_type = _get_training_type(
            constants.TrainingType.TrainAndValidation)

        if not (num_cv_folds == 0 or num_cv_folds is None):
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="n_cross_validations",
                    arguments=', '.join(['validation_data/X_valid', 'n_cross_validations'])
                )
            )

        if not (frac_valid == 0.0 or frac_valid is None):
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="validation_size",
                    arguments=', '.join(['validation_data/X_valid', 'validation_size'])
                )
            )

        if y_valid is None:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ArgumentBlankOrEmpty, target="y_valid", argument_name="y_valid"
                )
            )

        logger.info('Parsing simple train validate dataset.')
        dataset.parse_simple_train_validate(name=default_dataset_name,
                                            X=X,
                                            y=y,
                                            sample_weight=sample_weight,
                                            X_valid=X_valid,
                                            y_valid=y_valid,
                                            sample_weight_valid=sample_weight_valid,
                                            task=task_type,
                                            y_min=y_min,
                                            y_max=y_max,
                                            init_all_stats=init_all_stats,
                                            transformers=transformers,
                                            X_raw=X_raw, y_raw=y_raw,
                                            X_valid_raw=X_valid_raw, y_valid_raw=y_valid_raw)

    else:
        if (num_cv_folds == 0 or num_cv_folds is None) and cv_splits_indices is None:
            training_type = _get_training_type(
                constants.TrainingType.TrainAndValidation)
        else:
            if cv_splits_indices is not None:
                num_cv_folds = len(cv_splits_indices)
            training_type = _get_training_type(
                constants.TrainingType.MeanCrossValidation, num_cv_folds)

        logger.info('Parsing cross validation dataset.')
        dataset.parse_data(name=default_dataset_name,
                           X=X,
                           y=y,
                           sample_weight=sample_weight,
                           cv_splits=cv_splits,
                           num_classes=num_classes,
                           task=task_type,
                           y_min=y_min,
                           y_max=y_max,
                           init_all_stats=init_all_stats,
                           transformers=transformers,
                           X_raw=X_raw, y_raw=y_raw,
                           X_valid_raw=X_valid_raw, y_valid_raw=y_valid_raw)

    dataset.training_type = training_type
    return dataset


def init_streaming_dataset(
        transformed_data_context: StreamingTransformedDataContext,
        task_type: str,
        experiment_data_settings: ExperimentDataSettings
) -> StreamingDataset:
    """
    Initialize a streaming dataset (a dataset where where all data may not fit into memory at once).

    :param transformed_data_context: The transformed data context.
    :return: A StreamingDataset
    """
    if experiment_data_settings.label_column_name is None:
        raise ConfigException._with_error(
            AzureMLError.create(
                ArgumentBlankOrEmpty, target="label_column_name", argument_name="label_column_name"
            )
        )

    featurized_column_names = transformed_data_context.get_featurized_column_names()

    dataset_metadata = {DatasetMetadataKeys.feature_column_names: featurized_column_names,
                        DatasetMetadataKeys.label_column_name: experiment_data_settings.label_column_name,
                        DatasetMetadataKeys.weight_column_name: experiment_data_settings.weight_column_name,
                        DatasetMetadataKeys.raw_data_snapshot: transformed_data_context.raw_data_snapshot}

    featurization_transformer = transformed_data_context.get_featurization_transformer()

    return StreamingDataset(task=task_type,
                            training_data=transformed_data_context.training_data,
                            dataset_metadata=dataset_metadata,
                            validation_data=transformed_data_context.validation_data,
                            y_min=experiment_data_settings.y_min,
                            y_max=experiment_data_settings.y_max,
                            featurization_transformer=featurization_transformer)


def _get_training_type(training_type: str, folds: int = 0) -> str:
    """
    Determine what type of training and validation to do based on user inputs.
    """
    # TODO: make this simpler
    valid_training_types = (constants.TrainingType.TrainAndValidation,
                            constants.TrainingType.MeanCrossValidation)
    if training_type not in valid_training_types:
        raise ConfigException._with_error(
            AzureMLError.create(
                InvalidArgumentWithSupportedValues, target="training_type",
                arguments="training_type ({})".format(training_type), supported_values="%s, %s" % valid_training_types
            )
        )
    is_cv = training_type == constants.TrainingType.MeanCrossValidation
    if not ((is_cv and folds) or (not is_cv and not folds)):
        # This isn't very user friendly / actionable.
        raise ConfigException._with_error(
            AzureMLError.create(
                ConflictingValueForArguments, target="cross_validation_folds",
                arguments=', '.join(['training_type ({})'.format(constants.TrainingType.MeanCrossValidation),
                                     'cross_validation_folds'])
            )
        )
    if folds < 0 or folds == 1:
        raise ConfigException._with_error(
            AzureMLError.create(
                ArgumentOutOfRange, target="cross_validation_folds",
                argument_name="cross_validation_folds", min=2, max="inf"
            )
        )
    return training_type


def _extract_user_data(
        user_script: Any
) -> Dict[str, Optional[Union[pd.DataFrame, np.ndarray, List[str], float, List[int]]]]:
    """
    Extract data from user's module containing get_data().

    This method automatically runs during an automated machine learning experiment.
    Arguments:
        user_script {module} -- Python module containing get_data() function.

    Raises:
        DataException -- Get data script was not defined and X, y inputs were not provided.
        DataException -- Could not execute get_data() from user script.
        DataException -- Could not extract data from user script.

    Returns:
        dict -- Dictionary containing
        X_train, y_train, sample_weight, X_valid, y_valid,
        sample_weight_valid, cv_splits_indices.

    """
    Validation.validate_value(user_script, "user_script")
    try:
        output = user_script.get_data()  # type: Union[Dict[str, Any], Tuple[Any, Any, Any, Any]]
    except Exception as ex:
        msg = ("Could not execute get_data() from user script."
               "Exception: {}")
        raise UserException(msg.format(ex)).with_generic_msg(msg.format(MASKED)) from None
    if isinstance(output, dict):
        return _extract_data_from_dict(output)
    elif isinstance(output, tuple):
        return _extract_data_from_tuple(output)
    else:
        raise DataException("The output of get_data() from user script is not a dict or a tuple.", has_pii=False)


def _extract_data_from_dict(
        output: Dict[str, Any]
) -> Dict[str, Optional[Union[pd.DataFrame, np.ndarray, List[str], float, List[int]]]]:
    """
    Extract user data if it is passed as a dictionary.

    Arguments:
        output {dict} -- dictionary containing user data and metadata.

    Raises:
        DataException -- Invalid data or encountered processing issues.

    Returns:
        dict -- Dictionary containing AutoML relevant data.

    """
    X = utilities.get_value_from_dict(output, ['X'], None)
    y = utilities.get_value_from_dict(output, ['y'], None)
    sample_weight = utilities.get_value_from_dict(output, ['sample_weight'], None)
    X_valid = utilities.get_value_from_dict(output, ['X_valid'], None)
    y_valid = utilities.get_value_from_dict(output, ['y_valid'], None)
    sample_weight_valid = utilities.get_value_from_dict(
        output, ['sample_weight_valid'], None)
    X_test = utilities.get_value_from_dict(output, ['X_test'], None)
    y_test = utilities.get_value_from_dict(output, ['y_test'], None)
    data = utilities.get_value_from_dict(output, ['data_train'], None)
    columns = utilities.get_value_from_dict(output, ['columns'], None)
    label = utilities.get_value_from_dict(output, ['label'], None)
    cv_splits_indices = utilities.get_value_from_dict(
        dictionary=output,
        names=["cv_splits_indices"], default_value=None)
    x_raw_column_names = None

    if data is not None:
        if label is None and X is None and y is None:
            # This is just called in the get_data code path.
            # get_data is to soon expected to be deprecated (and has non-existent usage among customers)
            raise DataException(
                'Pandas data array received without a label. Please add a ''label'' element to the '
                'get_data() output.', has_pii=False)
        if not isinstance(label, list):
            assert (isinstance(label, str) or isinstance(label, int))
            label = [label]
        y_extracted = data[label].values
        X_extracted = data[data.columns.difference(label)]
        if columns is not None:
            X_extracted = X_extracted[X_extracted.columns.intersection(columns)]

        if X is None and y is None:
            X = X_extracted
            y = y_extracted
        else:
            if np.array_equiv(X, X_extracted.values):
                raise DataException(
                    "Different values for X and data were provided. "
                    "Please return either X and y or data and label.", has_pii=False)
            if np.array_equiv(y, y_extracted.values):
                raise DataException(
                    "Different values for y and label were provided. "
                    "Please return either X and y or data and label.", has_pii=False)
    if isinstance(X, pd.DataFrame):
        x_raw_column_names = X.columns.values
    if isinstance(y, pd.DataFrame):
        y = y.values
    if isinstance(y_valid, pd.DataFrame):
        y_valid = y_valid.values
    if isinstance(y_test, pd.DataFrame):
        y_test = y_test.values

    if X is None:
        raise DataException(
            "Could not retrieve X train data from get_data() call. "
            "Please ensure you are either returning either "
            "{X_train: <numpy array>, y_train: <numpy array>"
            "or {data: <pandas dataframe>, label: <string>", has_pii=False)
    if y is None:
        raise DataException(
            "Could not retrieve y train data from get_data() call. "
            "Please ensure you are either returning either "
            "{X_train: <numpy array>, y_train: <numpy array>"
            "or {data: <pandas dataframe>, label: <string>", has_pii=False)

    if (X_valid is None) is not (y_valid is None):
        raise DataException(
            'Received only one of X_valid or y_valid.'
            'Either both or neither value should be provided.', has_pii=False)

    return {
        "X": X,
        "y": y,
        "x_raw_column_names": x_raw_column_names,
        "sample_weight": sample_weight,
        "X_valid": X_valid,
        "y_valid": y_valid,
        "sample_weight_valid": sample_weight_valid,
        "X_test": X_test,
        "y_test": y_test,
        "cv_splits_indices": cv_splits_indices,
    }


def _extract_data_from_tuple(
        output: Tuple[Union[pd.DataFrame, np.ndarray], Union[pd.DataFrame, np.ndarray],
                      Union[pd.DataFrame, np.ndarray], Union[pd.DataFrame, np.ndarray]]
) -> Dict[str, Optional[Union[pd.DataFrame, np.ndarray, List[str], float, List[int]]]]:
    """
    Extract user data if it is passed as a tuple.

    Arguments:
        output {tuple} -- tuple containing user data.

    Raises:
        DataException -- Could not extract X, y from get_data() in user script. get_data only output {0} values.

    Returns:
        tuple -- tuple containing X_train, y_train, X_test, y_test

    """
    X_valid, y_valid = None, None
    if len(output) < 2:
        msg = ("Could not extract X, y from get_data() in user "
               "script. get_data only output {0} values.")
        raise DataException(msg.format(len(output))).with_generic_msg(msg.format(MASKED)) from None
    x_raw_column_names = None
    X = output[0]
    y = output[1]
    if isinstance(X, pd.DataFrame):
        x_raw_column_names = X.columns.values
    if isinstance(y, pd.DataFrame):
        y = y.values

    if len(output) >= 4:
        X_valid = output[2]
        y_valid = output[3]
        if isinstance(y_valid, pd.DataFrame):
            y_valid = y_valid.values

    return {
        "X": X,
        "y": y,
        "sample_weight": None,
        "x_raw_column_names": x_raw_column_names,
        "X_valid": X_valid,
        "y_valid": y_valid,
        "sample_weight_valid": None,
        "X_test": None,
        "y_test": None,
        "cv_splits_indices": None,
    }


def _extract_data_from_combined_dataframe(
        training_data: pd.DataFrame,
        label_column_name: str,
        sample_weight_column_name: Optional[str] = None,
        cv_split_column_names: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, np.ndarray, Any, Any]:
    """
    Extract user data from a Pandas dataframe if it contains both training features & labels.

    :param training_data: The Pandas dataframe to extract X, y, sample_valid from.
    :param label_column_name: Name of the label column used to extract y.
    :param sample_weight_column_name: Name of the sample weight column.
    :param cv_split_column_names: List of names of the cv split columns.
    :return: A Dictionary with keys being X, y, sample_weight, cv_splits_indices extracted from training_data.
    """
    col_names_to_drop = [label_column_name]
    sample_weight = None
    cv_splits_indices = None

    if sample_weight_column_name is not None:
        col_names_to_drop.append(sample_weight_column_name)
        if sample_weight_column_name not in training_data.columns:
            raise DataException._with_error(AzureMLError.create(
                MissingColumnsInData, target='sample_weight_column_name', columns=sample_weight_column_name,
                data_object_name='training_data',
                reference_code=ReferenceCodes._EXTRACT_DATA_FROM_COMBINED_DATAFRAME_SAMPLE_WEIGHT_MISSING)
            )
        sample_weight = training_data[sample_weight_column_name].values

    if cv_split_column_names is not None:
        col_names_to_drop.extend(cv_split_column_names)
        for cv_split_column_name in cv_split_column_names:
            if cv_split_column_name not in training_data.columns:
                raise DataException._with_error(AzureMLError.create(
                    MissingColumnsInData, target='cv_split_column_names', columns=cv_split_column_name,
                    data_object_name='training_data',
                    reference_code=ReferenceCodes._EXTRACT_DATA_FROM_COMBINED_DATAFRAME_CV_SPLIT_COLUMNS_MISSING)
                )
        cv_split_columns = training_data[cv_split_column_names]
        cv_splits_indices = _convert_cv_split_columns_to_cv_splits_indices(cv_split_columns)

    X = training_data[training_data.columns.difference(col_names_to_drop)]
    if label_column_name not in training_data.columns:
        raise DataException._with_error(
            AzureMLError.create(MissingColumnsInData, target='X', columns=label_column_name, data_object_name='X')
        )
    y = training_data[label_column_name].values

    return X, y, sample_weight, cv_splits_indices


def _extract_data_from_combined_dataflow(
        training_data: dprep.Dataflow,
        label_column_name: str,
        sample_weight_column_name: Optional[str] = None,
        cv_split_column_names: Optional[List[str]] = None,
        validate_columns_exist: bool = True
) -> Tuple[Any, Any, Any, Any]:
    """
    Extract user data from a Dataflow if it contains both training features & labels.

    :param training_data: The Dataflow to extract X, y, sample_valid from.
    :param label_column_name: Name of the label column used to extract y.
    :param sample_weight_column_name: Name of the sample weight column.
    :param cv_split_column_names: List of names of the cv split columns.
    :return: A Dictionary with keys being X, y, sample_weight, cv_splits_indices extracted from training_data.
    """
    col_names_to_drop = []
    if label_column_name is not None:
        col_names_to_drop.append(label_column_name)
    sample_weight = None
    cv_splits_indices = None

    if sample_weight_column_name is not None:
        col_names_to_drop.append(sample_weight_column_name)
        try:
            sample_weight = training_data.keep_columns([sample_weight_column_name],
                                                       validate_column_exists=validate_columns_exist)
        except DataflowValidationError:
            raise DataException._with_error(AzureMLError.create(
                MissingColumnsInData, target="weight_column_name", data_object_name="X",
                columns="{} (weight_column_name)".format(sample_weight_column_name),
                reference_code=ReferenceCodes._EXTRACT_DATA_FROM_COMBINED_DATAFLOW_SAMPLE_WEIGHT_MISSING)
            )

    if cv_split_column_names is not None:
        cv_split_column_names = list(filter(None, cv_split_column_names))
        col_names_to_drop.extend(cv_split_column_names)
        try:
            cv_split_columns = training_data.keep_columns(cv_split_column_names,
                                                          validate_column_exists=validate_columns_exist)
            if cv_split_columns.row_count:
                cv_splits_indices = _convert_cv_split_columns_to_cv_splits_indices(cv_split_columns)
        except DataflowValidationError:
            raise DataException._with_error(AzureMLError.create(
                MissingColumnsInData, target="cv_split_column_names", data_object_name="X",
                columns="{} (cv_split_column_names)".format(cv_split_column_names),
                reference_code=ReferenceCodes._EXTRACT_DATA_FROM_COMBINED_DATAFLOW_CV_SPLIT_COLUMNS_MISSING)
            )

    X = training_data.drop_columns(col_names_to_drop)
    try:
        y = training_data.keep_columns([label_column_name],
                                       validate_column_exists=validate_columns_exist) \
            if label_column_name is not None else None
    except DataflowValidationError:
        raise DataException._with_error(AzureMLError.create(
            MissingColumnsInData, target="label_column_name", data_object_name="X",
            columns="{} (label_column_name)".format(label_column_name),
            reference_code=ReferenceCodes._EXTRACT_DATA_FROM_COMBINED_DATAFLOW_LABEL_COLUMN_MISSING)
        )
    return X, y, sample_weight, cv_splits_indices


def _convert_cv_split_columns_to_cv_splits_indices(
        cv_split_columns: Union[dprep.Dataflow, pd.DataFrame]
) -> List[List[Any]]:
    cv_splits_indices = []
    if isinstance(cv_split_columns, pd.DataFrame):
        cv_split_columns_numpy = cv_split_columns.values
    else:
        cv_split_columns_numpy = dataprep_utilities.materialize_dataflow(cv_split_columns, as_numpy=True)
    if cv_split_columns_numpy.ndim == 1:
        training_indices, validation_indices = _get_column_to_cv_splits_indices(cv_split_columns_numpy)
        cv_splits_indices.append([training_indices, validation_indices])
    else:
        for i in range(cv_split_columns_numpy.shape[1]):
            column = cv_split_columns_numpy[:, i]
            training_indices, validation_indices = _get_column_to_cv_splits_indices(column)
            cv_splits_indices.append([training_indices, validation_indices])
    return cv_splits_indices


def _get_column_to_cv_splits_indices(column: np.ndarray) -> Tuple[Any, Any]:
    try:
        training_indices, = np.where(column.astype(int) == 1)
        validation_indices, = np.where(column.astype(int) == 0)

        # verify number of indices extracted equal number of total rows
        if len(training_indices) + len(validation_indices) != len(column):
            raise ValueError("cv split column had values outside of the set {0, 1}")
    except ValueError as ve:
        raise DataException._with_error(
            AzureMLError.create(InvalidValuesInCVSplitColumn, target="cv_split_column_names",
                                reference_code=ReferenceCodes._CV_SPLIT_COLUMN_CONVERSION_INCORRECT_INT_VALUE),
            inner_exception=ve
        ) from ve

    return training_indices, validation_indices


def _check_if_automl_model_is_explainable(automl_algo_tag: str, is_ensemble: bool = False) -> bool:
    unexplainable_models = [constants.SupportedModels.Forecasting.Average,
                            constants.SupportedModels.Forecasting.ExponentialSmoothing,
                            constants.SupportedModels.Forecasting.Naive,
                            constants.SupportedModels.Forecasting.SeasonalAverage,
                            constants.SupportedModels.Forecasting.SeasonalNaive,
                            constants.SupportedModels.Forecasting.TCNForecaster
                            ]
    explainable = True
    if is_ensemble:
        # Parse the tag assuming it is a string representation of a Python list
        ensemble_algo_list = ast.literal_eval(automl_algo_tag)
        if len(set(unexplainable_models).intersection(ensemble_algo_list)) > 0:
            explainable = False
    else:
        if automl_algo_tag in unexplainable_models:
            explainable = False

    return explainable


def _get_model_exp_property(automl_run: Any) -> bool:
    try:
        from azureml.train.automl.runtime._remote_script import model_exp_wrapper
        automl_algo_name = automl_run.properties.get('run_algorithm')
        if automl_algo_name != 'StackEnsemble' and automl_algo_name != 'VotingEnsemble':
            if_model_is_explainable = \
                _check_if_automl_model_is_explainable(automl_algo_name, is_ensemble=False)
            if logger is not None and not if_model_is_explainable:
                logger.warning(automl_algo_name + ' is not explainable for AutoML run ' + str(automl_run.id))

            return if_model_is_explainable
        else:
            ensemble_algo_names_list_str = automl_run.tags.get('ensembled_algorithms')
            if ensemble_algo_names_list_str is not None:
                if_ensemble_model_is_explainable = \
                    _check_if_automl_model_is_explainable(ensemble_algo_names_list_str, is_ensemble=True)
                if logger is not None and not if_ensemble_model_is_explainable:
                    msg = ('{} with constituent models {} is not explainable for AutoML run {}'
                           .format(automl_algo_name, ensemble_algo_names_list_str, automl_run.id))
                    logger.warning(msg)

                return if_ensemble_model_is_explainable
            else:
                return True
    except Exception:
        return False
