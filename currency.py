
def round_rate(rate):
    """
    Function that will round an input float to 4 decimals places.

    Parameters
    ----------
    rate: float
        Rate to be rounded

    Returns
    -------
    float
        Rounded rate
    """

    return round(float(rate), 4)
    

def reverse_rate(rate):
    """
    Function that will calculate the inverse rate from the provided input rate.
    It will check if the provided input rate is not equal to zero.
    If it not the case, it will calculate the inverse rate and round it to 4 decimal places.
    Otherwise it will return zero.

    Parameters
    ----------
    rate: float
        FX conversion rate to be inverted

    Returns
    -------
    float
        Inverse of input FX conversion rate
    """

    try:
        rate_value = float(rate)
    except (TypeError, ValueError):
        return 0

    if rate_value == 0:
        return 0

    return round(1 / rate_value, 4)
    
def format_output(date, from_currency, to_currency, rate, amount):
    """
    Function that will format the text to be displayed in the Streamlit app.

    Parameters
    ----------
    date: str
        Date of the conversion rate
    from_currency: str
        Origin currency code
    to_currency: str
        Destination currency code
    rate: float
        Conversion rate
    amount: float
        Amount to be converted

    Returns
    -------
    str
        Formatted text for display
    """

    rounded_rate = round_rate(rate)
    converted_amount = round_rate(amount * rounded_rate)
    inverse = reverse_rate(rounded_rate)
    amount_rounded = round_rate(amount)

    return (
        f"The conversion rate on {date} from {from_currency} to {to_currency} was {rounded_rate}. "
        f"So {amount_rounded} in {from_currency} correspond to {converted_amount} in {to_currency}. "
        f"The inverse rate was {inverse}."
    )
   