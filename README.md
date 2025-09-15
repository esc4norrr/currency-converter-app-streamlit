# Currency Converter App

Author: Your Name (Student ID: your-id)

This project implements a simple currency converter using [Frankfurter](https://www.frankfurter.app/) data. Users can convert between currencies, view latest and historical rates, and see the inverse conversion rate.

## Python modules

- `api.get(endpoint, params=None)` - helper to perform HTTP GET requests.
- `frankfurter.get_currencies()` - list available currency codes.
- `frankfurter.get_latest_rate(from_currency, to_currency, amount)` - latest rate.
- `frankfurter.get_historical_rate(date, from_currency, to_currency, amount)` - rate on a given date.
- `currency.format_conversion(date, from_currency, to_currency, rate, from_amount, to_amount, inverse_rate)` - generate display text for results.

## Running the app

```bash
pip install streamlit requests
streamlit run app.py
```
