import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from brain import ask_ai_about_data
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()
raw_password = "@Anvesha94"
password = quote_plus(raw_password)
db_url = f"postgresql://postgres:{password}@localhost:5432/agentic_bi"
engine = create_engine(db_url)

# ============= PAGE CONFIGURATION =============
st.set_page_config(
    page_title="AI Sales Analyst", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= CUSTOM STYLING =============
st.markdown("""
    <style>
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #0e1117 0%, #161b22 100%);
    }
    
    /* Metric Cards */
    .stMetric {
        background: linear-gradient(135deg, #1f6feb 0%, #238636 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #58a6ff;
        font-weight: 700;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #21262d;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# ============= HEADER =============
st.title("📊 Agentic BI Dashboard")
st.markdown("**Your AI-Powered Sales Analysis Engine** | Powered by Gemini + PostgreSQL")
st.divider()

# ============= QUERY SECTION =============
st.subheader("🔍 Ask Your Data")

col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input(
        "Ask me anything about your sales data:",
        placeholder="e.g., What are the total sales by category? or What is the top selling product?",
        label_visibility="collapsed"
    )
with col2:
    run_button = st.button("🚀 Analyze", use_container_width=True)

# ============= QUERY EXECUTION =============
if run_button:
    if query:
        with st.spinner("🧠 AI Brain analyzing your data..."):
            try:
                response = ask_ai_about_data(query)
                
                if isinstance(response, list) and len(response) > 0:
                    st.success("✅ Analysis Complete!")
                    
                    # Try to convert to DataFrame for visualization
                    df_result = None
                    
                    try:
                        # If response has multiple columns, convert to DataFrame
                        if len(response[0]) > 1:
                            # Multi-column response
                            columns = [f"Col_{i+1}" for i in range(len(response[0]))]
                            df_result = pd.DataFrame(response, columns=columns)
                        else:
                            # Single column response
                            df_result = pd.DataFrame({"Result": [row[0] for row in response]})
                    except Exception as e:
                        st.warning(f"Could not convert to DataFrame: {e}")
                    
                    # ============= METRICS SECTION =============
                    if df_result is not None and len(df_result) > 0:
                        try:
                            # Try to extract numeric values
                            first_value = df_result.iloc[0, 0]
                            if isinstance(first_value, (int, float)):
                                formatted_val = "{:,.2f}".format(float(first_value))
                                
                                col_metric1, col_metric2 = st.columns(2)
                                with col_metric1:
                                    st.metric(
                                        label="💰 Primary Value",
                                        value=f"₹ {formatted_val}",
                                        delta="📊 From Analysis"
                                    )
                                with col_metric2:
                                    st.metric(
                                        label="📈 Data Points",
                                        value=len(df_result),
                                        delta="Results Retrieved"
                                    )
                        except Exception as e:
                            st.info(f"Note: Could not format as metric - showing as table instead")
                    
                    # ============= VISUALIZATION SECTION =============
                    st.divider()
                    
                    if df_result is not None and len(df_result) > 0:
                        # Display the data
                        st.subheader("📋 Data Results")
                        st.dataframe(df_result, use_container_width=True)
                        
                        # Try to create visualizations
                        try:
                            # Check if we have enough data for charts
                            if len(df_result) > 1 and len(df_result.columns) >= 1:
                                st.subheader("📊 Visualizations")
                                
                                # Try numeric column detection for charting
                                numeric_cols = df_result.select_dtypes(include=['number']).columns.tolist()
                                
                                if len(numeric_cols) > 0 and len(df_result) > 1:
                                    # Create a bar chart
                                    fig = px.bar(
                                        df_result,
                                        x=df_result.columns[0] if len(df_result.columns) > 1 else df_result.index,
                                        y=numeric_cols[0] if len(numeric_cols) > 0 else df_result.columns[0],
                                        title="📊 Sales Breakdown",
                                        color=numeric_cols[0] if len(numeric_cols) > 0 else None,
                                        color_continuous_scale="Viridis"
                                    )
                                    fig.update_layout(
                                        height=400,
                                        template="plotly_dark",
                                        hovermode="x unified"
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.info(f"📌 Note: Could not create automatic visualization: {e}")
                    
                    # ============= DETAILS SECTION =============
                    with st.expander("🔧 Technical Details & Raw Output"):
                        st.info("**Raw Database Response:**")
                        st.code(str(response), language="python")
                        if df_result is not None:
                            st.info("**DataFrame Info:**")
                            st.write(f"Shape: {df_result.shape} | Columns: {list(df_result.columns)}")
                else:
                    st.error(f"❌ No data returned: {response}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Tip: Try asking simpler questions or check your database connection")
    else:
        st.warning("⚠️ Please enter a question about your sales data!")

# ============= PREDEFINED QUERIES SECTION =============
st.divider()
st.subheader("⚡ Quick Queries")

quick_queries = {
    "💰 Total Sales": "What is the total sales amount?",
    "📦 Total Orders": "How many orders do we have?",
    "🏆 Top Category": "Which category has the highest sales?",
    "🌍 Regional Sales": "Show me sales by region",
}

cols = st.columns(len(quick_queries))
for idx, (label, quick_query) in enumerate(quick_queries.items()):
    with cols[idx]:
        if st.button(label, use_container_width=True, key=f"quick_{idx}"):
            with st.spinner(f"Running: {label}..."):
                response = ask_ai_about_data(quick_query)
                if isinstance(response, list) and len(response) > 0:
                    st.success(f"✅ {label}")
                    try:
                        if len(response[0]) > 1:
                            columns = [f"Col_{i+1}" for i in range(len(response[0]))]
                            df_display = pd.DataFrame(response, columns=columns)
                        else:
                            df_display = pd.DataFrame({"Result": [row[0] for row in response]})
                        st.dataframe(df_display, use_container_width=True)
                    except Exception as e:
                        st.write(response)
                else:
                    st.error(f"Could not retrieve: {response}")

# ============= SIDEBAR =============
with st.sidebar:
    st.markdown("### 🛠️ Project Stack")
    st.info("""
    **Model:** Gemini Flash Lite

    **Database:** PostgreSQL

    **Visualization:** Plotly

    **Framework:** Streamlit
    """)
    
    st.divider()
    
    st.markdown("### 📊 Dashboard Stats")
    try:
        with engine.connect() as conn:
            total_records = conn.execute(text("SELECT COUNT(*) FROM raw_sales_data")).fetchone()[0]
            total_sales = conn.execute(text("SELECT SUM(sales_amount) FROM raw_sales_data")).fetchone()[0]
            
        st.metric("📈 Total Records", f"{total_records:,}")
        st.metric("💰 Total Sales", f"₹ {total_sales:,.2f}" if total_sales else "₹ 0")
    except Exception as e:
        st.warning(f"Could not fetch stats: {e}")
    
    st.divider()
    st.markdown("### 👨‍💼 About")
    st.caption("Developed by: **Anvesha**")
    st.caption("🎯 **Progress:** 60-70% Complete")
    st.caption("⭐ Features: AI Query | Data Viz | Real-time Analytics")