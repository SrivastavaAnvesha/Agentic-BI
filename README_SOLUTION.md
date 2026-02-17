# Agentic BI Project - API Issue Resolution

## What I've Created For You

### 1. **list_models.py** - Model Discovery Script
```bash
python list_models.py
```
Shows all available Gemini models on your Free Tier API key, including:
- Model names
- Token limits
- Generation methods
- Which ones you can actually use

**This is your first step** - run this to identify working models.

---

### 2. **brain.py** - Updated Main Module
Completely refactored with:

#### Features:
- **`ask_ai_about_data(question)`** - Ask the AI about your database
  - Automatically fetches database schema
  - Provides context to the AI
  - Handles 429 and 404 errors with helpful messages
  
- **`ask_ai_generate_sql(question)`** - Generate and execute SQL
  - Converts natural language to SQL
  - Executes the query
  - Returns structured results
  
- **`test_connection()`** - Validates everything works
  - Tests PostgreSQL connection
  - Tests Gemini API
  - Shows which model is active

#### Configuration:
```python
GEMINI_MODEL = "gemini-2.0-flash-exp"  # Change this based on list_models.py results
```

---

### 3. **rate_limiter.py** - Handle Rate Limits
Implements exponential backoff retry logic for graceful 429 error handling.

Use as decorator:
```python
@retry_with_backoff(max_retries=5)
def my_api_call():
    return genai.Client().models.generate_content(...)
```

---

### 4. **TROUBLESHOOTING.md** - Complete Guide
Detailed breakdown of:
- Why you're getting 429 and 404 errors
- How to fix them
- Library comparison (google-genai vs google-generativeai)
- Free tier quotas and limitations

---

## Quick Start Guide

### Step 1: Identify Available Models
```bash
python list_models.py
```

Look for a model that says available/working. Common ones on Free Tier:
- `gemini-2.0-flash-exp` ✅ (Most likely to work)
- `gemini-1.5-flash` (Maybe)
- `gemini-pro` (Legacy, usually works)

### Step 2: Update brain.py
Edit line 25 in brain.py:
```python
GEMINI_MODEL = "your_model_from_step_1"
```

### Step 3: Test
```bash
python brain.py
```

This will:
- Test PostgreSQL connection
- Test Gemini API with your model
- Run 2 example queries

### Step 4: Use in Your Project
```python
from brain import ask_ai_about_data, ask_ai_generate_sql

# Ask about data
answer = ask_ai_about_data("What are the top 5 products by revenue?")
print(answer)

# Generate and run SQL
results = ask_ai_generate_sql("Show me monthly sales trends")
print(results)
```

---

## Library Recommendation: **STICK WITH google-genai** ✅

### Why Not Switch to google-generativeai?

**The Problem Isn't The Library**
- Both libraries hit the same API quotas
- Both get the same 429 and 404 errors
- Switching libraries won't fix your issues

**Why google-genai (New) is Better:**
1. **Modern**: This is Google's current library (old one is being deprecated)
2. **Better Models**: Access to gemini-2.0-flash-exp
3. **Cleaner API**: Easier to use
4. **Future-Proof**: Will have all new features
5. **Better Errors**: More informative error messages

**The Real Solution:**
- The 429 errors are due to **Free Tier rate limits** (same for both libraries)
- The 404 errors are because those **models don't exist on your free tier**
- Use the `retry_with_backoff` decorator to handle transient failures
- Switch to a paid tier if you need production-grade reliability

---

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| 429 RESOURCE_EXHAUSTED | Rate limit hit | Wait 1-2 hours, use retry decorator |
| 404 NOT_FOUND | Model unavailable on free tier | Run `list_models.py`, use available model |
| Invalid API Key | Wrong GOOGLE_API_KEY | Check .env file |
| PostgreSQL connection error | Database not running | Start PostgreSQL service |

---

## Free Tier Limits (Important!)

- **Rate Limit**: ~60 requests/minute (varies)
- **Daily Quota**: Limited (resets daily)
- **Concurrent Requests**: Limited
- **Models Available**: gemini-2.0-flash-exp, gemini-1.5-flash, gemini-pro

To avoid hitting limits:
1. Add `time.sleep(1)` between requests
2. Use the `retry_with_backoff` decorator
3. Cache responses when possible
4. Test during off-peak hours

---

## Files Overview

```
Agentic_BI_Project/
├── brain.py                    # Main AI + DB module (UPDATED)
├── ingest_data.py             # Your existing data ingestion
├── list_models.py             # NEW - Model discovery script
├── rate_limiter.py            # NEW - Retry logic for rate limits
├── TROUBLESHOOTING.md         # NEW - Complete troubleshooting guide
├── data/
│   └── sales_data.csv
└── .env                       # Your API keys (must have GOOGLE_API_KEY)
```

---

## What To Do Next

1. **Run:** `python list_models.py`
2. **Copy:** Working model name
3. **Edit:** brain.py line 25 with that model
4. **Test:** `python brain.py`
5. **Use:** Import functions from brain.py in your project

---

## Support

If you're still having issues after these steps, check:
- [Google Generative AI docs](https://ai.google.dev)
- [API pricing](https://ai.google.dev/pricing) - Free tier limits
- Your API key validity in Google Cloud Console

Good luck! 🚀
