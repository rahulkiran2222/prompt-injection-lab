<div align="center">

# 🛡️ Prompt Injection Lab (PIL)

### A Reproducible Evaluation Framework for Indirect Prompt Injection in Retrieval-Augmented Generation

<p align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-yellow)](https://huggingface.co/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![Research](https://img.shields.io/badge/Research-AI%20Security-indigo)]()

</p>

**Evaluating the robustness of modern Large Language Models against published indirect prompt injection benchmarks through reproducible experimentation, standardized metrics, and modular defenses.**

---

</div>

# Overview

Prompt Injection Lab (PIL) is an open research framework for studying **indirect prompt injection** in Retrieval-Augmented Generation (RAG) systems.

Unlike repositories focused on collecting jailbreak prompts or exploits, PIL emphasizes **measurement, reproducibility, and empirical evaluation**. The framework enables researchers to benchmark multiple language models against **published indirect prompt injection datasets** while evaluating representative defensive strategies under a unified experimental protocol.

---

# Research Motivation

Large Language Models increasingly interact with:

- Web pages
- PDFs
- Knowledge bases
- Enterprise documents
- External APIs

These inputs cannot always be trusted.

Prompt injection has emerged as one of the most important security challenges for LLM-powered systems. Existing evaluations are often fragmented across datasets, models, and reporting methodologies.

PIL aims to provide a **reproducible evaluation framework** for comparing model robustness and defensive techniques.

---

# Research Question

> **How robust are modern open-source Large Language Models against documented indirect prompt injection attacks in Retrieval-Augmented Generation systems, and how effective are representative defensive strategies under a common evaluation framework?**

---

# Research Contributions

- 📚 Reproducible evaluation framework for indirect prompt injection
- 🔬 Unified benchmarking pipeline across multiple open-source LLMs
- 🛡️ Modular defense evaluation framework
- 📊 Standardized security metrics and statistical reporting
- 📈 Publication-quality visualizations and experiment reports
- 🤗 Interactive Hugging Face demo for reproducible experiments

---

# Experimental Scope

## Threat Model

✔ Indirect Prompt Injection

## Application Domain

✔ Retrieval-Augmented Generation (RAG)

## Models

- Qwen 2.5 Instruct
- Llama 3.1 Instruct
- Gemma
- *(Additional models can be added through adapters.)*

## Defensive Baselines

- Baseline (No Defense)
- Context Separation
- Input Sanitization

---

# Evaluation Pipeline

```text
Published Benchmark
        │
        ▼
 Dataset Loader
        │
        ▼
  Model Adapter
        │
        ▼
 Defense Wrapper
        │
        ▼
 Evaluation Engine
        │
        ▼
 Statistical Analysis
        │
        ▼
 Visualization & Report
```

---

# Benchmark Architecture

```text
                User Query
                     │
                     ▼
           Retrieved Documents
                     │
                     ▼
         Prompt Injection Lab
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 Dataset       Model Adapter     Defense
      │              │              │
      └──────────────┼──────────────┘
                     ▼
          Evaluation Engine
                     │
                     ▼
             Metrics & Reports
```

---

# Supported Benchmarks

The framework is designed to support **published academic benchmark datasets**.

Planned integrations include:

- BIPIA
- InjecAgent
- Additional peer-reviewed indirect prompt injection datasets

> PIL evaluates documented benchmark scenarios and does **not** generate new prompt injection attacks.

---

# Standardized Metrics

| Metric | Description |
|----------|-------------|
| Attack Success Rate (ASR) | Percentage of successful benchmark attacks |
| Defense Success Rate | Improvement achieved by a defense |
| Task Success Rate | Utility retained after defense |
| False Positive Rate | Benign prompts incorrectly flagged |
| Confidence Intervals | Statistical uncertainty estimates |

---

# Repository Structure

```text
prompt-injection-lab/

├── app.py
├── README.md
├── requirements.txt
├── Dockerfile
│
├── benchmarks/
├── models/
├── defenses/
```

---

# Quick Start

## Clone Repository

```bash
git clone https://github.com/rahulkiran2222/prompt-injection-lab.git

cd prompt-injection-lab
```

## Install

```bash
pip install -r requirements.txt
```

## Launch

```bash
python app.py
```

---

# Docker

```bash
docker build -t prompt-injection-lab .

docker run -p 7860:7860 prompt-injection-lab
```

---

# Interactive Demo

The project includes an interactive interface built with **Gradio** and deployable on **Hugging Face Spaces**.

Users can:

- Select benchmark
- Select model
- Select defense
- Execute evaluation
- Visualize security metrics
- Export experiment reports

---

# Results Gallery

Future releases will include:

- Attack Success Rate comparisons
- Defense effectiveness charts
- Cross-model robustness analysis
- Statistical summaries
- Publication-quality figures

Example:

```
figures/

├── architecture.png
├── benchmark_pipeline.png
├── asr_comparison.png
├── defense_analysis.png
└── robustness_heatmap.png
```
graph TD
    A[Benchmark Dataset] --> B[Defense Library]
    B --> C[Evaluation Engine]
    C --> D[Model Adapters]
    D --> E[Inference API]
    E --> F[Response Parser]
    F --> G[Metric Scorer]
    G --> H[Leaderboard & Charts]
---

# Technology Stack

### Models

- Hugging Face Transformers
- Hugging Face Inference API

### AI Frameworks

- PyTorch
- Transformers

### Analysis

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib

### Deployment

- Gradio
- Hugging Face Spaces
- Docker

---

# Research Roadmap

- [x] Project specification
- [x] System architecture
- [ ] Benchmark integration
- [ ] Model adapters
- [ ] Defense implementations
- [ ] Evaluation engine
- [ ] Statistical analysis
- [ ] Interactive demo
- [ ] Technical report
- [ ] Workshop paper

---

# Future Directions

Future versions will extend the framework toward:

- Agent security
- Secure RAG
- Multi-agent safety
- Tool-use security
- Memory poisoning
- AI alignment evaluation

---

# Citation

If you use this project in your research, please cite:

```bibtex
@misc{rahul2026pil,
  title={Prompt Injection Lab: A Reproducible Evaluation Framework for Indirect Prompt Injection in Retrieval-Augmented Generation},
  author={Rahul Kiran},
  year={2026},
  note={Work in Progress}
}
```

---

# License

Distributed under the MIT License.

See **LICENSE** for details.

---

# Author

**Rahul Kiran**

AI Safety • AI Security • Foundation Models • LLM Evaluation

- GitHub: https://github.com/rahulkiran2222
- Hugging Face: https://huggingface.co/rahulkiran2222
- LinkedIn: https://linkedin.com/rahul-g-kiran

---

<div align="center">

### ⭐ If you find this project useful, consider giving it a star.

**Building reproducible AI security research for trustworthy foundation models.**

</div>
