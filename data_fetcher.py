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
        
        logger.info("Data úspěšně získána z API")
        return response.json()

    except requests.exceptions.HTTPError as e:
        logger.error("HTTP chyba při volání API (status=%s)", e.response.status_code)
    except requests.exceptions.Timeout:
        logger.exception("Požadavek vypršel (timeout)")
    except requests.exceptions.ConnectionError:
        logger.exception("Problém s připojením k API")
    except requests.exceptions.RequestException:
        logger.exception("Obecná chyba při HTTP požadavku")
    except ValueError:
        logger.exception("Odpověď není validní JSON")
    return None
