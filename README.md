# Agentic-BI: Autonomous Data Analytics & Intelligence Engine

> A Major Research Project — Bachelor of Computer Applications (Data Science & AI)  
> Shri Ramswaroop Memorial University, 2026

---

## What is Agentic-BI?

Agentic-BI is an AI-powered business intelligence system that lets non-technical users interact with their data using plain English (or even Hinglish). Instead of writing SQL queries or manually building dashboards, users simply ask questions — and the system thinks, queries, corrects itself, and visualizes the answer automatically.

---

## The Problem It Solves

In most organizations, non-technical managers have to wait for data analysts to generate reports. Tools like Tableau or Power BI are powerful but still require manual configuration. Agentic-BI eliminates this bottleneck by automating the entire pipeline — from understanding the question to rendering the chart.

---

## Key Features

- **Natural Language to SQL** — Converts plain English queries into optimized PostgreSQL queries using LangChain + Gemini API
- **Self-Healing Loop** — If the generated code throws an error, the system reads the traceback, sends it back to the AI, and retries automatically — no manual debugging needed
- **Smart Visualization** — Automatically picks the best chart type (bar, line, scatter) based on the nature of the data
- **Data Ingestion Engine** — Upload any CSV; the system auto-detects column types and builds a persistent PostgreSQL schema
- **Streamlit UI** — Clean, interactive interface accessible without any technical knowledge

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| AI Framework | LangChain, Google Gemini API |
| Database | PostgreSQL, SQLite |
| Data Processing | Pandas, SQLAlchemy |
| Visualization | Plotly |
| UI | Streamlit |
| IDE | VS Code |

---

## How It Works

```
User asks a question in plain English
        ↓
Gemini API reads the question + database schema
        ↓
Generates an optimized SQL query
        ↓
Query executes on PostgreSQL
        ↓
If error → Self-Healing loop fixes and retries
        ↓
Result rendered as interactive Plotly chart
```

---

## Architecture — ReAct Framework

This project follows the **ReAct (Reason + Act)** pattern:

1. **Thought** — Agent analyzes the user's question and the DB schema
2. **Action** — Agent writes and executes a SQL query or Python script
3. **Observation** — Agent checks if the result is logically correct
4. **Correction** — If wrong, the Error-Refinement Module rewrites and retries

---

## Target Users

- Business Managers who need instant data insights
- Non-technical Team Leads working with sales/revenue data
- SMEs in Retail, E-commerce, and Healthcare

---

## Project Status

**In Development** — Major Research Project (Expected: May 2026)

---

## Author

**Anvesha Srivastava**  
BCA — Data Science & Artificial Intelligence  
Shri Ramswaroop Memorial University, Lucknow  
[LinkedIn](https://www.linkedin.com/in/anvesha-srivastava-86485428a/) • [GitHub](https://github.com/SrivastavaAnvesha)