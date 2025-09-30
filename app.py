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


def display_conversion_details(result: dict):
    """Render the conversion summary, metrics and trend chart."""

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

    trend_data = load_rate_trend(from_currency, to_currency, years=2)
    if trend_data:
        sorted_dates = sorted(trend_data.keys())
        trend_df = pd.DataFrame(
            {"Rate": [trend_data[date_key] for date_key in sorted_dates]},
            index=pd.to_datetime(sorted_dates),
        )
        trend_df.index.name = "Date"
        st.markdown("#### Rate Trend Over the Last 2 Years")
        st.line_chart(trend_df)
    else:
        st.info("Rate trend data is not available right now. Please try again later.")


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

    st.session_state.setdefault("from_currency", default_from)
    st.session_state.setdefault("to_currency", default_to)
    st.session_state.setdefault("amount_input", 1.0)
    st.session_state.setdefault("historical_date", datetime.date.today())
    st.session_state.setdefault("latest_result", None)
    st.session_state.setdefault("historical_result", None)

    st.subheader("Conversion Setup")
    selection_cols = st.columns([2, 3, 1, 3])

    amount = selection_cols[0].number_input(
        "Amount",
        min_value=0.0,
        value=st.session_state.amount_input,
        key="amount_input",
        step=0.01,
        format="%.2f",
        on_change=reset_results,
    )

    from_currency = selection_cols[1].selectbox(
        "From",
        currencies,
        index=currencies.index(st.session_state.from_currency)
        if st.session_state.from_currency in currencies
        else 0,
        key="from_currency",
        on_change=reset_results,
    )

    swap_clicked = selection_cols[2].button("🔄 Swap", use_container_width=True, type="secondary")

    to_currency = selection_cols[3].selectbox(
        "To",
        currencies,
        index=currencies.index(st.session_state.to_currency)
        if st.session_state.to_currency in currencies
        else 0,
        key="to_currency",
        on_change=reset_results,
    )

    if swap_clicked:
        st.session_state.from_currency, st.session_state.to_currency = (
            st.session_state.to_currency,
            st.session_state.from_currency,
        )
        reset_results()
        st.experimental_rerun()

    st.divider()

    latest_tab, historical_tab = st.tabs(["Latest Rate", "Historical Rate"])

    with latest_tab:
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
            display_conversion_details(st.session_state.latest_result)

    with historical_tab:
        st.write("Look up the conversion rate for a specific date in the past.")
        selected_date = st.date_input(
            "Select Date",
            value=st.session_state.historical_date,
            key="historical_date",
            max_value=datetime.date.today(),
            on_change=reset_results,
        )

        if st.button(
            "Convert using historical rate",
            key="historical_button",
            use_container_width=True,
        ):
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










