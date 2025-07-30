# 📰 Clarifai News Chatbot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Clarifai](https://img.shields.io/badge/Clarifai-API-orange.svg)](https://clarifai.com)
[![Google ADK](https://img.shields.io/badge/Google-ADK-green.svg)](https://developers.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🤖 **AI-powered news chatbot** built with Clarifai API, Google Agent Development Kit (ADK), and Streamlit for intelligent news search and analysis.

## ✨ Features

- 🌐 **Real-time News Search** - Powered by Google ADK and MCP tools
- 🤖 **AI-powered Analysis** - Multiple model support via Clarifai API
- 💬 **Interactive Chat Interface** - Beautiful Streamlit web application with modern dark theme
- 🎯 **Quick Start Cards** - Pre-built queries for World News, Tech & Business, Health & Science
- 🔄 **Model Selection** - Support for GPT-4o, Claude 3.5 Sonnet, LLaMA models
- 📊 **LLM Statistics Tracking** - Real-time token usage, response times, and performance metrics
- 📱 **Responsive Design** - Mobile-friendly interface with modern black/white styling
- 🔍 **Debug Mode** - Comprehensive logging for troubleshooting
- ⚡ **LiteLLM Integration** - Unified interface for multiple AI providers
- 📈 **Performance Analytics** - Session-wide statistics and per-message metrics
- 🎨 **Enhanced UI/UX** - Markdown rendering, styled containers, and professional design

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  News Agent     │────│  Clarifai API   │
│   (Frontend)    │    │  (Core Logic)   │    │  (AI Models)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────│  Google ADK     │-─────────────┘
                        │  (News Search)  │
                        └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Conda or pip package manager
- Clarifai Personal Access Token
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

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your credentials:

   ```env
   CLARIFAI_PAT=your_clarifai_personal_access_token_here
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
   ```

5. **Start the application**

   ```bash
   # Using the start script
   ./start.sh
   
   # Or manually
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501` to access the chatbot interface.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `CLARIFAI_PAT` | Clarifai Personal Access Token | ✅ Yes | None |
| `GOOGLE_API_KEY` | Google Custom Search API Key | ⚠️ Optional | None |
| `GOOGLE_SEARCH_ENGINE_ID` | Google Search Engine ID | ⚠️ Optional | None |
| `LITELLM_LOG` | Enable LiteLLM debug logging | ❌ No | `INFO` |

### Getting API Keys

#### Clarifai Personal Access Token

1. Sign up at [Clarifai](https://clarifai.com)
2. Navigate to Settings → Security
3. Create a new Personal Access Token
4. Copy the token to your `.env` file

#### Google Custom Search API (Optional)

1. Visit [Google Cloud Console](https://console.cloud.google.com)
2. Enable the Custom Search JSON API
3. Create credentials and get your API key
4. Set up a Custom Search Engine at [Google CSE](https://cse.google.com)

## 🎯 Usage

### Sample Queries

The chatbot comes with three pre-built query cards:

- **🌍 World News**: "What are the top 5 world news stories today?"
- **💼 Tech & Business**: "What are the latest developments in AI and technology?"
- **🏥 Health & Science**: "What are the recent medical and scientific discoveries?"

### Custom Queries

You can ask about any topic using natural language:

```
"Tell me about the latest climate change developments"
"What's happening in the stock market today?"
"Any recent breakthroughs in quantum computing?"
"Summary of today's political news"
```

### Model Selection

Choose from multiple AI models in the sidebar:

- **GPT-4o** - OpenAI's latest flagship model
- **GPT-4o Mini** - Faster, cost-effective version
- **Claude 3.5 Sonnet** - Anthropic's advanced model
- **LLaMA 3.1 8B** - Meta's open-source model

### 📊 LLM Statistics & Performance Monitoring

The application provides comprehensive real-time analytics for LLM usage:

#### Sidebar Statistics Panel
- **Latest Response Metrics**: Model used, tokens consumed, response speed, duration
- **Session Totals**: Cumulative token usage, total responses, average speed
- **Performance Tracking**: Tokens per second, response timing analysis

#### Per-Message Statistics
Each AI response includes detailed performance metrics:
- **Model Information**: Which AI model processed the request
- **Token Breakdown**: Prompt tokens, response tokens, total usage
- **Performance Data**: Response duration and processing speed
- **Cost Estimation**: Token usage for billing and optimization

#### Key Metrics Tracked
- 🔢 **Token Usage**: Prompt tokens, response tokens, total consumption
- ⏱️ **Response Time**: Processing duration in seconds
- 🚀 **Speed**: Tokens generated per second
- 📈 **Session Analytics**: Cumulative statistics across the session
- 🎯 **Model Performance**: Compare efficiency across different AI models

This helps users:
- Monitor API usage and costs
- Compare model performance
- Optimize query efficiency
- Track session productivity

### 🎨 Enhanced User Interface

The application features a modern, professional interface with:

#### Dark Theme Design
- **Modern Styling**: Black backgrounds with white text for reduced eye strain
- **Styled Containers**: Consistent design language across all UI components
- **Professional Layout**: Clean, organized interface with intuitive navigation

#### Interactive Elements
- **Markdown Rendering**: Full support for formatted text, lists, and headers
- **Responsive Design**: Optimized for desktop and mobile devices
- **Quick Start Cards**: One-click access to popular query types
- **Real-time Updates**: Live statistics and performance monitoring

#### Visual Features
- **Status Indicators**: Color-coded connection and agent status
- **Statistics Containers**: Styled boxes for performance metrics display
- **Message Styling**: Distinct formatting for user and AI messages
- **Loading States**: Professional spinners and progress indicators

## 🧪 Testing

### Run Unit Tests

```bash
# Test Clarifai connection
python test_clarifai.py

# Test full chatbot functionality
python test_chatbot.py
```

### Debug Mode

Enable detailed logging by setting environment variable:

```bash
export LITELLM_LOG=DEBUG
./start.sh
```

## 📁 Project Structure

```
chatbot-news-agentic-adk/
├── 📄 app.py                 # Main Streamlit application
├── 🤖 news_agent_clarifai.py # Core agent logic with Clarifai integration
├── ⚙️ config.py              # Configuration management
├── 📋 requirements.txt       # Python dependencies
├── 📋 requirements-minimal.txt # Minimal dependencies
├── 🔧 .env.example           # Environment variables template
├── 🚀 start.sh              # Application launcher script
├── 📊 status.sh             # Status monitoring script
├── 🛑 stop.sh               # Application terminator script
├── 🧪 test_clarifai.py      # Clarifai API tests
├── 🧪 test_chatbot.py       # Chatbot functionality tests
├── 📚 README.md             # This documentation
├── 📋 SoftwareSpec.md       # Technical specifications
├── 📄 LICENSE               # MIT License
└── 🚫 .gitignore            # Git ignore rules
```

## 🔍 API Integration

### Clarifai Models

The chatbot supports multiple Clarifai models through LiteLLM:

```python
# Model format for Clarifai
model_format = "openai/openai/chat-completion/models/{model_name}"

# Supported models
models = [
    "gpt-4o",
    "gpt-4o-mini",
    "claude-3-5-sonnet-20241022",
    "meta-llama/Meta-Llama-3.1-8B-Instruct"
]
```

### News Search Integration

```python
# Google ADK integration with fallback
try:
    from google_adk import search_news
    results = search_news(query)
except ImportError:
    # Fallback to mock results
    results = generate_mock_news(query)
```

## 🎨 UI Features

### Design Elements

- **Gradient Header** - Eye-catching blue-orange gradient
- **Sample Cards** - Interactive query buttons with hover effects
- **Chat Interface** - Clean message bubbles with timestamps
- **Dark Theme Support** - Proper text contrast for all themes
- **Responsive Layout** - Mobile-friendly column design

### Custom CSS Styling

- Message bubbles with distinct colors for user/assistant
- Status indicators with green/red color coding
- Hover animations for interactive elements
- Professional typography and spacing

## 🐛 Troubleshooting

### Common Issues

#### 1. Clarifai Connection Failed

```bash
# Check your PAT token
echo $CLARIFAI_PAT

# Test connection manually
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('PAT:', os.getenv('CLARIFAI_PAT')[:10] + '...')
"
```

#### 2. Model Not Found Error

- Ensure your Clarifai account has access to the selected model
- Try switching to `gpt-4o-mini` which is more widely available
- Check Clarifai documentation for model availability

#### 3. News Search Not Working

- Google ADK is optional; the app uses mock results as fallback
- Check Google API credentials if using real search
- Verify search engine configuration

#### 4. Streamlit Port Already in Use

```bash
# Kill existing Streamlit processes
pkill -f streamlit

# Or use a different port
streamlit run app.py --server.port 8502
```

### Debug Information

Enable comprehensive logging:

```bash
export LITELLM_LOG=DEBUG
export STREAMLIT_LOGGER_LEVEL=DEBUG
./start.sh
```

Check the terminal output for detailed API requests and responses.

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests before submitting
python test_clarifai.py
python test_chatbot.py

# Format code (optional)
black app.py news_agent_clarifai.py
```

## 🆕 Recent Updates

### Version 1.2.0 - LLM Analytics & Enhanced UI (January 2025)

#### ✨ New Features
- **📊 LLM Statistics Tracking**: Real-time monitoring of token usage, response times, and performance metrics
- **🎨 Enhanced Dark Theme**: Modern black/white styling with professional visual design
- **📈 Performance Analytics**: Session-wide statistics and per-message metrics display
- **📝 Improved Markdown**: Enhanced text rendering with proper formatting support
- **🔧 Styled Containers**: Consistent design language across all UI components

#### 🚀 Performance Improvements
- **Optimized Token Counting**: Accurate estimation for cost monitoring
- **Response Timing**: Precise duration tracking for performance analysis
- **Statistics Caching**: Efficient session state management
- **UI Responsiveness**: Faster rendering of statistics and chat messages

#### 🐛 Bug Fixes
- Fixed statistics container HTML structure for proper styling
- Improved message formatting and display consistency
- Enhanced error handling for API failures
- Better mobile responsiveness and layout stability

## 📋 Roadmap

- [ ] **Enhanced News Sources** - Integration with multiple news APIs
- [ ] **Real-time Updates** - WebSocket support for live news feeds
- [ ] **User Preferences** - Customizable news categories and sources
- [ ] **Export Features** - Save conversations and news summaries
- [ ] **Multi-language Support** - International news in various languages
- [ ] **Advanced Analytics** - News sentiment analysis and trends
- [ ] **Mobile App** - React Native or Flutter implementation

## 📊 Performance

### Metrics

- **Response Time**: ~2-3 seconds for news analysis
- **Model Support**: 4+ AI models via Clarifai
- **Concurrent Users**: Supports multiple Streamlit sessions
- **Memory Usage**: ~200MB base + model overhead

### Optimization Tips

- Use `gpt-4o-mini` for faster responses
- Enable caching for repeated queries
- Monitor token usage in debug mode

## 🏆 Acknowledgments

- **[Clarifai](https://clarifai.com)** - AI model hosting and inference
- **[Google ADK](https://developers.google.com)** - Agent Development Kit and tools
- **[LiteLLM](https://github.com/BerriAI/litellm)** - Unified LLM interface
- **[Streamlit](https://streamlit.io)** - Web application framework
- **[OpenAI](https://openai.com)** - GPT model development
- **[Anthropic](https://anthropic.com)** - Claude model development
- **[Meta](https://ai.meta.com)** - LLaMA model development

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/toswari-ai/chatbot-news-agentic-adk/issues)
- **Discussions**: [Community discussions](https://github.com/toswari-ai/chatbot-news-agentic-adk/discussions)
- **Documentation**: This README and inline code comments

---

<div align="center">

**🌟 Star this repo if you find it useful! 🌟**

Made with ❤️ by [toswari-ai](https://github.com/toswari-ai)

</div>
