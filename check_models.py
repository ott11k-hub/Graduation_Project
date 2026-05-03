import google.generativeai as genai # type: ignore
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyCZq9UNfdJ1qyO0tr_UHNwEbBcPDQRP3LA"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("Available Gemini Models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"-> {m.name}")