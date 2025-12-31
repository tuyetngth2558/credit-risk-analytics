@echo off
REM Credit Risk Analytics Dashboard - Run Script
REM ============================================

echo.
echo ========================================
echo  Credit Risk Analytics Dashboard
echo ========================================
echo.
echo Starting Streamlit dashboard...
echo.
echo Dashboard will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ERROR: Streamlit is not installed!
    echo.
    echo Please install requirements first:
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Run the dashboard
streamlit run app.py

pause
