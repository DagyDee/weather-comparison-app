import pandas as pd
from config import METRICS

import logging
from utils import setup_logger

from validators import (
    validate_metric_for_processing,
    validate_required_columns,
    validate_aggregation
)

setup_logger()
logger = logging.getLogger(__name__)

ALLOWED_AGGREGATIONS = {"mean", "sum", "min", "max"}

def aggregate_monthly(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Applies monthly aggregation to a specified metric column based on METRICS configuration.
    The function groups data by city and month and aggregates metrics column by the configured 'aggregation'.
 
    Parameters:
        df (pd.DataFrame): Input dataframe.
        metric (str): Metric name corresponding to a column in the DataFrame and a key in the METRICS configuration.
    Returns: Aggregated monthly values or empty DataFrame if validation fails."""
    
    if not validate_metric_for_processing(df, metric, f"aggregate_monthly:{metric}"):
        return pd.DataFrame()
    
    required_columns = {"city", "month"}
    if not validate_required_columns(df, required_columns):
        return pd.DataFrame()

    df_copy = df.copy()
    metric_config = METRICS[metric]
    agg_type = metric_config.get("aggregation")

    if not validate_aggregation(agg_type, ALLOWED_AGGREGATIONS):
        return pd.DataFrame()

    return (
        df_copy
        .groupby(["city", "month"], as_index=False)[metric]
        .agg(agg_type)
    )

