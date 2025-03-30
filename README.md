# AI News Analysis Application

A Streamlit-based application for analyzing news via LLM-powered agents.

## Features
- Multimodal news search
- Sentiment and theme analysis
- PDF/CSV/JSON exports
- Support for OpenAI/Anthropic models
- Local model option (Ollama)

## Requirements
- Python 3.11+
- Conda environment
- API keys for:
  - OpenAI
  - Anthropic
  - DuckDuckGo Search

## Quick Start
1. **Install Dependencies**
   ```bash
   conda env create -f environment.yaml
   conda activate news-analysis
Setup Environment Variables

bash
cp .env.example .env  # Enter your keys
Run the App

bash
streamlit run src/main.py
Access via Browser
Visit http://localhost:8501


