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
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
        color: #000000 !important;
    }
    .assistant-message * {
        color: #000000 !important;
    }
    .user-message * {
        color: #000000 !important;
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
        st.rerun()
    
    # Refresh connection button
    if st.button("🔄 Refresh Connection", use_container_width=True):
        st.session_state.clarifai_connected = test_clarifai_connection()
        st.rerun()

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
                        response = st.session_state.news_agent.search_and_analyze(sample['query'])
                        
                        # Add assistant response
                        response_timestamp = datetime.now().strftime("%H:%M:%S")
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response,
                            "timestamp": response_timestamp
                        })
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
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You</strong> <small>{timestamp}</small><br>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 News AI</strong> <small>{timestamp}</small><br>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

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
    st.markdown(f"""
    <div class="chat-message user-message">
        <strong>👤 You</strong> <small>{timestamp}</small><br>
        {prompt}
    </div>
    """, unsafe_allow_html=True)
    
    # Generate response
    with st.spinner("🤖 News AI is thinking..."):
        try:
            if st.session_state.news_agent:
                response = st.session_state.news_agent.search_and_analyze(prompt)
                
                # Add assistant response
                response_timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "timestamp": response_timestamp
                })
                
                # Display assistant response
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 News AI</strong> <small>{response_timestamp}</small><br>
                    {response}
                </div>
                """, unsafe_allow_html=True)
                
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
