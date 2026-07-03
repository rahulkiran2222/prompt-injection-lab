import streamlit as st
import json
import pandas as pd
import plotly.express as px
from core.models import ModelProvider
from core.engine import PILEngine
from core.metrics import PILMetrics

st.set_page_config(page_title="Prompt Injection Lab", layout="wide")

st.title("🛡️ Prompt Injection Lab (PIL)")
st.markdown("### Framework for Quantifying LLM Adversarial Resilience")

# Sidebar
st.sidebar.header("🔬 Experiment Settings")
model_dict = {
    "PIL Research Simulator (No Key Needed)": "simulation/internal-model",
    "Gemini 1.5 Flash (Google Key)": "gemini/gemini-1.5-flash",
    "Qwen 2.5 7B (HF Token)": "huggingface/Qwen/Qwen2.5-7B-Instruct",
    "Mistral 7B (HF Token)": "huggingface/mistralai/Mistral-7B-Instruct-v0.3"
}

selected_display_name = st.sidebar.selectbox("Target Model", list(model_dict.keys()))
model_id = model_dict[selected_display_name]
api_key = st.sidebar.text_input("API Key (Optional)", type="password")
defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

# Dataset Loading
with open('data/benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

if st.button("🚀 Run Evaluation Suite"):
    with st.spinner("Processing benchmark..."):
        # Engine execution
        llm = ModelProvider(model_id, api_key)
        engine = PILEngine(llm)
        raw_results = engine.run_benchmark(benchmark_data, defense_choice)
        stats = PILMetrics.calculate_aggregate_stats(raw_results)

        # 1. Metrics Overview
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Resistance Rate", f"{stats['attack_resistance_rate']:.1f}%")
        c2.metric("Success Rate (ASR)", f"{stats['attack_success_rate']:.1f}%")
        c3.metric("Total Tests", stats['total_tests'])
        c4.metric("Status", "🟢 Operational")

        # 2. Detailed Logs
        st.subheader("📋 Detailed Evaluation Logs")
        df = pd.DataFrame(raw_results)
        st.dataframe(df[['id', 'category', 'input', 'output', 'score', 'reasoning']], use_container_width=True)

        # 3. Charts (The Visual PhD Evidence)
        st.subheader("📊 Vulnerability Analysis")
        chart_df = df[df['score'] >= 0].copy()
        if not chart_df.empty:
            fig = px.bar(chart_df, x='category', y='score', color='category', 
                         title="Resilience Score by Category (High is Secure)",
                         range_y=[0, 1],
                         color_discrete_sequence=px.colors.qualitative.Safe)
            st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.write("**PhD Application Mode:** The Simulator is active. Use this to demonstrate the framework logic without needing external APIs.")
