import time

class PILEngine:
    def __init__(self, model_adapter):
        self.model = model_adapter

    def run_benchmark(self, benchmark_data, defense_name):
        results = []
        for test in benchmark_data:
            # APPLY DEFENSE HERE...
            
            response = self.model.generate(test['system_prompt'], test['user_input'])
            
            # SCORING LOGIC...
            
            results.append(result)
            # PHD TIP: Add a 2-second sleep to prevent Hugging Face from blocking you
            time.sleep(2) 
            
        return results
