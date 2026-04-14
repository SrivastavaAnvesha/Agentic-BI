"""Reusable Streamlit UI components."""

import streamlit as st
from typing import Any, Dict, List, Optional, Callable
from agentic_bi.utils import (
    format_number,
    format_currency,
    format_percentage,
    get_trend_indicator,
)


def metric_card(
    label: str,
    value: Any,
    icon: str = "",
    delta: Optional[float] = None,
    delta_label: str = "",
    unit: str = "",
) -> None:
    """
    Display a metric card with optional delta and animated trend.

    Args:
        label: Metric label
        value: Metric value
        icon: Icon emoji
        delta: Previous value for trend calculation
        delta_label: Label for delta
        unit: Unit of measurement
    """
    col1, col2 = st.columns([3, 1])

    with col1:
        # Format value
        if isinstance(value, (int, float)):
            if unit == "₹":
                formatted_value = format_currency(value)
            elif unit == "%":
                formatted_value = format_percentage(value)
            else:
                formatted_value = format_number(value)
        else:
            formatted_value = str(value)

        # Display metric with enhanced HTML and animations
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(8, 145, 178, 0.15) 0%, rgba(6, 90, 130, 0.15) 100%);
                border: 1px solid rgba(8, 145, 178, 0.4);
                border-radius: 12px;
                padding: 1.5rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                animation: slideIn 0.5s ease-out;
                position: relative;
                overflow: hidden;
            ">
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 2px;
                    background: linear-gradient(90deg, #0891B2, #065A82, transparent);
                    opacity: 0;
                    animation: slideInTop 0.6s ease-out forwards;
                "></div>
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.75rem; font-weight: 500;">
                    {icon} {label}
                </div>
                <div style="
                    font-size: 2.2rem; 
                    font-weight: 700; 
                    color: #0891B2; 
                    margin-bottom: 0.5rem;
                    background: linear-gradient(135deg, #0891B2 0%, #06b6d4 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                ">
                    {formatted_value}
                </div>
                {f'<div style="font-size: 0.75rem; color: #64748b;">{delta_label}</div>' if delta_label else ''}
                <style>
                    @keyframes slideIn {{
                        from {{ opacity: 0; transform: translateY(10px); }}
                        to {{ opacity: 1; transform: translateY(0); }}
                    }}
                    @keyframes slideInTop {{
                        from {{ transform: scaleX(0); }}
                        to {{ transform: scaleX(1); }}
                    }}
                </style>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        if delta is not None and isinstance(value, (int, float)):
            indicator, percentage = get_trend_indicator(value, delta)
            is_positive = indicator == "↑"
            color = "#10b981" if is_positive else "#ef4444"
            bg_color = "#10b981" if is_positive else "#ef4444"
            st.markdown(
                f"""
                <div style="
                    background: rgba({16 if is_positive else 239}, {185 if is_positive else 68}, {129 if is_positive else 68}, 0.15);
                    border: 1px solid rgba({16 if is_positive else 239}, {185 if is_positive else 68}, {129 if is_positive else 68}, 0.4);
                    border-radius: 8px;
                    padding: 0.75rem;
                    text-align: center;
                    transition: all 0.3s ease;
                    animation: pulse 1.5s ease-in-out infinite;
                ">
                    <div style="font-size: 1.4rem; font-weight: 700; color: {color};">
                        {indicator}
                    </div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.25rem;">
                        {percentage:.1f}%
                    </div>
                </div>
                <style>
                    @keyframes pulse {{
                        0%, 100% {{ opacity: 1; }}
                        50% {{ opacity: 0.7; }}
                    }}
                </style>
                """,
                unsafe_allow_html=True,
            )


def progress_bar(
    label: str, value: float, max_value: float = 100, color: str = "#0891B2"
) -> None:
    """Display a styled progress bar."""
    percentage = min((value / max_value) * 100, 100)

    st.markdown(
        f"""
        <div style="margin-bottom: 1rem;">
            <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem;">
                {label} <span style="float: right; color: #0891B2;">{percentage:.0f}%</span>
            </div>
            <div style="
                background: rgba(30, 41, 59, 0.5);
                border: 1px solid rgba(8, 145, 178, 0.2);
                border-radius: 4px;
                height: 8px;
                overflow: hidden;
            ">
                <div style="
                    background: linear-gradient(90deg, {color}, {color}dd);
                    height: 100%;
                    width: {percentage}%;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text: str, status: str = "info") -> None:
    """Display a styled status badge."""
    colors = {
        "success": ("#10b981", "rgba(16, 185, 129, 0.1)"),
        "error": ("#ef4444", "rgba(239, 68, 68, 0.1)"),
        "warning": ("#f59e0b", "rgba(245, 158, 11, 0.1)"),
        "info": ("#0891B2", "rgba(8, 145, 178, 0.1)"),
    }

    color, bg = colors.get(status, colors["info"])

    st.markdown(
        f"""
        <div style="
            display: inline-block;
            background: {bg};
            border: 1px solid {color};
            color: {color};
            padding: 0.35rem 0.75rem;
            border-radius: 16px;
            font-size: 0.85rem;
            font-weight: 600;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def chat_message(
    message: str, role: str = "assistant", avatar: str = "🤖"
) -> None:
    """Display a chat message."""
    alignment = "left" if role == "assistant" else "right"
    bg_color = "rgba(8, 145, 178, 0.1)" if role == "assistant" else "rgba(8, 145, 178, 0.2)"
    border_color = "#0891B2" if role == "assistant" else "#065A82"

    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: flex-start;
            margin-bottom: 1rem;
            justify-content: {'flex-start' if role == 'assistant' else 'flex-end'};
        ">
            {f'<div style="margin-right: 0.5rem; font-size: 1.5rem;">{avatar}</div>' if role == 'assistant' else ''}
            <div style="
                background: {bg_color};
                border: 1px solid {border_color};
                border-radius: 12px;
                padding: 1rem;
                max-width: 70%;
                word-wrap: break-word;
            ">
                <p style="color: #F8FAFC; margin: 0;">{message}</p>
            </div>
            {f'<div style="margin-left: 0.5rem; font-size: 1.5rem;">{avatar}</div>' if role == 'user' else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, content: Callable[[], None], collapsible: bool = False) -> None:
    """Display a styled card."""
    if collapsible:
        with st.expander(f"📦 {title}"):
            content()
    else:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(8, 145, 178, 0.1) 0%, rgba(6, 90, 130, 0.1) 100%);
                border: 1px solid rgba(8, 145, 178, 0.3);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
            ">
                <h3 style="color: #F8FAFC; margin-top: 0;">{title}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        content()


def loading_spinner(text: str = "Loading...") -> None:
    """Display a loading spinner with text."""
    with st.spinner(f"⏳ {text}"):
        st.write("")


def section_header(title: str, icon: str = "📊", divider: bool = True) -> None:
    """Display a section header."""
    st.markdown(
        f"""
        <div style="
            margin-top: 2rem;
            margin-bottom: 1.5rem;
        ">
            <h2 style="
                color: #F8FAFC;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin: 0;
            ">
                <span>{icon}</span>
                {title}
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if divider:
        st.divider()


def code_block(code: str, language: str = "sql") -> None:
    """Display styled code block."""
    st.code(code, language=language)


def stat_comparison(
    label: str,
    current: float,
    previous: float,
    format_func: Callable = format_number,
) -> None:
    """Display two statistics side by side for comparison."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current", format_func(current))

    with col2:
        st.write("")  # Spacer
        indicator, percentage = get_trend_indicator(current, previous)
        color = "🟢" if indicator == "↑" else "🔴"
        st.metric("Change", f"{color} {percentage:.1f}%")

    with col3:
        st.metric("Previous", format_func(previous))
