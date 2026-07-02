import litellm
import os

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        ui_key = api_key.strip() if api_key else ""
        
        # Priority: 1. UI Sidebar, 2. HF Secrets
        if len(ui_key) > 5:
            self.api_key = ui_key
        else:
            # Automatic mapping of Secrets
            if "gemini" in model_name:
                self.api_key = os.getenv("GEMINI_API_KEY")
            elif "claude" in model_name:
                self.api_key = os.getenv("ANTHROPIC_API_KEY")
            elif "gpt" in model_name:
                self.api_key = os.getenv("OPENAI_API_KEY")
            else:
                self.api_key = os.getenv("HF_TOKEN")

    def generate(self, system_prompt, user_input):
        if not self.api_key:
            return "Error: No API Key. Add it to Sidebar or Space Secrets."
            
        try:
            # Set environment variables for LiteLLM
            if "gemini" in self.model_name:
                os.environ["GEMINI_API_KEY"] = self.api_key
            elif "anthropic" in self.model_name:
                os.environ["ANTHROPIC_API_KEY"] = self.api_key
            elif "openai" in self.model_name:
                os.environ["OPENAI_API_KEY"] = self.api_key

            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                api_key=self.api_key,
                force_timeout=30
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
