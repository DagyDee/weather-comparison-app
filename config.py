from datetime import datetime

API_URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"

START_DATE = "2022-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")

METRICS = {
    "sunshine_duration": {
        "api_name": "sunshine_duration",
        "unit_divider": 3600,  # sec → hod
        "aggregation": "mean",
        "label": "Sluneční svit (h)",
        "title": "Průměrná denní doba slunečního svitu podle měsíců"},
    "precipitation_sum": {
        "api_name": "precipitation_sum",
        "unit_divider": None,  # mm
        "aggregation": "mean",
        "label": "Srážky (mm)",
        "title": "Průměrné denní množství srážek podle měsíců"},
    "precipitation_hours": {
        "api_name": "precipitation_hours",
        "unit_divider": None,  # hod
        "aggregation": "mean",
        "label": "Doba se srážkami (h)",
        "title": "Průměrná denní doba se srážkami podle měsíců"},
    }   

DEFAULT_PARAMS = {
    "start_date": START_DATE,
    "end_date": END_DATE,
    "daily": ",".join(metric["api_name"] for metric in METRICS.values()),
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