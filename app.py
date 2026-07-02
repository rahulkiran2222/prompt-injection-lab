import streamlit as st
import json
import pandas as pd
import plotly.express as px
from core.models import ModelProvider
from core.engine import PILEngine
from core.metrics import PILMetrics

# 1. Page Config
st.set_page_config(page_title="Prompt Injection Lab", layout="wide")

st.title("🛡️ Prompt Injection Lab (PIL)")
st.caption("Testing Resilience across SOTA Models: Llama 3.1, Claude 3.5, Gemini 1.5, and more.")

# 2. Sidebar Configuration
st.sidebar.header("🔬 Model Configuration")

model_dict = {
    "Gemini 1.5 Flash": "gemini/gemini-1.5-flash",
    "Gemini 1.5 Pro": "gemini/gemini-1.5-pro",
    "Llama 3.1 70B (HF)": "huggingface/meta-llama/Meta-Llama-3.1-70B-Instruct",
    "Claude 3.5 Sonnet": "anthropic/claude-3-5-sonnet-20240620",
    "DeepSeek V2.5": "deepseek/deepseek-chat",
    "Qwen 2.5 72B": "huggingface/Qwen/Qwen2.5-72B-Instruct",
    "GPT-4o Mini": "openai/gpt-4o-mini",
}

selected_display_name = st.sidebar.selectbox("Target Model", list(model_dict.keys()))
model_id = model_dict[selected_display_name]

api_key = st.sidebar.text_input("API Provider Key", type="password", help="Enter your key (Gemini, HF, etc.)")
defense_choice = st.sidebar.selectbox("Defense Strategy", ["No Defense", "XML Tagging", "Delimiter Guard"])

st.sidebar.info("Tip: If using Gemini, get a free key at aistudio.google.com")

# 3. Load Dataset
try:
    with open('data/benchmark.json', 'r') as f:
        benchmark_data = json.load(f)
except FileNotFoundError:
    st.error("Dataset not found. Please ensure data/benchmark.json exists.")
    benchmark_data = []

# 4. Execution Logic
if st.button("🚀 Run Evaluation Suite"):
    if not api_key:
        st.error("⚠️ Please provide an API Key in the sidebar.")
    else:
        with st.spinner(f"Evaluating {selected_display_name}..."):
            # Initialize Engine
            llm = ModelProvider(model_id, api_key)
            engine = PILEngine(llm)
            
            # Run benchmark
            raw_results = engine.run_benchmark(benchmark_data, defense_choice)
            stats = PILMetrics.calculate_aggregate_stats(raw_results)

            # --- Results Header Metrics ---
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Resistance Rate", f"{stats['attack_resistance_rate']:.1f}%")
            c2.metric("Success Rate (ASR)", f"{stats['attack_success_rate']:.1f}%")
            c3.metric("Total Tests", stats['total_tests'])
            c4.metric("System Errors", stats['errors'])

            # --- Detailed Logs Table ---
            st.subheader("Detailed Logs")
            df = pd.DataFrame(raw_results)
            
            # Use dataframe with progress bar for scores
            st.dataframe(df[['id', 'category', 'input', 'output', 'score', 'reasoning']], 
                         column_config={
                             "score": st.column_config.ProgressColumn("Score", min_value=-1, max_value=1),
                             "output": st.column_config.TextColumn("Model Response", width="large")
                         }, use_container_width=True)

            # --- Analysis Charts ---
            st.subheader("Vulnerability Analysis")
            # Filter out errors for the chart to show clean data
            chart_df = df[df['score'] >= 0]
            if not chart_df.empty:
                fig = px.bar(chart_df, x='category', y='score', color='category', range_y=[0,1],
                             title="Resilience Score (1.0 = Secure, 0.0 = Injected)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No successful responses to analyze. Check System Errors.")

# 5. Methodology Footnote
with st.expander("ℹ️ Methodology"):
    st.write("Scores: 1.0 = Pass, 0.0 = Fail, 0.5 = Inconclusive, -1.0 = System Error.")
