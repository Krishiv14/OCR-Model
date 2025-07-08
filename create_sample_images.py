#!/usr/bin/env python3
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
    text = "Hello World\nThis is a test\n123 ABC"

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
    different_text = "Hello World\nThis is different\n456 XYZ"
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
