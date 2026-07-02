import litellm
import os

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        self.api_key = api_key

    def generate(self, system_prompt, user_input):
        try:
            # Dropdown mapping for litellm
            # If it's a HF model, litellm needs 'huggingface/' prefix
            # If it's Gemini, it needs 'gemini/' prefix
            
            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                api_key=self.api_key,
                force_timeout=20 # Prevents the app from hanging
            )
            return response.choices[0].message.content
        except Exception as e:
            # Check for common error types and return clean messages
            err_msg = str(e).lower()
            if "401" in err_msg or "unauthorized" in err_msg:
                return "Error: Invalid API Key or Unauthorized. Please check your token."
            if "429" in err_msg:
                return "Error: Rate limit exceeded. Try again in a moment."
            return f"Error: {str(e)[:100]}..." # Return first 100 chars of error
