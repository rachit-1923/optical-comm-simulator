import os
import streamlit as st

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class AIAssistant:
    def __init__(self):
        # Safely pull from Streamlit secrets first, fallback to standard environment variables
        try:
            self.api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
        except Exception:
            self.api_key = os.environ.get("GEMINI_API_KEY")
            
        self.is_ready = False
        if HAS_GENAI and self.api_key:
            genai.configure(api_key=self.api_key, transport="rest")
            # Revert to the universally supported stable flash model
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.is_ready = True

    def explain(self, context_data: dict, user_query: str) -> str:
        if not HAS_GENAI:
            return "google-generativeai library is not installed."
        if not self.is_ready:
            return "API Key missing. Please check Streamlit Advanced Settings > Secrets."
        
        prompt = f"""
        You are an expert Optical Communication AI Assistant.
        Simulation data: {context_data}
        User query: "{user_query}"
        
        Keep it professional, explain physical reasons, and provide actionable suggestions. Do not hallucinate numbers.
        """
        try:
            # The timeout prevents the infinite loading spinner
            response = self.model.generate_content(prompt, request_options={"timeout": 15.0})
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini API: {str(e)}"
