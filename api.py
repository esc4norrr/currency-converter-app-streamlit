import requests

def get_url(url: str) -> (int, str):
    """
    Function that will call a provided GET API endpoint url and return its
    status code and either its content or error message as a string.

    Parameters
    ----------
    url : str
        URL of the GET API endpoint to be called.

    Returns
    -------
    int
        API call response status code.
    str
        Text from API call response.
    """

    try:
        response = requests.get(url, timeout=10)
        return response.status_code, response.text
    except requests.RequestException as exc:
        # In case of exception, return 0 as status code and the error message
        return 0, str(exc)

