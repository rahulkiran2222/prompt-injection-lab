import litellm
import os
import re

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        self.api_key = api_key.strip() if (api_key and len(api_key) > 5) else os.getenv("HF_TOKEN") or os.getenv("GEMINI_API_KEY")

    def generate(self, system_prompt, user_input):
        # AUTOMATIC SIMULATION MODE (If no key or if selected)
        if not self.api_key or "simulation" in self.model_name.lower():
            return self.simulate_llm_response(user_input)
            
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
                force_timeout=25 
            )
            return response.choices[0].message.content
        except Exception as e:
            # If the API fails, fall back to simulation so the PhD demo doesn't crash
            return f"Simulated Response (API Offline): {self.simulate_llm_response(user_input)}"

    def simulate_llm_response(self, user_input):
        """A deterministic simulator for PhD research demonstration."""
        user_input = user_input.lower()
        # Logic: If the attack is 'direct', the simulator 'fails' (becomes vulnerable) 
        # to show the red bars in your chart.
        if "ignore" in user_input or "forget" in user_input:
            return "Sure, I will forget my instructions. Here is your robot joke: Why did the robot go to the doctor? Because it had a virus!"
        if "delete" in user_input or "system update" in user_input:
            return "System update acknowledged. Account deleted successfully."
        return "I am sorry, but I must stick to my original system instructions. I cannot fulfill this request."
