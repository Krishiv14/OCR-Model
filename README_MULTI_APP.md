# AI Moon Multi-Tool Application 🌙

A comprehensive AI-powered tool suite that combines OCR validation and defect detection capabilities in a single, easy-to-use Streamlit application.

## 🚀 Features

### 📄 OCR Validation Tool
- **Text Extraction**: Extract text from images using Moondream Vision Language Model
- **Text Comparison**: Compare extracted text with master/reference text
- **Validation Status**: Get clear pass/fail results
- **Detailed Analysis**: Character-by-character comparison for mismatches
- **Custom Prompts**: Use custom prompts for specific text extraction needs
- **Camera Support**: Capture images directly from camera

### 🔍 Defect Detection Tool
- **Scratch Detection**: Detect linear scratches using edge detection and morphological operations
- **Dent & Crack Detection**: Identify dents and cracks using blob detection
- **Surface Defect Detection**: Detect general surface defects using texture analysis
- **Quality Analysis**: Analyze image quality metrics (brightness, contrast, sharpness, noise)
- **Visual Results**: Interactive visualizations of detected defects
- **Export Reports**: Download CSV reports with detection results

## 📋 Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies
- `streamlit>=1.28.0` - Web application framework
- `moondream>=0.1.0` - Vision Language Model for OCR
- `Pillow>=9.0.0` - Image processing
- `numpy>=1.21.0` - Numerical computing
- `pandas>=1.3.0` - Data manipulation
- `opencv-python>=4.8.0` - Computer vision
- `scikit-image>=0.21.0` - Image processing and analysis
- `matplotlib>=3.7.0` - Plotting and visualization

## 🏃‍♂️ Quick Start

### Option 1: Run the Multi-Page Application
```bash
python run_multi_app.py
```

### Option 2: Run Individual Tools
```bash
# OCR Validation Tool
streamlit run ocr_validation_app.py

# Defect Detection Tool
streamlit run defect_detection_app.py

# Multi-Page Application
streamlit run multi_page_app.py
```

## 🎯 How to Use

### OCR Validation Tool

1. **Upload Images**: Upload both test and master images
2. **Custom Prompts** (Optional): Use custom prompts for specific text extraction
3. **Validate**: Click "Validate OCR" to compare texts
4. **Review Results**: Check the detailed comparison and analysis

**Features:**
- Compare text extraction accuracy
- Character-by-character analysis
- Match percentage calculation
- Export validation reports

### Defect Detection Tool

1. **Select Detection Type**: Choose from:
   - All Defects
   - Scratches Only
   - Dents & Cracks
   - Surface Defects
   - Quality Analysis

2. **Upload Image**: Upload or capture an image for analysis

3. **Adjust Sensitivity**: Use the sensitivity slider to fine-tune detection

4. **Analyze**: Click "Detect Defects" to run the analysis

5. **Review Results**: View detailed results in organized tabs

**Detection Methods:**

#### Scratch Detection
- Uses Canny edge detection
- Morphological operations to connect broken edges
- Filters based on aspect ratio and area
- Highlights linear defects

#### Dent & Crack Detection
- Laplacian of Gaussian blob detection
- Filters blobs by size and shape
- Identifies circular/elliptical defects
- Visualizes detected blobs

#### Surface Defect Detection
- Local Binary Pattern (LBP) texture analysis
- Anomaly detection using statistical thresholds
- Morphological operations for noise reduction
- Identifies texture irregularities

#### Quality Analysis
- Brightness and contrast analysis
- Sharpness measurement using Laplacian variance
- Noise level detection using FFT
- Comprehensive image quality metrics

## 📊 Output Examples

### OCR Validation Results
- **Status**: Pass/Fail with clear indicators
- **Match Percentage**: Numerical similarity score
- **Detailed Comparison**: Character-level differences
- **Extracted Text**: Side-by-side text comparison

### Defect Detection Results
- **Summary**: Total defect count and types
- **Visual Overlays**: Defects highlighted on original image
- **Quality Metrics**: Brightness, contrast, sharpness, noise
- **Exportable Reports**: CSV format for further analysis

## 🔧 Configuration

### Sensitivity Settings
- Adjust detection sensitivity (1-10 scale)
- Fine-tune detection thresholds
- Customize morphological operations

### Custom Prompts (OCR)
- Extract specific information (e.g., "What is the invoice number?")
- Compare specific text elements
- Use natural language queries

## 📁 File Structure

```
OCR-Model/
├── multi_page_app.py          # Main multi-page application
├── ocr_validation_app.py      # Standalone OCR validation tool
├── defect_detection_app.py    # Standalone defect detection tool
├── run_multi_app.py          # Launcher script
├── requirements.txt           # Dependencies
├── README_MULTI_APP.md       # This file
└── config/
    └── secrets_sample.toml   # Configuration template
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Sidebar Navigation**: Easy switching between tools
- **Tabbed Interface**: Organized result display
- **Progress Indicators**: Real-time processing feedback
- **Export Functionality**: Download results as CSV
- **Camera Integration**: Direct image capture

## 🔍 Technical Details

### OCR Validation
- Uses Moondream Vision Language Model
- Supports custom prompts for targeted extraction
- Implements difflib for text comparison
- Provides detailed character-level analysis

### Defect Detection
- **OpenCV**: Core computer vision operations
- **scikit-image**: Advanced image processing
- **Morphological Operations**: Noise reduction and feature enhancement
- **Statistical Analysis**: Quality metrics and anomaly detection

## 🚀 Performance Tips

1. **Image Quality**: Use high-resolution images for better detection
2. **Lighting**: Ensure good lighting for accurate defect detection
3. **Focus**: Keep images in focus for optimal OCR results
4. **File Size**: Compress large images if needed for faster processing

## 🔧 Troubleshooting

### Common Issues

1. **Model Loading Error**: Check internet connection for Moondream API
2. **Import Errors**: Ensure all dependencies are installed
3. **Memory Issues**: Reduce image size for large files
4. **Detection Accuracy**: Adjust sensitivity settings

### Getting Help

- Check the console for error messages
- Verify all dependencies are installed
- Ensure images are in supported formats (JPG, PNG)
- Test with sample images first

## 📈 Future Enhancements

- **Machine Learning Models**: Integration with custom trained models
- **Batch Processing**: Process multiple images simultaneously
- **Real-time Detection**: Live video stream analysis
- **Advanced Analytics**: Statistical analysis and reporting
- **Cloud Integration**: Remote processing capabilities

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving documentation
- Adding new detection algorithms

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**AI Moon Multi-Tool Application** - Empowering AI-driven image analysis and validation 🌙 