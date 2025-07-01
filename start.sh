#!/bin/bash

# ATS-Smart CV Generator - Quick Start Script
# This script sets up and runs both backend and frontend servers

set -e  # Exit on any error

echo "🚀 ATS-Smart CV Generator - Quick Start"
echo "======================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Backend setup
echo "🔧 Setting up backend..."
cd cv-generator-backend

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Download NLTK data if not already present
echo "📚 Setting up NLTK data..."
python -c "
import nltk
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('taggers/averaged_perceptron_tagger')
    print('NLTK data already available')
except LookupError:
    print('Downloading NLTK data...')
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    print('NLTK data downloaded successfully')
"

# Start backend server in background
echo "🚀 Starting backend server..."
python app.py &
BACKEND_PID=$!

# Give backend time to start
sleep 3

# Check if backend started successfully
if curl -s http://localhost:5002/api/health > /dev/null; then
    echo "✅ Backend running on http://localhost:5002"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Frontend setup
echo ""
echo "🔧 Setting up frontend..."
cd ../cv-generator-frontend

# Install Node.js dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install > /dev/null 2>&1
else
    echo "✅ Node.js dependencies already installed"
fi

# Start frontend server in background
echo "🚀 Starting frontend server..."
npm run dev &
FRONTEND_PID=$!

# Give frontend time to start
sleep 5

# Check if frontend started successfully
if curl -s http://localhost:5173 > /dev/null; then
    echo "✅ Frontend running on http://localhost:5173"
else
    echo "❌ Frontend failed to start"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo "🎉 ATS-Smart CV Generator is now running!"
echo "======================================="
echo "📱 Frontend: http://localhost:5173"
echo "🔗 Backend:  http://localhost:5002"
echo ""
echo "📖 How to use:"
echo "1. Open http://localhost:5173 in your browser"
echo "2. Enter a job description to analyze"
echo "3. Fill out your information"
echo "4. Generate your ATS-optimized CV"
echo ""
echo "🛑 To stop the servers:"
echo "Press Ctrl+C or run: kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Save PIDs for cleanup
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# Wait for user to stop servers
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; rm -f .backend.pid .frontend.pid; echo '✅ Servers stopped'; exit 0" INT

echo "⌨️  Press Ctrl+C to stop the servers"
wait
