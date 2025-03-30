from typing import Dict
from agent_protocol import Agent, AgentState  # Ensure correct imports
from .agents import create_researcher_agent, create_summarizer_agent  # Use explicit functions

async def analyze_news_workflow(
    provider_config: Dict,
    topic: str,
    max_sources: int,
    recency_days: int = 7
) -> Dict:
    """End-to-end analysis workflow with agent coordination"""
    # Initialize agents using explicit factory functions
    researcher = create_researcher_agent(provider_config)
    summarizer = create_summarizer_agent(provider_config)
    
    try:
        # Step 1: Gather sources with correct parameters
        research_response = await researcher.invoke({
            "topic": topic,
            "max_results": max_sources,
            "recency_days": recency_days  # Use parameter name expected by search tool
        })
        
        # Extract sources (adjust key based on actual response structure)
        sources = research_response.get("results", []) or research_response.get("hits", [])
        
        # Step 2: Perform synthesis with source URLs
        analysis_response = await summarizer.invoke({
            "sources": [article['url'] for article in sources if 'url' in article],
            "output_type": "markdown"
        })
        
        return {
            "status": "success",
            "sources": sources,
            "analysis": analysis_response.get("content", "No analysis available")
        }
        
    except AgentState.Error as e:
        return {
            "status": "error",
            "error": str(e.error_message) if hasattr(e, "error_message") else str(e)
        }
    finally:
        # Cleanup (ensure agent has async close method)
        if hasattr(researcher, "aclose") and hasattr(summarizer, "aclose"):
            await researcher.aclose()
            await summarizer.aclose()

def sync_run_workflow(*args, **kwargs):
    """Synchronous wrapper for trio compatibility"""
    import trio
    return trio.run(analyze_news_workflow, *args, **kwargs)
