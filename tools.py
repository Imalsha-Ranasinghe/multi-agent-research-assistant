# tools.py
import os
from dotenv import load_dotenv
from config import get_secret
from tavily import TavilyClient

# load_dotenv()

tavily_key = get_secret("TAVILY_API_KEY")

if not tavily_key:
    raise RuntimeError("TAVILY_API_KEY is missing")

search_client = TavilyClient(api_key=tavily_key)

def web_search(query: str) -> dict:
    """Search the live web and return relevant source information."""

    if not query or not query.strip():
        return {"results": [], "error": "Search query is empty."}

    try:
        response = search_client.search(
            query=query,
            max_results=5,
            search_depth="basic",
        )

        results = []

        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
            })

        return {
            "query": query,
            "results": results,
            "message": (
                "These are live web search results. "
                "Verify claims against the original sources."
            ),
        }

    except Exception as error:
        return {
            "query": query,
            "results": [],
            "error": f"Web search failed: {error}",
        }
