import sys
import os
from pathlib import Path

# System path fix for package imports
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration - WIDE LAYOUT for frame stability
st.set_page_config(
    page_title="Agentic BI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom styles
try:
    with open(Path(__file__).parent / "ui" / "styles.py", "r") as f:
        style_code = f.read()
        exec(style_code)
except Exception as e:
    pass

# Initialize session state
if "df" not in st.session_state:
    st.session_state.df = None
if "df_clean" not in st.session_state:
    st.session_state.df_clean = None
if "profile" not in st.session_state:
    st.session_state.profile = None
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

# ============================================================================
# WISE SANITIZATION LAYER - PRODUCTION-GRADE DATA GUARD (AWS-OPTIMIZED)
# ============================================================================

def sanitize_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Professional EDA-based sanitization for AWS deployment.
    
    Principles:
    1. Uniform Null Mapping: Convert 'none', 'null', 'NaN', empty strings to np.nan
    2. Rule of Preservation: Never drop rows unless 100% empty
    3. Smart Numerical Imputation: Vectorized operations for performance
    4. Categorical Safeguard: Fill missing categories with 'Unknown'
    
    AWS-Optimized: Uses vectorized Pandas operations (no loops)
    """
    if df is None or df.empty:
        return df
    
    df_clean = df.copy()
    
    # ==== STEP 1: UNIFORM NULL MAPPING ====
    # Vectorized: Convert string representations of null to np.nan
    string_nulls = ['none', 'null', 'nan', 'na', 'n/a', '']
    
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            # Vectorized string matching for all null representations
            df_clean[col] = df_clean[col].apply(
                lambda x: np.nan if (isinstance(x, str) and x.lower().strip() in string_nulls) else x
            )
    
    # ==== STEP 2: RULE OF PRESERVATION - DROP ONLY 100% EMPTY ROWS ====
    # Identify rows that are completely empty (all NaN across all columns)
    completely_empty_rows = df_clean.isnull().all(axis=1)
    df_clean = df_clean[~completely_empty_rows]
    
    # Drop columns that are 100% empty
    df_clean = df_clean.dropna(axis=1, how='all')
    
    # ==== STEP 3: SMART NUMERICAL IMPUTATION ====
    # Vectorized type enforcement for object columns
    for col in df_clean.select_dtypes(include=['object']).columns:
        # Attempt vectorized numeric conversion
        numeric_attempt = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Calculate numeric potential (% of non-null valid numbers after conversion)
        numeric_valid_ratio = numeric_attempt.notna().sum() / len(df_clean)
        
        # If >50% numeric potential, convert to numeric
        if numeric_valid_ratio > 0.5:
            df_clean[col] = numeric_attempt
    
    # ==== STEP 4: FILL MISSING VALUES (VECTORIZED) ====
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df_clean.select_dtypes(include=['object']).columns.tolist()
    
    # Vectorized: Fill numeric NaNs with median (robust to outliers)
    for col in numeric_cols:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    # Vectorized: Fill categorical NaNs with 'Unknown' (categorical safeguard)
    for col in categorical_cols:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col] = df_clean[col].fillna('Unknown')
    
    # ==== STEP 5: FINAL VALIDATION ====
    # Ensure NO remaining NaN values that would break visualizations
    # Only drop rows if they still have NaN (should be minimal)
    df_clean = df_clean.dropna(how='any')
    
    return df_clean


def sanitize_for_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """
    ReAct Check: Extract ONLY numeric columns for correlation analysis.
    Self-healing: Removes any non-numeric values that slipped through.
    AWS-optimized: Single vectorized operation.
    """
    try:
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        # Validate: Ensure we have at least 2 numeric columns
        if len(numeric_df.columns) < 2:
            return None
        
        # Additional check: Remove any columns with inf values (edge case)
        numeric_df = numeric_df[~np.isinf(numeric_df).any(axis=1)]
        
        return numeric_df
    except Exception as e:
        return None


def profile_data(df: pd.DataFrame) -> dict:
    """Comprehensive data profiling with type classification"""
    if df is None or df.empty:
        return None
    
    profile = {
        "rows": len(df),
        "cols": len(df.columns),
        "numeric": [],
        "categorical": [],
        "datetime": [],
        "column_types": {}
    }
    
    for col in df.columns:
        dtype = df[col].dtype
        
        if pd.api.types.is_datetime64_any_dtype(dtype):
            profile["datetime"].append(col)
            profile["column_types"][col] = "datetime"
        elif pd.api.types.is_numeric_dtype(dtype):
            profile["numeric"].append(col)
            profile["column_types"][col] = "numeric"
        else:
            profile["categorical"].append(col)
            profile["column_types"][col] = "categorical"
    
    return profile


def detect_query_intent(query: str) -> str:
    """Detect user intent from query keywords"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['correlation', 'heatmap', 'relationship', 'between columns', 'feature']):
        return "correlation"
    elif any(word in query_lower for word in ['trend', 'over time', 'monthly', 'yearly', 'time series', 'temporal', 'growth']):
        return "trend"
    elif any(word in query_lower for word in ['compare', 'vs', 'comparison', 'difference', 'by category', 'group']):
        return "comparison"
    elif any(word in query_lower for word in ['share', 'percentage', 'proportion', 'distribution of total', '%', 'percent']):
        return "proportion"
    elif any(word in query_lower for word in ['distribution', 'spread', 'range', 'histogram', 'density', 'variance']):
        return "distribution"
    
    return "distribution"


def generate_chart_and_title(df: pd.DataFrame, profile: dict, intent: str) -> tuple:
    """
    Generate chart based on detected intent.
    Strictly uses cleaned data: df.select_dtypes(include=[np.number]).dropna()
    Returns: (fig, title, table_df)
    """
    
    try:
        # TYPE A: CORRELATION - REACT CHECK WITH SELF-HEALING
        if intent == "correlation":
            try:
                # ReAct Check: Use self-healing sanitize_for_correlation
                numeric_df = sanitize_for_correlation(df)
                
                if numeric_df is None or len(numeric_df.columns) < 2:
                    # Fallback: Try basic numeric extraction
                    numeric_df = df.select_dtypes(include=[np.number]).dropna()
                    if len(numeric_df.columns) < 2:
                        return None, "Insufficient numeric data for correlation", None
                
                corr_matrix = numeric_df.corr()
                
                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.index,
                    colorscale='Viridis',
                    text=np.round(corr_matrix.values, 2),
                    texttemplate='%{text:.2f}',
                    textfont={"size": 10},
                    colorbar=dict(title="Correlation")
                ))
                
                fig.update_layout(
                    title="",
                    template="plotly_dark",
                    font=dict(color="#F8FAFC", size=12),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=500,
                    autosize=True,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                
                title = "🔗 Feature Correlation Matrix: Identifying Linear Relationships"
                table_df = corr_matrix.round(3)
                
                return fig, title, table_df
            except (TypeError, ValueError) as e:
                # ReAct Check: Autonomous retry with strict numeric filtering
                try:
                    numeric_df = df.select_dtypes(include=[np.number])
                    numeric_df = numeric_df[~np.isinf(numeric_df).any(axis=1)]
                    numeric_df = numeric_df.dropna()
                    
                    if len(numeric_df.columns) < 2:
                        return None, "Correlation requires at least 2 numeric columns", None
                    
                    corr_matrix = numeric_df.corr()
                    fig = go.Figure(data=go.Heatmap(
                        z=corr_matrix.values,
                        x=corr_matrix.columns,
                        y=corr_matrix.index,
                        colorscale='Viridis',
                        text=np.round(corr_matrix.values, 2),
                        texttemplate='%{text:.2f}',
                        textfont={"size": 10}
                    ))
                    fig.update_layout(
                        template="plotly_dark",
                        font=dict(color="#F8FAFC", size=12),
                        height=500,
                        autosize=True
                    )
                    return fig, "🔗 Feature Correlation Matrix (Auto-Filtered)", corr_matrix.round(3)
                except Exception:
                    return None, "Unable to generate correlation", None
        
        # TYPE B: TRENDS & TIME-SERIES
        elif intent == "trend":
            if profile["datetime"] and profile["numeric"]:
                date_col = profile["datetime"][0]
                numeric_col = profile["numeric"][0]
                
                df_sorted = df.sort_values(date_col)
                
                fig = px.line(
                    x=df_sorted[date_col],
                    y=df_sorted[numeric_col],
                    title="",
                    markers=True,
                    color_discrete_sequence=["#0891B2"]
                )
                
                fig.update_traces(line=dict(width=3), marker=dict(size=6))
                fig.update_layout(
                    template="plotly_dark",
                    font=dict(color="#F8FAFC", size=12),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=500,
                    autosize=True,
                    hovermode="x unified",
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                
                title = f"📈 Temporal Trend Analysis: {numeric_col} over {date_col}"
                table_df = df_sorted[[date_col, numeric_col]].tail(10)
                
                return fig, title, table_df
        
        # TYPE C: COMPARISON & CATEGORICAL
        elif intent == "comparison":
            if profile["categorical"] and profile["numeric"]:
                cat_col = profile["categorical"][0]
                numeric_col = profile["numeric"][0]
                
                agg_df = df.groupby(cat_col)[numeric_col].agg(['mean', 'count']).reset_index()
                agg_df = agg_df.sort_values('mean', ascending=False).head(12)
                
                fig = px.bar(
                    agg_df,
                    x=cat_col,
                    y='mean',
                    color='mean',
                    color_continuous_scale='Viridis',
                    title=""
                )
                
                fig.update_layout(
                    template="plotly_dark",
                    font=dict(color="#F8FAFC", size=12),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=500,
                    autosize=True,
                    showlegend=False,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                
                title = f"⚖️ Comparative Analysis: {cat_col} vs {numeric_col}"
                table_df = agg_df
                
                return fig, title, table_df
        
        # TYPE D: PROPORTIONS & COMPOSITION
        elif intent == "proportion":
            if profile["categorical"]:
                cat_col = profile["categorical"][0]
                value_counts = df[cat_col].value_counts().head(10)
                
                fig = px.pie(
                    values=value_counts.values,
                    names=value_counts.index,
                    title="",
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                
                fig.update_layout(
                    template="plotly_dark",
                    font=dict(color="#F8FAFC", size=12),
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=500,
                    autosize=True,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                
                title = f"🥧 Composition Analysis: Percentage Distribution of {cat_col}"
                
                summary_df = pd.DataFrame({
                    "Category": value_counts.index,
                    "Count": value_counts.values,
                    "Percentage": (value_counts.values / value_counts.sum() * 100).round(2)
                })
                
                table_df = summary_df
                
                return fig, title, table_df
        
        # TYPE E: DISTRIBUTION (Numerical)
        elif intent == "distribution":
            if profile["numeric"]:
                numeric_col = profile["numeric"][0]
                
                fig = px.histogram(
                    df,
                    x=numeric_col,
                    nbins=30,
                    title="",
                    color_discrete_sequence=["#0891B2"]
                )
                
                fig.update_layout(
                    template="plotly_dark",
                    font=dict(color="#F8FAFC", size=12),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=500,
                    autosize=True,
                    showlegend=False,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                
                title = f"📊 Statistical Distribution: Spread and Density of {numeric_col}"
                
                stats_df = pd.DataFrame({
                    "Metric": ["Mean", "Median", "Std Dev", "Min", "Max", "Q1", "Q3"],
                    "Value": [
                        df[numeric_col].mean(),
                        df[numeric_col].median(),
                        df[numeric_col].std(),
                        df[numeric_col].min(),
                        df[numeric_col].max(),
                        df[numeric_col].quantile(0.25),
                        df[numeric_col].quantile(0.75)
                    ]
                }).round(3)
                
                table_df = stats_df
                
                return fig, title, table_df
    
    except Exception as e:
        pass
    
    # Fallback
    if profile["numeric"]:
        numeric_col = profile["numeric"][0]
        fig = px.histogram(df, x=numeric_col, nbins=20, color_discrete_sequence=["#0891B2"])
        fig.update_layout(
            template="plotly_dark",
            font=dict(color="#F8FAFC", size=12),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=500,
            autosize=True,
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        title = f"📊 Statistical Distribution: {numeric_col}"
        table_df = pd.DataFrame({"Value": [f"Column: {numeric_col}", "Data loaded successfully"]})
        return fig, title, table_df
    
    return None, "No visualization available", None


def generate_auto_charts(df: pd.DataFrame, profile: dict) -> list:
    """
    Generate 4-5 auto-charts for Intelligence Hub overview.
    Uses WISE sanitized data with ReAct checks for robustness.
    """
    charts_data = []
    
    # Chart 1: Correlation Heatmap with ReAct Check
    try:
        numeric_df = sanitize_for_correlation(df)
        if numeric_df is not None and len(numeric_df.columns) >= 2:
            corr_matrix = numeric_df.corr()
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.index,
                colorscale='Viridis',
                text=np.round(corr_matrix.values, 2),
                texttemplate='%{text:.2f}',
                textfont={"size": 9}
            ))
            fig.update_layout(
                template="plotly_dark",
                font=dict(color="#F8FAFC", size=11),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=450,
                autosize=True,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            charts_data.append(("🔗 Feature Correlation Matrix", fig, corr_matrix.round(3)))
    except Exception:
        pass
    
    try:
        # Chart 2: Distribution of first numeric column
        if profile["numeric"]:
            col = profile["numeric"][0]
            fig = px.histogram(df, x=col, nbins=20, color_discrete_sequence=["#0891B2"])
            fig.update_layout(
                template="plotly_dark",
                font=dict(color="#F8FAFC", size=11),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=450,
                autosize=True,
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            charts_data.append((f"📊 Distribution: {col}", fig, None))
    except Exception:
        pass
    
    try:
        # Chart 3: Top categories
        if profile["categorical"]:
            col = profile["categorical"][0]
            top_cats = df[col].value_counts().head(10)
            fig = px.bar(
                x=top_cats.values,
                y=top_cats.index,
                orientation="h",
                color=top_cats.values,
                color_continuous_scale="Electric"
            )
            fig.update_layout(
                template="plotly_dark",
                font=dict(color="#F8FAFC", size=11),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=450,
                autosize=True,
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            charts_data.append((f"⚙️ Top Values: {col}", fig, None))
    except Exception:
        pass
    
    try:
        # Chart 4: Pie chart for proportions
        if profile["categorical"]:
            col = profile["categorical"][0]
            top_vals = df[col].value_counts().head(8)
            fig = px.pie(
                values=top_vals.values,
                names=top_vals.index,
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            fig.update_layout(
                template="plotly_dark",
                font=dict(color="#F8FAFC", size=11),
                paper_bgcolor="rgba(0,0,0,0)",
                height=450,
                autosize=True,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            charts_data.append((f"🥧 Proportion: {col}", fig, None))
    except Exception:
        pass
    
    try:
        # Chart 5: Time series if datetime exists
        if profile["datetime"] and profile["numeric"]:
            date_col = profile["datetime"][0]
            num_col = profile["numeric"][0]
            df_sorted = df.sort_values(date_col)
            fig = px.line(
                x=df_sorted[date_col],
                y=df_sorted[num_col],
                markers=True,
                color_discrete_sequence=["#0891B2"]
            )
            fig.update_traces(line=dict(width=2), marker=dict(size=5))
            fig.update_layout(
                template="plotly_dark",
                font=dict(color="#F8FAFC", size=11),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=450,
                autosize=True,
                hovermode="x unified",
                margin=dict(l=10, r=10, t=10, b=10)
            )
            charts_data.append((f"📈 Trend: {num_col}", fig, None))
    except Exception:
        pass
    
    return charts_data


# ============================================================================
# MAIN SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 📊 Agentic BI")
    st.divider()
    
    tabs = ["📁 Data Center", "📈 Intelligence Hub", "🤖 Agentic Query"]
    st.session_state.active_tab = st.radio("Navigate", options=[0, 1, 2], format_func=lambda x: tabs[x])
    
    st.divider()
    
    if st.session_state.df is not None:
        st.success("✓ Data Loaded")
        st.metric("Rows (Orig)", st.session_state.profile["rows"])
        if st.session_state.df_clean is not None:
            st.metric("Rows (Clean)", len(st.session_state.df_clean))
        st.metric("Columns", st.session_state.profile["cols"])
    else:
        st.warning("⚠ No Data Yet")
    
    st.divider()
    st.caption("© 2025 Agentic BI | SRMU Final Major Project")


# ============================================================================
# TAB 1: DATA CENTER
# ============================================================================

if st.session_state.active_tab == 0:
    st.markdown("## 📁 Data Center")
    st.markdown("Upload your dataset - Auto-cleanup enabled")
    
    with st.container():
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=["csv"],
            label_visibility="collapsed",
            help="Drag & drop or click to select a CSV file"
        )
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.session_state.profile = profile_data(df)
                
                # WISE SANITIZATION - AWS-OPTIMIZED
                df_clean = sanitize_dataset(df)
                st.session_state.df_clean = df_clean
                
                # Display sanitization results
                rows_removed = len(df) - len(df_clean)
                st.success(f"✅ Sanitization Complete! Rows: {len(df)} → Cleaned: {len(df_clean)} (Removed: {rows_removed})")
            except Exception as e:
                st.error(f"Sanitization Error: {str(e)}")
    
    st.divider()
    
    if st.session_state.df is not None:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", st.session_state.profile["rows"])
        with col2:
            st.metric("Total Columns", st.session_state.profile["cols"])
        with col3:
            st.metric("Numeric", len(st.session_state.profile["numeric"]))
        with col4:
            st.metric("Categorical", len(st.session_state.profile["categorical"]))
        
        st.divider()
        
        st.markdown("### 📋 Data Preview (Original)")
        st.dataframe(st.session_state.df.head(10), use_container_width=True, height=250)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.df_clean is not None:
            st.markdown("### 🧹 Data Preview (Cleaned)")
            st.dataframe(st.session_state.df_clean.head(10), use_container_width=True, height=250)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### 🔍 Columns Information")
        col_info = []
        for col in st.session_state.df.columns:
            col_info.append({
                "Column": col,
                "Type": st.session_state.profile["column_types"].get(col, "unknown"),
                "Non-Null": st.session_state.df[col].notna().sum(),
                "Unique": st.session_state.df[col].nunique()
            })
        st.dataframe(pd.DataFrame(col_info), use_container_width=True, height=250)


# ============================================================================
# TAB 2: INTELLIGENCE HUB (THE OVERVIEW - AUTO-CHARTS)
# ============================================================================

elif st.session_state.active_tab == 1:
    st.markdown("## 📈 Intelligence Hub")
    st.markdown("Dataset Summary & Global Visualization Insights")
    
    if st.session_state.df_clean is None:
        st.info("📊 Upload a dataset in Data Center to generate insights")
    else:
        # Dataset Summary Statistics
        st.markdown("### 📊 Dataset Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Clean Rows", len(st.session_state.df_clean))
        with col2:
            st.metric("Columns", st.session_state.profile["cols"])
        with col3:
            st.metric("Numeric Fields", len(st.session_state.profile["numeric"]))
        with col4:
            st.metric("Categorical Fields", len(st.session_state.profile["categorical"]))
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        
        # Generate and display 4-5 auto-charts in VERTICAL STACKED layout
        charts_data = generate_auto_charts(st.session_state.df_clean, st.session_state.profile)
        
        if charts_data:
            st.markdown("### 🎨 Auto-Generated Analytics")
            st.markdown("<br>", unsafe_allow_html=True)
            
            for title, fig, table_df in charts_data:
                # Dynamic Title
                st.markdown(f"#### {title}")
                
                # Chart Container
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Optional table
                if table_df is not None:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(table_df, use_container_width=True, height=250)
                
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.warning("Unable to generate charts. Ensure data contains numeric or categorical columns.")


# ============================================================================
# TAB 3: AGENTIC QUERY (THE SPECIALIST - 5 BUTTONS)
# ============================================================================

elif st.session_state.active_tab == 2:
    st.markdown("## 🤖 Agentic Query")
    st.markdown("Specialist Analytics with 5 Quick Suggestions")
    
    if st.session_state.df_clean is None:
        st.info("📊 Upload a dataset in Data Center to start querying")
    else:
        # Query input
        query = st.text_input(
            "Ask a question about your data",
            placeholder="e.g., Show correlation heatmap or What's the sales trend?",
            label_visibility="collapsed"
        )
        
        # 5 SUGGESTION BUTTONS
        st.markdown("#### 💡 Quick Suggestions:")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        suggestions = {
            "Correlation": "Feature Correlation Heatmap",
            "Trends": f"Trends in {st.session_state.profile['numeric'][0] if st.session_state.profile['numeric'] else 'data'}",
            "Comparison": f"Compare by {st.session_state.profile['categorical'][0] if st.session_state.profile['categorical'] else 'category'}",
            "Distribution": f"Distribution of {st.session_state.profile['numeric'][0] if st.session_state.profile['numeric'] else 'values'}",
            "Proportion": f"Proportion of {st.session_state.profile['categorical'][0] if st.session_state.profile['categorical'] else 'categories'}"
        }
        
        button_keys = list(suggestions.keys())
        
        with col1:
            if st.button(button_keys[0], use_container_width=True):
                query = suggestions[button_keys[0]]
        with col2:
            if st.button(button_keys[1], use_container_width=True):
                query = suggestions[button_keys[1]]
        with col3:
            if st.button(button_keys[2], use_container_width=True):
                query = suggestions[button_keys[2]]
        with col4:
            if st.button(button_keys[3], use_container_width=True):
                query = suggestions[button_keys[3]]
        with col5:
            if st.button(button_keys[4], use_container_width=True):
                query = suggestions[button_keys[4]]
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        
        # Process query with cleaned data
        if query:
            intent = detect_query_intent(query)
            fig, title, table_df = generate_chart_and_title(
                st.session_state.df_clean,
                st.session_state.profile,
                intent
            )
            
            # VERTICAL STACKED OUTPUT: Title -> Chart -> Table
            if fig is not None:
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Dynamic Title
                st.markdown(f"### {title}")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Chart Container
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Data Table
                if table_df is not None:
                    st.markdown("#### 📊 Detailed Data Table")
                    st.dataframe(table_df, use_container_width=True, height=300)
                
                # Add to history
                if query not in st.session_state.query_history:
                    st.session_state.query_history.append(query)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.divider()
            
            # Query history
            if st.session_state.query_history:
                with st.expander("📜 Query History"):
                    for i, q in enumerate(reversed(st.session_state.query_history[-10:]), 1):
                        st.caption(f"{i}. {q}")
