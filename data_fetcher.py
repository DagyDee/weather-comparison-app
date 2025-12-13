import requests

import logging
from utils import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

def fetch_data(url: str, params: dict) -> dict | None:
    """Fetches weather data from the specified API endpoint 
    and parses the JSON response into a Python dictionary."""
    try:
        response = requests.get(url, params=params, timeout=(5, 30))
        response.raise_for_status()
        
        print("Data úspěšně získána")
        return response.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("Požadovaný zdroj nebyl nalezen (404)")
        elif e.response.status_code == 500:
            print("Chyba na straně serveru (500)")
        else:
            print(f"HTTP chyba: {e}")
    except requests.exceptions.Timeout:
        print("Požadavek vypršel (timeout)")
    except requests.exceptions.ConnectionError:
        print("Problém s připojením")
    except requests.exceptions.RequestException as e:
        print(f"Nastala chyba: {e}")
    except ValueError:
        print("Odpověď není validní JSON")
    return None
