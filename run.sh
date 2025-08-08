#!/bin/bash

# Photo2Pixel Quick Start Script
# 照片转像素画快速启动脚本

echo "🎨 Photo2Pixel Quick Start"
echo "=========================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    echo "✅ Virtual environment created and dependencies installed"
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
source .venv/bin/activate

# Check if convert.py exists
if [ ! -f "convert.py" ]; then
    echo "❌ Error: convert.py not found!"
    exit 1
fi

echo "🚀 Starting Photo2Pixel in interactive mode..."
echo "💡 You can drag and drop images directly!"
echo ""

# Run the program
python convert.py --interactive
