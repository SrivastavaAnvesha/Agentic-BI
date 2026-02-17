import os
import time
from dotenv import load_dotenv
from google import genai
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Database setup
raw_password = "@Anvesha94" # <--- Apna password sahi likhein
password = quote_plus(raw_password)
db_url = f"postgresql://postgres:{password}@localhost:5432/agentic_bi"
engine = create_engine(db_url)

def ask_ai_about_data(user_query):
    context = """
    You are a SQL expert. Table: 'raw_sales_data'.
    Columns: order_id, order_date, product_name, category, sales_amount, region, customer_type.
    Return ONLY the SQL query. No markdown, no backticks.
    Example: SELECT SUM(sales_amount) FROM raw_sales_data;
    """
    
    # Hum 'flash-lite' use karenge kyunki ye quota kam khata hai
    model_id = 'gemini-flash-lite-latest' 
    
    for attempt in range(3): # 3 baar koshish karega agar quota khatam ho
        try:
            response = client.models.generate_content(
                model=model_id, 
                contents=f"{context}\nQuestion: {user_query}"
            )
            
            sql_query = response.text.strip().replace('```sql', '').replace('```', '').strip()
            print(f"--- AI generated SQL: {sql_query} ---")
            
            with engine.connect() as conn:
                result = conn.execute(text(sql_query))
                return result.fetchall()
                
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Quota full! Attempt {attempt+1}/3. Waiting 10 seconds...")
                time.sleep(10) # 10 second ka break
            else:
                return f"Error: {e}"
                
    return "Failed after 3 attempts due to Quota limits."

if __name__ == "__main__":
    question = "What is the total sales amount?"
    print(f"Question: {question}")
    answer = ask_ai_about_data(question)
    print(f"Answer from Database: {answer}")