# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Holding the featurization functions."""
import json
import logging
from typing import cast, Dict, Optional, Any, Tuple, Union, List

import numpy as np
import pandas as pd
from azureml.automl.runtime.featurization import data_transformer_utils

from scipy import sparse
from sklearn import preprocessing
from sklearn.utils.class_weight import compute_class_weight
from azureml._common._error_definition import AzureMLError
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core._experiment_observer import ExperimentObserver, NullExperimentObserver
from azureml.automl.core.constants import FeatureType
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import constants, logging_utilities, utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternal,
    InvalidArgumentType)
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.automl.core.shared.exceptions import ClientException, DataException, ValidationException
from azureml.automl.core.shared.reference_codes import ReferenceCodes

import azureml.automl.runtime._ml_engine as ml_engine

from azureml.automl.runtime import data_cleaning
from azureml.automl.runtime.column_purpose_detection import StatsAndColumnPurposeType

from azureml.automl.runtime.featurizer.transformer.featurization_utilities import skip_featurization
from azureml.automl.runtime.shared import memory_utilities, utilities as runtime_utilities
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from azureml.dataprep import Dataflow

from . import _data_transformation_utilities
from ._feature_sweeped_state_container import FeatureSweepedStateContainer
from .data_context import RawDataContext, TransformedDataContext
from .faults_verifier import VerifierManager, VerifierResults
from .featurization import DataTransformer, StreamingFeaturizer
from .featurization._featurizer_container import FeaturizerContainer
from .stats_computation import RawFeatureStats
from .streaming_data_context import StreamingTransformedDataContext

_logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)
_DUMMY_VALUES_FOR_TYPE = {
    "bytes": "example_value",
    "bool": False,
    "datetime": "2000-1-1",
    "float": 0.0,
    "int": 0,
    "object": "example_value",
    "str": "example_value",
    "timedelta": "1000"
}

_DUMMY_VALUES_FOR_FEATURE = {
    FeatureType.Numeric: _DUMMY_VALUES_FOR_TYPE["int"],
    FeatureType.DateTime: _DUMMY_VALUES_FOR_TYPE["datetime"]
}


# TODO: Remove defaults.
def _suggest_featurizers_and_create_datatransformer(task: str,
                                                    X: pd.DataFrame,
                                                    y: Optional[DataSingleColumnInputType] = None,
                                                    featurization_config: Optional[FeaturizationConfig] = None,
                                                    is_onnx_compatible: bool = False,
                                                    observer: ExperimentObserver = NullExperimentObserver(),
                                                    enable_feature_sweeping: bool = True,
                                                    feature_sweeping_timeout: Optional[int] = None,
                                                    is_cross_validation: bool = True,
                                                    enable_dnn: bool = False,
                                                    force_text_dnn: bool = False,
                                                    feature_sweeping_config: Dict[str, Any] = {},
                                                    working_dir: Optional[str] = None,
                                                    _test_transforms: Optional[List[Any]] = None,
                                                    _feature_sweeper: Optional[Any] = None) -> DataTransformer:
    """
    Identify the transformations for all the columns in the dataframe.

    :param task: Experiment task.
    :param X: Input training data.
    :param y: Optional label data.
    :param featurization_config: Featurization configuration if provided by the user.
    :param is_onnx_compatible: If the model needs to be ONNX compatible.
    :param observer: Experiment observer.
    :param enable_feature_sweeping: If feature sweeping is enabled.
    :param feature_sweeping_timeout: Specific timeout for feature sweeping in case it is enabled.
    :param is_cross_validation: If the current experiment is cross validation based.
    :param enable_dnn: If DNN is enabled.
    :param force_text_dnn: If DNN should be forced.
    :param feature_sweeping_config: Feature sweeping configuration.
    :param working_dir: Working directory
    :param _test_transforms: (Internal only)Any test transforms that need to be added.
    :param _feature_sweeper: (Internal only)Custom feature sweeper for testing.
    :return: A DataTransformer
    """
    with tracer.start_as_current_span(
            constants.TelemetryConstants.SPAN_FORMATTING.format(
                constants.TelemetryConstants.COMPONENT_NAME, constants.TelemetryConstants.FEATURIZATION_STRATEGY
            ),
            user_facing_name=constants.TelemetryConstants.FEATURIZATION_STRATEGY_USER_FACING
    ):
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)

        (
            raw_feature_names,
            pre_processing_stats,
            stats_and_column_purposes,
            engg_featname_gen_holder,
            transformer_and_mapper_list,
        ) = ml_engine.suggest_featurizers(
            task=task,
            X=X,
            y=y,
            featurization_config=featurization_config,
            is_onnx_compatible=is_onnx_compatible,
            observer=observer,
            enable_feature_sweeping=enable_feature_sweeping,
            feature_sweeping_timeout=feature_sweeping_timeout or DataTransformer.DEFAULT_DATA_TRANSFORMER_TIMEOUT_SEC,
            is_cross_validation=is_cross_validation,
            enable_dnn=enable_dnn,
            force_text_dnn=force_text_dnn,
            feature_sweeping_config=feature_sweeping_config,
            working_dir=working_dir,
            _test_transforms=_test_transforms,
            _feature_sweeper=_feature_sweeper
        )

        dt = DataTransformer(task=task,
                             is_onnx_compatible=is_onnx_compatible,
                             enable_feature_sweeping=enable_feature_sweeping,
                             enable_dnn=enable_dnn,
                             force_text_dnn=force_text_dnn,
                             observer=observer,
                             featurization_config=featurization_config,
                             is_cross_validation=is_cross_validation,
                             feature_sweeping_config=feature_sweeping_config,
                             working_dir=working_dir,
                             )

        dt._columns_types_mapping = data_transformer_utils.get_pandas_columns_types_mapping(X)
        dt._raw_feature_names = raw_feature_names
        dt._pre_processing_stats = pre_processing_stats
        dt.stats_and_column_purposes = stats_and_column_purposes
        dt._engineered_feature_names_class = engg_featname_gen_holder
        dt.transformer_and_mapper_list = transformer_and_mapper_list
        dt._is_text_dnn = any(dt._set_is_text_dnn_if_available(t) for t in transformer_and_mapper_list)
        dt._feature_sweeped = enable_feature_sweeping
        return dt


def build_feature_sweeped_state_container(
        raw_data_context: RawDataContext,
        cache_store: CacheStore,
        is_onnx_compatible: bool,
        experiment_observer: ExperimentObserver,
        enable_feature_sweeping: bool,
        feature_sweeping_config: Dict[str, Any],
        enable_dnn: bool,
        force_text_dnn: bool,
        featurizer_container: FeaturizerContainer
) -> FeatureSweepedStateContainer:
    """
    Builds a feature sweeped state container.

    :param raw_data_context: The raw input data.
    :param cache_store: The object that should be used to cache featurized data.
    :param is_onnx_compatible: If works in onnx compatible mode.
    :param experiment_observer: The experiment observer.
    :param enable_feature_sweeping: Enable or disable feature sweeping.
    :param feature_sweeping_config: Config used for feature sweeping.
    :param enable_dnn: Flag to enable neural networks for forecasting and natural language processing.
    :param force_text_dnn: Flag to force add neural networks for natural language processing in feature sweeping.
    :param featurizer_container: The featurizer container.
    :return: The feature sweeped state container to use for featurization.
    """
    transformed_data_context, y_transformer, X, y = create_transformed_data_context_no_streaming(
        raw_data_context,
        cache_store)
    transformed_data_context.X = _data_transformation_utilities._add_raw_column_names_to_X(
        transformed_data_context.X,
        raw_data_context.x_raw_column_names)

    featurization_config = raw_data_context.featurization if isinstance(raw_data_context.featurization,
                                                                        FeaturizationConfig) else None
    data_transformer = DataTransformer(
        task=raw_data_context.task_type,
        is_onnx_compatible=is_onnx_compatible,
        enable_feature_sweeping=enable_feature_sweeping,
        enable_dnn=enable_dnn,
        force_text_dnn=force_text_dnn,
        observer=experiment_observer,
        featurization_config=featurization_config,
        is_cross_validation=transformed_data_context._is_cross_validation_scenario(),
        feature_sweeping_config=feature_sweeping_config
    )
    # This is a separate featurization run, so we need to restore the data_transformer.
    _data_transformation_utilities.load_and_update_from_sweeping(data_transformer, transformed_data_context.X)
    data_transformer.set_cached_featurizers(
        _data_transformation_utilities.pull_fitted_featurizers_from_cache(cache_store, featurizer_container))
    data_transformer._featurizer_container = featurizer_container

    return FeatureSweepedStateContainer(
        data_transformer, transformed_data_context, y_transformer, X, y)


def create_transformed_data_context_no_streaming(raw_data_context: RawDataContext,
                                                 cache_store: CacheStore,
                                                 verifier: Optional[VerifierManager] = None) \
        -> Tuple[TransformedDataContext, Optional[preprocessing.LabelEncoder], DataInputType, np.ndarray]:
    """
    Helper function for transforming input raw data from JOS to a transformed data context for further processing.
    We have already checked to ensure that streaming is not turned on.

    :param raw_data_context: The raw input data.
    :param cache_store: The object that should be used to cache featurized data.
    :param verifier: The verifier to check input data quality.
    :return: Transformed data context.
    """
    _logger.info("Pre-processing user data")
    _logger.info("The size of the raw data is: " + str(raw_data_context._get_memory_size()))

    y_df = raw_data_context.y
    Validation.validate_value(y_df, "y", reference_code=ReferenceCodes._DATA_TRANSFORMATION_INVALID_Y)

    if not isinstance(y_df, pd.DataFrame):
        try:
            y_df = pd.DataFrame(y_df)
        except ValueError as ve:
            raise ValidationException._with_error(
                AzureMLError.create(InvalidArgumentType, target="y", argument="y", actual_type=type(y_df),
                                    expected_types="pandas.DataFrame"),
                inner_exception=ve
            ) from ve

    y_raw_stats = RawFeatureStats(y_df.iloc[:, 0])
    utilities._log_raw_data_stat(
        y_raw_stats,
        prefix_message="[YCol]"
    )

    x_is_sparse = sparse.issparse(raw_data_context.X)
    if skip_featurization(raw_data_context.featurization) or x_is_sparse:
        # log the data characteristics as it won't be going into featurization.
        if x_is_sparse:
            _logger.info("The sparse matrix is not supported for getting col characteristics.")
        else:
            x_df = raw_data_context.X
            if not isinstance(x_df, pd.DataFrame):
                x_df = pd.DataFrame(raw_data_context.X)
            for column in x_df.columns:
                raw_stats = RawFeatureStats(x_df[column])
                utilities._log_raw_data_stat(
                    raw_stats,
                    prefix_message="[XColNum:{}]".format(x_df.columns.get_loc(column))
                )

    _log_data_info('X_raw', raw_data_context.X)
    _log_data_info('X_valid_raw', raw_data_context.X_valid)
    _log_data_info('y_raw', raw_data_context.y)
    _log_data_info('y_valid_raw', raw_data_context.y_valid)

    X, y, sample_weight = data_cleaning._remove_nan_rows_in_X_y(
        raw_data_context.X, raw_data_context.y,
        sample_weight=raw_data_context.sample_weight,
        is_timeseries=raw_data_context.timeseries,
        target_column=raw_data_context.label_column_name,
        featurization_config=raw_data_context.featurization
    )

    X_valid, y_valid, sample_weight_valid = data_cleaning._remove_nan_rows_in_X_y(
        raw_data_context.X_valid, raw_data_context.y_valid,
        sample_weight=raw_data_context.sample_weight_valid,
        is_timeseries=raw_data_context.timeseries,
        target_column=raw_data_context.label_column_name,
        featurization_config=raw_data_context.featurization
    )

    # Save off raw cleaned data to be cached
    X_raw_cleaned = X
    y_raw_cleaned = y
    X_valid_raw_cleaned = X_valid
    y_valid_raw_cleaned = y_valid

    # After NaNs are handled from data_cleaning._remove_nan_rows_in_X_y(),
    # if featurization is turned off (which means AutoML is not handling missing value)
    # and data is sparse (data contains 50 percent or more NaNs),
    # we need to convert it to sparse.spmatrix so that Miro can suggest pipelines that are sparse-compatible.
    if skip_featurization(raw_data_context.featurization, raw_data_context.timeseries):
        count_nans = _data_transformation_utilities.count_nans_in_data(X)
        if count_nans > 0:
            if _data_transformation_utilities.should_convert_data_to_sparse(X, count_nans):
                _logger.info("Data detected as sparse with more than 50 percent NaNs, "
                             "but featurization is turned off and is omitting imputation. "
                             "Converting the data into sparse matrix.")
                X = _data_transformation_utilities.convert_data_to_sparse(X)
                X_valid = _data_transformation_utilities.convert_data_to_sparse(X_valid)
            else:
                _logger.info("Data contains NaN but is detected as dense since it contains less than 50 percent NaNs. "
                             "Featurization is turned off and is omitting imputation. "
                             "If NaNs are not expected, consider turning on featurization or cleaning up data.")
            if verifier is not None:
                verifier.update_data_verifier_for_missing_values(verifier_result=VerifierResults.ALERTED)

    y_transformer, y, y_valid = _y_transform(y, y_valid, raw_data_context.task_type)

    enable_class_balancing = False
    class_balancing_fixed = False
    if raw_data_context.task_type == constants.Tasks.CLASSIFICATION and verifier is not None:
        enable_class_balancing, size_of_smallest_class, name_of_smallest_class = \
            _class_balancing_check(y, y_transformer)
        verifier.update_data_verifier_for_class_balancing_validation(enable_class_balancing,
                                                                     class_balancing_fixed,
                                                                     size_of_smallest_class,
                                                                     name_of_smallest_class, y.shape[0])

    transformed_data_context = TransformedDataContext(X=X,
                                                      y=y,
                                                      X_valid=X_valid,
                                                      y_valid=y_valid,
                                                      sample_weight=sample_weight,
                                                      sample_weight_valid=sample_weight_valid,
                                                      x_raw_column_names=raw_data_context.x_raw_column_names,
                                                      cv_splits_indices=raw_data_context.cv_splits_indices,
                                                      num_cv_folds=raw_data_context.num_cv_folds,
                                                      validation_size=raw_data_context.validation_size,
                                                      timeseries=raw_data_context.timeseries,
                                                      timeseries_param_dict=raw_data_context.timeseries_param_dict,
                                                      cache_store=cache_store,
                                                      task_type=raw_data_context.task_type,
                                                      X_raw_cleaned=X_raw_cleaned,
                                                      y_raw_cleaned=y_raw_cleaned,
                                                      X_valid_raw_cleaned=X_valid_raw_cleaned,
                                                      y_valid_raw_cleaned=y_valid_raw_cleaned)

    _log_data_info('X', transformed_data_context.X)
    _log_data_info('X_valid', transformed_data_context.X_valid)
    _log_data_info('y', transformed_data_context.y)
    _log_data_info('y_valid', transformed_data_context.y_valid)

    return transformed_data_context, y_transformer, X, y


def get_transformers_for_full_featurization(raw_data_context: RawDataContext,
                                            cache_store: CacheStore,
                                            is_onnx_compatible: bool = False,
                                            experiment_observer: Optional[ExperimentObserver] = None,
                                            enable_feature_sweeping: bool = False,
                                            verifier: Optional[VerifierManager] = None,
                                            enable_streaming: bool = False,
                                            feature_sweeping_config: Dict[str, Any] = {},
                                            enable_dnn: bool = False,
                                            force_text_dnn: bool = False,
                                            working_dir: Optional[str] = None) \
        -> Optional[FeatureSweepedStateContainer]:
    """
    Performs the feature sweeping part of data transformation for all standard code paths.

    :param raw_data_context: The raw input data.
    :param cache_store: The object that should be used to cache featurized data.
    :param is_onnx_compatible: If works in onnx compatible mode.
    :param experiment_observer: The experiment observer.
    :param enable_feature_sweeping: Enable or disable feature sweeping.
    :param verifier: The verifier to check input data quality.
    :param enable_streaming: Enable or disable streaming.
    :param feature_sweeping_config: Config used for feature sweeping.
    :param enable_dnn: Flag to enable neural networks for forecasting and natural language processing.
    :param force_text_dnn: Flag to force add neural networks for natural language processing in feature sweeping.
    :param working_dir: Working directory to use for featurization/training.
    :return: Container for objects generated by feature sweeping that will be needed in full featurization.
    """
    if enable_streaming or raw_data_context.timeseries or \
            skip_featurization(raw_data_context.featurization, raw_data_context.timeseries):
        scenario_types_for_logging = []
        if enable_streaming:
            scenario_types_for_logging.append("streaming")
        if raw_data_context.timeseries:
            scenario_types_for_logging.append("timeseries")
        if skip_featurization(raw_data_context.featurization, raw_data_context.timeseries):
            scenario_types_for_logging.append("skip featurization")
        _logger.info("Skipping mainstream sweeping logic. Detected {} scenario.".format(
            " + ".join(scenario_types_for_logging)))
        return None

    transformed_data_context, y_transformer, X, y = \
        create_transformed_data_context_no_streaming(raw_data_context,
                                                     cache_store,
                                                     verifier)
    if not sparse.issparse(transformed_data_context.X):
        transformed_data_context.X = _data_transformation_utilities._add_raw_column_names_to_X(
            transformed_data_context.X, raw_data_context.x_raw_column_names)

        featurization_config = None
        if isinstance(raw_data_context.featurization, FeaturizationConfig):
            featurization_config = raw_data_context.featurization

        is_cross_validation = transformed_data_context._is_cross_validation_scenario()
        with logging_utilities.log_activity(logger=_logger, activity_name="Beginning feature sweeping."):
            data_transformer = _suggest_featurizers_and_create_datatransformer(
                task=raw_data_context.task_type,
                X=transformed_data_context.X,
                y=transformed_data_context.y,
                featurization_config=featurization_config,
                observer=experiment_observer or NullExperimentObserver(),
                enable_feature_sweeping=enable_feature_sweeping,
                is_onnx_compatible=is_onnx_compatible,
                enable_dnn=enable_dnn,
                force_text_dnn=force_text_dnn,
                feature_sweeping_config=feature_sweeping_config,
                is_cross_validation=is_cross_validation,
                working_dir=working_dir)

        if verifier is not None:
            verifier.update_data_verifier_for_missing_values(data_transformer)
            verifier.update_data_verifier_for_text_class_validation(data_transformer.stats_and_column_purposes)

        return FeatureSweepedStateContainer(data_transformer=data_transformer,
                                            transformed_data_context=transformed_data_context,
                                            y_transformer=y_transformer,
                                            x=X,
                                            y=y)
    return None


def transform_data_streaming(raw_data_context: RawDataContext,
                             observer: Optional[ExperimentObserver] = None) -> StreamingTransformedDataContext:
    """
    Transform the input from RawDataContext to StreamingTransformedDataContext

    :param raw_data_context: The raw input data.
    :return: Transformed data context.
    """
    result = StreamingTransformedDataContext(x_raw_column_names=raw_data_context.x_raw_column_names,
                                             training_data=raw_data_context.training_data,
                                             label_column_name=raw_data_context.label_column_name,
                                             raw_data_snapshot='',
                                             weight_column_name=raw_data_context.weight_column_name,
                                             validation_data=raw_data_context.validation_data)

    if not skip_featurization(raw_data_context.featurization):
        streaming_featurizer = StreamingFeaturizer(
            raw_data_context.training_data,
            raw_data_context.label_column_name,
            raw_data_context.weight_column_name,
            observer=observer,
            featurization_config=raw_data_context.featurization
            if isinstance(raw_data_context.featurization, FeaturizationConfig) else None)

        _logger.info("Learning streaming transformations...")
        streaming_featurization_transformer = streaming_featurizer.learn_transformations()

        result.set_featurization_transformer(streaming_featurization_transformer)
        result.set_featurized_column_names(streaming_featurizer.get_transformed_vector_column_names())

    return result


def _log_data_info(data_name: str,
                   data: Optional[np.ndarray]) -> None:
    """
    Log details about the data.

    :param data_name: Name of data to inspect.
    :param data: Data to inspect.
    """
    if data is not None:
        message_format = "{} datatype is {}, shape is {}, datasize is {}."
        memory_size = memory_utilities.get_data_memory_size(data)
        _logger.info(message_format.format(data_name, type(data), data.shape, memory_size))
    else:
        message_format = "{} is None, no data details to log."
        _logger.info(message_format.format(data_name))


def _get_dummy_value_by_purpose_or_dtype(purpose: Optional[FeatureType] = None,
                                         npdtype: Optional[np.dtype] = None) -> Any:
    """
    Get dummy values by either purpose or dtype of the column. If dtype is provided, it will get preference
    over purpose since dtypes are more accurate. If dtype is not provided, dummy value is picked based on
    the purpose.

    :param purpose: The FeatureType of the column
    :param npdtype: The dtype of the column
    :return: The dummy value
    """
    if npdtype:
        # we know the dtype because it was pandas dataframe
        for dtype_substring in _DUMMY_VALUES_FOR_TYPE.keys():
            if dtype_substring in npdtype.name:
                return _DUMMY_VALUES_FOR_TYPE[dtype_substring]

    if purpose:
        # if the user passed a numpy array we rely on the column purpose.
        return _DUMMY_VALUES_FOR_FEATURE.get(str(purpose), _DUMMY_VALUES_FOR_TYPE['str'])

    # If neither the dtype nor column purpose is known, it means featurization was turned off and
    # the user passed a numpy array or a sparse matrix. We can safely return a numeric value.
    return _DUMMY_VALUES_FOR_TYPE['int']


def _get_data_snapshot_helper(data: Union[pd.DataFrame, pd.Series],
                              column_names_and_types: Optional[Dict[str, np.dtype]] = None,
                              column_purposes: Optional[List[StatsAndColumnPurposeType]] = None) -> str:
    Contract.assert_type(data, "data", (pd.DataFrame, pd.Series))
    if isinstance(data, pd.DataFrame):
        Contract.assert_value(column_names_and_types, "column_names_and_types")
        col_str_list = []
        column_names_and_types = cast(Dict[str, np.dtype], column_names_and_types)
        for col in column_names_and_types.keys():
            dtype = column_names_and_types[col]
            col_val = _get_dummy_value_by_purpose_or_dtype(npdtype=dtype)
            col_val = json.dumps([col_val]) if isinstance(col_val, str) else [col_val]
            col_str = "{0}: pd.Series({1}, dtype={2})".format(
                json.dumps(str(col)), col_val, json.dumps(str(dtype)))
            col_str_list.append(col_str)
        snapshot_str = "{" + ", ".join(col_str_list) + "}"
    else:
        # data is of type pd.Series
        if not column_purposes:
            # if column_purposes is not set, featurization was turned off
            # construct the column purpose array and set the purpose and raw_stats set to None
            column_purposes = [(None, None, col) for col in range(len(data))]  # type:ignore
        dummy_data = pd.Series([_get_dummy_value_by_purpose_or_dtype(purpose=purpose)  # type:ignore
                                for rawstats, purpose, col in column_purposes])
        snapshot_json_str = dummy_data.to_json(orient='values', date_format='iso')
        snapshot_str = str(json.loads(snapshot_json_str))
    return snapshot_str


def _get_data_snapshot(data: DataInputType, column_names_and_types: Optional[Dict[str, np.dtype]] = None,
                       column_purposes: Optional[List[StatsAndColumnPurposeType]] = None,
                       is_forecasting: bool = False) -> Any:
    Contract.assert_value(data, "data")
    try:
        if isinstance(data, Dataflow) and not column_names_and_types:
            # We need some data to figure out pandas dtypes.
            data = data.take(1000).to_pandas_dataframe()

        Validation.validate_type(data, "data", (np.ndarray, pd.DataFrame, sparse.spmatrix))

        if isinstance(data, pd.DataFrame) or isinstance(data, Dataflow):
            first_row = data.head(1)
            if not column_names_and_types:
                column_names_and_types = data.dtypes.to_dict()
            df_str = _get_data_snapshot_helper(first_row,
                                               column_names_and_types=column_names_and_types,
                                               column_purposes=column_purposes)
            sample_df_str = 'pd.DataFrame(' + df_str + ')'
            return sample_df_str
        elif isinstance(data, np.ndarray):
            np_array_str = _get_data_snapshot_helper(pd.Series(data[0]), column_purposes=column_purposes)
            sample_numpy_array_str = 'np.array([' + np_array_str + '])'
            return sample_numpy_array_str
        elif sparse.issparse(data):
            # Assuming that sparse matrix will be inferenced as a numpy array
            # TODO: Test sparse matrices with inference scenario
            np_array_str = _get_data_snapshot_helper(pd.Series(data[0, :].toarray().ravel()),
                                                     column_purposes=column_purposes)
            sample_sparse_array_str = 'np.array([' + np_array_str + '])'
            return sample_sparse_array_str
    except (DataException, ValidationException):
        raise
    except Exception as e:
        exception_error_msg = "Raw data snapshot failed with exception of type: {}".format(type(e))
        _logger.error(exception_error_msg)
        error = AzureMLError.create(AutoMLInternal, error_details=exception_error_msg)
        raise ClientException(azureml_error=error, inner_exception=e) from e


def _y_transform(
        y: np.ndarray, y_valid: Optional[np.ndarray], task_type: str
) -> Tuple[Optional[preprocessing.LabelEncoder], np.ndarray, Optional[np.ndarray]]:
    """
    Apply label encoder for string, float and negative int type y data.

    :param y: y data
    :param y_valid: Validation y data
    :param task_type: CLASSIFICATION/REGRESSION
    :return:
    """
    y_transformer = None
    if task_type == constants.Tasks.CLASSIFICATION:
        y_type = runtime_utilities._get_column_data_type_as_str(y)
        y_valid_type = None if y_valid is None else runtime_utilities._get_column_data_type_as_str(y_valid)
        if runtime_utilities._is_y_transform_needed(y, y_type) or \
                runtime_utilities._is_y_transform_needed(y_valid, y_valid_type):
            # Currently y_transformer only support the label encoder for negative, float and categorical data.
            y_is_numeric = utilities._check_if_column_data_type_is_numerical(y_type)
            if y_valid is None:
                if runtime_utilities._is_y_mixed_type(y_type) and not y_is_numeric:
                    y = pd.Series(y).apply(str).values
            else:
                y_valid_type = str(y_valid_type)
                y_valid_is_numeric = utilities._check_if_column_data_type_is_numerical(y_valid_type)
                if runtime_utilities._is_y_conversion_needed(y_type, y_is_numeric, y_valid_type, y_valid_is_numeric):
                    y = pd.Series(y).apply(str).values
                if runtime_utilities._is_y_conversion_needed(y_valid_type, y_valid_is_numeric, y_type, y_is_numeric):
                    y_valid = pd.Series(y_valid).apply(str).values

            _logger.info("Start doing label encoding on y data.")
            y_transformer = preprocessing.LabelEncoder()
            if y_valid is None:
                le = y_transformer.fit(y)
                y = le.transform(y)
            else:
                le = y_transformer.fit(np.vstack([y.reshape(-1, 1), y_valid.reshape(-1, 1)]))
                y = le.transform(y)
                y_valid = le.transform(y_valid)
            _logger.info("End doing label encoding on y data.")
    return y_transformer, y, y_valid


def _class_balancing_check(y, y_transformer):
    """
    Class balancing check based on y distribution.
    Imbalance would be detected if the Size of the minority class/Size of the majority class <= 20%.
    Comparison between minority & majority class, as opposed to minority class & overall training samples,
    makes more sense as demonstrated with this example:

    For a four class problem with data distributed among labels like this:{'a': 20, 'b': 20, 'c': 20, 'd': 200},
    the fraction of minority to majority is 10%, while minority to overall is 7.7%.

    For a four class problem with data distributed among labels like this:{'a': 20, 'b': 200, 'c': 200, 'd': 200},
    the fraction of minority to majority is 10%, while minority to overall is 3.2%.

    The first fraction is consistent, regardless of other classes and hence gives a more stable estimate of what
    clearly is an imbalance.

    :param y: Training y data
    :param y_transformer: Label-Encoder/Transformer used to encode target/label values
    :return: is class imbalanced, size of smallest class in y, name of smallest class in y
    """
    _logger.info("Start checking class balancing on y data.")
    if y_transformer is not None:
        y = y_transformer.inverse_transform(y)
    labels, counts = np.unique(y, return_counts=True)
    _logger.info("Num of classes: {}, Minority class size: {}, Majority class size: {}".format(len(counts),
                                                                                               min(counts),
                                                                                               max(counts)))
    is_class_imbalanced = False
    if float(min(counts)) <= constants.CheckImbalance.MINORITY_TO_MAJORITY_THRESHOLD_RATIO * float(max(counts)):
        is_class_imbalanced = True
    if is_class_imbalanced:
        _logger.info("Classes are imbalanced in training data.")

    size_of_smallest_class = min(counts)
    name_of_smallest_class = labels[np.argwhere(counts == size_of_smallest_class)]
    name_of_smallest_class = ', '.join(map(str, name_of_smallest_class.flatten()))
    return is_class_imbalanced, size_of_smallest_class, name_of_smallest_class


def _compute_sample_weight(y: DataSingleColumnInputType) -> np.ndarray:
    """
    Compute sample weight based on class weight.

    :param y: Input labels.
    :return: sample weights.
    """

    unique_vals = np.unique(y)

    class_weight = compute_class_weight('balanced', unique_vals, y)
    weights = {uniq: weight for uniq, weight in zip(unique_vals, class_weight)}
    sample_class_weight = [weights[label] for label in y]

    return np.array(sample_class_weight)
