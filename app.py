"""
Clarifai News Chatbot - Streamlit Application
A sophisticated news chatbot built with Google ADK and Clarifai models via LiteLLM
"""

import streamlit as st
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from news_agent_clarifai import NewsAgent
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="📰 News Chatbot - Clarifai AI",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .sample-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #f8f9fa;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .sample-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 2px 8px rgba(31, 119, 180, 0.2);
    }
    .status-indicator {
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .status-connected {
        background-color: #d4edda;
        color: #155724;
    }
    .status-disconnected {
        background-color: #f8d7da;
        color: #721c24;
    }
    .status-partial {
        background-color: #fff3cd;
        color: #856404;
    }
    .status-card {
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #ffffff;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        color: #000000 !important;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #000000 !important;
    }
    .assistant-message {
        background-color: #1a1a1a;
        color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    .assistant-message * {
        color: #ffffff !important;
    }
    .assistant-message .content {
        line-height: 1.4;
        white-space: normal;
    }
    .assistant-message ul, .assistant-message ol {
        margin: 0.3rem 0;
        padding-left: 1.2rem;
    }
    .assistant-message li {
        margin: 0.1rem 0;
        line-height: 1.3;
    }
    .assistant-message p {
        margin: 0.3rem 0;
    }
    .assistant-message-content {
        background-color: #1a1a1a;
        color: #ffffff !important;
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 0.5rem;
    }
    .assistant-message-content * {
        color: #ffffff !important;
    }
    .assistant-message-content ul, .assistant-message-content ol {
        margin: 0.3rem 0;
        padding-left: 1.2rem;
    }
    .assistant-message-content li {
        margin: 0.1rem 0;
        line-height: 1.3;
    }
    .assistant-message-content p {
        margin: 0.3rem 0;
        line-height: 1.4;
    }
    .assistant-message-content h1, .assistant-message-content h2, .assistant-message-content h3 {
        color: #ffffff !important;
        margin: 0.5rem 0 0.3rem 0;
    }
        .user-message * {
        color: #000000 !important;
    }
    .llm-stats {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.8rem;
        color: #6c757d;
    }
    .llm-stats-dark {
        background-color: #2d2d2d;
        border: 1px solid #444444;
        color: #cccccc;
    }
    .stat-item {
        display: inline-block;
        margin-right: 1rem;
        margin-bottom: 0.2rem;
    }
    .stat-label {
        font-weight: bold;
    }
    .stats-container {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .stats-container-dark {
        background-color: #2d2d2d;
        border: 1px solid #444444;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'news_agent' not in st.session_state:
    st.session_state.news_agent = None
if 'clarifai_connected' not in st.session_state:
    st.session_state.clarifai_connected = False
if 'llm_stats' not in st.session_state:
    st.session_state.llm_stats = []

def process_assistant_content(content):
    """Process assistant content to improve formatting for Markdown"""
    import re
    
    # Keep numbered lists as they are for proper Markdown rendering
    # Markdown will handle the formatting automatically
    
    # Remove excessive line breaks (more than 2 consecutive newlines)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Ensure proper spacing around headers
    content = re.sub(r'\n(#+\s)', r'\n\n\1', content)
    
    # Ensure proper spacing around lists
    content = re.sub(r'\n(\d+\.\s|\*\s|-\s)', r'\n\1', content)
    
    return content.strip()

def calculate_tokens(text):
    """Estimate token count (approximate)"""
    # Simple approximation: ~4 characters per token for English text
    return len(text) // 4

def format_llm_stats(prompt, response, duration, model_name):
    """Format LLM statistics for display"""
    prompt_tokens = calculate_tokens(prompt)
    response_tokens = calculate_tokens(response)
    total_tokens = prompt_tokens + response_tokens
    tokens_per_second = response_tokens / duration if duration > 0 else 0
    
    return {
        "model": model_name,
        "prompt_tokens": prompt_tokens,
        "response_tokens": response_tokens,
        "total_tokens": total_tokens,
        "duration": duration,
        "tokens_per_second": tokens_per_second
    }

def display_llm_stats(stats, dark_theme=True):
    """Display LLM statistics as HTML"""
    theme_class = "llm-stats-dark" if dark_theme else ""
    
    stats_html = f"""
    <div class="llm-stats {theme_class}">
        <div class="stat-item">
            <span class="stat-label">Model:</span> {stats['model']}
        </div>
        <div class="stat-item">
            <span class="stat-label">Prompt Tokens:</span> {stats['prompt_tokens']:,}
        </div>
        <div class="stat-item">
            <span class="stat-label">Response Tokens:</span> {stats['response_tokens']:,}
        </div>
        <div class="stat-item">
            <span class="stat-label">Total Tokens:</span> {stats['total_tokens']:,}
        </div>
        <div class="stat-item">
            <span class="stat-label">Duration:</span> {stats['duration']:.2f}s
        </div>
        <div class="stat-item">
            <span class="stat-label">Tokens/sec:</span> {stats['tokens_per_second']:.1f}
        </div>
    </div>
    """
    return stats_html

def initialize_agent(model_name):
    """Initialize the news agent with selected model"""
    try:
        agent = NewsAgent(model_name=model_name)
        st.session_state.news_agent = agent
        st.session_state.clarifai_connected = agent.test_connection()
        return True
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return False

def test_clarifai_connection():
    """Test Clarifai connection"""
    try:
        clarifai_pat = os.getenv('CLARIFAI_PAT')
        if not clarifai_pat or clarifai_pat == 'your_clarifai_personal_access_token_here':
            return False
        
        # Simple test to verify connection
        if st.session_state.news_agent:
            return st.session_state.news_agent.test_connection()
        
        # If no agent yet, just check if PAT is set
        return len(clarifai_pat.strip()) > 20  # Basic validation
        
    except Exception as e:
        # If there's an error, but we have a PAT, assume it might work
        clarifai_pat = os.getenv('CLARIFAI_PAT', '')
        return bool(clarifai_pat and clarifai_pat != 'your_clarifai_personal_access_token_here')

# Sidebar configuration
with st.sidebar:
    st.header("🛠️ Configuration")
    
    # Model selection
    st.subheader("🤖 Model Selection")
    model_options = [
        "gpt-4o",
        "gpt-4o-mini", 
        "claude-3-5-sonnet-20241022",
        "meta-llama/Meta-Llama-3.1-8B-Instruct"
    ]
    
    selected_model = st.selectbox(
        "Choose AI Model:",
        model_options,
        index=0,
        help="Select the AI model for news analysis and responses"
    )
    
    # Initialize agent when model changes
    if st.session_state.news_agent is None or st.session_state.get('current_model') != selected_model:
        with st.spinner("Initializing agent..."):
            if initialize_agent(selected_model):
                st.session_state.current_model = selected_model
                st.success(f"✅ Agent initialized with {selected_model}")
            else:
                st.error("❌ Failed to initialize agent")
    
    # Connection status
    st.subheader("📡 Connection Status")
    connection_status = test_clarifai_connection()
    
    if connection_status:
        st.markdown('<div class="status-indicator status-connected">🟢 Clarifai Connected</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-disconnected">🔴 Clarifai Disconnected</div>', 
                   unsafe_allow_html=True)
        st.warning("⚠️ Set CLARIFAI_PAT in .env file for AI features")
    
    # Agent status
    if st.session_state.news_agent:
        st.markdown('<div class="status-indicator status-connected">🟢 Agent Ready</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-indicator status-disconnected">🔴 Agent Not Ready</div>', 
                   unsafe_allow_html=True)
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.llm_stats = []
        st.rerun()
    
    # Refresh connection button
    if st.button("🔄 Refresh Connection", use_container_width=True):
        st.session_state.clarifai_connected = test_clarifai_connection()
        st.rerun()
    
    # LLM Statistics section
    st.subheader("📊 LLM Statistics")
    if st.session_state.llm_stats:
        latest_stats = st.session_state.llm_stats[-1]
        
        # Show total stats
        total_tokens = sum(stat['total_tokens'] for stat in st.session_state.llm_stats)
        total_responses = len(st.session_state.llm_stats)
        avg_speed = sum(stat['tokens_per_second'] for stat in st.session_state.llm_stats) / total_responses
        
        # Create a styled container for the statistics
        stats_content = f"""
        <div class="stats-container stats-container-dark">
            <div style="margin-bottom: 1rem;">
                <strong>Latest Response:</strong><br>
                • <strong>Model:</strong> <code>{latest_stats['model']}</code><br>
                • <strong>Tokens:</strong> {latest_stats['total_tokens']:,}<br>
                • <strong>Speed:</strong> {latest_stats['tokens_per_second']:.1f} tok/sec<br>
                • <strong>Duration:</strong> {latest_stats['duration']:.2f}s
            </div>
            <hr style="border-color: #444444; margin: 0.5rem 0;">
            <div>
                <strong>Session Totals:</strong><br>
                • <strong>Total Tokens:</strong> {total_tokens:,}<br>
                • <strong>Responses:</strong> {total_responses}<br>
                • <strong>Avg Speed:</strong> {avg_speed:.1f} tok/sec
            </div>
        </div>
        """
        
        st.markdown(stats_content, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Stats", use_container_width=True):
            st.session_state.llm_stats = []
            st.rerun()
    else:
        st.info("No statistics available yet. Send a message to see LLM performance metrics.")

# Main header
st.markdown("""
<div class="main-header">
    <h1>📰 News Chatbot</h1>
    <p>Powered by Clarifai AI & Google ADK</p>
</div>
""", unsafe_allow_html=True)

# Sample query cards
st.subheader("🎯 Quick Start - Sample Queries")

col1, col2, col3 = st.columns(3)

sample_queries = [
    {
        "title": "🌍 World News",
        "description": "Latest global news and events",
        "query": "What are the top 5 world news stories today?"
    },
    {
        "title": "💼 Tech & Business", 
        "description": "Technology and business updates",
        "query": "What are the latest developments in AI and technology?"
    },
    {
        "title": "🏥 Health & Science",
        "description": "Health and scientific breakthroughs", 
        "query": "What are the recent medical and scientific discoveries?"
    }
]

for i, (col, sample) in enumerate(zip([col1, col2, col3], sample_queries)):
    with col:
        if st.button(
            f"**{sample['title']}**\n\n{sample['description']}", 
            key=f"sample_{i}",
            use_container_width=True
        ):
            # Add sample query to chat
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({
                "role": "user", 
                "content": sample['query'],
                "timestamp": timestamp
            })
            
            # Process the query immediately
            with st.spinner("🤖 News AI is thinking..."):
                try:
                    if st.session_state.news_agent:
                        st.write("🔍 Processing your query...")  # Debug output
                        
                        # Track timing for statistics
                        import time
                        start_time = time.time()
                        
                        response = st.session_state.news_agent.search_and_analyze(sample['query'])
                        
                        # Calculate duration and statistics
                        end_time = time.time()
                        duration = end_time - start_time
                        
                        # Add assistant response
                        response_timestamp = datetime.now().strftime("%H:%M:%S")
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response,
                            "timestamp": response_timestamp
                        })
                        
                        # Calculate and store LLM statistics
                        current_model = st.session_state.get('current_model', 'Unknown')
                        stats = format_llm_stats(sample['query'], response, duration, current_model)
                        st.session_state.llm_stats.append(stats)
                        
                        st.write("✅ Response generated!")  # Debug output
                        
                    else:
                        error_msg = "❌ News agent is not initialized. Please check your configuration."
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg,
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
                        st.error("Agent not ready")
                        
                except Exception as e:
                    error_msg = f"❌ Error generating response: {str(e)}"
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    st.error(f"Error: {str(e)}")  # Debug output
            
            st.rerun()

st.divider()

# Chat interface
st.subheader("💬 Chat with News AI")

# Display chat messages
for message in st.session_state.messages:
    timestamp = message.get('timestamp', '')
    
    if message["role"] == "user":
        # Escape HTML in message content to prevent rendering issues
        import html
        escaped_content = html.escape(message["content"])
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You</strong> <small>{timestamp}</small><br>
            <div style="white-space: pre-wrap;">{escaped_content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Process content and render as Markdown
        processed_content = process_assistant_content(message["content"])
        
        # Render everything in a single container
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 News AI</strong> <small>{timestamp}</small><br>
        """, unsafe_allow_html=True)
        st.markdown(processed_content)
        
        # Find and display corresponding LLM statistics
        message_index = len(st.session_state.messages) - 1 - list(reversed(st.session_state.messages)).index(message)
        if message_index < len(st.session_state.llm_stats):
            stats = st.session_state.llm_stats[message_index]
            stats_html = display_llm_stats(stats, dark_theme=True)
            st.markdown(stats_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask me about news, current events, or any topic..."):
    # Add user message
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Display user message immediately
    import html
    escaped_prompt = html.escape(prompt)
    st.markdown(f"""
    <div class="chat-message user-message">
        <strong>👤 You</strong> <small>{timestamp}</small><br>
        <div style="white-space: pre-wrap;">{escaped_prompt}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate response
    with st.spinner("🤖 News AI is thinking..."):
        try:
            if st.session_state.news_agent:
                # Track timing for statistics
                import time
                start_time = time.time()
                
                response = st.session_state.news_agent.search_and_analyze(prompt)
                
                # Calculate duration and statistics
                end_time = time.time()
                duration = end_time - start_time
                
                # Add assistant response
                response_timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "timestamp": response_timestamp
                })
                
                # Calculate and store LLM statistics
                current_model = st.session_state.get('current_model', 'Unknown')
                stats = format_llm_stats(prompt, response, duration, current_model)
                st.session_state.llm_stats.append(stats)
                
                # Display assistant response with Markdown rendering
                processed_response = process_assistant_content(response)
                
                # Render everything in a single container
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 News AI</strong> <small>{response_timestamp}</small><br>
                """, unsafe_allow_html=True)
                st.markdown(processed_response)
                
                # Display LLM statistics for this response
                stats_html = display_llm_stats(stats, dark_theme=True)
                st.markdown(stats_html, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                error_msg = "❌ News agent is not initialized. Please check your configuration."
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                st.error(error_msg)
                
        except Exception as e:
            error_msg = f"❌ Error generating response: {str(e)}"
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_msg,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.error(error_msg)
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    🔥 Powered by <strong>Clarifai AI</strong> • 🛠️ Built with <strong>Google ADK</strong> • 
    ⚡ Enhanced by <strong>LiteLLM</strong> • 🎨 Designed with <strong>Streamlit</strong>
</div>
""", unsafe_allow_html=True)
