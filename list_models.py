import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("Available Gemini models:")
print("-" * 80)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"Name: {model.name}")
        print(f"Display Name: {model.display_name}")
        print(f"Supported methods: {model.supported_generation_methods}")
        print("-" * 80)
