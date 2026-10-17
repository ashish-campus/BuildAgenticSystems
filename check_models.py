import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env file")
    exit()

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url).json()

print("\n--- Available Models for your API Key ---")
if "models" in response:
    for model in response["models"]:
        # Only show models that support text generation
        if "generateContent" in model.get("supportedGenerationMethods", []):
            print(model["name"].replace("models/", ""))
else:
    print("Error fetching models:", response)
print("-----------------------------------------\n")