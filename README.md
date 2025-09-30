# Currency Converter App

## Author
Name: _Not provided_
Student ID: _Not provided_

## Description
Interactive Streamlit application that converts currency amounts using the
[Frankfurter](https://www.frankfurter.app/) API. The interface lets users fetch
the most recent exchange rate or a historical rate for a chosen date, and then
displays a detailed breakdown of the conversion along with a two-year trend
chart for the selected currency pair when working with the latest market rate.

### Highlights
- Fetches available currencies from Frankfurter with graceful error handling if
  the service is unavailable.
- Provides numeric input for the amount and dropdowns for selecting source and
  target currencies with sensible defaults.
- Offers buttons to convert using either the latest market rate or a
  user-selected historical date.
- Shows success messaging, the rounded conversion rate, converted amount, and
  inverse rate metrics after each conversion.
- Renders a line chart highlighting the trend over the last two years for the
  selected currency pair after a latest-rate conversion, with labels that pair
  month abbreviations and years for clarity.

### Challenges
- Handling API connectivity failures and ensuring the UI communicates issues to
  the user clearly.
- Managing Streamlit session state so that conversion results persist across
  reruns while still clearing stale information when inputs change.

### Future Enhancements
- Support for comparing multiple target currencies simultaneously.
- Additional visualisations such as moving averages or volatility indicators.
- Persisting user preferences (e.g., favourite currency pairs) across sessions.

## How to Setup
1. Ensure you have **Python 3.9+** installed (the app was built with Python
   3.10).
2. Install the required packages:
   ```bash
   pip install streamlit==1.30.0 requests==2.31.0 pandas==2.2.0
   ```

## How to Run the Program
1. Activate your Python environment (virtualenv, Conda, etc.).
2. From the project root directory, launch the Streamlit server:
   ```bash
   streamlit run app.py
   ```
3. A browser window will open automatically. If it does not, navigate to the
   URL printed in the terminal (typically http://localhost:8501).
4. Enter the amount you wish to convert, pick the source and target currencies,
   and click **Convert using latest rate** to fetch the newest rate.
5. To look up a historical conversion, select a past date with the calendar
   input and click **Convert using historical rate**.
6. Review the success message, conversion metrics, and the "Rate Trend Over the
   Last 2 Years" chart to understand how the rate has moved over time.

## Project Structure
- `app.py` – Streamlit user interface and application logic, including caching
  of rate trend data and rendering of conversion metrics and charts.
- `api.py` – Generic HTTP helper for GET requests.
- `frankfurter.py` – Functions interacting with the Frankfurter API.
- `currency.py` – Helper functions for rate calculations and formatting.
- `README.md` – Project documentation.

## Citations
Data provided by the [Frankfurter](https://www.frankfurter.app/) API.
