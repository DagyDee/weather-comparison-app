import pandas as pd
from data_fetcher import fetch_data
from config import API_URL, DATA_KEY, CITY_PARAMS

import logging
from utils import setup_logger

from validators import (
    validate_city,
    validate_response,
    validate_weather_data,
    validate_dataframe_not_empty,
)

setup_logger()
logger = logging.getLogger(__name__)

def get_city_data(city: str) -> pd.DataFrame:
    """Fetch weather data for a given city based on configured DATA_KEY and returns it as a DataFrame."""
    
    if not validate_city(city, CITY_PARAMS):
        return pd.DataFrame()
    
    response = fetch_data(API_URL, CITY_PARAMS[city])
    if not validate_response(response):
        return pd.DataFrame()

    data = response.get(DATA_KEY)
    if not validate_weather_data(data):
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    df["city"] = city
    return df

def merge_dataframes(df_list: list[pd.DataFrame]) -> pd.DataFrame:
    """Concatenates a list of weather DataFrames into a single DataFrame.
    Empty DataFrames are filtered out before concatenation.

    Parameters: df_list (list[pd.DataFrame]): List of DataFrames for individual cities.
    Returns: pd.DataFrame: Unified DataFrame or empty DataFrame if no valid data provided."""
    
    valid_dfs = [df for df in df_list if validate_dataframe_not_empty(df, "merge_dataframes")]
    if not valid_dfs:
        logger.warning("Všechna vstupní data jsou prázdná – zpracování přerušeno")
        return pd.DataFrame()
    return pd.concat(valid_dfs, ignore_index=True)

