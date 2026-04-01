import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Test connection
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Say 'Connection successful' in exactly 2 words.")
    print("✅ Gemini API Working!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")