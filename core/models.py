import litellm
import os

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        # Use key from sidebar if provided, else use Space Secrets
        self.api_key = api_key or os.getenv("HF_TOKEN") or os.getenv("GEMINI_API_KEY")

    def generate(self, system_prompt, user_input):
        if not self.api_key:
            return "Error: No API key provided. Please paste your token in the sidebar."

        try:
            # Set environment variables for litellm
            if "gemini" in self.model_name:
                os.environ["GEMINI_API_KEY"] = self.api_key
            else:
                os.environ["HUGGINGFACE_API_KEY"] = self.api_key

            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                api_key=self.api_key,
                force_timeout=35
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
