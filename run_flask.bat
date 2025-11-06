@echo off
echo ========================================
echo Starting Flask App Locally
echo ========================================
echo.
echo Make sure you're in the project directory!
echo.
cd /d "%~dp0"
echo Current directory: %CD%
echo.
echo Starting Flask server...
echo Browser will open automatically at http://localhost:5000
echo.
timeout /t 3 /nobreak >nul
start http://localhost:5000
python app.py
pause

