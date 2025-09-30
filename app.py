import datetime

import pandas as pd
import streamlit as st

from currency import format_output, reverse_rate, round_rate
from frankfurter import (
    get_currencies_list,
    get_historical_rate,
    get_latest_rates,
    get_rate_trend,
)


st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")
st.title("Currency Converter")
st.caption("Powered by the Frankfurter API")


@st.cache_data(show_spinner=False)
def load_rate_trend(from_currency: str, to_currency: str, years: int = 2):
    """Cached helper to retrieve rate trend data."""

    return get_rate_trend(from_currency, to_currency, years)


def display_conversion_details(result: dict, *, show_trend: bool = False):
    """Render the conversion summary, metrics and optional trend chart."""


    if not result:
        return

    amount = result["amount"]
    from_currency = result["from_currency"]
    to_currency = result["to_currency"]
    date = result["date"]
    rate = result["rate"]

    rounded_rate = round_rate(rate)
    converted_amount = round_rate(amount * rounded_rate)
    inverse_rate = reverse_rate(rounded_rate)

    st.success(format_output(date, from_currency, to_currency, rate, amount))

    metric_cols = st.columns(3)
    metric_cols[0].metric("Rate", f"{rounded_rate}")
    metric_cols[1].metric(
        f"Converted Amount ({to_currency})", f"{converted_amount}"
    )
    metric_cols[2].metric("Inverse Rate", f"{inverse_rate}")

    if show_trend:
        trend_data = load_rate_trend(from_currency, to_currency, years=2)
        if trend_data:
            sorted_dates = sorted(trend_data.keys())
            trend_df = pd.DataFrame(
                {
                    "Date": pd.to_datetime(sorted_dates),
                    "Rate": [trend_data[date_key] for date_key in sorted_dates],
                }
            )
            trend_df["Period"] = trend_df["Date"].dt.strftime("%b %Y")
            trend_df = trend_df.set_index("Period")[["Rate"]]
            st.markdown("#### Rate Trend Over the Last 2 Years")
            st.line_chart(trend_df)
        else:
            st.info(
                "Rate trend data is not available right now. Please try again later."
            )


def reset_results():
    """Clear cached conversion results when inputs change."""

    st.session_state.latest_result = None
    st.session_state.historical_result = None


# Get the list of available currencies from Frankfurter
currencies = get_currencies_list()

# If the list of available currencies is None, display an error message in Streamlit App
if currencies is None:
    st.error("Unable to retrieve currency list from Frankfurter API.")
else:
    default_from = "EUR" if "EUR" in currencies else currencies[0]
    other_currencies = [code for code in currencies if code != default_from]
    default_to = "USD" if "USD" in other_currencies else (other_currencies[0] if other_currencies else default_from)

    if "from_currency" not in st.session_state:
        st.session_state.from_currency = default_from
    if "to_currency" not in st.session_state:
        st.session_state.to_currency = default_to
    if "amount_input" not in st.session_state:
        st.session_state.amount_input = 1.0
    if "historical_date" not in st.session_state:
        st.session_state.historical_date = datetime.date.today()
    if "latest_result" not in st.session_state:
        st.session_state.latest_result = None
    if "historical_result" not in st.session_state:
        st.session_state.historical_result = None

    st.subheader("Conversion Setup")
    amount = st.number_input(
        "Amount",
        min_value=0.0,
        key="amount_input",
        step=0.01,
        format="%.2f",
        on_change=reset_results,
    )

    currency_cols = st.columns(2)

    from_currency = currency_cols[0].selectbox(
        "From",
        currencies,
        index=currencies.index(st.session_state.from_currency)
        if st.session_state.from_currency in currencies
        else 0,
        key="from_currency",
        on_change=reset_results,
    )

    to_currency = currency_cols[1].selectbox(
        "To",
        currencies,
        index=currencies.index(st.session_state.to_currency)
        if st.session_state.to_currency in currencies
        else 0,
        key="to_currency",
        on_change=reset_results,
    )

    st.divider()

    st.write("Get the most recent conversion rate available from the Frankfurter API.")
    if st.button("Convert using latest rate", key="latest_button", use_container_width=True):
        if amount <= 0:
            st.warning("Please enter an amount greater than zero to convert.")
        else:
            with st.spinner("Fetching latest rate..."):
                date, rate = get_latest_rates(from_currency, to_currency, amount)
            if rate is None or date is None:
                st.error("Unable to fetch latest conversion rate.")
                st.session_state.latest_result = None
            else:
                st.session_state.latest_result = {
                    "date": date,
                    "rate": rate,
                    "amount": amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                }

    if st.session_state.latest_result:
        display_conversion_details(st.session_state.latest_result, show_trend=True)


    st.divider()

    st.write("Look up the conversion rate for a specific date in the past.")
    selected_date = st.date_input(
        "Select Date",
        key="historical_date",
        max_value=datetime.date.today(),
        on_change=reset_results,
    )

    if st.button("Convert using historical rate", key="historical_button", use_container_width=True):
        if amount <= 0:
            st.warning("Please enter an amount greater than zero to convert.")
        else:
            date_str = selected_date.strftime("%Y-%m-%d")
            with st.spinner("Fetching historical rate..."):
                rate = get_historical_rate(from_currency, to_currency, date_str, amount)
            if rate is None:
                st.error("Unable to fetch historical conversion rate.")
                st.session_state.historical_result = None
            else:
                st.session_state.historical_result = {
                    "date": date_str,
                    "rate": rate,
                    "amount": amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                }

    if st.session_state.historical_result:
        display_conversion_details(st.session_state.historical_result)