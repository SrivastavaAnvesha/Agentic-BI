"""Data visualization module using Plotly."""

import logging
from typing import List, Dict, Any, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

logger = logging.getLogger(__name__)


class Visualizer:
    """Create interactive Plotly visualizations."""

    # Color scheme - professional teal/blue
    COLORS = {
        "primary": "#0891B2",
        "secondary": "#065A82",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "dark_bg": "#0F172A",
        "light_text": "#F8FAFC",
        "grid": "#1E293B",
    }

    @staticmethod
    def create_bar_chart(
        data: List[Dict[str, Any]],
        x_col: str,
        y_col: str,
        title: str = "Bar Chart",
        color_col: Optional[str] = None,
    ) -> go.Figure:
        """Create interactive bar chart."""
        df = pd.DataFrame(data)

        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=color_col or y_col,
            title=title,
            color_continuous_scale="Teal",
            height=400,
        )

        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor=Visualizer.COLORS["dark_bg"],
            paper_bgcolor=Visualizer.COLORS["dark_bg"],
            font=dict(color=Visualizer.COLORS["light_text"]),
            hovermode="x unified",
            showlegend=True,
        )

        return fig

    @staticmethod
    def create_line_chart(
        data: List[Dict[str, Any]],
        x_col: str,
        y_col: str,
        title: str = "Line Chart",
    ) -> go.Figure:
        """Create interactive line chart."""
        df = pd.DataFrame(data)

        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            title=title,
            height=400,
        )

        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor=Visualizer.COLORS["dark_bg"],
            paper_bgcolor=Visualizer.COLORS["dark_bg"],
            font=dict(color=Visualizer.COLORS["light_text"]),
            hovermode="x unified",
        )

        fig.update_traces(
            line=dict(color=Visualizer.COLORS["primary"], width=3),
            fill="tozeroy",
            fillcolor=Visualizer.COLORS["primary"] + "20",
        )

        return fig

    @staticmethod
    def create_pie_chart(
        data: List[Dict[str, Any]],
        values_col: str,
        names_col: str,
        title: str = "Pie Chart",
    ) -> go.Figure:
        """Create interactive pie chart."""
        df = pd.DataFrame(data)

        fig = px.pie(
            df,
            values=values_col,
            names=names_col,
            title=title,
            height=400,
            color_discrete_sequence=[
                Visualizer.COLORS["primary"],
                Visualizer.COLORS["secondary"],
                "#06b6d4",
                "#0ea5e9",
                "#3b82f6",
            ],
        )

        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor=Visualizer.COLORS["dark_bg"],
            paper_bgcolor=Visualizer.COLORS["dark_bg"],
            font=dict(color=Visualizer.COLORS["light_text"]),
        )

        return fig

    @staticmethod
    def create_scatter_chart(
        data: List[Dict[str, Any]],
        x_col: str,
        y_col: str,
        title: str = "Scatter Chart",
        size_col: Optional[str] = None,
        color_col: Optional[str] = None,
    ) -> go.Figure:
        """Create interactive scatter plot."""
        df = pd.DataFrame(data)

        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            size=size_col,
            color=color_col,
            title=title,
            height=400,
            color_continuous_scale="Teal",
        )

        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor=Visualizer.COLORS["dark_bg"],
            paper_bgcolor=Visualizer.COLORS["dark_bg"],
            font=dict(color=Visualizer.COLORS["light_text"]),
            hovermode="closest",
        )

        fig.update_traces(marker=dict(size=10, opacity=0.8))

        return fig

    @staticmethod
    def create_histogram(
        data: List[Dict[str, Any]],
        col: str,
        title: str = "Distribution",
        nbins: int = 30,
    ) -> go.Figure:
        """Create histogram for distribution analysis."""
        df = pd.DataFrame(data)

        fig = px.histogram(
            df,
            x=col,
            title=title,
            nbins=nbins,
            height=400,
        )

        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor=Visualizer.COLORS["dark_bg"],
            paper_bgcolor=Visualizer.COLORS["dark_bg"],
            font=dict(color=Visualizer.COLORS["light_text"]),
            hovermode="x unified",
        )

        fig.update_traces(marker=dict(color=Visualizer.COLORS["primary"]))

        return fig

    @staticmethod
    def create_box_plot(
        data: List[Dict[str, Any]],
        y_col: str,
        x_col: Optional[str] = None,
        title: str = "Box Plot",
    ) -> go.Figure:
        """Create box plot for statistical analysis."""
        df = pd.DataFrame(data)

        fig = px.box(
            df,
            y=y_col,
            x=x_col,
            title=title,
            height=400,
        )

        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor=Visualizer.COLORS["dark_bg"],
            paper_bgcolor=Visualizer.COLORS["dark_bg"],
            font=dict(color=Visualizer.COLORS["light_text"]),
        )

        return fig

    @staticmethod
    def suggest_chart_type(data: List[Dict[str, Any]]) -> str:
        """Suggest appropriate chart type based on data."""
        if not data or len(data) == 0:
            return "table"

        first_row = data[0]
        numeric_cols = sum(
            1 for v in first_row.values() if isinstance(v, (int, float))
        )
        categorical_cols = len(first_row) - numeric_cols

        if numeric_cols == 0:
            return "table"
        elif numeric_cols == 1 and categorical_cols == 1:
            return "bar"
        elif numeric_cols >= 2:
            return "scatter"
        else:
            return "bar"
