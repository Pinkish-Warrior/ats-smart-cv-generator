@echo off
REM ATS-Smart CV Generator - Quick Start Script for Windows
REM This script sets up and runs both backend and frontend servers

echo 🚀 ATS-Smart CV Generator - Quick Start
echo =======================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Backend setup
echo 🔧 Setting up backend...
cd cv-generator-backend

REM Check if virtual environment exists, create if not
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt >nul 2>&1

REM Download NLTK data
echo 📚 Setting up NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('punkt_tab', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True)"

REM Start backend server
echo 🚀 Starting backend server...
start /B python app.py

REM Give backend time to start
timeout /t 3 /nobreak >nul

REM Frontend setup
echo.
echo 🔧 Setting up frontend...
cd ..\cv-generator-frontend

REM Install Node.js dependencies
if not exist "node_modules" (
    echo 📦 Installing Node.js dependencies...
    npm install >nul 2>&1
) else (
    echo ✅ Node.js dependencies already installed
)

REM Start frontend server
echo 🚀 Starting frontend server...
start /B npm run dev

echo.
echo 🎉 ATS-Smart CV Generator is now running!
echo =======================================
echo 📱 Frontend: http://localhost:5173
echo 🔗 Backend:  http://localhost:5002
echo.
echo 📖 How to use:
echo 1. Open http://localhost:5173 in your browser
echo 2. Enter a job description to analyze
echo 3. Fill out your information
echo 4. Generate your ATS-optimized CV
echo.
echo 🛑 To stop the servers, close this window or press Ctrl+C
echo.

pause
