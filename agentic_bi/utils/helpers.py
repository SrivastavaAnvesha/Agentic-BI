"""Utility functions module."""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def format_number(value: float, decimals: int = 2) -> str:
    """Format number with thousand separators."""
    return f"{value:,.{decimals}f}"


def format_currency(value: float, currency: str = "₹") -> str:
    """Format value as currency."""
    return f"{currency} {format_number(value)}"


def format_percentage(value: float) -> str:
    """Format value as percentage."""
    return f"{value:.1f}%"


def truncate_string(text: str, max_length: int = 50) -> str:
    """Truncate string to max length."""
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text


def get_trend_indicator(current: float, previous: float) -> tuple:
    """Get trend indicator and percentage change."""
    if previous == 0:
        percentage = 0
    else:
        percentage = ((current - previous) / previous) * 100

    indicator = "↑" if percentage >= 0 else "↓"
    return indicator, abs(percentage)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for file operations."""
    import re
    
    # Remove special characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    # Ensure filename is not empty
    return filename or "export"
