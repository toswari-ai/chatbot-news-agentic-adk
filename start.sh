#!/bin/bash

# Clarifai News Chatbot Startup Script

# Cleanup function for graceful exit
cleanup() {
    echo ""
    echo "🛑 Startup interrupted. Cleaning up..."
    exit 1
}

# Set trap for cleanup on exit
trap cleanup SIGINT SIGTERM

echo "📰 Starting Clarifai News Chatbot..."

# check conda env agent_312
if conda env list | grep -q "agent_312"; then
    echo "✅ Conda environment 'agent_312' found"
else
    echo "❌ Conda environment 'agent_312' not found"
    #create conda env agent_312
    echo "Creating conda environment 'agent_312'..."
    conda create -n agent_312 python=3.12 -y
    echo "✅ Conda environment 'agent_312' created successfully"
fi

# Activate conda environment
echo "Activating conda environment 'agent_312'..."
source activate agent_312
echo "✅ Conda environment activated"

# Install dependencies
echo "Installing dependencies..."
if [ -f "requirements-minimal.txt" ]; then
    echo "Installing minimal requirements for basic functionality..."
    if conda run -n agent_312 pip install -r requirements-minimal.txt >/dev/null 2>&1; then
        echo "✅ Minimal requirements installed successfully"
    else
        echo "⚠️  Failed to install minimal requirements. Trying basic packages..."
        conda run -n agent_312 pip install streamlit python-dotenv || {
            echo "❌ Failed to install basic packages. Please check your internet connection."
            exit 1
        }
        echo "✅ Basic packages installed"
    fi
elif [ -f "requirements.txt" ]; then
    echo "Installing full requirements..."
    if conda run -n agent_312 pip install -r requirements.txt >/dev/null 2>&1; then
        echo "✅ Full requirements installed successfully"
    else
        echo "⚠️  Failed to install from requirements file. Trying essential packages..."
        conda run -n agent_312 pip install streamlit python-dotenv || {
            echo "❌ Failed to install essential packages. Please check your internet connection."
            exit 1
        }
        echo "✅ Essential packages installed"
    fi
else
    echo "⚠️  No requirements file found. Installing essential packages..."
    conda run -n agent_312 pip install streamlit python-dotenv || {
        echo "❌ Failed to install essential packages. Please check your internet connection."
        exit 1
    }
    echo "✅ Essential packages installed"
fi


# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ .env file created successfully!"
    else
        echo "⚠️  .env.example not found, creating basic .env file..."
        echo "# Clarifai News Chatbot Environment Variables" > .env
        echo "CLARIFAI_PAT=your_clarifai_personal_access_token_here" >> .env
        echo "✅ Basic .env file created!"
    fi
    echo "ℹ️  Note: News search uses Google ADK - no additional API keys required"
    echo "ℹ️  Optional: Set CLARIFAI_PAT in .env for AI-powered responses"
    echo ""
fi

# Run the application
echo "🚀 Starting Clarifai-powered news chatbot..."
echo "🌐 Access the app at: http://localhost:8501"
echo "🛑 To stop the app: Press Ctrl+C or run './stop.sh' in another terminal"
echo ""

# Check if CLARIFAI_PAT is set
if [ -f ".env" ] && grep -q "CLARIFAI_PAT=" .env && ! grep -q "CLARIFAI_PAT=your_clarifai" .env; then
    echo "✅ Clarifai PAT detected - AI features enabled"
else
    echo "ℹ️  Running without Clarifai PAT - basic functionality only"
    echo "💡 To enable AI features, add your Clarifai PAT to .env file"
fi
echo ""

# Configure logging environment variables
echo "🔧 Configuring debug logging..."

echo "✅ Debug logging enabled:"
echo "   - LiteLLM: DEBUG level"
echo "   - Python: INFO level"
echo "   - Streamlit: INFO level"
echo ""
echo "📊 Logger info will be displayed in the terminal output below"
echo "🔍 Look for messages with ✅, 🔧, ⚠️, and 🔴 emojis for agent status"
echo ""

# Run with environment variables passed to conda
LITELLM_LOG=DEBUG PYTHONPATH="${PYTHONPATH}:." STREAMLIT_LOGGER_LEVEL=INFO conda run -n agent_312 streamlit run app.py
