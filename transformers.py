import pandas as pd
from config import METRICS

import logging
from utils import setup_logger

from validators import (
    validate_column_exists,
    validate_datetime_column,
    validate_time_column_ready,
    validate_metric_for_processing,
    validate_unit_divider,
)

setup_logger()
logger = logging.getLogger(__name__)

def ensure_datetime(df: pd.DataFrame, column: str = "time") -> pd.DataFrame:
    """Converts a dataframe column to datetime.

    Parameters:
        df (pd.DataFrame): Input dataframe.
        column (str): Column name to convert to datetime.
    Returns: DataFrame with converted datetime column or empty DataFrame if validation fails."""

    if not validate_column_exists(df, column):
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy[column] = pd.to_datetime(df_copy[column], errors="coerce")
    
    if not validate_datetime_column(df_copy, column):
        return pd.DataFrame()
    return df_copy

def add_month_column(df: pd.DataFrame, column: str = "time") -> pd.DataFrame:
    """Adds a 'month' column extracted from a datetime column.
    
    Parameters:
        df (pd.DataFrame): Input dataframe.
        column (str): Name of the datetime column.
    Returns: DataFrame with added 'month' column or empty DataFrame if validation fails."""

    if not validate_time_column_ready(df, column):
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy["month"] = df_copy[column].dt.month
    return df_copy

def apply_unit_conversion(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Applies unit conversion to a specified metric column based on METRICS configuration.
    The function divides the metric column by the configured 'unit_divider'.
    If no unit_divider is defined, the DataFrame is returned unchanged.
    Parameters:
        df (pd.DataFrame): Input dataframe.
        metric (str): Metric name corresponding to a column in the DataFrame and a key in the METRICS configuration.
    Returns: DataFrame with converted metric values or empty DataFrame if validation fails."""
    
    if not validate_metric_for_processing(df, metric, f"apply_unit_conversion:{metric}"):
        return pd.DataFrame()
    
    df_copy = df.copy()
    metric_config = METRICS[metric]
    unit_divider = metric_config.get("unit_divider")

    if unit_divider is None:
        return df_copy

    if not validate_unit_divider(unit_divider, metric):
        return pd.DataFrame()

    df_copy[metric] = df_copy[metric] / unit_divider
    return df_copy

