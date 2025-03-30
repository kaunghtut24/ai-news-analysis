from openai import AsyncOpenAI
from agent_protocol import Agent
from src.tools.search_utils import search_news  # Fixed import

def get_model_provider(provider, model_name=None):
    if provider == "ollama":
        raise NotImplementedError("Use OpenAI/Anthropic for now")
    elif provider == "openai":
        client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE", None)
        )
        return {
            "client": client,
            "model": model_name or "gpt-3.5-turbo",
            "type": "openai"
        }
    elif provider == "anthropic":
        return {
            "client": Anthropic(
                api_key=os.getenv("ANTHROPIC_KEY"),
                model=model_name or "claude-3-sonnet"
            ),
            "type": "anthropic"
        }
    raise ValueError(f"Unsupported provider: {provider}")

def configure_agent(llm_config):
    if llm_config["type"] == "openai":
        return Agent(
            llm=llm_config["client"],
            model=llm_config["model"],
            tools=[search_news]  # Use imported function
        )
    else:
        return Agent(
            llm=llm_config["client"],
            tools=[search_news]
        )
