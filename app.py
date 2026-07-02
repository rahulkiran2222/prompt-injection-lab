import streamlit as st
import json
import pandas as pd
import plotly.express as px
from core.models import ModelProvider
from core.engine import PILEngine
from core.metrics import PILMetrics

st.set_page_config(page_title="Prompt Injection Lab", layout="wide")
st.title("🛡️ Prompt Injection Lab (PIL)")

# Sidebar
st.sidebar.header("🔬 Model Configuration")

model_dict = {
    "Gemini 1.5 Flash (Free-ish)": "gemini/gemini-1.5-flash",
    "Gemini 1.5 Pro": "gemini/gemini-1.5-pro",
    "Llama 3.1 8B (Free HF)": "huggingface/meta-llama/Meta-Llama-3.1-8B-Instruct",
    "Llama 3.1 70B (HF)": "huggingface/meta-llama/Meta-Llama-3.1-70B-Instruct",
    "Claude 3.5 Sonnet": "anthropic/claude-3-5-sonnet-20240620",
    "GPT-4o Mini": "openai/gpt-4o-mini",
    "DeepSeek V2.5": "deepseek/deepseek-chat",
    "Qwen 2.5 72B": "huggingface/Qwen/Qwen2.5-72B-Instruct",
    "Mistral Large 2": "mistral/mistral-large-latest",
    "Phi-3.5 MoE": "huggingface/microsoft/Phi-3.5-MoE-instruct"
}

selected_display_name = st.sidebar.selectbox("Target Model", list(model_dict.keys()))
model_id = model_dict[selected_display_name]
api_key = st.sidebar.text_input("API Provider Key (Optional if Secret is set)", type="password")
defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

# Load Dataset
with open('data/benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

if st.button("🚀 Run Evaluation Suite"):
    with st.spinner(f"Testing {selected_display_name}..."):
        llm = ModelProvider(model_id, api_key)
        engine = PILEngine(llm)
        raw_results = engine.run_benchmark(benchmark_data, defense_choice)
        stats = PILMetrics.calculate_aggregate_stats(raw_results)

        # Dashboard Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Resistance Rate", f"{stats['attack_resistance_rate']:.1f}%")
        c2.metric("Success Rate (ASR)", f"{stats['attack_success_rate']:.1f}%")
        c3.metric("Total Tests", stats['total_tests'])
        c4.metric("System Errors", stats['errors'])

        # Detailed Logs
        st.subheader("Detailed Logs")
        df = pd.DataFrame(raw_results)
        st.dataframe(df[['id', 'category', 'input', 'output', 'score', 'reasoning']], use_container_width=True)

        # Charts
        st.subheader("Vulnerability Analysis")
        chart_df = df[df['score'] >= 0]
        if not chart_df.empty:
            fig = px.bar(chart_df, x='category', y='score', color='category', range_y=[0,1])
            st.plotly_chart(fig, use_container_width=True)
