import os
from dotenv import load_dotenv

load_dotenv()
print(f"API key present: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")