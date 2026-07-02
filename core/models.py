import litellm
import os

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        
        # 1. Look for key in UI sidebar
        # 2. Look for key in HF Secrets
        ui_key = api_key.strip() if (api_key and len(api_key) > 5) else None
        
        if ui_key:
            self.api_key = ui_key
        elif "gemini" in model_name:
            self.api_key = os.getenv("GEMINI_API_KEY")
        else:
            self.api_key = os.getenv("HF_TOKEN")

    def generate(self, system_prompt, user_input):
        if not self.api_key:
            return "Error: No API Key found. Please add HF_TOKEN or GEMINI_API_KEY to Space Secrets."
            
        try:
            # FORCE environment variables (This is what LiteLLM needs)
            if "gemini" in self.model_name:
                os.environ["GEMINI_API_KEY"] = self.api_key
                os.environ["GOOGLE_API_KEY"] = self.api_key
            else:
                os.environ["HUGGINGFACE_API_KEY"] = self.api_key

            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                # We pass it both ways to be 100% sure
                api_key=self.api_key,
                force_timeout=40 
            )
            return response.choices[0].message.content
        except Exception as e:
            # If the free API is down, this will tell us
            return f"Error: {str(e)}"
