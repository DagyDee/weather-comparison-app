import pandas as pd
from data_fetcher import fetch_data
from config import API_URL, CITY_PARAMS


def get_city_data(city: str) -> pd.DataFrame:
    """Retrieves and transforms hourly or daily weather data
    for a given city into a structured pandas DataFrame."""
    
    if city not in CITY_PARAMS:
        print(f"Parametry pro město '{city}' nejsou nadefinované")
        return pd.DataFrame()
    
    response = fetch_data(API_URL, CITY_PARAMS[city])
    if not response:
        print("Nedodány data ke zpracování")
        return pd.DataFrame()

    data = response.get("hourly") or response.get("daily")
    
    df = pd.DataFrame(data)
    df["city"] = city
    return df


def prepare_weather_data(df_list: list[pd.DataFrame]) -> pd.DataFrame:
    """Concatenates a list of city weather DataFrames into one unified DataFrame,
    converts the 'time' column to datetime, and normalizes units.

    Parameters: List of DataFrames obtained for individual cities.
    Returns: Combined and cleaned DataFrame with unified formats."""

    df_data = pd.concat(df_list)  # sloučení dataframů pod sebe
    df_data["time"] = pd.to_datetime(df_data["time"])  # převod formátu na datum
    df_data["sunshine_duration"] = df_data["sunshine_duration"] / 3600  # převod sec -> hod
    return df_data


def get_monthly_averages(df_data: pd.DataFrame) -> pd.DataFrame:
    """Compute monthly average sunshine duration for each city.

    Parameters: Input DataFrame containing daily weather data with columns
    'time', 'city', and 'sunshine_duration'.

    Returns: A DataFrame aggregated by city and month, containing the mean
    daily sunshine duration for each month. Suitable for visualization."""

    df_data["month"] = df_data["time"].dt.month
    
    # Group by city + month and compute mean sunshine duration
    df_monthly_data = (
        df_data
        .groupby(["city", "month"], as_index=False)["sunshine_duration"]
        .mean()
        .rename(columns={"sunshine_duration": "mean_sunshine_duration"})
        )
    
    return df_monthly_data