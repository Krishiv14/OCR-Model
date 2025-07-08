#!/usr/bin/env python3
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
        print("\n" + "="*60)
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
