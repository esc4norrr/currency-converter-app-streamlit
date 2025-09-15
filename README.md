# Currency Converter App

## Author
Name: _Your Name Here_
Student ID: _Your Student ID_

## Description
Simple Streamlit web application that converts amounts between currencies using
the [Frankfurter](https://www.frankfurter.app/) API. Users can retrieve the
latest exchange rates or query historical rates for a specific date.

## How to Setup
1. Ensure you have **Python 3.9+** installed.
2. Install required packages:
   ```bash
   pip install streamlit requests
   ```

## How to Run the Program
Run the Streamlit application:

```bash
streamlit run app.py
```

## Project Structure
- `app.py` – Streamlit user interface and application logic.
- `api.py` – Generic HTTP helper for GET requests.
- `frankfurter.py` – Functions interacting with the Frankfurter API.
- `currency.py` – Helper functions for rate calculations and formatting.
- `README.md` – Project documentation.

## Citations
Data provided by the [Frankfurter](https://www.frankfurter.app/) API.
