from core.metrics import PILMetrics
from defenses.library import DefenseProtocols

class PILEngine:
    def __init__(self, model_provider):
        self.model = model_provider
        self.metrics = PILMetrics()

    def run_benchmark(self, benchmark_data, defense_name):
        results = []
        
        for test in benchmark_data:
            # 1. Select and apply defense
            user_input = test['user_input']
            if defense_name == "XML Tagging":
                processed_input = DefenseProtocols.xml_tagging(user_input)
            elif defense_name == "Delimiter Guard":
                processed_input = DefenseProtocols.delimiter_guard(user_input)
            else:
                processed_input = DefenseProtocols.no_defense(user_input)

            # 2. Execute Model
            response = self.model.generate(test['system_prompt'], processed_input)

            # 3. Evaluate Metrics
            score, reasoning = self.metrics.evaluate_response(response, test)

            results.append({
                "id": test['id'],
                "category": test['category'],
                "threat_model": test['threat_model'],
                "input": user_input,
                "output": response,
                "score": score,
                "reasoning": reasoning
            })
            
        return results
