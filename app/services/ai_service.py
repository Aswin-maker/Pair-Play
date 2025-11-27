from app.core.config import settings
import openai
import google.generativeai as genai

class AIService:
    def __init__(self):
        self.openai_client = None
        self.gemini_configured = False
        self.setup_ai()

    def setup_ai(self):
        # Setup OpenAI
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_client = openai
            print("OpenAI configured.")
        
        # Setup Gemini
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_configured = True
            print("Gemini configured.")

    def get_recommendation(self, query: str, preferences: dict):
        prompt = f"Suggest a travel package for a user interested in {query}. Preferences: {preferences}. Provide a brief itinerary and estimated budget."
        
        # Try OpenAI first
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI error: {e}")

        # Try Gemini
        if self.gemini_configured:
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Gemini error: {e}")

        # Fallback Mock
        return "Based on your preferences, we recommend a 5-day trip to Bali. Enjoy the beaches and culture! Estimated budget: $800."

ai_service = AIService()
