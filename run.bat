@echo off
REM Quick start script for OCR Validation Tool (Windows)

echo 🔍 OCR Validation Tool - Quick Start
echo ==================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create sample images if they don't exist
if not exist "sample_images" (
    echo 🎨 Creating sample test images...
    python create_sample_images.py
)

echo.
echo ✅ Setup complete!
echo.
echo 🚀 Starting Streamlit app...
echo 📱 Open your browser to: http://localhost:8501
echo.
echo 💡 Don't forget to add your Moondream API key in the sidebar!
echo.

REM Start Streamlit
streamlit run ocr_validation_app.py
