"""
Rate Limit Handler for Gemini API
Implements exponential backoff to gracefully handle 429 errors
"""
import time
import random
from functools import wraps

class RateLimitError(Exception):
    """Custom exception for rate limiting"""
    pass

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    """
    Decorator to retry function calls with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds (doubles each retry)
        max_delay: Maximum delay between retries
        
    Example:
        @retry_with_backoff(max_retries=5)
        def my_api_call():
            return client.models.generate_content(...)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    error_str = str(e)
                    last_exception = e
                    
                    # Check if it's a rate limit error
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        if attempt < max_retries:
                            # Calculate delay with exponential backoff + jitter
                            delay = min(base_delay * (2 ** attempt), max_delay)
                            jitter = random.uniform(0, delay * 0.1)
                            wait_time = delay + jitter
                            
                            print(f"\n⏳ Rate limit hit (429). Attempt {attempt + 1}/{max_retries + 1}")
                            print(f"   Waiting {wait_time:.1f} seconds before retry...")
                            time.sleep(wait_time)
                        else:
                            print(f"\n❌ Rate limit exceeded. Gave up after {max_retries} retries.")
                            raise RateLimitError(
                                f"API rate limited after {max_retries} retries. "
                                f"Free tier quota exhausted. Try again in 1-2 hours."
                            )
                    else:
                        # Not a rate limit error, re-raise immediately
                        raise
            
            raise last_exception
        
        return wrapper
    return decorator

def rate_limited_call(func, *args, max_retries=3, **kwargs):
    """
    Non-decorator version of retry logic. Use this if you can't use decorators.
    
    Example:
        response = rate_limited_call(
            client.models.generate_content,
            model="gemini-2.0-flash-exp",
            contents="Hello"
        )
    """
    return retry_with_backoff(max_retries=max_retries)(
        lambda: func(*args, **kwargs)
    )()

# Example usage in your code:
"""
# Method 1: Using decorator
@retry_with_backoff(max_retries=5, base_delay=2)
def ask_ai_with_retry(question):
    response = genai.Client().models.generate_content(
        model=GEMINI_MODEL,
        contents=question
    )
    return response.text

# Method 2: Wrapping existing function
def ask_ai_about_data_improved(user_question):
    def api_call():
        response = genai.Client().models.generate_content(
            model=GEMINI_MODEL,
            contents=user_question
        )
        return response.text
    
    return rate_limited_call(api_call, max_retries=5)
"""
