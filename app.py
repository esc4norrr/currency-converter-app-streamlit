import datetime

import streamlit as st

from frankfurter import get_currencies, get_historical_rate, get_latest_rate
from currency import format_conversion

st.title("Currency Converter")

currencies = get_currencies()
codes = sorted(currencies.keys())

amount = st.number_input("Amount", min_value=0.0, value=1.0)
from_currency = st.selectbox("From", codes, index=codes.index("EUR") if "EUR" in codes else 0)
to_currency = st.selectbox("To", codes, index=codes.index("USD") if "USD" in codes else 0)

if st.button("Convert Latest"):
    try:
        result = get_latest_rate(from_currency, to_currency, amount)
        st.text(
            format_conversion(
                result["date"],
                result["from"],
                result["to"],
                result["rate"],
                result["from_amount"],
                result["to_amount"],
                result["inverse_rate"],
            )
        )
    except Exception as exc:  # pragma: no cover - simple user feedback
        st.error(str(exc))

date = st.date_input("Date", datetime.date.today())
if st.button("Convert Historical"):
    try:
        result = get_historical_rate(date.isoformat(), from_currency, to_currency, amount)
        st.text(
            format_conversion(
                result["date"],
                result["from"],
                result["to"],
                result["rate"],
                result["from_amount"],
                result["to_amount"],
                result["inverse_rate"],
            )
        )
    except Exception as exc:  # pragma: no cover - simple user feedback
        st.error(str(exc))
