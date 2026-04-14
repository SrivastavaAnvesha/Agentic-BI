import streamlit as st

# ============================================================================
# GLOBAL CSS STYLING - AGENTIC BI (NOISE-RESISTANT + REORGANIZED)
# ============================================================================

css = """
<style>
/* GLOBAL RESET & BACKGROUND */
html, body {
    background-color: #000000 !important;
    color: #F8FAFC;
}

[data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
}

/* MAIN CONTAINER - FRAME LOCK */
.main .block-container {
    max-width: 100vw !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    overflow-x: hidden !important;
}

/* SIDEBAR - DEEP MATTE CHARCOAL (#0D1B2A) WITH CYAN GLOW */
[data-testid="stSidebar"] {
    background-color: #0D1B2A !important;
    border-right: 1px solid #0891B2 !important;
    box-shadow: 2px 0px 15px rgba(8, 145, 178, 0.25) !important;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlockBg"] {
    background-color: #0D1B2A !important;
}

[data-testid="stSidebar"] .stMarkdown {
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
    font-weight: 700 !important;
}

/* DATAFRAME - TABLE FRAME LOCK */
[data-testid="stDataFrame"], .stDataFrame {
    width: 100% !important;
    max-width: 100% !important;
}

[data-testid="stDataFrame"] > div {
    overflow-x: auto !important;
}

/* DATAFRAME STYLING */
[data-testid="stDataFrame"] table {
    border-collapse: collapse;
    width: 100%;
}

[data-testid="stDataFrame"] thead {
    background: linear-gradient(90deg, #0891B2, #065A82) !important;
}

[data-testid="stDataFrame"] thead th {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #0891B2, #065A82) !important;
    border: 1px solid #0891B2 !important;
    padding: 12px 8px !important;
}

[data-testid="stDataFrame"] tbody td {
    color: #F8FAFC !important;
    border: 1px solid #0F1729 !important;
    background-color: #000000 !important;
    padding: 10px 8px !important;
}

[data-testid="stDataFrame"] tbody tr:hover {
    background-color: #0F1729 !important;
}

/* BUTTONS - BOLD WHITE TEXT */
button, [data-testid="baseButton-primary"], [data-testid="baseButton-secondary"], [data-testid="baseButton-tertiary"] {
    color: #FFFFFF !important;
    font-weight: bold !important;
    background: linear-gradient(135deg, #0891B2, #065A82) !important;
    border: none !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    font-size: 14px !important;
}

button:hover, [data-testid="baseButton-primary"]:hover, [data-testid="baseButton-secondary"]:hover {
    background: linear-gradient(135deg, #0AAFCC, #0891B2) !important;
    box-shadow: 0 0 20px rgba(8, 145, 178, 0.6) !important;
    color: #FFFFFF !important;
    font-weight: bold !important;
    transform: translateY(-2px) !important;
}

button span, button p, button strong, button div {
    color: #FFFFFF !important;
    font-weight: bold !important;
}

[data-testid="baseButton-primary"] span, [data-testid="baseButton-primary"] p, [data-testid="baseButton-primary"] strong {
    color: #FFFFFF !important;
    font-weight: bold !important;
}

[data-testid="baseButton-secondary"] span, [data-testid="baseButton-secondary"] p, [data-testid="baseButton-secondary"] strong {
    color: #FFFFFF !important;
    font-weight: bold !important;
}

/* RADIO BUTTONS */
[data-testid="stRadio"] > label {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

[data-testid="stRadio"] > div > div > label {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

/* TEXT INPUTS */
input, textarea {
    background-color: #0F1729 !important;
    color: #F8FAFC !important;
    border: 1px solid #0891B2 !important;
    border-radius: 8px !important;
    padding: 0.6rem 0.8rem !important;
}

input::placeholder, textarea::placeholder {
    color: #64748B !important;
}

input:focus, textarea:focus {
    border-color: #0AAFCC !important;
    box-shadow: 0 0 12px rgba(8, 145, 178, 0.5) !important;
    outline: none !important;
}

/* METRICS */
[data-testid="metric-container"] {
    background-color: #0F1729 !important;
    border: 1px solid #0891B2 !important;
    border-radius: 8px !important;
    padding: 1.2rem !important;
}

[data-testid="stMetricValue"] {
    color: #0891B2 !important;
    font-weight: 700 !important;
    font-size: 28px !important;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* HEADINGS - BOLD WHITE */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

h1 { font-size: 2.5rem !important; }
h2 { font-size: 2rem !important; margin-top: 0.5rem !important; }
h3 { font-size: 1.5rem !important; margin-top: 0.3rem !important; }
h4 { font-size: 1.25rem !important; }

/* MARKDOWN TEXT */
.stMarkdown, p, span, li {
    color: #F8FAFC !important;
}

/* ALERTS */
[data-testid="stAlert"] {
    background-color: #0F1729 !important;
    border: 1px solid #0891B2 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

[data-testid="stAlert"] p, [data-testid="stAlert"] span {
    color: #F8FAFC !important;
}

/* DIVIDER */
hr {
    border-color: #0891B2 !important;
    border-style: solid !important;
    opacity: 0.3 !important;
    margin: 1.5rem 0 !important;
}

/* EXPANDER */
[data-testid="stExpander"] > div > button {
    color: #F8FAFC !important;
    background-color: #0F1729 !important;
    border: 1px solid #0891B2 !important;
    font-weight: 600 !important;
}

[data-testid="stExpander"] > div > button:hover {
    background-color: #1A2938 !important;
    border-color: #0AAFCC !important;
}

/* CHART CONTAINERS - CUSTOM CLASS */
.chart-container {
    border: 1px solid #0891B2 !important;
    border-radius: 12px !important;
    background-color: #000000 !important;
    padding: 20px !important;
    margin: 1.5rem 0 !important;
    box-shadow: 0 0 15px rgba(8, 145, 178, 0.15) !important;
}

/* PLOTLY CHARTS */
.plotly-container {
    background-color: transparent !important;
}

.plotly-graph-div {
    background-color: transparent !important;
}

[data-testid="stPlotlyChart"] {
    background-color: transparent !important;
}

/* LINKS */
a {
    color: #0891B2 !important;
    text-decoration: none !important;
}

a:hover {
    color: #0AAFCC !important;
    text-decoration: underline !important;
}

/* SCROLLBARS */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #0F1729;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #0891B2, #065A82);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #0AAFCC, #0891B2);
}

/* FILE UPLOADER */
[data-testid="fileUploadDropzone"] {
    border: 2px dashed #0891B2 !important;
    border-radius: 8px !important;
    background-color: #0F1729 !important;
    padding: 2rem !important;
    transition: all 0.3s ease !important;
}

[data-testid="fileUploadDropzone"]:hover {
    border-color: #0AAFCC !important;
    background-color: #1A2938 !important;
    box-shadow: 0 0 15px rgba(8, 145, 178, 0.3) !important;
}

[data-testid="fileUploadDropzone"] p {
    color: #F8FAFC !important;
}

/* CAPTION & SMALL TEXT */
.stCaption, small {
    color: #94A3B8 !important;
    font-size: 12px !important;
}

/* VERTICAL SPACING */
.stMarkdown {
    margin-bottom: 1rem !important;
}

/* COLUMNS & CONTAINERS */
[data-testid="stColumn"] {
    width: 100% !important;
}

.stContainer {
    width: 100% !important;
    max-width: 100% !important;
}

[data-testid="stVerticalBlock"] {
    padding: 0 !important;
}

.element-container {
    width: 100% !important;
}

/* MOBILE RESPONSIVENESS */
@media (max-width: 768px) {
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    [data-testid="stSidebar"] {
        width: 100% !important;
        border-right: none !important;
        border-bottom: 1px solid #0891B2 !important;
    }
    
    h1 { font-size: 1.75rem !important; }
    h2 { font-size: 1.5rem !important; }
    h3 { font-size: 1.25rem !important; }
    
    .chart-container {
        padding: 15px !important;
    }
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)
