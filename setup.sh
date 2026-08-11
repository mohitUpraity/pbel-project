#!/bin/bash

# Setup and run script for Legal Document Risk Analyzer

# Exit immediately if a command exits with a non-zero status
set -e

# Clear screen for clean terminal presentation
clear

echo "==========================================================="
echo "⚖️  LawBot360: Legal Document Risk Analyzer Setup & Launcher"
echo "==========================================================="
echo ""

# 1. Verify python3 exists
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed or not in your PATH."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# 2. Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment 'venv'..."
    python3 -m venv venv
    echo "✅ Virtual environment created successfully."
else
    echo "✅ Virtual environment 'venv' already exists."
fi

# 3. Activate Virtual Environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# 4. Upgrade pip & Install requirements
echo "⚡ Upgrading pip..."
pip install --upgrade pip

echo "📥 Installing dependencies from requirements.txt (this may take a few moments)..."
pip install -r requirements.txt
echo "✅ Dependencies installed successfully."

# 5. Configuration Setup
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📝 Creating '.env' file from '.env.example'..."
        cp .env.example .env
        echo "⚠️  Important: Open the '.env' file and add your GEMINI_API_KEY."
    else
        echo "📝 Creating basic '.env' file..."
        echo "GEMINI_API_KEY=" > .env
        echo "TESSERACT_CMD=/usr/local/bin/tesseract" >> .env
    fi
else
    echo "✅ Configuration '.env' file already exists."
fi

echo ""
echo "==========================================================="
echo "🚀 Launching Application Diagnostics & Streamlit Service"
echo "==========================================================="
echo ""

# 6. Launch the runner script inside virtual environment
python3 run.py
