"""
MCP Server Configuration for News Agent with Serper API Integration
Defines tools and capabilities for the Model Context Protocol
"""

import json
from typing import Dict, List, Any, Optional
from serper_search_tool import SERPER_TOOLS, google_search_tool, google_news_search_tool

class MCPNewsServer:
    """MCP Server for News Agent with integrated search tools"""
    
    def __init__(self):
        """Initialize the MCP server with available tools"""
        self.tools = {}
        self.setup_tools()
    
    def setup_tools(self):
        """Setup all available tools for MCP"""
        # Add Serper API tools
        for tool in SERPER_TOOLS:
            self.tools[tool["name"]] = tool
        
        # Add custom news analysis tools
        self.add_news_analysis_tools()
    
    def add_news_analysis_tools(self):
        """Add news-specific analysis tools"""
        # News summarization tool
        self.tools["news_summarize"] = {
            "name": "news_summarize",
            "description": "Summarize multiple news articles into key points",
            "function": self._summarize_news,
            "parameters": {
                "type": "object",
                "properties": {
                    "articles": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "content": {"type": "string"},
                                "source": {"type": "string"}
                            }
                        },
                        "description": "Array of news articles to summarize"
                    },
                    "focus": {
                        "type": "string",
                        "description": "Specific aspect to focus on (optional)",
                        "default": "general"
                    }
                },
                "required": ["articles"]
            }
        }
        
        # News trend analysis tool
        self.tools["news_trends"] = {
            "name": "news_trends",
            "description": "Analyze trends and patterns in news articles",
            "function": self._analyze_trends,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Topic to analyze trends for"
                    },
                    "timeframe": {
                        "type": "string",
                        "description": "Time period for trend analysis",
                        "enum": ["24h", "week", "month"],
                        "default": "week"
                    }
                },
                "required": ["query"]
            }
        }
        
        # Source credibility checker
        self.tools["check_source_credibility"] = {
            "name": "check_source_credibility",
            "description": "Evaluate the credibility and bias of news sources",
            "function": self._check_source_credibility,
            "parameters": {
                "type": "object",
                "properties": {
                    "source_url": {
                        "type": "string",
                        "description": "URL of the news source to evaluate"
                    },
                    "source_name": {
                        "type": "string",
                        "description": "Name of the news source"
                    }
                },
                "required": ["source_name"]
            }
        }
    
    def _summarize_news(self, articles: List[Dict], focus: str = "general") -> str:
        """Summarize news articles"""
        if not articles:
            return "❌ No articles provided for summarization"
        
        summary_parts = []
        summary_parts.append(f"📰 **News Summary** ({focus.title()} Focus)")
        summary_parts.append("=" * 50)
        
        # Group by source if multiple articles
        sources = {}
        for article in articles:
            source = article.get("source", "Unknown")
            if source not in sources:
                sources[source] = []
            sources[source].append(article)
        
        # Create summary
        for source, source_articles in sources.items():
            summary_parts.append(f"\n**{source}:**")
            for article in source_articles:
                title = article.get("title", "No title")
                content = article.get("content", article.get("snippet", "No content"))
                summary_parts.append(f"• {title}")
                if content and len(content) > 100:
                    summary_parts.append(f"  💡 {content[:200]}...")
                else:
                    summary_parts.append(f"  💡 {content}")
        
        # Add key insights
        summary_parts.append(f"\n**🔍 Key Insights:**")
        summary_parts.append(f"• Total articles analyzed: {len(articles)}")
        summary_parts.append(f"• Sources covered: {len(sources)}")
        summary_parts.append(f"• Focus area: {focus}")
        
        return "\n".join(summary_parts)
    
    def _analyze_trends(self, query: str, timeframe: str = "week") -> str:
        """Analyze news trends for a topic"""
        # Use Serper API to search for recent articles
        try:
            from serper_search_tool import SerperSearchTool
            tool = SerperSearchTool()
            
            # Search for recent news
            results = tool.search_news(f"{query} {timeframe}", num_results=10)
            
            if "error" in results:
                return f"❌ Error analyzing trends: {results['error']}"
            
            # Analyze trends
            trend_analysis = []
            trend_analysis.append(f"📈 **Trend Analysis: {query}** (Past {timeframe})")
            trend_analysis.append("=" * 50)
            
            if "news" in results and results["news"]:
                articles = results["news"]
                
                # Analyze sources
                sources = {}
                for article in articles:
                    source = article.get("source", "Unknown")
                    sources[source] = sources.get(source, 0) + 1
                
                trend_analysis.append(f"\n**📊 Coverage Statistics:**")
                trend_analysis.append(f"• Total articles found: {len(articles)}")
                trend_analysis.append(f"• Unique sources: {len(sources)}")
                trend_analysis.append(f"• Top sources: {', '.join(list(sources.keys())[:3])}")
                
                # Recent headlines
                trend_analysis.append(f"\n**📰 Recent Headlines:**")
                for i, article in enumerate(articles[:5], 1):
                    title = article.get("title", "No title")
                    date = article.get("date", "No date")
                    trend_analysis.append(f"{i}. {title} ({date})")
                
                return "\n".join(trend_analysis)
            else:
                return f"📊 No recent news trends found for '{query}' in the past {timeframe}."
                
        except Exception as e:
            return f"❌ Trend analysis failed: {str(e)}"
    
    def _check_source_credibility(self, source_name: str, source_url: str = None) -> str:
        """Check source credibility"""
        # Simple credibility checker based on known sources
        credible_sources = {
            "reuters": {"score": 9, "bias": "center", "description": "Highly credible international news agency"},
            "associated press": {"score": 9, "bias": "center", "description": "Highly credible news cooperative"},
            "bbc": {"score": 8, "bias": "center-left", "description": "Credible international broadcaster"},
            "cnn": {"score": 7, "bias": "left", "description": "Major news network with left-leaning bias"},
            "fox news": {"score": 6, "bias": "right", "description": "Major news network with right-leaning bias"},
            "npr": {"score": 8, "bias": "center-left", "description": "Public radio with high factual reporting"},
            "wall street journal": {"score": 8, "bias": "center-right", "description": "Financial newspaper with center-right bias"},
            "the guardian": {"score": 7, "bias": "left", "description": "British newspaper with left-leaning bias"},
            "the times": {"score": 8, "bias": "center-right", "description": "British newspaper with center-right bias"}
        }
        
        source_lower = source_name.lower()
        
        # Check if source is in our database
        for known_source, info in credible_sources.items():
            if known_source in source_lower:
                return f"""
🔍 **Source Credibility Report: {source_name}**

**Credibility Score:** {info['score']}/10
**Political Bias:** {info['bias'].title()}
**Assessment:** {info['description']}

**Recommendations:**
• {"✅ Highly reliable source" if info['score'] >= 8 else "⚠️ Generally reliable but verify with other sources" if info['score'] >= 6 else "❌ Use with caution"}
• Consider the {info['bias']} bias when reading articles
• Cross-reference with other sources for complete picture
"""
        
        # Unknown source
        return f"""
🔍 **Source Credibility Report: {source_name}**

**Status:** Unknown source - not in credibility database

**Recommendations:**
• ⚠️ Verify information with known credible sources
• Check source's "About" page and editorial standards
• Look for professional journalism standards
• Cross-reference facts with multiple sources
• Be cautious of potential bias or misinformation

**URL:** {source_url if source_url else "Not provided"}
"""
    
    def get_tool_schema(self) -> Dict[str, Any]:
        """Get the complete MCP tool schema"""
        return {
            "tools": list(self.tools.values()),
            "version": "1.0.0",
            "description": "News Agent MCP Server with Serper API integration",
            "capabilities": [
                "google_search",
                "google_news_search", 
                "news_analysis",
                "trend_analysis",
                "source_credibility_check"
            ]
        }
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """Execute a tool with given parameters"""
        if tool_name not in self.tools:
            return f"❌ Unknown tool: {tool_name}"
        
        try:
            tool = self.tools[tool_name]
            function = tool["function"]
            return function(**parameters)
        except Exception as e:
            return f"❌ Tool execution failed: {str(e)}"

# Create global server instance
mcp_server = MCPNewsServer()

def get_mcp_tools() -> List[Dict[str, Any]]:
    """Get list of all available MCP tools"""
    return list(mcp_server.tools.values())

def execute_mcp_tool(tool_name: str, parameters: Dict[str, Any]) -> str:
    """Execute an MCP tool"""
    return mcp_server.execute_tool(tool_name, parameters)

if __name__ == "__main__":
    # Test the MCP server
    print("🛠️ Testing MCP News Server...")
    print("=" * 50)
    
    # Show available tools
    schema = mcp_server.get_tool_schema()
    print(f"📋 Available tools: {len(schema['tools'])}")
    for tool in schema['tools']:
        print(f"  • {tool['name']}: {tool['description']}")
    
    # Test a simple tool
    print("\n🔍 Testing google_search tool...")
    result = mcp_server.execute_tool("google_search", {
        "query": "latest technology news",
        "num_results": 3
    })
    print(result[:500] + "..." if len(result) > 500 else result)
