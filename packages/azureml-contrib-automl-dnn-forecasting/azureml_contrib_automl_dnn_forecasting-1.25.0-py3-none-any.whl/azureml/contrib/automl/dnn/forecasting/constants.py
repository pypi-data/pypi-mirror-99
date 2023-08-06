# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module containing Forecast Constants."""

import importlib
import os
importlib.import_module('azureml.automl.core')
importlib.import_module('azureml.automl.runtime')
# Above import sets the path needed to import the below module automl.client.
import azureml.automl.core.shared.constants as constants   # noqa E402


class ForecastConstant:
    """Constants for Forecast DNN training."""

    Deep4Cast = 'Deep4Cast'
    ForecastTCN = 'TCNForecaster'
    model = 'model'
    output_dir = 'output_dir'
    primary_metric = 'primary_metric'
    default_primary_metric = 'normalized_root_mean_squared_error'
    report_interval = 'report_interval'
    dataset_json = 'dataset_json'
    dataset_json_file = 'dataset_json_file'
    num_epochs = 'num_epochs'
    Learning_rate = 'learning_rate'
    Horizon = 'max_horizon'
    Lookback = 'lookback'
    LabelColumnName = 'label_column_name'
    Batch_size = 'batch_size'
    Optim = 'optim'
    Loss = 'loss'
    Device = 'device'
    n_layers = 'n_layers'
    year_iso_col = 'year_iso'
    year_col = 'year_iso'
    namespace = 'azureml.contrib.automl.dnn.forecasting'
    dataset_settings = 'dataset_settings'
    config_json = 'config_json'
    config_json_default = 'settings.json'
    apply_timeseries_transform = 'apply_timeseries_transform'
    time_column_name = constants.TimeSeries.TIME_COLUMN_NAME
    max_horizon_default = constants.TimeSeriesInternal.MAX_HORIZON_DEFAULT
    auto = constants.TimeSeries.AUTO
    grain_column_names = constants.TimeSeries.GRAIN_COLUMN_NAMES
    drop_column_names = constants.TimeSeries.DROP_COLUMN_NAMES
    country_region = constants.TimeSeries.COUNTRY_OR_REGION
    dummy_grain_column = constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN
    cross_validations = constants.TimeSeriesInternal.CROSS_VALIDATIONS
    time_series_internal = constants.TimeSeriesInternal
    time_series = constants.TimeSeries
    automl_constants = constants
    MODEL_PATH = constants.OUTPUT_PATH + "/" + 'model.pt'
    LOCAL_MODEL_PATH = constants.LOCAL_OUTPUT_PATH + "/" + 'model.pt'
    MODEL_FILENAME = 'model.pt'
    FORECAST_VALID_SETTINGS = [apply_timeseries_transform,
                               drop_column_names,
                               country_region,
                               dummy_grain_column,
                               grain_column_names,
                               time_column_name,
                               LabelColumnName,
                               cross_validations]
    SMALL_DATASET_MAX_ROWS = 10000


# TODO: remove FeatureType class once we have new automl sdk and this code is in prod,
# we need to update automl-core dependency in requirements.txt once we move to use latest code.
class FeatureType:
    """Names for feature types that are recognized."""

    Numeric = 'Numeric'
    DateTime = 'DateTime'
    Categorical = 'Categorical'
    CategoricalHash = 'CategoricalHash'
    Text = 'Text'
    Hashes = 'Hashes'
    Ignore = 'Ignore'
    AllNan = 'AllNan'


class TCNForecastParameters:
    """Model parameters constants for TCN Model."""

    NUM_CELLS = 'num_cells'  # Number of cells for backbone
    MULTILEVEL = 'multilevel'  # MultilevelType for backbones
    DEPTH = 'depth'  # Cell depth
    NUM_CHANNELS = 'num_channels'  # Number of channels
    DROPOUT_RATE = 'dropout_rate'  # Dropout rate


DROP_COLUMN_LIST = {constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN, ForecastConstant.year_col,
                    ForecastConstant.year_iso_col}
