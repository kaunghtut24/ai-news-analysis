import hashlib
import asyncio
from functools import lru_cache
import nest_asyncio
from streamlit_extras import caching
from app.tools.search_utils import search_news


nest_asyncio.apply()

def async_lru_cache(maxsize=128):
    """Asynchronous LRU cache decorator for async functions"""
    def decorator(func):
        cached = lru_cache(maxsize)(func)
        async def wrapper(*args, **kwargs):
            return cached(*args, **kwargs)
        return wrapper
    return decorator

@async_lru_cache()
async def async_search_cache(query: str, max_results: int) -> list:
    """Cached search using DuckDuckGo"""
    results = await search_news(query, max_results)
    filtered = [{"title": item['title'], "url": item['url']} 
                for item in results if item.get('url')]
    return filtered

def sync_search_cache(query: str, max_results: int) -> list:
    """Sync wrapper for cached search"""
    return asyncio.run(async_search_cache(query, max_results))
