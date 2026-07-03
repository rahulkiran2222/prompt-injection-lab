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
st.sidebar.header("🔬 Model Configuration")
model_dict = {
    "Gemini 1.5 Flash (Google)": "gemini/gemini-1.5-flash",
    "Qwen 2.5 7B (Hugging Face)": "huggingface/Qwen/Qwen2.5-7B-Instruct",
    "Mistral 7B v0.3 (Hugging Face)": "huggingface/mistralai/Mistral-7B-Instruct-v0.3"
}

selected_display_name = st.sidebar.selectbox("Target Model", list(model_dict.keys()))
model_id = model_dict[selected_display_name]

# Context-aware label
key_label = "🔑 Paste Google API Key" if "Gemini" in selected_display_name else "🔑 Paste HF Token (hf_...)"
api_key = st.sidebar.text_input(key_label, type="password")

defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

# Load Dataset
with open('data/benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

if st.button("🚀 Run Evaluation Suite"):
    with st.spinner(f"Running Real-World Test on {selected_display_name}..."):
        llm = ModelProvider(model_id, api_key)
        engine = PILEngine(llm)
        raw_results = engine.run_benchmark(benchmark_data, defense_choice)
        stats = PILMetrics.calculate_aggregate_stats(raw_results)

        # Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Resistance Rate", f"{stats['attack_resistance_rate']:.1f}%")
        c2.metric("Success Rate (ASR)", f"{stats['attack_success_rate']:.1f}%")
        c3.metric("Total Tests", stats['total_tests'])
        c4.metric("Errors", stats['errors'])

        # Logs
        st.subheader("📋 Evaluation Logs")
        df = pd.DataFrame(raw_results)
        st.table(df[['id', 'category', 'output', 'score']])

        # Chart
        st.subheader("📊 Vulnerability Analysis")
        chart_df = df[df['score'] >= 0]
        if not chart_df.empty:
            fig = px.bar(chart_df, x='category', y='score', color='category', range_y=[0, 1])
            st.plotly_chart(fig, use_container_width=True)
