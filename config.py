from datetime import datetime

API_URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"

START_DATE = "2022-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")

DEFAULT_PARAMS = {
    "start_date": START_DATE,
    "end_date": END_DATE,
    "daily": "sunshine_duration",
    "timezone": "Europe/Berlin"
    }

CITY_PARAMS = {
    "Brno": {
        "latitude": 49.1952,
        "longitude": 16.608,
        **DEFAULT_PARAMS
        },
    "Plzeň": {
        "latitude": 49.6752,
        "longitude": 13.2746,
        **DEFAULT_PARAMS
        },
    }

MONTH_NAMES = {
    1: "Leden", 2: "Únor", 3: "Březen", 4: "Duben",
    5: "Květen", 6: "Červen", 7: "Červenec", 8: "Srpen",
    9: "Září", 10: "Říjen", 11: "Listopad", 12: "Prosinec"
}

CITY_COLORS = {
    "Brno": "#ff7f0e",
    "Plzeň": "#1f77b4",
}