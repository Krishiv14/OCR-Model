# Create an example script for programmatic usage
example_script = '''#!/usr/bin/env python3
"""
Example script showing how to use the OCR validation functionality programmatically
(without the Streamlit interface)
"""

import moondream as md
from PIL import Image
import argparse
import sys

def validate_ocr_programmatic(test_image_path, master_image_path, api_key):
    """
    Programmatic version of the OCR validation function
    """
    try:
        # Initialize the model
        model = md.vl(api_key=api_key)
        
        # Load images
        test_image = Image.open(test_image_path)
        master_image = Image.open(master_image_path)
        
        print("🔍 Extracting text from test image...")
        extracted_text = model.query(test_image, question="Extract all text from this image")["answer"].strip()
        
        print("🔍 Extracting text from master image...")
        master_text = model.query(master_image, question="Extract all text from this image")["answer"].strip()
        
        # Compare texts
        match = extracted_text == master_text
        
        # Print results
        print("\\n" + "="*60)
        print("📊 OCR VALIDATION RESULTS")
        print("="*60)
        print(f"Status: {'✅ PASS' if match else '❌ FAIL'}")
        print(f"Match: {'Yes' if match else 'No'}")
        print()
        print("📝 EXTRACTED TEXT:")
        print("-" * 30)
        print(extracted_text)
        print()
        print("📋 MASTER TEXT:")
        print("-" * 30)
        print(master_text)
        print()
        
        if not match:
            print("🔍 DETAILED ANALYSIS:")
            print("-" * 30)
            print(f"Extracted length: {len(extracted_text)} characters")
            print(f"Master length: {len(master_text)} characters")
            
            # Find first difference
            for i, (c1, c2) in enumerate(zip(extracted_text, master_text)):
                if c1 != c2:
                    print(f"First difference at position {i}: '{c1}' vs '{c2}'")
                    break
        
        return match, extracted_text, master_text
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, "", ""

def main():
    parser = argparse.ArgumentParser(description="OCR Validation Tool - Command Line Version")
    parser.add_argument("test_image", help="Path to the test image")
    parser.add_argument("master_image", help="Path to the master/reference image")
    parser.add_argument("--api-key", required=True, help="Moondream API key")
    
    args = parser.parse_args()
    
    # Validate inputs
    try:
        test_img = Image.open(args.test_image)
        master_img = Image.open(args.master_image)
    except Exception as e:
        print(f"❌ Error loading images: {e}")
        sys.exit(1)
    
    # Run validation
    match, extracted, master = validate_ocr_programmatic(
        args.test_image, 
        args.master_image, 
        args.api_key
    )
    
    # Exit with appropriate code
    sys.exit(0 if match else 1)

if __name__ == "__main__":
    main()
'''

with open("ocr_validation_cli.py", "w", encoding="utf-8") as f:
    f.write(example_script)

# Create a demo/test script
demo_script = '''#!/usr/bin/env python3
"""
Demo script to test the OCR validation functionality
This script creates sample images with text for testing purposes
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_images():
    """Create sample images with text for testing"""
    
    # Create directory for sample images
    os.makedirs("sample_images", exist_ok=True)
    
    # Sample text
    text = "Hello World\\nThis is a test\\n123 ABC"
    
    # Create first image (test image)
    img1 = Image.new('RGB', (400, 200), color='white')
    draw1 = ImageDraw.Draw(img1)
    
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    draw1.text((50, 50), text, fill='black', font=font)
    img1.save("sample_images/test_image.png")
    
    # Create second image (master image - identical)
    img2 = Image.new('RGB', (400, 200), color='white')
    draw2 = ImageDraw.Draw(img2)
    draw2.text((50, 50), text, fill='black', font=font)
    img2.save("sample_images/master_image.png")
    
    # Create third image (different text for testing mismatch)
    different_text = "Hello World\\nThis is different\\n456 XYZ"
    img3 = Image.new('RGB', (400, 200), color='white')
    draw3 = ImageDraw.Draw(img3)
    draw3.text((50, 50), different_text, fill='black', font=font)
    img3.save("sample_images/different_image.png")
    
    print("✅ Sample images created in 'sample_images/' directory:")
    print("  - test_image.png (for testing)")
    print("  - master_image.png (identical to test)")
    print("  - different_image.png (different text)")
    print()
    print("💡 You can use these images to test the OCR validation tool!")

if __name__ == "__main__":
    create_sample_images()
'''

with open("create_sample_images.py", "w", encoding="utf-8") as f:
    f.write(demo_script)

print("✅ Additional utility files created!")
print("\nUtility files created:")
print("- ocr_validation_cli.py (Command-line version)")
print("- create_sample_images.py (Generate test images)")
print("\nTo create sample test images, run:")
print("  python create_sample_images.py")
print("\nTo use the command-line version:")
print("  python ocr_validation_cli.py test_image.png master_image.png --api-key YOUR_KEY")