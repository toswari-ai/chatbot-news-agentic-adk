# Software Specification - Clarifai News Chatbot

## 🎯 Project Goals

- Provide comprehensive Streamlit application utilizing Google ADK and LiteLLM for Clarifai inference
- Build intelligent chatbot for news searches and analysis
- Implement modern UI/UX with dark theme and professional styling
- Provide real-time LLM performance monitoring and analytics
- Support multiple AI models with unified interface

## 🏗️ Core Features

### User Interface Components

- **Main Chat Interface**: Interactive conversation with AI assistant
- **Sample Query Cards**: 3 pre-built query options (World News, Tech & Business, Health & Science)
- **Sidebar Configuration**: Model selection, connection status, and controls
- **Real-time Statistics**: LLM performance monitoring and analytics
- **Modern Dark Theme**: Professional black/white styling with responsive design

### Sidebar Features

- **AI Model Selection**: Support for GPT-4o, GPT-4o Mini, Claude 3.5 Sonnet, LLaMA 3.1 8B
- **Response Settings**: Toggle for streaming vs non-streaming responses
- **Connection Status**: Real-time Clarifai API and agent status indicators
- **Control Buttons**: Clear chat, refresh connection, clear statistics
- **LLM Statistics Panel**: Comprehensive performance metrics display

### Analytics & Performance Monitoring

- **Token Tracking**: Real-time prompt, response, and total token counting
- **Performance Metrics**: Response time, tokens per second, duration analysis
- **Session Analytics**: Cumulative statistics, average performance, response tracking
- **Visual Statistics**: Styled containers with professional metric display

## 🛠️ Technical Implementation

### Python Environment

- **Environment Name**: `agent_312`
- **Python Version**: 3.12
- **Auto-creation**: If environment doesn't exist, create using `python=3.12`
- **Package Management**: pip with requirements.txt

### Core Agents

- **News Search Agent**: Utilizes Google ADK for intelligent news retrieval
- **MCP Tool Integration**: Model Context Protocol for tool execution
- **LiteLLM Agent**: Unified interface for multiple AI model providers
- **Statistics Engine**: Real-time performance tracking and analytics

### Architecture Components

#### Frontend (Streamlit)

- **app.py**: Main application with enhanced UI and statistics tracking
- **Custom CSS**: Modern dark theme styling with responsive design
- **Interactive Elements**: Markdown rendering, styled containers, status indicators
- **Real-time Updates**: Live statistics and performance monitoring

#### Backend (Agent Logic)

- **news_agent_clarifai.py**: Core agent with Clarifai API integration
- **LiteLLM Integration**: Multi-model support with unified interface
- **Token Calculation**: Accurate estimation for cost monitoring
- **Performance Tracking**: Duration timing and speed analytics

#### Configuration

- **Environment Variables**: Secure API key management
- **Model Configuration**: Dynamic model switching and initialization
- **Connection Management**: Robust error handling and status monitoring

## 📊 Enhanced Features (Version 1.2.0)

### LLM Statistics & Analytics

- **Real-time Token Counting**: Accurate prompt and response token estimation
- **Performance Metrics**: Response timing, tokens per second, duration tracking
- **Session Management**: Cumulative statistics across user interactions
- **Visual Display**: Styled statistics containers with dark theme integration

### UI/UX Improvements

- **Dark Theme Design**: Modern black backgrounds with white text
- **Professional Styling**: Consistent design language across components
- **Markdown Support**: Enhanced text rendering with formatting support
- **Responsive Layout**: Optimized for desktop and mobile devices
- **Status Indicators**: Color-coded connection and agent status displays

### Advanced Functionality

- **Multi-model Support**: Seamless switching between AI models
- **Error Handling**: Comprehensive exception management and user feedback
- **Debug Logging**: Detailed information for troubleshooting
- **Performance Optimization**: Efficient session state management

## 🔧 Configuration Requirements

### API Keys & Environment

```env
CLARIFAI_PAT=your_clarifai_personal_access_token_here
GOOGLE_API_KEY=your_google_api_key_here (optional)
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here (optional)
LITELLM_LOG=INFO
```

### Supported Models

- **OpenAI**: GPT-4o, GPT-4o Mini
- **Anthropic**: Claude 3.5 Sonnet (20241022)
- **Meta**: LLaMA 3.1 8B Instruct
- **Future**: Extensible for additional model providers

## 🚀 Launch Specifications

### Startup Process

- **Script**: `start.sh` with enhanced logging
- **Port**: Default Streamlit port 8501
- **Auto-initialization**: Automatic agent setup with selected model
- **Status Monitoring**: Real-time connection and performance tracking

### Deployment Requirements

- **Dependencies**: requirements.txt with all necessary packages
- **Environment**: Conda environment with Python 3.12
- **Security**: Environment variable-based configuration
- **Monitoring**: Built-in status checking and error reporting

## 📈 Performance Targets

### Response Metrics

- **Average Response Time**: 2-3 seconds for news analysis
- **Token Processing**: Efficient counting and tracking
- **Memory Usage**: ~200MB base + model overhead
- **Concurrent Support**: Multiple Streamlit sessions

### User Experience

- **Interface Responsiveness**: < 100ms UI updates
- **Real-time Statistics**: Live performance monitoring
- **Error Recovery**: Graceful handling of API failures
- **Professional Design**: Modern, intuitive interface

## 🔗 Technical References

### Google ADK Integration

- [Clarifai Examples - Google ADK](https://github.com/Clarifai/examples/tree/main/agents/Google-ADK)
- [Google ADK Built-in Tools](https://google.github.io/adk-docs/tools/built-in-tools/#use-built-in-tools-with-other-tools)
- [MCP Tools with ADK](https://google.github.io/adk-docs/tools/mcp-tools/#step-1-define-your-agent-with-mcptoolset)
- [MCP Tools Outside ADK Web](https://google.github.io/adk-docs/tools/mcp-tools/#using-mcp-tools-in-your-own-agent-out-of-adk-web)

### LiteLLM & Model Integration

- [LiteLLM Documentation](https://github.com/BerriAI/litellm)
- [Clarifai API Documentation](https://docs.clarifai.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

### Additional Resources

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Meta LLaMA Documentation](https://ai.meta.com/llama/)

## 📋 Implementation Checklist

### Core Functionality ✅

- [x] Streamlit application with modern UI
- [x] Google ADK integration for news search
- [x] LiteLLM integration for multi-model support
- [x] Clarifai API integration
- [x] Sample query cards implementation
- [x] Sidebar model selection
- [x] Chat interface with message history

### Enhanced Features ✅

- [x] LLM statistics tracking and display
- [x] Dark theme with professional styling
- [x] Real-time performance monitoring
- [x] Token counting and cost estimation
- [x] Responsive design and mobile support
- [x] Error handling and status indicators
- [x] Markdown rendering support
- [x] **Streaming Responses** - Real-time AI text generation with live updates

### Future Enhancements 🔄

- [x] **Streaming Responses** - Real-time LLM response streaming for better user experience
- [ ] Multi-language support
- [ ] Export conversation functionality
- [ ] Advanced analytics dashboard
- [ ] Custom news source integration
- [ ] Real-time news notifications
- [ ] User preference management
- [ ] Integrate Serper API for live search

## Sample code for serper ai search

import requests
import json

url = "<https://google.serper.dev/search>"

payload = json.dumps({
  "q": "top 5 news today"
})
headers = {
  'X-API-KEY': '9c82fd604ec4e106e845ac732c5a9c3fae947140',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

## 🎯 Success Criteria

### Functional Requirements

1. **News Search**: Accurate retrieval and analysis of current news
2. **AI Integration**: Successful inference with multiple models
3. **User Experience**: Intuitive interface with professional design
4. **Performance**: Sub-3 second response times for most queries
5. **Reliability**: Graceful error handling and recovery

### Non-Functional Requirements

1. **Scalability**: Support for multiple concurrent users
2. **Maintainability**: Clean, documented, and modular code
3. **Security**: Secure API key management and data handling
4. **Monitoring**: Comprehensive logging and performance tracking
5. **Accessibility**: Responsive design for various devices and screen sizes

---
