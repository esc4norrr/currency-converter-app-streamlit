def format_conversion(date, from_currency, to_currency, rate, from_amount, to_amount, inverse_rate):
    """Format a currency conversion result into a readable sentence."""
    return (
        f"The conversion rate on {date} from {from_currency} to {to_currency} was {rate:.2f}. "
        f"So {from_amount:.2f} in {from_currency} correspond to {to_amount:.2f} in {to_currency} "
        f"The inverse rate was {inverse_rate:.4f}."
    )
