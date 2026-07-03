import pandas as pd
import plotly.express as px
import os

def save_research_plots(df):
    if not os.path.exists('figures'): os.makedirs('figures')
    
    # 1. ASR Comparison
    asr_df = df.groupby('model')['score'].apply(lambda x: (1 - x.mean()) * 100).reset_index()
    fig1 = px.bar(asr_df, x='model', y='score', title="ASR Comparison across LLMs")
    fig1.write_image("figures/asr_comparison.png")
    
    # 2. Robustness Heatmap
    pivot = df.pivot_table(index='model', columns='category', values='score', aggfunc='mean')
    fig2 = px.imshow(pivot, color_continuous_scale='RdYlGn')
    fig2.write_image("figures/robustness_heatmap.png")
    
    # 3. Defense Analysis
    # (Requires running the same model with different defenses)
    fig3 = px.box(df, x="category", y="score", color="model")
    fig3.write_image("figures/defense_analysis.png")

print("Research figures generated in /figures folder.")
