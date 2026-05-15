import pandas as pd
import logging
from config import METRICS

logger = logging.getLogger(__name__)

def validate_city(city: str, city_params: dict) -> bool:
    """Validate that city exists in CITY_PARAMS."""
    if city not in city_params:
        logger.warning("Parametry pro město '%s' nejsou nadefinované", city)
        return False
    return True

def validate_response(response: dict | None) -> bool:
    """Validate API response."""
    if not response:
        logger.error("Nebyla dodána žádná data ke zpracování.")
        return False
    return True

def validate_weather_data(data: dict | None) -> bool:
    """Validate hourly/daily data from API."""
    if not data:
        logger.error("API neobsahuje žádná hourly/daily data")
        return False
    return True

def validate_dataframe_not_empty(df: pd.DataFrame, context: str) -> bool:
    """Check that DataFrame is not empty."""
    if df.empty:
        logger.warning("DataFrame je prázdný – zdroj: %s", context)
        return False
    return True

def validate_column_exists(df: pd.DataFrame, column: str) -> bool:
    """Check that column exists in DataFrame."""
    if column not in df.columns:
        logger.warning("Sloupec '%s' není v DataFrame.", column)
        return False
    return True

def validate_required_columns(df: pd.DataFrame, columns: set[str]) -> bool:
    """Check that required columns exist."""
    if not columns.issubset(df.columns):
        missing = columns - set(df.columns)
        logger.error("Chybí povinné sloupce: %s", missing)
        return False
    return True

def validate_datetime_column(df: pd.DataFrame, column: str) -> bool:
    """Check that column is datetime. Assumes that the column exists in the DataFrame."""
    if not pd.api.types.is_datetime64_any_dtype(df[column]):
        logger.warning("Sloupec '%s' není typu datetime.", column)
        return False
    return True

def validate_metric(metric: str) -> bool:
    """Check that metric exists in configuration."""
    if metric not in METRICS:
        logger.error("Neznámá metrika: %s", metric)
        return False
    return True

def validate_metric_column(df: pd.DataFrame, metric: str) -> bool:
    """Check that metric column exists."""
    if metric not in df.columns:
        logger.error("Sloupec '%s' chybí v datech.", metric)
        return False
    return True

def validate_numeric_column(df: pd.DataFrame, column: str) -> bool:
    """Check that column is numeric."""
    if not pd.api.types.is_numeric_dtype(df[column]):
        logger.error("Sloupec '%s' musí mít číselnou hodnotu.", column)
        return False
    return True

def validate_unit_divider(divider: int | float | None, metric: str) -> bool:
    """Validate unit divider."""
    if divider == 0:
        logger.error("unit_divider pro metriku '%s' nesmí být 0", metric)
        return False
    return True

def validate_aggregation(agg_type: str, allowed: set[str]) -> bool:
    """Validate aggregation type."""
    if agg_type not in allowed:
        logger.error("Nepodporovaná agregace: %s", agg_type)
        return False
    return True

# composed helpers

def validate_time_column_ready(df: pd.DataFrame, column: str) -> bool:
    """Check that DataFrame has a valid datetime column."""
    return (
        validate_dataframe_not_empty(df, f"validate_time_column_ready:{column}")
        and validate_column_exists(df, column)
        and validate_datetime_column(df, column)
    )

def validate_metric_for_processing(df: pd.DataFrame, metric: str, context: str) -> bool:
    """Check that metric is valid and ready for processing."""
    return (
        validate_dataframe_not_empty(df, context)
        and validate_metric(metric)
        and validate_metric_column(df, metric)
        and validate_numeric_column(df, metric)
    )

