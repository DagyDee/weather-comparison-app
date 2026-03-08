import pandas as pd
from data_fetcher import fetch_data
from config import API_URL, CITY_PARAMS, METRICS

import logging
from utils import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

ALLOWED_AGGREGATIONS = {"mean", "sum", "min", "max"}

def get_city_data(city: str) -> pd.DataFrame:
    """Fetches hourly or daily weather data for a given city and returns it as a DataFrame."""
    
    if city not in CITY_PARAMS:
        logger.warning("Parametry pro město '%s' nejsou nadefinované", city)
        return pd.DataFrame()
    
    response = fetch_data(API_URL, CITY_PARAMS[city])
    if not response:
        logger.error("Nebyla dodána žádná data ke zpracování.")
        return pd.DataFrame()

    data = response.get("hourly") or response.get("daily")
    if not data:
        logger.error("API neobsahuje žádná hourly/daily data")
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    df["city"] = city
    return df

def merge_dataframes(df_list: list[pd.DataFrame]) -> pd.DataFrame:
    """Concatenates a list of weather DataFrames into a single DataFrame.
    Empty DataFrames are filtered out before concatenation.

    Parameters: df_list (list[pd.DataFrame]): List of DataFrames for individual cities.
    Returns: pd.DataFrame: Unified DataFrame or empty DataFrame if no valid data provided."""
    
    valid_dfs = [df for df in df_list if not df.empty]
    if not valid_dfs:
        logger.warning("Všechna vstupní data jsou prázdná – zpracování přerušeno")
        return pd.DataFrame()
    return pd.concat(valid_dfs, ignore_index=True)

def ensure_datetime(df: pd.DataFrame, column: str = "time") -> pd.DataFrame:
    """Converts a dataframe column to datetime.

    Parameters:
        df (pd.DataFrame): Input dataframe.
        column (str): Column name to convert to datetime.
    Returns: DataFrame with converted datetime column or empty DataFrame if validation fails."""

    if column not in df.columns:
        logger.warning("Sloupec '%s' není v DataFrame.", column)
        return pd.DataFrame()
    
    df_copy = df.copy()
    df_copy[column] = pd.to_datetime(df_copy[column], errors="coerce")
    
    if df_copy[column].isna().any():
        logger.warning("Sloupec '%s' obsahuje neplatné hodnoty datetime.", column)
        return pd.DataFrame()
    return df_copy

def add_month_column(df: pd.DataFrame, column: str = "time") -> pd.DataFrame:
    """Adds a 'month' column extracted from a datetime column.
    
    Parameters:
        df (pd.DataFrame): Input dataframe.
        column (str): Name of the datetime column.
    Returns: DataFrame with added 'month' column or empty DataFrame if validation fails."""

    if df.empty:
        logger.warning("Vstupní DataFrame je prázdný.")
        return pd.DataFrame()

    if column not in df.columns:
        logger.warning("Sloupec '%s' není v DataFrame.", column)
        return pd.DataFrame()

    if not pd.api.types.is_datetime64_any_dtype(df[column]):
        logger.warning("Sloupec '%s' není typu datetime.", column)
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
    
    if df.empty:
        logger.warning("Vstupní DataFrame pro přepočet jednotek je prázdný")
        return pd.DataFrame()
    
    if metric not in METRICS:
        logger.error("Neznámá metrika: %s", metric)
        return pd.DataFrame()

    if metric not in df.columns:
        logger.error("Sloupec %s chybí v datech", metric)
        return pd.DataFrame()
    
    if not pd.api.types.is_numeric_dtype(df[metric]):
        logger.error("Sloupec '%s' musí mít číselnou hodnotu.", metric)
        return pd.DataFrame()
    
    df_copy = df.copy()
    metric_config = METRICS[metric]
    unit_divider = metric_config.get("unit_divider")

    if unit_divider is None:
        return df_copy

    if unit_divider == 0:
        logger.error("unit_divider pro metriku '%s' nesmí být 0", metric)
        return pd.DataFrame()

    df_copy[metric] = df_copy[metric] / unit_divider
    return df_copy

def aggregate_monthly(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Applies monthly aggregation to a specified metric column based on METRICS configuration.
    The function groups data by city and month and aggregates metrics column by the configured 'aggregation'.
 
    Parameters:
        df (pd.DataFrame): Input dataframe.
        metric (str): Metric name corresponding to a column in the DataFrame and a key in the METRICS configuration.
    Returns: Aggregated monthly values or empty DataFrame if validation fails."""
    
    if df.empty:
        logger.warning("Vstupní DataFrame pro agregaci je prázdný")
        return pd.DataFrame()
    
    if metric not in METRICS:
        logger.error("Neznámá metrika: %s", metric)
        return pd.DataFrame()

    if metric not in df.columns:
        logger.error("Sloupec %s chybí v datech", metric)
        return pd.DataFrame()
    
    if not pd.api.types.is_numeric_dtype(df[metric]):
        logger.error("Sloupec '%s' musí mít číselnou hodnotu.", metric)
        return pd.DataFrame()
    
    required_columns = {"city", "month"}
    if not required_columns.issubset(df.columns):
        logger.error("Chybí povinné sloupce pro agregaci: %s", required_columns)
        return pd.DataFrame()

    df_copy = df.copy()
    metric_config = METRICS[metric]
    agg_type = metric_config.get("aggregation")

    if agg_type not in ALLOWED_AGGREGATIONS:
        logger.error(f"Nepodporovaná agregace: {agg_type}")
        return pd.DataFrame()

    return (
        df_copy
        .groupby(["city", "month"], as_index=False)[metric]
        .agg(agg_type)
    )

def compute_monthly_metrics() -> pd.DataFrame:
    """
    Fetch weather data for all configured cities and compute
    monthly aggregated metrics.

    Processing steps:
    1. Fetch data for each city.
    2. Merge city DataFrames into a single DataFrame.
    3. Ensure the time column is in datetime format.
    4. Add a 'month' column derived from the time column.
    5. For each configured metric:
        - apply unit conversion
        - compute monthly aggregation

    Returns:
        pd.DataFrame: DataFrame containing monthly aggregated
        metrics for each city and month.
        Returns empty DataFrame if processing fails.
    """

    dfs = [get_city_data(city) for city in CITY_PARAMS]

    df = merge_dataframes(dfs)
    if df.empty:
        return df

    df = ensure_datetime(df)
    if df.empty:
        return df

    df = add_month_column(df)
    if df.empty:
        return df

    metric_results = []

    for metric in METRICS:
        df_metric = apply_unit_conversion(df, metric)
        if df_metric.empty:
            continue

        df_metric = aggregate_monthly(df_metric, metric)
        if df_metric.empty:
            continue

        metric_results.append(df_metric)

    if not metric_results:
        return pd.DataFrame()

    df = pd.concat(metric_results, ignore_index=True)
    return df.groupby(['city', 'month'], as_index=False).first()
