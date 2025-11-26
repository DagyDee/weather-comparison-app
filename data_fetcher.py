import requests

def fetch_data(url: str, params: dict) -> dict | None:
    """Fetches weather data from the specified API endpoint 
    and parses the JSON response into a Python dictionary."""
    try:
        response = requests.get(url, params=params, timeout=(5, 30))  # timeout=(connect_timeout, read_timeout) 

        if response.status_code == 200:
            try:
                data = response.json()
                print("Data úspěšně získána")
                return data
            except ValueError:
                print("Odpověď není validní JSON")
                return None

        elif response.status_code == 404:
            print("Požadovaný zdroj nebyl nalezen (404)")
        elif response.status_code == 500:
            print("Chyba na straně serveru (500)")
        else:
            print(f"Neočekávaná chyba: {response.status_code}")

    except requests.exceptions.Timeout:
        print("Požadavek vypršel (timeout)")
    except requests.exceptions.ConnectionError:
        print("Problém s připojením")
    except requests.exceptions.RequestException as e:
        print(f"Nastala chyba: {e}")

    return None
