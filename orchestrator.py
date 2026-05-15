import pandas as pd
from config import CITY_PARAMS, METRICS

from loaders import get_city_data, merge_dataframes
from transformers import ensure_datetime, add_month_column, apply_unit_conversion
from aggregations import aggregate_monthly

import logging
from utils import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

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
