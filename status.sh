#!/bin/bash

# Weather Chatbot Status Check Script

echo "🔍 Weather Chatbot Status Check"
echo "================================"
echo ""

# Check for running Streamlit processes
echo "📱 Streamlit Applications:"
streamlit_processes=$(pgrep -f "streamlit")
if [ -n "$streamlit_processes" ]; then
    echo "✅ Running Streamlit processes found:"
    ps aux | grep streamlit | grep -v grep | while read line; do
        echo "   $line"
    done
else
    echo "❌ No Streamlit processes running"
fi
echo ""

# Check for Python weather app processes
echo "🐍 Python Weather App Processes:"
weather_processes=$(pgrep -f "app.py")
if [ -n "$weather_processes" ]; then
    echo "✅ Running weather app processes found:"
    ps aux | grep -E "(app\.py)" | grep -v grep | while read line; do
        echo "   $line"
    done
else
    echo "❌ No weather app processes running"
fi
echo ""

# Check ports
echo "🌐 Port Status:"
check_port() {
    local port=$1
    local service=$2
    if lsof -i:$port >/dev/null 2>&1; then
        local pid=$(lsof -ti:$port 2>/dev/null)
        echo "✅ Port $port ($service): In use by PID $pid"
    else
        echo "❌ Port $port ($service): Available"
    fi
}

check_port 8501 "Streamlit Default"
check_port 8502 "Streamlit Alt"
check_port 8503 "Streamlit Alt 2"
echo ""

# Check application files
echo "📂 Application Files:"
files=("app.py" "start.sh" "stop.sh" "requirements.txt")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done
echo ""

# Check virtual environment
echo "🐍 Virtual Environment:"
if [ -d "venv" ]; then
    echo "✅ Virtual environment 'venv' exists"
    if [ -f "venv/bin/activate" ]; then
        echo "✅ Virtual environment activation script found"
    else
        echo "❌ Virtual environment activation script missing"
    fi
else
    echo "❌ Virtual environment 'venv' not found"
fi
echo ""

# Quick dependency check
echo "📦 Dependencies:"
if command -v python3 >/dev/null 2>&1; then
    echo "✅ Python3 available"
    
    # Check if we're in a virtual environment
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "✅ Virtual environment active: $VIRTUAL_ENV"
    else
        echo "⚠️  No virtual environment active"
    fi
    
    # Check for key packages
    if python3 -c "import streamlit" 2>/dev/null; then
        echo "✅ Streamlit installed"
    else
        echo "❌ Streamlit not installed"
    fi
    
    if python3 -c "import requests" 2>/dev/null; then
        echo "✅ Requests installed"
    else
        echo "❌ Requests not installed"
    fi
else
    echo "❌ Python3 not available"
fi
echo ""

# Summary and recommendations
echo "📋 Summary:"
if [ -n "$streamlit_processes" ]; then
    echo "🟢 Weather Chatbot is currently RUNNING"
    echo "   Access it at: http://localhost:8501"
    echo "   To stop: ./stop.sh"
else
    echo "🔴 Weather Chatbot is currently STOPPED"
    echo "   To start: ./start.sh"
fi
echo ""
echo "🆘 Commands:"
echo "   ./start.sh   - Start the weather chatbot"
echo "   ./stop.sh    - Stop the weather chatbot"
echo "   ./status.sh  - Show this status (current script)"
