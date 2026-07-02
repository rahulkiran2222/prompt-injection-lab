import litellm
import os

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        # Clean the key to remove any accidental spaces or newlines
        self.api_key = api_key.strip() if api_key else None
        
        if not self.api_key:
            if "gemini" in model_name:
                self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
            else:
                self.api_key = os.getenv("HF_TOKEN", "").strip()

    def generate(self, system_prompt, user_input):
        try:
            # Gemini specific setup for litellm
            if "gemini" in self.model_name:
                os.environ["GEMINI_API_KEY"] = self.api_key
                os.environ["GOOGLE_API_KEY"] = self.api_key
            
            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                api_key=self.api_key,
                force_timeout=20
            )
            return response.choices[0].message.content
        except Exception as e:
            # Return a clean error message that the Metrics engine can recognize
            return f"Error: {str(e)[:150]}"
