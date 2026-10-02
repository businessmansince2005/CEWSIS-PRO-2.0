@echo off
cd /d "%~dp0"
echo.
echo ========================================
echo CEWSIS Web Dashboard
echo ========================================
echo.
echo Starting server at http://127.0.0.1:8000
echo Open that URL in your browser, then click "Initiate Deep Scan"
echo.
echo Press Ctrl+C to stop the server.
echo.
python main.py
pause
