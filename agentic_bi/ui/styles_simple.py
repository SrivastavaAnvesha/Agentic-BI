"""Simple & Elegant Dark Theme Styles - Agentic BI."""

CUSTOM_CSS = """
<style>
/* ========== GLOBAL ========== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    background: #0F172A !important;
    color: #F8FAFC !important;
    font-family: 'Segoe UI', sans-serif !important;
}

/* ========== STREAMLIT ========== */
.main {
    background: transparent !important;
    padding: 2rem !important;
}

.stApp {
    background: #0F172A !important;
}

[data-testid="stSidebar"] {
    background: #0F172A !important;
    border-right: 1px solid rgba(8, 145, 178, 0.1) !important;
}

/* ========== TEXT ========== */
h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

h1 { font-size: 28px !important; margin-bottom: 0.5rem !important; }
h2 { font-size: 20px !important; margin-bottom: 1rem !important; }
h3 { font-size: 16px !important; margin-bottom: 0.75rem !important; }

p {
    color: #94a3b8 !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
}

/* ========== METRICS ========== */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(8, 145, 178, 0.08) 0%, rgba(6, 90, 130, 0.08) 100%) !important;
    border: 1px solid rgba(8, 145, 178, 0.15) !important;
    border-radius: 8px !important;
    padding: 15px 20px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stMetric"]:hover {
    border-color: rgba(8, 145, 178, 0.3) !important;
    box-shadow: 0 4px 12px rgba(8, 145, 178, 0.1) !important;
}

/* ========== BUTTONS ========== */
.stButton > button {
    background: linear-gradient(135deg, #0891B2 0%, #065A82 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    box-shadow: 0 4px 12px rgba(8, 145, 178, 0.25) !important;
    transform: translateY(-1px) !important;
}

/* ========== INPUTS ========== */
input, textarea, select {
    background: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid rgba(8, 145, 178, 0.15) !important;
    color: #F8FAFC !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    font-size: 14px !important;
}

input::placeholder, textarea::placeholder {
    color: #64748b !important;
}

input:focus, textarea:focus {
    background: rgba(30, 41, 59, 0.9) !important;
    border-color: #0891B2 !important;
    box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.08) !important;
    outline: none !important;
}

/* ========== TABLES ========== */
table {
    background: rgba(30, 41, 59, 0.4) !important;
}

thead {
    background: rgba(8, 145, 178, 0.08) !important;
}

thead th {
    color: #F8FAFC !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

tbody td {
    color: #cbd5e1 !important;
    font-size: 13px !important;
}

tbody tr:hover {
    background: rgba(8, 145, 178, 0.04) !important;
}

/* ========== ALERTS ========== */
.stAlert {
    border-radius: 6px !important;
    border-left: 3px solid !important;
}

.stSuccess {
    background: rgba(16, 185, 129, 0.08) !important;
    border-left-color: #10b981 !important;
}

.stError {
    background: rgba(239, 68, 68, 0.08) !important;
    border-left-color: #ef4444 !important;
}

.stWarning {
    background: rgba(245, 158, 11, 0.08) !important;
    border-left-color: #f59e0b !important;
}

.stInfo {
    background: rgba(8, 145, 178, 0.08) !important;
    border-left-color: #0891B2 !important;
}

/* ========== EXPANDERS ========== */
.streamlit-expanderHeader {
    background: rgba(8, 145, 178, 0.04) !important;
    color: #F8FAFC !important;
    font-weight: 500 !important;
}

/* ========== DIVIDERS ========== */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(8, 145, 178, 0.15), transparent) !important;
    margin: 1rem 0 !important;
}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(8, 145, 178, 0.25);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(8, 145, 178, 0.4);
}
</style>
"""
