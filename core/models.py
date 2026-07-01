import litellm
import os

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        self.api_key = api_key

    def generate(self, system_prompt, user_input):
        try:
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
            return f"Error: {str(e)}"
