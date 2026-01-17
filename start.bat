@echo off
REM Kalainayam Development Start Script for Windows

echo.
echo 🎨 Kalainayam — Fashion Intelligence Platform
echo =============================================
echo.

REM Check if we're in the right directory
if not exist "backend\app.py" (
    echo Error: Please run this script from the Kalainayam root directory
    pause
    exit /b 1
)

REM Start backend
echo Starting backend server...
cd backend

REM Check if Python virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt > nul 2>&1

REM Start Flask server
echo Backend running on http://localhost:5000
echo Press Ctrl+C to stop
start python app.py

REM Go back to root
cd ..

REM Start frontend server
echo.
echo Starting frontend server...
cd frontend

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Frontend running on http://localhost:8000
    echo Press Ctrl+C to stop
    python -m http.server 8000
) else (
    echo Error: Python not found
    pause
    exit /b 1
)
