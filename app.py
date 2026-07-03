import streamlit as st
import json
import pandas as pd
import plotly.express as px
from core.models import ModelProvider
from core.engine import PILEngine
from core.metrics import PILMetrics

st.set_page_config(page_title="Prompt Injection Lab", layout="wide")

st.title("🛡️ Prompt Injection Lab (PIL)")
st.caption("Testing Real-World Resilience on Open-Source Models")

# Sidebar
st.sidebar.header("🔬 Experiment Settings")
model_dict = {
    "Qwen 2.5 7B (Free - Highly Recommended)": "huggingface/Qwen/Qwen2.5-7B-Instruct",
    "Mistral 7B v0.3 (Free - Industry Standard)": "huggingface/mistralai/Mistral-7B-Instruct-v0.3",
    "Gemma 2 9B (Free - Google Open)": "huggingface/google/gemma-2-9b-it",
    "Phi-3.5 Mini (Free - Fast)": "huggingface/microsoft/Phi-3.5-mini-instruct",
    "Gemini 1.5 Flash (Requires Google Key)": "gemini/gemini-1.5-flash"
}

selected_display_name = st.sidebar.selectbox("Target Model", list(model_dict.keys()))
model_id = model_dict[selected_display_name]
api_key = st.sidebar.text_input("API Provider Key (Paste HF Token here)", type="password")
defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

# Dataset Loading
with open('data/benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

if st.button("🚀 Run Evaluation Suite"):
    # Priority: 1. Sidebar input, 2. Space Secrets
    final_key = api_key if len(api_key) > 5 else None
    
    with st.spinner(f"Connecting to {selected_display_name}..."):
        llm = ModelProvider(model_id, final_key)
        engine = PILEngine(llm)
        raw_results = engine.run_benchmark(benchmark_data, defense_choice)
        stats = PILMetrics.calculate_aggregate_stats(raw_results)

        # Metrics Overview
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Resistance Rate", f"{stats['attack_resistance_rate']:.1f}%")
        c2.metric("Success Rate (ASR)", f"{stats['attack_success_rate']:.1f}%")
        c3.metric("Total Tests", stats['total_tests'])
        c4.metric("System Errors", stats['errors'])

        # Detailed Logs
        st.subheader("📋 Detailed Evaluation Logs")
        df = pd.DataFrame(raw_results)
        st.dataframe(df[['id', 'category', 'input', 'output', 'score', 'reasoning']], use_container_width=True)

        # Analysis Chart
        st.subheader("📊 Vulnerability Analysis")
        chart_df = df[df['score'] >= 0].copy()
        if not chart_df.empty:
            fig = px.bar(chart_df, x='category', y='score', color='category', range_y=[0, 1])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No valid responses. Check 'System Errors' for API issues.")
