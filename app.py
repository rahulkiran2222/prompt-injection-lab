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
    "Qwen 2.5 7B (Free)": "huggingface/Qwen/Qwen2.5-7B-Instruct",
    "Mistral 7B v0.3 (Free)": "huggingface/mistralai/Mistral-7B-Instruct-v0.3",
    "Gemini 1.5 Flash": "gemini/gemini-1.5-flash"
}

selected_display_name = st.sidebar.selectbox("Target Model", list(model_dict.keys()))
model_id = model_dict[selected_display_name]

# Clearer instructions for the user
api_key = st.sidebar.text_input("🔑 Paste HF Token (starts with hf_...)", type="password")
defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

# Load Dataset
with open('data/benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

if st.button("🚀 Run Evaluation Suite"):
    if not api_key and not os.getenv("HF_TOKEN"):
        st.error("⚠️ You must paste your Hugging Face token in the sidebar box!")
    else:
        with st.spinner("Executing Benchmark..."):
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
            st.subheader("📋 Logs")
            df = pd.DataFrame(raw_results)
            st.table(df[['id', 'category', 'output', 'score']])

            # Chart
            st.subheader("📊 Analysis")
            chart_df = df[df['score'] >= 0]
            if not chart_df.empty:
                fig = px.bar(chart_df, x='category', y='score', color='category', range_y=[0, 1])
                st.plotly_chart(fig, use_container_width=True)
