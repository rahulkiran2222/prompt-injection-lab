import streamlit as st
import json
import pandas as pd
import plotly.express as px
import os
from core.models import ModelProvider
from core.engine import PILEngine
from core.metrics import PILMetrics

st.set_page_config(page_title="PIL Research Lab", layout="wide")
st.title("🛡️ PIL: Multi-Model Robustness Leaderboard")

# Sidebar - Full Research Model List
st.sidebar.header("🔬 Experiment Configuration")

model_dict = {
    # --- Professional APIs ---
    "Gemini 1.5 Flash": "google/gemini-1.5-flash",
    "Gemini 1.5 Pro": "google/gemini-1.5-pro",
    "GPT-4o Mini": "openai/gpt-4o-mini",
    
    # --- Free / Open Source (Hugging Face) ---
    "Qwen 2.5 7B": "huggingface/Qwen/Qwen2.5-7B-Instruct",
    "Mistral 7B v0.3": "huggingface/mistralai/Mistral-7B-Instruct-v0.3",
    "Gemma 2 9B": "huggingface/google/gemma-2-9b-it",
    "Phi-3.5 Mini": "huggingface/microsoft/Phi-3.5-mini-instruct",
    "Llama 3.2 3B": "huggingface/meta-llama/Llama-3.2-3B-Instruct",
    "Falcon 7B": "huggingface/tiiuae/falcon-7b-instruct",
    "DeepSeek V2.5": "deepseek/deepseek-chat"
}

selected_models = st.sidebar.multiselect("Select Models to Compare", list(model_dict.keys()), default=["Gemini 1.5 Flash", "Qwen 2.5 7B"])
api_key = st.sidebar.text_input("🔑 API Key / HF Token", type="password", help="Paste your Google Key or HF Token here.")
defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

if 'all_results' not in st.session_state:
    st.session_state.all_results = pd.DataFrame()

if st.button("🚀 Run Comparative Evaluation"):
    all_data = []
    # Load Benchmark
    with open('data/benchmark.json', 'r') as f:
        benchmark_data = json.load(f)

    for m_name in selected_models:
        with st.spinner(f"Evaluating {m_name}..."):
            m_id = model_dict[m_name]
            llm = ModelProvider(m_id, api_key)
            engine = PILEngine(llm)
            
            raw = engine.run_benchmark(benchmark_data, defense_choice)
            for r in raw:
                r['model'] = m_name
                all_data.append(r)
    
    st.session_state.all_results = pd.DataFrame(all_data)

# --- Visualization ---
if not st.session_state.all_results.empty:
    df = st.session_state.all_results
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Adversarial Success Rate")
        asr_df = df.groupby('model')['score'].apply(lambda x: (1 - x.mean()) * 100).reset_index()
        fig_asr = px.bar(asr_df, x='model', y='score', title="ASR % (Lower is Safer)", color='model')
        st.plotly_chart(fig_asr, use_container_width=True)

    with col2:
        st.subheader("🔥 Robustness Heatmap")
        pivot = df.pivot_table(index='model', columns='category', values='score', aggfunc='mean')
        fig_heat = px.imshow(pivot, text_auto=".2f", color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_heat, use_container_width=True)
    
    st.subheader("🏆 Comparative Leaderboard")
    leaderboard = df.groupby('model').agg({'score': 'mean'}).sort_values('score', ascending=False).reset_index()
    st.table(leaderboard)
