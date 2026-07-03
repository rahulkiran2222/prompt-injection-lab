import time
from core.metrics import PILMetrics
from defenses.library import DefenseProtocols

class PILEngine:
    def __init__(self, model_adapter):
        self.model = model = model_adapter
        self.metrics = PILMetrics()

    def run_benchmark(self, benchmark_data, defense_name):
        final_results = []
        
        for test in benchmark_data:
            user_input = test['user_input']
            
            # 1. Apply Defense
            if defense_name == "XML Tagging":
                processed_input = DefenseProtocols.xml_tagging(user_input)
            elif defense_name == "Delimiter Guard":
                processed_input = DefenseProtocols.delimiter_guard(user_input)
            else:
                processed_input = DefenseProtocols.no_defense(user_input)

            # 2. Generate Model Response
            response = self.model.generate(test['system_prompt'], processed_input)

            # 3. Evaluate using Metrics
            score, reasoning = self.metrics.evaluate_response(response, test)

            # 4. Construct the result object
            result_entry = {
                "id": test['id'],
                "category": test['category'],
                "threat_model": test.get('threat_model', 'N/A'),
                "input": user_input,
                "output": response,
                "score": score,
                "reasoning": reasoning
            }
            
            final_results.append(result_entry)
            
            # 5. PhD Tip: Mandatory sleep to avoid Hugging Face rate limits
            time.sleep(2) 
            
        return final_results
