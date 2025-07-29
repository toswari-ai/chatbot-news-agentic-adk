#!/bin/bash

# Weather Chatbot Stop Script

echo "🛑 Stopping Weather Chatbot..."

# Function to kill processes by name
kill_processes() {
    local process_name=$1
    local pids=$(pgrep -f "$process_name")
    
    if [ -n "$pids" ]; then
        echo "Found $process_name processes: $pids"
        echo "Stopping $process_name processes..."
        pkill -f "$process_name"
        sleep 2
        
        # Force kill if still running
        local remaining=$(pgrep -f "$process_name")
        if [ -n "$remaining" ]; then
            echo "Force killing remaining $process_name processes..."
            pkill -9 -f "$process_name"
        fi
        echo "✅ $process_name processes stopped"
    else
        echo "ℹ️  No $process_name processes found"
    fi
}

# Stop Streamlit applications
kill_processes "streamlit"

# Stop any Python scripts related to the weather app
kill_processes "app.py"
kill_processes "weather_mcp_server.py"

# Stop any background tasks or servers
kill_processes "start.sh"

# Check for any remaining processes on common ports
echo ""
echo "🔍 Checking for processes on common ports..."

check_port() {
    local port=$1
    local pid=$(lsof -ti:$port 2>/dev/null)
    if [ -n "$pid" ]; then
        echo "Found process $pid on port $port, stopping..."
        kill $pid 2>/dev/null
        sleep 1
        # Force kill if still running
        if kill -0 $pid 2>/dev/null; then
            echo "Force killing process $pid on port $port..."
            kill -9 $pid 2>/dev/null
        fi
        echo "✅ Process on port $port stopped"
    else
        echo "ℹ️  No process found on port $port"
    fi
}

# Check common Streamlit ports
check_port 8501
check_port 8502
check_port 8503

# Clean up any temporary files
echo ""
echo "🧹 Cleaning up temporary files..."

# Remove any __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Remove any .pyc files
find . -name "*.pyc" -delete 2>/dev/null || true

# Remove any temporary log files
rm -f *.log 2>/dev/null || true
rm -f .streamlit/*.log 2>/dev/null || true

echo ""
echo "🏁 Weather Chatbot stopped successfully!"
echo ""
echo "To restart the application, run:"
echo "  ./start.sh"
echo ""
echo "Or manually run:"
echo "  streamlit run app.py         # Clarifai news chatbot"
