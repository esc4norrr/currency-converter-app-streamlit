from __future__ import annotations

from typing import Dict

from api import get


def get_currencies() -> Dict[str, str]:
    """Return mapping of currency codes to currency names."""
    return get("/currencies")


def get_latest_rate(from_currency: str, to_currency: str, amount: float) -> dict:
    """Fetch the latest conversion rate and amounts between two currencies."""
    data = get("/latest", params={"from": from_currency, "to": to_currency, "amount": amount})
    rate = data["rates"][to_currency]
    date = data["date"]
    to_amount = rate * amount
    inverse_rate = 1 / rate
    return {
        "date": date,
        "from": from_currency,
        "to": to_currency,
        "rate": rate,
        "from_amount": amount,
        "to_amount": to_amount,
        "inverse_rate": inverse_rate,
    }


def get_historical_rate(date: str, from_currency: str, to_currency: str, amount: float) -> dict:
    """Fetch historical conversion data for a given date."""
    data = get(f"/{date}", params={"from": from_currency, "to": to_currency, "amount": amount})
    rate = data["rates"][to_currency]
    to_amount = rate * amount
    inverse_rate = 1 / rate
    return {
        "date": date,
        "from": from_currency,
        "to": to_currency,
        "rate": rate,
        "from_amount": amount,
        "to_amount": to_amount,
        "inverse_rate": inverse_rate,
    }
