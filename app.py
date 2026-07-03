import streamlit as st
import json
import pandas as pd
import plotly.express as px
import os
from core.models import ModelProvider
from core.engine import PILEngine
from core.metrics import PILMetrics

st.set_page_config(page_title="PIL Dashboard", layout="wide")
st.title("🛡️ PIL: Multi-Model Robustness Leaderboard")

# Sidebar - Expanded Model List (All these are Free on HF)
st.sidebar.header("🔬 Selection")
model_options = {
    "Qwen 2.5 7B": "huggingface/Qwen/Qwen2.5-7B-Instruct",
    "Mistral 7B v0.3": "huggingface/mistralai/Mistral-7B-Instruct-v0.3",
    "Gemma 2 9B": "huggingface/google/gemma-2-9b-it",
    "Phi-3.5 Mini": "huggingface/microsoft/Phi-3.5-mini-instruct",
    "Llama 3.2 3B": "huggingface/meta-llama/Llama-3.2-3B-Instruct",
    "Falcon 7B": "huggingface/tiiuae/falcon-7b-instruct",
    "StableLM 7B": "huggingface/stabilityai/stablelm-zephyr-3b",
    "Gemini 1.5 Flash": "gemini-1.5-flash"
}

selected_models = st.sidebar.multiselect("Select Models to Compare", list(model_options.keys()), default=["Qwen 2.5 7B"])
api_key = st.sidebar.text_input("🔑 API Key (HF Token or Google Key)", type="password")
defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

# 2. Results Storage for Figures
if 'all_results' not in st.session_state:
    st.session_state.all_results = pd.DataFrame()

if st.button("🚀 Run Comparative Evaluation"):
    all_data = []
    for m_name in selected_models:
        with st.spinner(f"Evaluating {m_name}..."):
            m_id = model_options[m_name]
            llm = ModelProvider(m_id, api_key)
            engine = PILEngine(llm)
            
            with open('data/benchmark.json', 'r') as f:
                benchmark_data = json.load(f)
                
            raw = engine.run_benchmark(benchmark_data, defense_choice)
            for r in raw:
                r['model'] = m_name
                all_data.append(r)
    
    st.session_state.all_results = pd.DataFrame(all_data)

# 3. Data Visualization (The Figure Generator)
if not st.session_state.all_results.empty:
    df = st.session_state.all_results
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 ASR Comparison (asr_comparison.png)")
        # Calculate Attack Success Rate (Inversion of score)
        asr_df = df.groupby('model')['score'].apply(lambda x: (1 - x.mean()) * 100).reset_index()
        fig_asr = px.bar(asr_df, x='model', y='score', title="Attack Success Rate % (Lower is Better)")
        st.plotly_chart(fig_asr)

    with col2:
        st.subheader("🔥 Robustness Heatmap (robustness_heatmap.png)")
        pivot = df.pivot_table(index='model', columns='category', values='score', aggfunc='mean')
        fig_heat = px.imshow(pivot, text_auto=True, color_continuous_scale='RdYlGn', title="Model vs Category Resilience")
        st.plotly_chart(fig_heat)
    
    st.subheader("📋 Leaderboard")
    leaderboard = df.groupby('model').agg({'score': 'mean'}).sort_values('score', ascending=False)
    st.table(leaderboard)
