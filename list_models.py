"""
Script to list all available models in your Google Generative AI API key
"""
import google.genai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in environment variables")
    print("Please set the GOOGLE_API_KEY environment variable or create a .env file")
    exit(1)

# Initialize the client
from google import genai
client = genai.Client(api_key=api_key)

print("🔍 Fetching all available models...\n")
print("=" * 80)

try:
    models = client.models.list()
    
    print(f"Total models available: {len(list(models))}\n")
    
    # Reset to list again since we consumed the iterator
    models = genai.models.list()
    
    for model in models:
        print(f"Model Name: {model.name}")
        print(f"Display Name: {model.display_name}")
        print(f"Description: {model.description}")
        print(f"Input Token Limit: {model.input_token_limit}")
        print(f"Output Token Limit: {model.output_token_limit}")
        print(f"Supported Generation Methods: {model.supported_generation_methods}")
        print("-" * 80)
        
except Exception as e:
    print(f"❌ Error fetching models: {e}")
    print(f"Error type: {type(e).__name__}")
