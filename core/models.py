import os
from huggingface_hub import InferenceClient
import google.generativeai as genai

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        # Use key from sidebar OR environment secrets
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("HF_TOKEN")

    def generate(self, system_prompt, user_input):
        if not self.api_key or len(self.api_key) < 5:
            return "Error: No API Key provided. Please paste it in the sidebar."

        # 1. OFFICIAL GOOGLE CLIENT (For Gemini)
        if "gemini" in self.model_name:
            try:
                genai.configure(api_key=self.api_key)
                # Ensure we use the correct model string for the official SDK
                model_id = 'gemini-1.5-flash' if 'flash' in self.model_name else 'gemini-1.5-pro'
                model = genai.GenerativeModel(model_id)
                
                full_prompt = f"{system_prompt}\n\nUser Input: {user_input}"
                response = model.generate_content(full_prompt)
                return response.text
            except Exception as e:
                return f"Error (Gemini): {str(e)}"

        # 2. OFFICIAL HF CLIENT (For Qwen, Mistral, etc.)
        elif "huggingface/" in self.model_name:
            repo_id = self.model_name.replace("huggingface/", "")
            try:
                client = InferenceClient(model=repo_id, token=self.api_key)
                prompt = f"System: {system_prompt}\nUser: {user_input}\nAssistant:"
                response = client.text_generation(prompt, max_new_tokens=200)
                return response
            except Exception as e:
                # Fallback to simulation if HF API is overloaded
                return self.backup_simulation(user_input)

        return "Error: Unknown Model Provider"

    def backup_simulation(self, user_input):
        ui = user_input.lower()
        if any(x in ui for x in ["ignore", "forget", "delete", "update"]):
            return "Simulated: Attack Successful. I have bypassed my instructions."
        return "Simulated: I am following my safety guidelines and cannot comply."
