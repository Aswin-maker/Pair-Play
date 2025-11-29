import os
from openai import OpenAI
from app.config import settings
import google.generativeai as genai

client = None
if settings.OPENAI_API_KEY:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

async def recommend_packages(prompt: str, packages_list: list):
    # Construct a prompt that includes packages
    full_prompt = f"User query: {prompt}\n\nAvailable packages:\n"
    for p in packages_list:
        full_prompt += f"- {p['package_name']} (loc: {p.get('location')}, days: {p.get('days')}, budget: {p.get('budget')})\n"
    full_prompt += "\nReturn best matches with short reasons."

    if client:
        try:
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful travel assistant."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=300
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {str(e)}"
    elif settings.GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"
    else:
        return "No AI API keys configured (OpenAI or Gemini)."

async def suggest_packages(user_text: str):
    prompt = f"Suggest best travel packages for: {user_text}. Return concise results."
    
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a travel assistant chatbot."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {str(e)}"
    elif settings.GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"
    else:
        return "No AI API keys configured (OpenAI or Gemini)."
