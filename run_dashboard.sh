#!/bin/bash
# Launch the AI-Powered Project Generator Dashboard

echo "🚀 Starting AI-Powered Project Generator..."
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Launch Streamlit
echo "🌐 Launching dashboard..."
echo "================================================"
echo ""
echo "Dashboard will open in your browser at:"
echo "👉 http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

streamlit run dashboard.py
