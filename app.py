import streamlit as st
import json
import pandas as pd
import plotly.express as px
import os
from core.models import ModelProvider
from core.engine import PILEngine
from core.metrics import PILMetrics

st.set_page_config(page_title="PIL Dashboard", layout="wide")

# Custom Title
st.title("🛡️ PIL: Multi-Model Robustness Leaderboard")
st.markdown("---")

# Sidebar - Configuration
st.sidebar.header("🔬 Experiment Selection")
model_options = {
    "Gemini 1.5 Flash": "gemini-1.5-flash",
    "Llama 3.2 3B": "huggingface/meta-llama/Llama-3.2-3B-Instruct",
    "Mistral 7B v0.3": "huggingface/mistralai/Mistral-7B-Instruct-v0.3",
    "Qwen 2.5 7B": "huggingface/Qwen/Qwen2.5-7B-Instruct",
    "Phi-3.5 Mini": "huggingface/microsoft/Phi-3.5-mini-instruct"
}

selected_models = st.sidebar.multiselect("Models to Compare", list(model_options.keys()), default=["Gemini 1.5 Flash"])
api_key = st.sidebar.text_input("🔑 API Provider Key", type="password")
defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

# Session state to hold results
if 'all_results' not in st.session_state:
    st.session_state.all_results = pd.DataFrame()

if st.button("🚀 Run Comparative Evaluation"):
    all_data = []
    for m_name in selected_models:
        with st.spinner(f"Testing {m_name}..."):
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

# --- VISUALIZATION SECTION ---
if not st.session_state.all_results.empty:
    df = st.session_state.all_results
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CLEAN HEADING
        st.subheader("📊 Adversarial Success Rate (ASR)") 
        asr_df = df.groupby('model')['score'].apply(lambda x: (1 - x.mean()) * 100).reset_index()
        fig_asr = px.bar(asr_df, x='model', y='score', 
                         title="ASR % (Lower is More Secure)",
                         labels={'score': 'Success Rate %', 'model': 'LLM Architecture'},
                         color='model', color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_asr, use_container_width=True)

    with col2:
        # CLEAN HEADING
        st.subheader("🔥 Cross-Category Robustness") 
        pivot = df.pivot_table(index='model', columns='category', values='score', aggfunc='mean')
        fig_heat = px.imshow(pivot, text_auto=".2f", 
                             color_continuous_scale='RdYlGn', 
                             title="Resilience Heatmap (1.0 = Fully Resilient)")
        st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🏆 Model Leaderboard")
    leaderboard = df.groupby('model').agg({'score': 'mean'}).sort_values('score', ascending=False).reset_index()
    leaderboard.columns = ['Model Name', 'Aggregate Resilience Score']
    st.table(leaderboard)
