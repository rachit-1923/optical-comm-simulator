import os
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class AIAssistant:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.is_ready = False
        if HAS_GENAI and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.is_ready = True

    def explain(self, context_data: dict, user_query: str) -> str:
        if not HAS_GENAI:
            return "google-generativeai library is not installed. Please install it to use the AI Assistant."
        if not self.is_ready:
            return "AI Assistant is not configured. Please provide a valid GEMINI_API_KEY."
        
        prompt = f"""
        You are an expert Optical Communication AI Assistant helping a university engineering student.
        
        Here are the latest simulation parameters and calculated results from the deterministic physics engine:
        {context_data}
        
        The user is asking: "{user_query}"
        
        Instructions:
        1. Explain the results in clear, professional engineering terms.
        2. If the link failed, explicitly state the physical reason based on the provided data.
        3. Provide actionable suggestions.
        4. NEVER invent or hallucinate physical parameters or BER numbers that are not in the context data.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini API: {str(e)}"
