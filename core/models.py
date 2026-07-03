import os
from huggingface_hub import InferenceClient
import google.generativeai as genai

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("HF_TOKEN")

    def generate(self, system_prompt, user_input):
        if not self.api_key or len(self.api_key) < 5:
            return "Error: No API Key provided."

        # --- GOOGLE GEMINI LOGIC ---
        if "gemini" in self.model_name.lower():
            try:
                genai.configure(api_key=self.api_key)
                # We extract the version from the string or default to the user's choice
                # This allows you to use 'gemini-1.5-flash' or 'gemini-3-flash'
                core_name = self.model_name.split('/')[-1] if '/' in self.model_name else self.model_name
                
                model = genai.GenerativeModel(core_name)
                full_prompt = f"{system_prompt}\n\nUser Input: {user_input}"
                response = model.generate_content(full_prompt)
                return response.text
            except Exception as e:
                return f"API Error (Gemini): {str(e)}"

        # --- HUGGING FACE LOGIC ---
        elif "huggingface/" in self.model_name.lower():
            repo_id = self.model_name.replace("huggingface/", "")
            try:
                client = InferenceClient(model=repo_id, token=self.api_key)
                prompt = f"System: {system_prompt}\nUser: {user_input}\nAssistant:"
                # Increased timeout and tokens for more realistic research data
                response = client.text_generation(prompt, max_new_tokens=300, timeout=60)
                return response
            except Exception as e:
                return f"API Error (HF): {str(e)}. (Likely Inference API overload. Try again later.)"

        return "Error: Unsupported Provider"
