
import streamlit as st
import numpy as np
import pandas as pd
import moondream as md
from PIL import Image
import io

# Configure page settings
st.set_page_config(
    page_title="OCR Validation Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_model():
    """Initialize the Moondream model with API key"""
    try:
        # Try to get API key from secrets first, then from session state
        api_key = None

        # Check secrets first (for production deployment)
        try:
            api_key = st.secrets.get("MOONDREAM_API_KEY")
        except:
            pass

        # If not in secrets, check session state
        if not api_key:
            api_key = st.session_state.get("moondream_api_key")

        if not api_key:
            return None

        model = md.vl(api_key=api_key)
        return model
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")
        return None

def validate_dynamic_master(image, master_image, model):
    """
    Validate OCR extraction by comparing text from an image with a master image
    """
    try:
        # Extract text from the main image
        extracted_text = model.query(image, question="Extract all text from this image")["answer"].strip()

        # Extract text from the master image
        master_text = model.query(master_image, question="Extract all text from this image")["answer"].strip()

        # Compare the texts
        result = {
            "status": "All Good" if extracted_text == master_text else "Reject",
            "extracted_text": extracted_text,
            "master_text": master_text,
            "comparison": "Match" if extracted_text == master_text else "Mismatch"
        }
        return result

    except Exception as e:
        return {"error": str(e), "status": "Failed"}

def main():
    st.title("🔍 OCR Validation Tool")
    st.markdown("---")

    # Sidebar for API key management
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Key management
        api_key_input = st.text_input(
            "Moondream API Key",
            type="password",
            value=st.session_state.get("moondream_api_key", ""),
            help="Enter your Moondream API key. Get one at https://console.moondream.ai"
        )

        if st.button("Save API Key"):
            if api_key_input:
                st.session_state.moondream_api_key = api_key_input
                st.success("API key saved!")
                st.rerun()
            else:
                st.error("Please enter a valid API key")

        if st.button("Clear API Key"):
            if "moondream_api_key" in st.session_state:
                del st.session_state.moondream_api_key
                st.success("API key cleared!")
                st.rerun()

        st.markdown("---")

        # Instructions
        st.markdown("""
        ### 📋 Instructions
        1. **Add API Key**: Enter your Moondream API key above
        2. **Upload Images**: Upload both the test image and master image
        3. **Run OCR**: Click "Validate OCR" to compare texts
        4. **Review Results**: Check the validation results
        """)

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.header("📤 Test Image")
        test_image = st.file_uploader(
            "Upload test image",
            type=['jpg', 'jpeg', 'png'],
            key="test_image",
            help="Upload the image you want to extract text from"
        )

        if test_image:
            image = Image.open(test_image)
            st.image(image, caption="Test Image", use_container_width=True)

    with col2:
        st.header("📤 Master Image")
        master_image = st.file_uploader(
            "Upload master image",
            type=['jpg', 'jpeg', 'png'],
            key="master_image",
            help="Upload the master/reference image to compare against"
        )

        if master_image:
            master_img = Image.open(master_image)
            st.image(master_img, caption="Master Image", use_container_width=True)

    st.markdown("---")

    # Validation section
    if st.button("🔍 Validate OCR", type="primary", use_container_width=True):
        if not test_image or not master_image:
            st.error("Please upload both test and master images!")
            return

        # Initialize model
        model = init_model()
        if not model:
            st.error("Please configure your Moondream API key in the sidebar!")
            return

        with st.spinner("Processing images and extracting text..."):
            # Load images
            test_img = Image.open(test_image)
            master_img = Image.open(master_image)

            # Perform validation
            result = validate_dynamic_master(test_img, master_img, model)

        # Display results
        st.header("📊 Validation Results")

        if "error" in result:
            st.error(f"Validation failed: {result['error']}")
        else:
            # Status indicator
            if result["status"] == "All Good":
                st.success(f"✅ Status: {result['status']}")
            else:
                st.error(f"❌ Status: {result['status']}")

            # Create tabs for detailed results
            tab1, tab2, tab3 = st.tabs(["📝 Extracted Text", "📋 Master Text", "🔍 Comparison"])

            with tab1:
                st.subheader("Text from Test Image")
                st.text_area("Extracted Text", result["extracted_text"], height=150, disabled=True)

            with tab2:
                st.subheader("Text from Master Image")
                st.text_area("Master Text", result["master_text"], height=150, disabled=True)

            with tab3:
                st.subheader("Comparison Result")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Comparison Status", result["comparison"])
                with col_b:
                    match_percentage = 100 if result["comparison"] == "Match" else 0
                    st.metric("Match Percentage", f"{match_percentage}%")

                # Character-by-character comparison
                if result["comparison"] == "Mismatch":
                    st.subheader("Detailed Analysis")

                    extracted = result["extracted_text"]
                    master = result["master_text"]

                    st.write("**Length Comparison:**")
                    st.write(f"- Extracted text: {len(extracted)} characters")
                    st.write(f"- Master text: {len(master)} characters")

                    # Show first few different characters
                    st.write("**Text Differences:**")
                    for i, (c1, c2) in enumerate(zip(extracted, master)):
                        if c1 != c2:
                            st.write(f"Position {i}: '{c1}' vs '{c2}'")
                            break

    # Additional features section
    st.markdown("---")
    with st.expander("💡 Additional Features"):
        st.markdown("""
        ### Features Available:
        - **Text Extraction**: Extract text from any image using Moondream Vision Language Model
        - **Text Comparison**: Compare extracted text with master/reference text
        - **Validation Status**: Get clear pass/fail results
        - **Detailed Analysis**: Character-by-character comparison for mismatches
        - **Secure API Key Management**: Store API keys securely using Streamlit's session state

        ### About Moondream:
        Moondream is a small but powerful vision-language model that can:
        - Extract text from images (OCR)
        - Answer questions about image content
        - Detect objects in images
        - Generate image captions
        """)

if __name__ == "__main__":
    main()
