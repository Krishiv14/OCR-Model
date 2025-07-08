# OCR Validation Tool - Streamlit App

A powerful Streamlit application for validating OCR (Optical Character Recognition) results by comparing extracted text from test images against master/reference images using the Moondream Vision Language Model.

## Features

- Image Upload: Support for JPG, JPEG, and PNG image formats
- OCR Text Extraction: Extract text from images using Moondream's advanced VLM
- Text Comparison: Compare extracted text with master/reference text
- Validation Results: Clear pass/fail status with detailed analysis
- Secure API Key Management: Store API keys securely using Streamlit's session state or secrets
- User-Friendly Interface: Clean, intuitive interface with real-time results

## Prerequisites

- Python 3.9 or higher
- Moondream API key (get one at [console.moondream.ai](https://console.moondream.ai))

## Installation

1. Clone or download the project files

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API key (choose one method):

   Method 1: Using Streamlit Secrets (Recommended for deployment)
   - Copy `.streamlit/secrets_sample.toml` to `.streamlit/secrets.toml`
   - Edit `.streamlit/secrets.toml` and add your API key:
     ```toml
     MOONDREAM_API_KEY = "your_actual_api_key_here"
     ```

   Method 2: Using the Web Interface
   - Enter your API key directly in the sidebar when running the app

## Running the Application

1. Start the Streamlit server:
   ```bash
   streamlit run ocr_validation_app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Configure your API key in the sidebar if you haven't used the secrets method

4. Upload your images:
   - Upload a test image (the image you want to extract text from)
   - Upload a master image (the reference image to compare against)

5. Click "Validate OCR" to process the images and see results

## How to Use

### Step-by-Step Guide

1. Setup: Ensure you have your Moondream API key ready
2. Upload Images: 
   - Test Image: The image you want to extract text from
   - Master Image: The reference image with known correct text
3. Run Validation: Click the "Validate OCR" button
4. Review Results: 
   - All Good: Text matches perfectly
   - Reject: Text doesn't match (see detailed analysis)

### Understanding Results

- Status: Overall validation result (All Good/Reject)
- Extracted Text: Text found in your test image
- Master Text: Text found in your reference image
- Comparison: Match/Mismatch indicator
- Detailed Analysis: Character-by-character comparison for mismatches

## API Key Security

### Best Practices

1. Never commit API keys to version control
2. Use environment variables or Streamlit secrets
3. Set appropriate usage limits on your API key
4. Monitor your API usage regularly

### Deployment

When deploying to Streamlit Community Cloud:
1. Go to your app settings
2. Click "Advanced settings"
3. Add your API key in the "Secrets" section:
   ```toml
   MOONDREAM_API_KEY = "your_actual_api_key_here"
   ```

## Project Structure

```
ocr-validation-tool/
├── ocr_validation_app.py      # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── .streamlit/
    ├── config.toml          # Streamlit configuration
    └── secrets_sample.toml  # API key template
```

## Troubleshooting

### Common Issues

**1. "Please configure your Moondream API key"**
- Ensure you've added your API key either in secrets.toml or via the sidebar
- Check that your API key is valid and active

**2. "Error initializing model"**
- Verify your API key is correct
- Check your internet connection
- Ensure you have sufficient API credits

**3. "Validation failed"**
- Check that your images are clear and contain readable text
- Ensure images are in supported formats (JPG, JPEG, PNG)
- Try with different images to isolate the issue

**4. Import errors**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using the correct Python environment

### Performance Tips

- Use high-quality, clear images for better OCR accuracy
- Ensure text in images is legible and well-contrasted
- Avoid extremely large image files (resize if needed)

## Customization

### Modifying the Validation Logic

You can customize the `validate_dynamic_master` function to:
- Add fuzzy text matching for slight variations
- Implement confidence scoring
- Add preprocessing for better OCR results

### UI Customization

Modify the Streamlit configuration in `.streamlit/config.toml` to change:
- Theme colors
- Layout settings
- Upload size limits

## About Moondream

Moondream is a small but powerful vision-language model that excels at:
- Text extraction from images (OCR)
- Visual question answering
- Object detection
- Image captioning

Learn more at [moondream.ai](https://moondream.ai)

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

This project is provided as-is for educational and practical use.

---

**Need help?** Check the troubleshooting section above or refer to the [Streamlit documentation](https://docs.streamlit.io) and [Moondream documentation](https://docs.moondream.ai).