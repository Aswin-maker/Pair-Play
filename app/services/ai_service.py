import os
from app.config import settings
import google.generativeai as genai

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

async def recommend_packages(prompt: str, packages_list: list):
    # Construct a prompt that includes packages
    full_prompt = f"User query: {prompt}\n\nAvailable packages:\n"
    for p in packages_list:
        full_prompt += f"- {p['package_name']} (loc: {p.get('location')}, days: {p.get('days')}, budget: {p.get('budget')})\n"
    full_prompt += "\nReturn best matches with short reasons."

    if settings.GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"
    else:
        return "No Gemini API key configured."

async def suggest_packages(user_text: str):
    prompt = f"Suggest best travel packages for: {user_text}. Return concise results."
    
    if settings.GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"
    else:
        return "No Gemini API key configured."
