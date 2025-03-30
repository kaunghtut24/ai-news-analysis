from typing import Dict
from agent_protocol import Agent
from src.tools.search_utils import search_news

class ResearchAgent(Agent):
    """Agent to gather news sources for the topic"""
    def __init__(self, llm_config: Dict):
        super().__init__(llm=llm_config['client'])
        self.add_tool({
            "name": "search_news",
            "func": search_news,
            "description": "Searches DuckDuckGo for news articles based on a query"
        })
        self.system_message = f"""
        Your task is to find 5-10 reliable news sources about {{topic}}. 
        Provide URLs and titles only, no summaries.
        """  # Use formatted string for dynamic replacement later

class SummarizeAgent(Agent):
    """Agent to analyze and synthesize news content"""
    def __init__(self, llm_config: Dict):
        super().__init__(llm=llm_config['client'])
        self.system_message = """
        You are a news analysis AI. 
        Instructions:
            1. Analyze the provided news articles
            2. Identify key themes and developments
            3. Generate a 500-word executive summary
            4. Highlight statistical facts and expert opinions
        """
        
def create_researcher_agent(provider_config: Dict):
    """Factory function for the research agent"""
    return ResearchAgent(provider_config)

def create_summarizer_agent(provider_config: Dict):
    """Factory function for the summary agent"""
    return SummarizeAgent(provider_config)
