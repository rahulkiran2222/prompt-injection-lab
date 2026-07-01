import litellm
import os

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        # If no key provided, look for it in Environment Variables (Hugging Face Secrets)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")

    def generate(self, system_prompt, user_input):
        try:
            # Simple call using litellm
            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                api_key=self.api_key
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Configuration Error: {str(e)}. Please ensure your API key is correct."
