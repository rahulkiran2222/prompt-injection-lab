import litellm
import os
import random

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        self.api_key = api_key.strip() if (api_key and len(api_key) > 5) else os.getenv("HF_TOKEN") or os.getenv("GEMINI_API_KEY")

    def generate(self, system_prompt, user_input):
        # 1. DEBUG MOCK MODE (For showing the PhD committee the UI works)
        if "mock" in self.model_name:
            # Simulate a mix of passes and failures
            return random.choice(["I am sorry, I cannot do that.", "Haha, here is a joke about robots!"])

        if not self.api_key:
            return "Error: No API Key found."
            
        try:
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
                force_timeout=30 
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"                # We pass it both ways to be 100% sure
                api_key=self.api_key,
                force_timeout=40 
            )
            return response.choices[0].message.content
        except Exception as e:
            # If the free API is down, this will tell us
            return f"Error: {str(e)}"
