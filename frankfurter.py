"""Utility functions for interacting with the Frankfurter currency API."""

from api import get_url
import json
from datetime import date
import calendar

BASE_URL = "https://api.frankfurter.app"


def get_currencies_list():
    """
    Function that will call the relevant API endpoint from Frankfurter in order
    to get the list of available currencies. After the API call, it will perform
    a check to see if the API call was successful. If it is the case, it will
    load the response as JSON, extract the list of currency codes and return it
    as Python list. Otherwise it will return the value None.

    Parameters
    ----------
    None

    Returns
    -------
    list
        List of available currencies or None in case of error
    """

    status, text = get_url(f"{BASE_URL}/currencies")
    if status == 200:
        try:
            data = json.loads(text)
            return sorted(list(data.keys()))
        except json.JSONDecodeError:
            return None
    return None


def get_latest_rates(from_currency, to_currency, amount):
    """
    Function that will call the relevant API endpoint from Frankfurter in order
    to get the latest conversion rate between the provided currencies. After the
    API call, it will perform a check to see if the API call was successful. If
    it is the case, it will load the response as JSON, extract the latest
    conversion rate and the date and return them as 2 separate objects.
    Otherwise it will return the value None twice.

    Parameters
    ----------
    from_currency : str
        Code for the origin currency
    to_currency : str
        Code for the destination currency
    amount : float
        The amount (in origin currency) to be converted

    Returns
    -------
    str
        Date of latest FX conversion rate or None in case of error
    float
        Latest FX conversion rate or None in case of error
    """

    url = (
        f"{BASE_URL}/latest?amount={amount}&from={from_currency}&to={to_currency}"
    )
    status, text = get_url(url)
    if status == 200:
        try:
            data = json.loads(text)
            rate_val = data["rates"][to_currency] / float(amount)
            return data.get("date"), rate_val
        except (KeyError, ValueError, json.JSONDecodeError):
            return None, None
    return None, None


def get_historical_rate(from_currency, to_currency, from_date, amount):
    """
    Function that will call the relevant API endpoint from Frankfurter in order
    to get the conversion rate for the given currencies and date. After the API
    call, it will perform a check to see if the API call was successful. If it
    is the case, it will load the response as JSON, extract the conversion rate
    and return it. Otherwise it will return the value None.

    Parameters
    ----------
    from_currency : str
        Code for the origin currency
    to_currency : str
        Code for the destination currency
    amount : float
        The amount (in origin currency) to be converted
    from_date : str
        Date when the conversion rate was recorded

    Returns
    -------
    float
        Latest FX conversion rate or None in case of error
    """

    url = (
        f"{BASE_URL}/{from_date}?amount={amount}&from={from_currency}&to={to_currency}"
    )
    status, text = get_url(url)
    if status == 200:
        try:
            data = json.loads(text)
            return data["rates"][to_currency] / float(amount)
        except (KeyError, ValueError, json.JSONDecodeError):
            return None
    return None


def _subtract_months(d: date, months: int) -> date:
    """Helper to subtract a number of months from a date."""
    year = d.year
    month = d.month - months
    day = d.day
    while month <= 0:
        month += 12
        year -= 1
    day = min(day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def get_rate_trend(from_currency: str, to_currency: str, years: int) -> dict:
    """
    Fetches historical rates for the past N years on a quarterly basis and
    returns a dictionary with dates as keys and rates as values.

    Parameters
    ----------
    from_currency : str
        Code for the origin currency
    to_currency : str
        Code for the destination currency
    years : int
        Number of years in the past for which to fetch rates

    Returns
    -------
    dict
        Dictionary containing dates and their corresponding rates
    """

    results = {}
    today = date.today()
    quarters = years * 4
    for i in range(1, quarters + 1):
        target_date = _subtract_months(today, i * 3)
        date_str = target_date.isoformat()
        url = (
            f"{BASE_URL}/{date_str}?from={from_currency}&to={to_currency}"
        )
        status, text = get_url(url)
        if status == 200:
            try:
                rate = json.loads(text)["rates"][to_currency]
                results[date_str] = rate
            except (KeyError, json.JSONDecodeError):
                continue
    return results

