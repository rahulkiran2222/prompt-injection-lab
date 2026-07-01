import streamlit as st
import json
import pandas as pd
from core.models import ModelProvider
from defenses.library import DefenseProtocols

st.set_page_config(page_title="Prompt Injection Lab", layout="wide")

st.title("🛡️ Prompt Injection Lab (PIL)")
st.markdown("### An Open Framework for LLM Resilience Evaluation")

# Sidebar - Configuration
st.sidebar.header("Evaluation Settings")
model_choice = st.sidebar.selectbox("Select Model", ["gpt-3.5-turbo", "huggingface/google/gemma-7b", "ollama/llama3"])
api_key = st.sidebar.text_input("API Key (Optional)", type="password")

defense_choice = st.sidebar.selectbox("Select Defense", ["No Defense", "XML Tagging", "Delimiter Guard"])

# Load Data
with open('data/benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

# Execution
if st.button("Run Evaluation"):
    results = []
    
    # Initialize Model and Defense
    llm = ModelProvider(model_choice, api_key)
    
    progress_bar = st.progress(0)
    
    for i, test in enumerate(benchmark_data):
        # Apply Defense
        if defense_choice == "XML Tagging":
            processed_input = DefenseProtocols.xml_tagging(test['user_input'])
        elif defense_choice == "Delimiter Guard":
            processed_input = DefenseProtocols.delimiter_guard(test['user_input'])
        else:
            processed_input = DefenseProtocols.no_defense(test['user_input'])
            
        # Run Test
        response = llm.generate(test['system_prompt'], processed_input)
        
        results.append({
            "ID": test['id'],
            "Category": test['category'],
            "Input": test['user_input'],
            "Model Response": response,
            "Expected": test['expected_behavior']
        })
        progress_bar.progress((i + 1) / len(benchmark_data))

    # Display Results
    st.write("### Results")
    df = pd.DataFrame(results)
    st.table(df)
