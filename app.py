import streamlit as st
import datetime

from frankfurter import get_currencies_list, get_latest_rates, get_historical_rate
from currency import reverse_rate, round_rate, format_output

st.title("Currency Converter")

# Get the list of available currencies from Frankfurter
currencies = get_currencies_list()

# If the list of available currencies is None, display an error message in Streamlit App
if currencies is None:
    st.error("Unable to retrieve currency list from Frankfurter API.")
else:
    # Add input fields for capturing amount, from and to currencies
    amount = st.number_input("Amount", min_value=0.0, value=1.0)
    from_currency = st.selectbox("From", currencies, index=currencies.index("EUR") if "EUR" in currencies else 0)
    to_currency = st.selectbox("To", currencies, index=currencies.index("USD") if "USD" in currencies else 0)

    # Add a button to get and display the latest rate for selected currencies and amount
    if st.button("Get Latest Rate"):
        date, rate = get_latest_rates(from_currency, to_currency, amount)
        if rate is None:
            st.error("Unable to fetch latest conversion rate.")
        else:
            st.text(format_output(date, from_currency, to_currency, rate, amount))

    # Add a date selector (calendar)
    selected_date = st.date_input("Select Date", datetime.date.today())

    # Add a button to get and display the historical rate for selected date, currencies and amount
    if st.button("Get Historical Rate"):
        date_str = selected_date.strftime("%Y-%m-%d")
        rate = get_historical_rate(from_currency, to_currency, date_str, amount)
        if rate is None:
            st.error("Unable to fetch historical conversion rate.")
        else:
            st.text(format_output(date_str, from_currency, to_currency, rate, amount))










