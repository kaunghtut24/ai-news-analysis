#from duckduckgo_search.ddg import DDG  # Fixed: Un-comment the import
from datetime import datetime
from dateutil.parser import parse as date_parse

def search_news(query: str, max_results: int=5, recency_days: int=7) -> list:
    try:
        # Initialize DDG search
        ddg = DDG()
        
        # Fetch results (news type, example parameters):
        # Update to correct API parameters for current duckduckgo_search version
        results = ddg.text(
            query,
            region="wt-w5",          # Global region code
            safesearch=True,         # Boolean instead of "On"
            time="y",                # "y" for last year; adjust based on needs
            max_results=max_results  # Explicitly set max_results
        )

        now = datetime.now()
        filtered = []
        for item in results[:max_results]:
            # Get date using multiple key checks to handle API response variations
            pub_date_str = (
                item.get('date') or 
                item.get('lastmod') or 
                item.get('datetime') or 
                item.get('publishedDate') or 
                "1970-01-01"  # Fallback
            )
            
            if pub_date_str:
                try:
                    pub_date = date_parse(pub_date_str)
                except Exception as parse_e:
                    print(f"Date parse error: {parse_e}")
                    continue  # Skip invalid entries
            
                if (now - pub_date).days <= recency_days:
                    filtered_article = {
                        'title': item.get('title', 'Untitled Article'),
                        'url': item.get('url') or item.get('href'),
                        'date': pub_date.strftime("%Y-%m-%d"),
                        'source': item.get('domain', item.get('host', 'Unknown'))
                    }
                    
                    # Basic validation
                    if not filtered_article['url']:
                        continue  # Skip entries without URL
                    
                    filtered.append(filtered_article)
                    
        return filtered[:max_results]
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]
