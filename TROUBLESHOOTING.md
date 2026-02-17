"""
GEMINI API TROUBLESHOOTING & LIBRARY COMPARISON GUIDE
======================================================

## ISSUE SUMMARY
You're experiencing:
1. 429 RESOURCE_EXHAUSTED for gemini-2.0-flash
2. 404 NOT_FOUND for 1.5-flash and 1.0-pro

Root cause: Free Tier model availability and rate limiting

---

## SOLUTION 1: RUN THE MODEL DISCOVERY SCRIPT

First, identify which models are actually available on your Free Tier API key:

    python list_models.py

This will show you:
- Model names and display names
- Token limits for each model
- Supported generation methods
- Full availability details

Expected working models on Free Tier:
- gemini-2.0-flash-exp (Experimental, most available)
- gemini-1.5-flash (May be available)
- gemini-pro (Legacy, usually available)
- gemini-1.5-pro (Less likely on free tier)

---

## SOLUTION 2: UPDATE brain.py with Working Model

The updated brain.py includes:

1. GEMINI_MODEL configuration at the top:
   
   GEMINI_MODEL = "gemini-2.0-flash-exp"
   
   Change this based on what works for your API key.

2. Enhanced ask_ai_about_data() function with:
   - Database schema context automatically fetched
   - Error handling for 429 and 404 errors
   - Clear error messages
   - Fallback suggestions

3. New ask_ai_generate_sql() function:
   - Generates SQL from natural language
   - Executes the generated query
   - Returns structured results

4. test_connection() function:
   - Validates PostgreSQL connection
   - Tests Gemini API availability
   - Shows which model is being used

---

## SOLUTION 3: LIBRARY COMPARISON

### google-genai (NEW - Currently using)
✅ Pros:
  - Modern library with latest API
  - Better async support
  - Cleaner API interface
  - Latest model access (2.0-flash)
  - Better error messages
  - More active development

❌ Cons:
  - Newer = fewer tested edge cases
  - Free tier API quota same as old library
  - 429 errors still common if exceeding quotas
  - Model availability may vary

Command: pip install google-genai


### google-generativeai (OLD - Previous version)
✅ Pros:
  - More mature/stable
  - Larger community support
  - Well-documented
  - Proven track record

❌ Cons:
  - Legacy library (google-genai is replacement)
  - May not support latest models
  - Slower development
  - Syntax is more verbose

Command: pip install google-generativeai


## RECOMMENDATION FOR YOUR USE CASE

### 🎯 STICK WITH google-genai (NEW LIBRARY)

Here's why:

1. **Model Access**: The new library gives you access to gemini-2.0-flash-exp, 
   which is NEWER and sometimes has better free tier quotas than older models

2. **Future-proof**: Google is deprecating the old library in favor of google-genai.
   Your project should use the modern library.

3. **The 429/404 Errors Are NOT Library Issues**:
   - 429 (Rate Limit): Happens with BOTH libraries on Free Tier
   - 404 (Model Not Found): Specific models may not be on your free tier plan
   
   Neither library can solve these—they're API-level restrictions.

4. **Better Error Handling**: google-genai has clearer error messages
   to help you debug (which is what the updated brain.py leverages)

---

## FREE TIER QUOTA LIMITS (affects both libraries)

⚠️ Both libraries use the same underlying API quotas:

- Rate limit: ~60 requests per minute (varies)
- Daily quota: Limited (exact amount not published)
- Concurrent requests: Limited

To avoid 429 errors:
1. Add delays between requests: time.sleep(1)
2. Implement exponential backoff retry logic
3. Cache responses when possible
4. Batch similar queries together

---

## ACTION STEPS

1. Run list_models.py to see available models
   
   python list_models.py

2. Update GEMINI_MODEL in brain.py with a working model from step 1

3. Test the connection:
   
   python brain.py

4. If you still get 429 errors:
   - Wait 1-2 hours and try again
   - Free tier has daily quotas that reset
   - Try during off-peak hours

5. If you need production stability:
   - Consider paid tier ($0.075-$0.30 per 1M tokens)
   - Or switch to Claude API (Anthropic)
   - Or use open-source models (Ollama, LLaMA)

---

## QUICK MODEL TROUBLESHOOTING

Error: 429 RESOURCE_EXHAUSTED
→ Solution: Wait 1+ hours, add rate limiting to your code

Error: 404 NOT_FOUND (gemini-1.5-flash, gemini-1.0-pro)
→ Solution: Use gemini-2.0-flash-exp instead, or check list_models.py for available ones

Error: API key invalid
→ Solution: Verify GOOGLE_API_KEY in .env file is correct

---

## CODE UPDATES TO brain.py

✅ ask_ai_about_data() - Now includes:
   - Automatic database schema fetching
   - Specific error handling for 429 and 404
   - Helpful error messages
   
✅ ask_ai_generate_sql() - New function to:
   - Generate SQL from questions
   - Execute the generated query
   - Return results
   
✅ test_connection() - Validates:
   - PostgreSQL connection
   - Gemini API availability
   - Currently selected model

---

## NEXT STEPS

1. Run: python list_models.py
2. Copy working model name (e.g., gemini-2.0-flash-exp)
3. Update line in brain.py: GEMINI_MODEL = "your_model_name"
4. Run: python brain.py
5. Test with sample questions

That's it! You're ready to go.
"""