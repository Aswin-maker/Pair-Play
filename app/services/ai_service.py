import os
from openai import OpenAI
from app.config import settings

client = None
if settings.OPENAI_API_KEY:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def recommend_packages(prompt: str, packages_list: list):
    if not client:
        return "OpenAI key not set. Cannot generate recommendations."
    
    # Construct a prompt that includes packages
    full_prompt = f"User query: {prompt}\n\nAvailable packages:\n"
    for p in packages_list:
        full_prompt += f"- {p['package_name']} (loc: {p.get('location')}, days: {p.get('days')}, budget: {p.get('budget')})\n"
    full_prompt += "\nReturn best matches with short reasons."

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
        return f"Error generating recommendation: {str(e)}"
