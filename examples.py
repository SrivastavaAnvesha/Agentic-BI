"""
Example: Complete Agentic BI Usage
Shows how to use the updated brain.py with your database
"""

# Example 1: Simple Query About Data
# ===================================

from brain import ask_ai_about_data

question = "What are our top 5 best-selling products?"
answer = ask_ai_about_data(question)
print(answer)


# Example 2: Generate and Execute SQL
# ====================================

from brain import ask_ai_generate_sql

question = "Show me total revenue by month"
result = ask_ai_generate_sql(question)
print(result)


# Example 3: With Rate Limiting (Recommended)
# ============================================

from brain import ask_ai_about_data, ask_ai_generate_sql
from rate_limiter import retry_with_backoff, RateLimitError

@retry_with_backoff(max_retries=5, base_delay=2)
def safe_query(question):
    """Query with automatic retry on rate limit"""
    return ask_ai_about_data(question)

try:
    answer = safe_query("What are recent trends?")
    print(answer)
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    print("Try again in a few hours")


# Example 4: Batch Queries with Rate Limiting
# ============================================

import time

questions = [
    "What are our top products?",
    "How much revenue did we make this month?",
    "What are the customer segments?",
]

for i, question in enumerate(questions, 1):
    print(f"\n[Query {i}/{len(questions)}]")
    print(f"Q: {question}")
    
    try:
        answer = ask_ai_about_data(question)
        print(f"A: {answer}\n")
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Be nice to the API - add delay between requests
    if i < len(questions):
        print("⏳ Waiting 2 seconds before next request...")
        time.sleep(2)


# Example 5: Test Everything First
# ==================================

from brain import test_connection

print("\n🧪 Testing your setup...")
if test_connection():
    print("✅ All systems ready! You can proceed with queries.")
else:
    print("❌ Please fix the issues shown above.")


# Example 6: Error Handling Pattern
# ==================================

def query_with_fallback(question):
    """
    Query with graceful error handling
    """
    try:
        return ask_ai_about_data(question)
    
    except Exception as e:
        if "429" in str(e):
            return "⏳ API rate limited. Please wait 1-2 hours and try again."
        elif "404" in str(e):
            return "❌ Model not available. Run: python list_models.py"
        else:
            return f"❌ Error: {e}"

answer = query_with_fallback("What's our revenue?")
print(answer)


# Example 7: Production-Ready Usage
# ==================================

from brain import ask_ai_generate_sql
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_sales_data(metric: str) -> dict:
    """
    Production-ready function to analyze sales data
    
    Args:
        metric: What to analyze (e.g., "revenue", "customer count", "growth rate")
        
    Returns:
        Dictionary with query result and metadata
    """
    try:
        question = f"Calculate the total {metric} for each product category"
        logger.info(f"Analyzing: {metric}")
        
        result = ask_ai_generate_sql(question)
        
        return {
            "status": "success",
            "metric": metric,
            "result": result,
            "error": None
        }
    
    except Exception as e:
        logger.error(f"Analysis failed for {metric}: {e}")
        return {
            "status": "error",
            "metric": metric,
            "result": None,
            "error": str(e)
        }

# Usage
result = analyze_sales_data("revenue")
print(result)


# Example 8: Caching to Avoid Rate Limits
# ========================================

from functools import lru_cache
from brain import ask_ai_about_data

@lru_cache(maxsize=32)
def cached_query(question):
    """Cache queries to avoid repeated API calls"""
    return ask_ai_about_data(question)

# First call - hits API
answer1 = cached_query("What's the average order value?")
print(answer1)

# Second call with same question - uses cache (instant, no API call)
answer2 = cached_query("What's the average order value?")
print(answer2)


# Example 9: Streaming Larger Queries (if supported)
# ==================================================

def query_large_dataset(question):
    """
    For large responses, you might want streaming
    Currently not implemented in brain.py, but here's the pattern:
    """
    # This would be added to brain.py if needed
    # response = client.models.generate_content(
    #     model=GEMINI_MODEL,
    #     contents=question,
    #     stream=True  # Enable streaming
    # )
    # for chunk in response:
    #     print(chunk.text, end="")
    pass


# Example 10: Full Workflow Example
# ==================================

def run_full_analysis():
    """Complete example of using the AI brain"""
    
    # Step 1: Check if everything works
    print("Step 1: Testing connections...")
    if not test_connection():
        return
    
    print("\nStep 2: Getting database insights...")
    insight = ask_ai_about_data(
        "Summarize the key metrics in our sales data"
    )
    print(insight)
    
    print("\nStep 3: Analyzing specific metrics...")
    revenue = ask_ai_generate_sql(
        "What is the total revenue by product?"
    )
    print(revenue)
    
    print("\nStep 4: Getting recommendations...")
    recommendation = ask_ai_about_data(
        "Based on the data, what are your top 3 recommendations for growth?"
    )
    print(recommendation)
    
    print("\n✅ Analysis complete!")

# Uncomment to run:
# run_full_analysis()
