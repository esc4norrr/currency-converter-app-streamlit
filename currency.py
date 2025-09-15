from __future__ import annotations


def format_conversion(data: dict) -> str:
    """Format a currency conversion result into a readable sentence."""
    return (
        f"The conversion rate on {data['date']} from {data['from']} to {data['to']} was {data['rate']:.2f}. "
        f"So {data['from_amount']:.2f} in {data['from']} correspond to {data['to_amount']:.2f} in {data['to']} "
        f"The inverse rate was {data['inverse_rate']:.4f}."
    )
