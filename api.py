import requests

BASE_URL = "https://api.frankfurter.app"


def get(endpoint: str, params: dict | None = None) -> dict:
    """Perform a GET request against the Frankfurter API and return JSON data.

    Parameters
    ----------
    endpoint:
        API endpoint starting with a leading ``/`` (e.g. ``"/latest"``).
    params:
        Optional dictionary of query string parameters.
    """
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
