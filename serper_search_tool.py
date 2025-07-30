"""
Serper API Google Search Tool for MCP Integration
Implements Google search functionality using Serper API
"""

import requests
import json
import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SerperSearchTool:
    """Google Search tool using Serper API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Serper search tool
        
        Args:
            api_key: Serper API key. If None, will try to get from environment
        """
        self.api_key = api_key or os.getenv('SERPER_API_KEY')
        if not self.api_key:
            raise ValueError("Serper API key is required. Set SERPER_API_KEY environment variable.")
        
        self.base_url = "https://google.serper.dev/search"
        self.headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def search(self, query: str, num_results: int = 10, location: str = None) -> Dict[str, Any]:
        """Perform a Google search using Serper API
        
        Args:
            query: Search query string
            num_results: Number of results to return (default: 10)
            location: Geographic location for search (optional)
            
        Returns:
            Dictionary containing search results
        """
        try:
            payload = {
                "q": query,
                "num": num_results
            }
            
            if location:
                payload["gl"] = location
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Search request failed: {str(e)}",
                "success": False
            }
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse response: {str(e)}",
                "success": False
            }
    
    def search_news(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """Search for news articles specifically
        
        Args:
            query: News search query
            num_results: Number of news results to return
            
        Returns:
            Dictionary containing news search results
        """
        try:
            payload = {
                "q": query,
                "num": num_results,
                "type": "news"
            }
            
            response = requests.post(
                "https://google.serper.dev/news",
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                "error": f"News search request failed: {str(e)}",
                "success": False
            }
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse news response: {str(e)}",
                "success": False
            }
    
    def format_search_results(self, results: Dict[str, Any]) -> str:
        """Format search results for display
        
        Args:
            results: Raw search results from Serper API
            
        Returns:
            Formatted string representation of search results
        """
        if "error" in results:
            return f"❌ Search Error: {results['error']}"
        
        formatted_output = []
        
        # Add search information
        if "searchParameters" in results:
            search_params = results["searchParameters"]
            formatted_output.append(f"🔍 **Search Query:** {search_params.get('q', 'N/A')}")
            formatted_output.append(f"📊 **Results Found:** {results.get('searchInformation', {}).get('totalResults', 'N/A')}")
            formatted_output.append("")
        
        # Format organic results
        if "organic" in results:
            formatted_output.append("## 🌐 Web Results")
            for i, result in enumerate(results["organic"][:10], 1):
                title = result.get("title", "No title")
                link = result.get("link", "")
                snippet = result.get("snippet", "No description available")
                
                formatted_output.append(f"### {i}. {title}")
                formatted_output.append(f"🔗 **URL:** {link}")
                formatted_output.append(f"📝 **Description:** {snippet}")
                formatted_output.append("")
        
        # Format news results if available
        if "news" in results:
            formatted_output.append("## 📰 News Results")
            for i, article in enumerate(results["news"][:5], 1):
                title = article.get("title", "No title")
                link = article.get("link", "")
                snippet = article.get("snippet", "No description available")
                source = article.get("source", "Unknown source")
                date = article.get("date", "No date")
                
                formatted_output.append(f"### {i}. {title}")
                formatted_output.append(f"📰 **Source:** {source}")
                formatted_output.append(f"📅 **Date:** {date}")
                formatted_output.append(f"🔗 **URL:** {link}")
                formatted_output.append(f"📝 **Summary:** {snippet}")
                formatted_output.append("")
        
        # Format people also ask if available
        if "peopleAlsoAsk" in results:
            formatted_output.append("## ❓ People Also Ask")
            for i, question in enumerate(results["peopleAlsoAsk"][:3], 1):
                formatted_output.append(f"{i}. {question.get('question', 'No question')}")
                if question.get("snippet"):
                    formatted_output.append(f"   💡 {question['snippet']}")
            formatted_output.append("")
        
        # Format related searches if available
        if "relatedSearches" in results:
            formatted_output.append("## 🔗 Related Searches")
            related_queries = [search.get("query", "") for search in results["relatedSearches"][:5]]
            for query in related_queries:
                if query:
                    formatted_output.append(f"• {query}")
            formatted_output.append("")
        
        return "\n".join(formatted_output)
    
    def test_connection(self) -> bool:
        """Test if the Serper API connection is working
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            test_result = self.search("test query", num_results=1)
            return "error" not in test_result
        except Exception:
            return False

# MCP Tool Functions for integration
def google_search_tool(query: str, num_results: int = 10, location: str = None) -> str:
    """MCP tool function for Google search
    
    Args:
        query: Search query string
        num_results: Number of results to return
        location: Geographic location for search
        
    Returns:
        Formatted search results as string
    """
    try:
        tool = SerperSearchTool()
        results = tool.search(query, num_results, location)
        return tool.format_search_results(results)
    except Exception as e:
        return f"❌ Search tool error: {str(e)}"

def google_news_search_tool(query: str, num_results: int = 10) -> str:
    """MCP tool function for Google news search
    
    Args:
        query: News search query
        num_results: Number of results to return
        
    Returns:
        Formatted news search results as string
    """
    try:
        tool = SerperSearchTool()
        results = tool.search_news(query, num_results)
        return tool.format_search_results(results)
    except Exception as e:
        return f"❌ News search tool error: {str(e)}"

# Tool definitions for MCP integration
SERPER_TOOLS = [
    {
        "name": "google_search",
        "description": "Search Google using Serper API for web results, news, and information",
        "function": google_search_tool,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to execute"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return (default: 10)",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 20
                },
                "location": {
                    "type": "string",
                    "description": "Geographic location for search (optional, e.g., 'us', 'uk', 'ca')",
                    "default": None
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "google_news_search",
        "description": "Search Google News using Serper API for latest news articles and current events",
        "function": google_news_search_tool,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The news search query to execute"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of news results to return (default: 10)",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 20
                }
            },
            "required": ["query"]
        }
    }
]

if __name__ == "__main__":
    # Test the Serper search tool
    try:
        tool = SerperSearchTool()
        
        print("🔍 Testing Serper Google Search Tool...")
        print("=" * 50)
        
        # Test connection
        if tool.test_connection():
            print("✅ Connection to Serper API successful!")
        else:
            print("❌ Connection to Serper API failed!")
            exit(1)
        
        # Test general search
        print("\n📝 Testing general search...")
        results = tool.search("artificial intelligence latest news", num_results=3)
        formatted = tool.format_search_results(results)
        print(formatted[:500] + "..." if len(formatted) > 500 else formatted)
        
        # Test news search
        print("\n📰 Testing news search...")
        news_results = tool.search_news("technology innovation 2024", num_results=3)
        news_formatted = tool.format_search_results(news_results)
        print(news_formatted[:500] + "..." if len(news_formatted) > 500 else news_formatted)
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
