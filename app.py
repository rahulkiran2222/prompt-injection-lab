import streamlit as st
import json
import pandas as pd
import plotly.express as px
from core.models import ModelProvider
from core.engine import PILEngine
from core.metrics import PILMetrics

st.set_page_config(page_title="Prompt Injection Lab", layout="wide")

# Custom CSS for a professional research look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_all_headers=True)

st.title("🛡️ Prompt Injection Lab (PIL)")
st.caption("A scientific framework for measuring LLM vulnerability and defense effectiveness.")

# Sidebar
st.sidebar.header("🔬 Experiment Configuration")
model_choice = st.sidebar.selectbox("Target Model", ["gpt-3.5-turbo", "gpt-4o-mini", "huggingface/meta-llama/Meta-Llama-3-8B-Instruct"])
api_key = st.sidebar.text_input("API Key", type="password", help="Enter your OpenAI or HuggingFace API key.")
defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

# Load Dataset
with open('data/benchmark.json', 'r') as f:
    benchmark_data = json.load(f)

if st.button("🚀 Run Evaluation Suite"):
    if not api_key and "huggingface" not in model_choice:
        st.error("Please provide an API Key for the selected model.")
    else:
        with st.spinner(f"Evaluating {model_choice} with {defense_choice}..."):
            # Initialize
            llm = ModelProvider(model_choice, api_key)
            engine = PILEngine(llm)
            
            # Run
            raw_results = engine.run_benchmark(benchmark_data, defense_choice)
            stats = PILMetrics.calculate_aggregate_stats(raw_results)

            # --- VISUALIZATION ---
            col1, col2, col3 = st.columns(3)
            col1.metric("Resistance Rate", f"{stats['attack_resistance_rate']}%")
            col2.metric("Success Rate (ASR)", f"{stats['attack_success_rate']}%")
            col3.metric("Tests Run", stats['total_tests'])

            # Results Table
            st.subheader("Detailed Logs")
            df = pd.DataFrame(raw_results)
            
            # Style the dataframe
            def color_score(val):
                color = '#ff4b4b' if val == 0 else '#28a745' if val == 1 else '#ffa500'
                return f'background-color: {color}; color: white'
            
            st.table(df.style.applymap(color_score, subset=['score']))

            # Category Analysis (PhD Highlight)
            st.subheader("Vulnerability by Category")
            fig = px.bar(df, x='category', y='score', color='category', 
                         title="Resilience Score per Threat Category",
                         labels={'score': 'Resilience (Higher is Better)'})
            st.plotly_chart(fig, use_container_width=True)

# Documentation Tab
with st.expander("ℹ️ Methodology & Research Goals"):
    st.markdown("""
    **Methodology:** This lab uses a controlled environment where a system prompt (the target) is attacked by a user prompt (the payload).
    
    **Metrics:** 
    - **Attack Resistance Rate (ARR):** % of attempts where the model maintained its original instructions.
    - **Heuristic Evaluation:** We analyze responses for refusal patterns and instruction adherence.
    """)
