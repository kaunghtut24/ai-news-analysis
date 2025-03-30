import streamlit as st
from app.utils.exports import export_to_pdf, export_to_csv, export_to_json, generate_downloader
from app.utils.cache import cached_search
from datetime import datetime

class NewsAnalyzerUI:
    def __init__(self, provider_config):
        self.provider_config = provider_config
        self.topic = None

    def run(self):
        # Tabs Setup
        tabs = st.tabs(["Search", "Results", "Settings"])
        with tabs[0]:
            self.show_search_tab()
        with tabs[1]:
            self.show_results()
        with tabs[2]:
            self.show_settings()  # Ensure method call with proper context

    # main_ui.py corrected code
def show_search_tab(self):
    topic = st.text_input("Enter topic", placeholder="e.g., 'Trade between India and Myanmar'")
    
    # Added input validation for slider values
    max_sources = st.slider("Max sources", 3, 20, 5, key="max_sources")
    recency = st.slider("Recency (days)", 1, 90, 7, key="recency")
    
    if st.button("Analyze") and topic.strip():
        with st.spinner("Analyzing..."):
            search_params = {
                "query": topic,
                "max_results": max_sources,
                "recency_days": recency  # Changed to match parameter naming
            }
            
            # Execute full workflow
            try:
                from app.agents.workflow import sync_run_workflow
                results = sync_run_workflow(
                    provider_config=self.provider_config,
                    topic=topic,
                    max_sources=max_sources,
                    recency_days=recency
                )
                
                # Store in session state
                if results.get("status") == "success":
                    st.session_state["results"] = {
                        "sources": results["sources"],
                        "analysis": results["analysis"]
                    }
                else:
                    st.error(f"Error: {results.get('error', 'Analysis failed')}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")


    def show_results(self):
        if "results" in st.session_state:
            analysis_data = st.session_state["results"]
            
            st.subheader("Analysis Results")
            st.write(analysis_data.get("analysis", "Analysis not yet generated."))
            
            sources = analysis_data.get("sources", [])
            
            # Formatting exports with placeholder data for demonstration
            col1, col2, col3 = st.columns(3)
            
            with col1:
                pdf_content = export_to_pdf({
                    "summary": analysis_data["analysis"],
                    "sources": sources
                })
                st.markdown(
                    generate_downloader("analysis.pdf", pdf_content,
                                       button_text="Download PDF", 
                                       file_type="application/pdf"),
                    unsafe_allow_html=True
                )
                
            with col2:
                st.markdown(
                    generate_downloader("sources.csv", export_to_csv(sources),
                                       button_text="Sources CSV", 
                                       file_type="text/csv"),
                    unsafe_allow_html=True
                )
                
            with col3:
                st.markdown(
                    generate_downloader("analysis.json", export_to_json(analysis_data),
                                       button_text="Full JSON", 
                                       file_type="application/json"),
                    unsafe_allow_html=True
                )

    def show_settings(self):  # Added 'self' parameter
        st.write("Advanced configuration coming soon! (e.g., API settings, export formats)")