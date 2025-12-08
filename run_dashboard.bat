@echo off
REM Launch the AI-Powered Project Generator Dashboard (Windows)

echo 🚀 Starting AI-Powered Project Generator...
echo ================================================

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📥 Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Launch Streamlit
echo 🌐 Launching dashboard...
echo ================================================
echo.
echo Dashboard will open in your browser at:
echo 👉 http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

streamlit run dashboard.py
