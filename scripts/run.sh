#!/bin/bash
# Quick start script for OCR Validation Tool

echo "🔍 OCR Validation Tool - Quick Start"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create sample images if they don't exist
if [ ! -d "sample_images" ]; then
    echo "🎨 Creating sample test images..."
    python create_sample_images.py
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Streamlit app..."
echo "📱 Open your browser to: http://localhost:8501"
echo ""
echo "💡 Don't forget to add your Moondream API key in the sidebar!"
echo ""

# Start Streamlit
streamlit run ocr_validation_app.py
