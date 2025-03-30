import sys
import os
import streamlit as st
from dotenv import load_dotenv

# Optionally adjust PYTHONPATH if your working directory is not the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.models.model_factories import get_model_provider, create_agent
from src.agents.agents import create_researcher_agent, create_summarizer_agent
from src.agents.workflow import sync_run_workflow
from src.tools.search_utils import search_news
from src.utils.cache import cached_search
from src.utils.exports import (
    export_to_pdf,
    export_to_json,
    export_to_csv,
    generate_downloader
)
from src.ui.main_ui import NewsAnalyzerUI

def main():
    load_dotenv()
    st.set_page_config(
        page_title="AI News Analyzer",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Search"

    # Select Model & Provider (via UI component)
    provider_name, model_name = load_model_selection()

    # Configure Model Provider
    try:
        provider_config = get_model_provider(provider_name, model_name)
        st.sidebar.success(f"Connected to {provider_name} using {provider_config['client'].__class__.__name__}")
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")
        provider_config = None

    # Main UI
    if provider_config:
        app = NewsAnalyzerUI(provider_config)
        app.run()
        
def load_model_selection():
    with st.sidebar:
        st.title("AI News Analyzer Config")
        provider_options = ["ollama", "openai", "anthropic"]
        provider_name = st.selectbox("Provider", provider_options)

        model_options = get_model_options(provider_name)
        model_name = st.selectbox("Model", model_options)
    
    return provider_name, model_name

def get_model_options(provider):
    if provider == "ollama":
        return ["llama3:latest", "mistral:latest", "phi3:latest"]
    elif provider == "openai":
        return ["gpt-3.5-turbo", "gpt-4"]
    elif provider == "anthropic":
        return ["claude-3-sonnet-20240229", "claude-3-opus-20240229"]
    return []

if __name__ == "__main__":
    main()
