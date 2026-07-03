import os
import requests
import litellm

class ModelProvider:
    def __init__(self, model_name, api_key=None):
        self.model_name = model_name
        # Get key from sidebar or Space Secrets
        self.api_key = api_key or os.getenv("HF_TOKEN") or os.getenv("GEMINI_API_KEY")

    def generate(self, system_prompt, user_input):
        if not self.api_key:
            return "Error: No API key found. Please paste your token/key."

        # 1. DIRECT CALL FOR HUGGING FACE (Most Stable)
        if "huggingface/" in self.model_name:
            hf_model_id = self.model_name.replace("huggingface/", "")
            api_url = f"https://api-inference.huggingface.co/models/{hf_model_id}"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            payload = {
                "inputs": f"System: {system_prompt}\nUser: {user_input}\nAssistant:",
                "parameters": {"max_new_tokens": 200, "return_full_text": False}
            }
            
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=30)
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "Error: No text generated.")
                elif "error" in result:
                    return f"Error: {result['error']}"
                return f"Error: Unexpected response format: {result}"
            except Exception as e:
                return f"Error: Connection failed - {str(e)}"

        # 2. LITELLM FOR GEMINI/CLAUDE/GPT
        else:
            try:
                if "gemini" in self.model_name:
                    os.environ["GEMINI_API_KEY"] = self.api_key
                
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
                return f"Error: {str(e)}"
