# 📰 Clarifai News Chatbot with Serper API & MCP Integration

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Clarifai](https://img.shields.io/badge/Clarifai-API-orange.svg)](https://clarifai.com)
[![Google ADK](https://img.shields.io/badge/Google-ADK-green.svg)](https://developers.google.com)
[![Serper API](https://img.shields.io/badge/Serper-API-purple.svg)](https://serper.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🤖 **AI-powered news chatbot** built with Clarifai API, Serper API, Google Agent Development Kit (ADK), and Streamlit for intelligent news search and analysis.

## ✨ Features

- 🌐 **Real-time News Search** - Powered by Serper API, Google ADK, and MCP tools
- 🤖 **AI-powered Analysis** - Multiple model support via Clarifai API
- 💬 **Interactive Chat Interface** - Beautiful Streamlit web application with modern dark theme
- 🎯 **Quick Start Cards** - Pre-built queries for World News, Tech & Business, Health & Science
- 🔄 **Model Selection** - Support for GPT-4o, Claude 3.5 Sonnet, LLaMA models
- 📊 **LLM Statistics Tracking** - Real-time token usage, response times, and performance metrics
- 🔄 **Streaming Responses** - Real-time AI text generation with live updates
- 📱 **Responsive Design** - Mobile-friendly interface with modern black/white styling
- 🔍 **Debug Mode** - Comprehensive logging for troubleshooting
- ⚡ **LiteLLM Integration** - Unified interface for multiple AI providers
- 📈 **Performance Analytics** - Session-wide statistics and per-message metrics
- 🎨 **Enhanced UI/UX** - Markdown rendering, styled containers, and professional design
- 🔎 **Advanced Search** - Serper API integration for enhanced Google search and news results
- 🛠️ **MCP Integration** - Model Context Protocol tools for extensible functionality

## 🏗️ Architecture

```mermaid
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  News Agent     │────│  Clarifai API   │
│   (Frontend)    │    │  (Core Logic)   │    │  (AI Models)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │  Serper API     │              │
         │              │ (Google Search) │              │
         │              └─────────────────┘              │
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────│  Google ADK     │──────────────┘
                        │  (News Tools)   │
                        └─────────────────┘
                               │
                        ┌─────────────────┐
                        │   MCP Server    │
                        │ (Tool Protocol) │
                        └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Conda or pip package manager
- Clarifai Personal Access Token
- Serper API Key (for enhanced search)
- Google ADK credentials (optional for enhanced search)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/toswari-ai/chatbot-news-agentic-adk.git
   cd chatbot-news-agentic-adk
   ```

2. **Set up Python environment**

   ```bash
   # Using conda (recommended)
   conda create -n news-chatbot python=3.12
   conda activate news-chatbot
   
   # Or using venv
   python -m venv news-chatbot
   source news-chatbot/bin/activate  # On Windows: news-chatbot\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```env
   # Required: Clarifai API
   CLARIFAI_PAT=your_clarifai_personal_access_token_here
   
   # Required: Serper API for enhanced Google search
   SERPER_API_KEY=your_serper_api_key_here
   
   # Optional: Google ADK (for fallback search)
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_CSE_ID=your_custom_search_engine_id_here
   
   # Optional: Debug mode
   DEBUG=true
   ```

### 🔑 API Keys Setup

#### Clarifai API (Required)
1. Go to [Clarifai Portal](https://clarifai.com/settings/security)
2. Create a new Personal Access Token (PAT)
3. Copy the token to your `.env` file

#### Serper API (Required for Enhanced Search)
1. Visit [Serper.dev](https://serper.dev)
2. Sign up for a free account (100 free searches/month)
3. Get your API key from the dashboard
4. Add to `.env` file as `SERPER_API_KEY`

#### Google ADK (Optional Fallback)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Custom Search API
3. Create credentials and get your API key
4. Set up a Custom Search Engine at [Google CSE](https://cse.google.com/)

### 🏃 Running the Application

1. **Start the chatbot**

   ```bash
   streamlit run news_agent_clarifai.py
   ```

2. **Access the web interface**

   Open your browser and navigate to `http://localhost:8501`

3. **Start chatting!**

   Use the pre-built cards or ask questions like:
   - "What are the latest developments in AI?"
   - "Tell me about recent tech innovations"
   - "What's happening in the stock market?"

## 🛠️ MCP Tools Integration

The application supports Model Context Protocol (MCP) tools for enhanced functionality:

### Available MCP Tools

#### 1. News Summarize Tool
```json
{
  "name": "news_summarize",
  "description": "Summarize news articles with key insights",
  "parameters": {
    "query": "string - News topic to summarize",
    "max_articles": "number - Maximum articles to analyze (default: 5)"
  }
}
```

#### 2. News Trends Tool
```json
{
  "name": "news_trends",
  "description": "Analyze current news trends and patterns",
  "parameters": {
    "category": "string - News category (tech, business, health, etc.)",
    "timeframe": "string - Time period (24h, week, month)"
  }
}
```

#### 3. Source Credibility Checker
```json
{
  "name": "check_source_credibility",
  "description": "Evaluate news source credibility and bias",
  "parameters": {
    "source_url": "string - URL of the news source to check",
    "article_content": "string - Article content for analysis"
  }
}
```

### Running MCP Server

```bash
# Start the MCP server
python mcp_server.py

# The server will be available for tool integrations
# Default port: 8080
```

## 📁 Project Structure

```
mcp-news-adk/
├── 📄 news_agent_clarifai.py      # Main Streamlit application
├── 🔧 serper_search_tool.py       # Serper API integration
├── 🛠️ mcp_server.py               # MCP server implementation
├── 📋 requirements.txt            # Python dependencies
├── 🧪 test_serper_integration.py  # Integration tests
├── 📚 README.md                   # Project documentation
├── 📋 SoftwareSpec.md             # Technical specifications
├── 🚀 start.sh                    # Quick start script
├── 📊 status.sh                   # Status check script
├── 🛑 stop.sh                     # Stop script
└── 🔐 .env                        # Environment variables (create this)
```

## 🔧 Configuration

### Search Priority System

The application uses a priority-based search system:

1. **Primary**: Serper API (fastest, most comprehensive)
2. **Secondary**: Google ADK (reliable fallback)
3. **Fallback**: Basic search functionality

### Model Configuration

Supported AI models through Clarifai:
- `gpt-4o` (OpenAI GPT-4 Omni)
- `claude-3-5-sonnet-20241022` (Anthropic Claude 3.5)
- `llama-3.1-70b-instruct` (Meta LLaMA 3.1)

### Debugging

Enable debug mode in `.env`:
```env
DEBUG=true
```

This provides:
- Detailed API response logging
- Token usage statistics
- Performance metrics
- Error stack traces

## 🧪 Testing

Run the integration tests:

```bash
# Test Serper API integration
python test_serper_integration.py

# Expected output:
# ✅ Serper API connection successful
# ✅ Search functionality working
# ✅ NewsAgent integration functional
# ✅ AI analysis pipeline complete
```

## 🚀 Deployment

### Local Development
```bash
streamlit run news_agent_clarifai.py --server.port 8501
```

### Production Deployment
```bash
# Using Docker (create Dockerfile)
docker build -t news-chatbot .
docker run -p 8501:8501 news-chatbot

# Using cloud platforms
# - Streamlit Cloud
# - Heroku
# - AWS/GCP/Azure
```

## 📊 Performance Metrics

The application tracks:
- **Response Time**: Average AI response generation time
- **Token Usage**: Input/output tokens per request
- **Cost Tracking**: Estimated API costs per session
- **Search Performance**: Query response times and success rates

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**
   ```
   Error: Invalid Clarifai PAT
   Solution: Check your CLARIFAI_PAT in .env file
   ```

2. **Search Not Working**
   ```
   Error: No search results
   Solution: Verify SERPER_API_KEY and network connectivity
   ```

3. **Model Loading Issues**
   ```
   Error: Model not found
   Solution: Check Clarifai model availability and spelling
   ```

### Debug Mode

Enable comprehensive logging:
```env
DEBUG=true
```

View logs in the Streamlit interface sidebar.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Clarifai](https://clarifai.com) for AI model access
- [Serper.dev](https://serper.dev) for Google search API
- [Google ADK](https://developers.google.com) for search tools
- [Streamlit](https://streamlit.io) for the web framework
- [LiteLLM](https://litellm.ai) for unified AI model interface

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the debug logs in the application

---

**Made with ❤️ by [toswari-ai](https://github.com/toswari-ai)**
