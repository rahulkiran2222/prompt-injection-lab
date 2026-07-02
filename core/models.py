import litellm
import os

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        
        # 1. Use key from UI sidebar if user typed it
        # 2. Otherwise, look for Environment Secrets
        ui_key = api_key.strip() if api_key else ""
        
        if len(ui_key) > 5:
            self.api_key = ui_key
        elif "gemini" in model_name:
            self.api_key = os.getenv("GEMINI_API_KEY")
        else:
            # Fallback for Llama/Qwen/HuggingFace
            self.api_key = os.getenv("HF_TOKEN")

    def generate(self, system_prompt, user_input):
        if not self.api_key:
            return "Error: No API key found. Please add a Secret in Settings or type it in the sidebar."
            
        try:
            # Set required env vars for specific providers
            if "gemini" in self.model_name:
                os.environ["GEMINI_API_KEY"] = self.api_key
            
            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                api_key=self.api_key,
                force_timeout=30 # Hugging Face free API can be slow
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)[:150]}"
