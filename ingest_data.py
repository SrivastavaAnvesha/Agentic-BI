import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os

# --- 1. CONFIGURATION ---
raw_password = "@Anvesha94" # <--- Apna sahi password likhein
password = quote_plus("@Anvesha94")
db_name = "agentic_bi"
file_path = "data/sales_data.csv" 
table_name = "raw_sales_data"

# Database Engine Setup
engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/{db_name}")

def start_ingestion():
    try:
        # File check karna
        if not os.path.exists(file_path):
            print(f"❌ Error: File '{file_path}' nahi mili! Check kijiye ki folder ka naam 'data' hi hai na?")
            return

        print(f"--- Step 1: Reading {file_path} ---")
        df = pd.read_csv(file_path)
        
        # --- EXPERT STEP: DATA CLEANING ---
        # Column names ko SQL friendly banana (Lowercase aur No Spaces)
        df.columns = [c.lower().replace(' ', '_').replace('-', '_').strip() for c in df.columns]
        
        print(f"--- Step 2: Uploading {len(df)} rows to PostgreSQL... ---")
        
        # Data ko Table mein bhejna
        # if_exists='replace' ka matlab hai agar table pehle se hai toh use update kar do
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print(f"✅ MISSION ACCOMPLISHED: '{table_name}' table database mein ban gayi hai!")
        print("Ab aapka AI Agent is data ko read karne ke liye taiyar hai.")
        
    except Exception as e:
        print(f"❌ OOPS! Kuch gadbad ho gayi: {e}")

if __name__ == "__main__":
    start_ingestion()