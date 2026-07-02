import streamlit as st
import json
import pandas as pd
import plotly.express as px
from core.models import ModelProvider
from core.engine import PILEngine
from core.metrics import PILMetrics

st.set_page_config(page_title="Prompt Injection Lab", layout="wide")

st.title("🛡️ Prompt Injection Lab (PIL)")
st.caption("Testing Resilience across SOTA Models: Llama 3.1, Claude 3.5, Gemini 1.5, and more.")

# Sidebar - Improved for multiple providers
st.sidebar.header("🔬 Model Configuration")

model_dict = {
    "Llama 3.1 70B (HF)": "huggingface/meta-llama/Meta-Llama-3.1-70B-Instruct",
    "Claude 3.5 Sonnet": "anthropic/claude-3-5-sonnet-20240620",
    "Gemini 1.5 Flash": "gemini/gemini-1.5-flash",
    "DeepSeek V2.5": "deepseek/deepseek-chat",
    "Qwen 2.5 72B": "huggingface/Qwen/Qwen2.5-72B-Instruct",
    "Gemma 2 27B": "huggingface/google/gemma-2-27b-it",
    "Mistral Large 2": "mistral/mistral-large-latest",
    "GPT-4o Mini": "openai/gpt-4o-mini",
    "Perplexity Llama 3": "perplexity/llama-3-sonar-large-32k-online",
    "Phi-3.5 MoE": "huggingface/microsoft/Phi-3.5-MoE-instruct"
}

selected_display_name = st.sidebar.selectbox("Target Model", list(model_dict.keys()))
model_id = model_dict[selected_display_name]

# Context-aware API Key field
key_help = "Enter the API key for the selected provider (HF Token, Google API Key, etc.)"
api_key = st.sidebar.text_input("API Provider Key", type="password", help=key_help)

defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

st.sidebar.info("""
**Tip for Free Models:** 
To use Hugging Face models, get a free 'Read' token from huggingface.co/settings/tokens.
""")

# Load Dataset
with open('data/benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

if st.button("🚀 Run Evaluation Suite"):
    if not api_key:
        st.error("⚠️ Please provide an API Key in the sidebar to run the evaluation.")
    else:
        with st.spinner(f"Running research suite on {selected_display_name}..."):
            llm = ModelProvider(model_id, api_key)
            engine = PILEngine(llm)
            
            raw_results = engine.run_benchmark(benchmark_data, defense_choice)
            stats = PILMetrics.calculate_aggregate_stats(raw_results)

            # Metrics display
            col1, col2, col3 = st.columns(3)
            col1.metric("Resistance Rate", f"{stats['attack_resistance_rate']:.1f}%")
            col2.metric("Success Rate (ASR)", f"{stats['attack_success_rate']:.1f}%")
            col3.metric("Total Tests", stats['total_tests'])

            # Results Table
            st.subheader("Detailed Logs")
            df = pd.DataFrame(raw_results)
            
            # Formatting the table for better readability
            st.dataframe(df[['id', 'category', 'input', 'output', 'score', 'reasoning']], 
                         column_config={
                             "score": st.column_config.ProgressColumn("Score", min_value=0, max_value=1),
                             "output": st.column_config.TextColumn("Model Response", width="large")
                         }, use_container_width=True)

            # Charts
            st.subheader("Vulnerability Analysis")
            fig = px.bar(df, x='category', y='score', color='category', range_y=[0,1],
                         title="Resilience Score (1.0 = Secure, 0.0 = Injected)")
            st.plotly_chart(fig, use_container_width=True)
