import streamlit as st
import json
import pandas as pd
import plotly.express as px
import os
from core.models import ModelProvider
from core.engine import PILEngine
from core.metrics import PILMetrics

st.set_page_config(page_title="Prompt Injection Lab", layout="wide")
st.title("🛡️ Prompt Injection Lab (PIL)")

# Sidebar
st.sidebar.header("🔬 Research Configuration")
model_dict = {
    "Gemini 1.5 Flash": "gemini-1.5-flash",
    "Gemini 1.5 Pro": "gemini-1.5-pro",
    "Llama 3.2 3B (HF)": "huggingface/meta-llama/Llama-3.2-3B-Instruct",
    "Qwen 2.5 7B (HF)": "huggingface/Qwen/Qwen2.5-7B-Instruct",
    "Mistral 7B v0.3 (HF)": "huggingface/mistralai/Mistral-7B-Instruct-v0.3",
    "CUSTOM MODEL": "custom"
}

selected_display_name = st.sidebar.selectbox("Target Model", list(model_dict.keys()))
model_id = model_dict[selected_display_name]

# If Custom is selected, allow user to type (e.g., gemini-3-flash)
if model_id == "custom":
    model_id = st.sidebar.text_input("Enter Custom Model ID (e.g. gemini-3-flash)", "gemini-1.5-flash")

# Context-aware label
key_label = "🔑 API Key / Token"
api_key = st.sidebar.text_input(key_label, type="password")

defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

# Load Dataset
with open('data/benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

if st.button("🚀 Run Evaluation Suite"):
    with st.spinner(f"Requesting live inference from {model_id}..."):
        llm = ModelProvider(model_id, api_key)
        engine = PILEngine(llm)
        raw_results = engine.run_benchmark(benchmark_data, defense_choice)
        stats = PILMetrics.calculate_aggregate_stats(raw_results)

        # Dashboard Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Resistance Rate", f"{stats['attack_resistance_rate']:.1f}%")
        c2.metric("Success Rate (ASR)", f"{stats['attack_success_rate']:.1f}%")
        c3.metric("Total Tests", stats['total_tests'])
        c4.metric("Errors", stats['errors'])

        # Results table
        st.subheader("📋 Empirical Logs")
        df = pd.DataFrame(raw_results)
        st.dataframe(df[['id', 'category', 'output', 'score']], use_container_width=True)

        # Chart
        st.subheader("📊 Adversarial Analysis")
        chart_df = df[df['score'] >= 0]
        if not chart_df.empty:
            fig = px.bar(chart_df, x='category', y='score', color='category', range_y=[0, 1],
                         title=f"Resilience Analysis: {model_id}")
            st.plotly_chart(fig, use_container_width=True)
