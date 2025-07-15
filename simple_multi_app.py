import streamlit as st
import numpy as np
import pandas as pd
import moondream as md
from PIL import Image
import io
import difflib
import cv2
import os

# This will always point to the godrej_logo.png in the project root
logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'godrej_logo.png'))
# st.image(logo_path, width=200, caption="Godrej")  # Remove logo from main page

# Page configuration
st.set_page_config(
    page_title="AI Moon - Simple Multi-Tool Application",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "OCR Validation"

def init_model():
    """Initialize the Moondream model with hardcoded API key"""
    try:
        api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiJmNzBmZjA2Yy0xOWNiLTQ2MjYtYTQ3Ny0wY2I1ZThjY2UwYTgiLCJvcmdfaWQiOiJ4NUlvVVZDclI5amNPUXUwNUc0UGtIeEtqeEtTV3daTCIsImlhdCI6MTc1MTUyMTA4MywidmVyIjoxfQ._JHn_LcpDX4F5s2YnQqeBaP1-iWnp6VPD02dQM7VQLk"
        model = md.vl(api_key=api_key)
        return model
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")
        return None

def validate_dynamic_master(image, master_image, model, prompt):
    """
    Validate OCR extraction by comparing text from an image with a master image using a custom prompt
    """
    try:
        # Extract text from the main image
        extracted_text = model.query(image, question=prompt)["answer"].strip()

        # Extract text from the master image
        master_text = model.query(master_image, question=prompt)["answer"].strip()

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

def detect_scratches_simple(image):
    """Detect scratches using basic OpenCV operations"""
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150)
    
    # Morphological operations to connect broken edges
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area and aspect ratio
    scratch_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:  # Minimum area threshold
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h if h > 0 else 0
            if aspect_ratio > 2 or aspect_ratio < 0.5:  # Scratch-like aspect ratio
                scratch_contours.append(contour)
    
    return scratch_contours, edges, closed

def detect_blobs_simple(image):
    """Detect blobs (dents/cracks) using simple blob detection"""
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Simple blob detection using thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by area
    valid_blobs = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if 100 < area < 5000:  # Filter by area
            valid_blobs.append(contour)
    
    return valid_blobs, blurred

def detect_surface_defects_simple(image):
    """Detect surface defects using simple thresholding"""
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use adaptive thresholding to detect defects
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Morphological operations to clean up
    kernel = np.ones((3, 3), np.uint8)
    cleaned = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_OPEN, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter by area
    valid_defects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:  # Minimum area threshold
            valid_defects.append(contour)
    
    return valid_defects, cleaned

def analyze_image_quality_simple(image):
    """Analyze image quality using basic metrics"""
    # Convert to numpy array
    img_array = np.array(image)
    
    # Calculate brightness
    brightness = np.mean(img_array)
    
    # Calculate contrast
    contrast = np.std(img_array)
    
    # Calculate sharpness using Laplacian variance
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    sharpness = laplacian.var()
    
    # Calculate noise level using standard deviation of differences
    diff = cv2.absdiff(gray, cv2.GaussianBlur(gray, (5, 5), 0))
    noise_level = np.std(diff)
    
    return {
        'brightness': brightness,
        'contrast': contrast,
        'sharpness': sharpness,
        'noise_level': noise_level
    }

def segment_image_kmeans(image, k=3):
    """Segment image using k-means clustering."""
    img = np.array(image)
    Z = img.reshape((-1, 3))
    Z = np.float32(Z)
    # Define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(Z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    segmented_img = res.reshape((img.shape))
    return segmented_img

def ocr_validation_page():
    """OCR Validation Tool Page"""
    st.title("OCR Validation Tool")
    st.markdown("---")

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.header("Test Image")
        test_tab_upload, test_tab_camera = st.tabs(["Upload", "Camera"])
        test_image = None
        with test_tab_upload:
            test_image = st.file_uploader(
                "Upload test image",
                type=['jpg', 'jpeg', 'png'],
                key="test_image_upload",
                help="Upload the image you want to extract text from"
            )
        with test_tab_camera:
            test_image_camera = st.camera_input(
                "Capture test image",
                key="test_image_camera"
            )
            if test_image_camera:
                test_image = test_image_camera
        if test_image:
            image = Image.open(test_image)
            st.image(image, caption="Test Image", use_container_width=True)

    with col2:
        st.header("Master Image")
        master_tab_upload, master_tab_camera = st.tabs(["Upload", "Camera"])
        master_image = None
        with master_tab_upload:
            master_image = st.file_uploader(
                "Upload master image",
                type=['jpg', 'jpeg', 'png'],
                key="master_image_upload",
                help="Upload the master/reference image to compare against"
            )
        with master_tab_camera:
            master_image_camera = st.camera_input(
                "Capture master image",
                key="master_image_camera"
            )
            if master_image_camera:
                master_image = master_image_camera
        if master_image:
            master_img = Image.open(master_image)
            st.image(master_img, caption="Master Image", use_container_width=True)

    st.markdown("---")

    # Only show custom prompt option after both images are uploaded
    if test_image and master_image:
        use_custom_prompt = st.checkbox("Use a custom prompt for Moondream", value=False)
        if use_custom_prompt:
            st.subheader("Custom Prompt for Moondream")
            prompt = st.text_area(
                "Enter your question for the Moondream model:",
                value="Extract all text from this image",
                help="You can ask anything about the image, e.g. 'What is the invoice number?' or 'Extract all text from this image'"
            )
        else:
            prompt = "Extract all text from this image"
    else:
        prompt = "Extract all text from this image"

    # Validation section
    if st.button("Validate OCR", type="primary", use_container_width=True):
        if not test_image or not master_image:
            st.error("Please upload both test and master images!")
            return

        # Initialize model
        model = init_model()
        if not model:
            st.error("Error initializing model!")
            return

        with st.spinner("Processing images and extracting text..."):
            # Load images
            test_img = Image.open(test_image)
            master_img = Image.open(master_image)

            # Perform validation with custom prompt
            result = validate_dynamic_master(test_img, master_img, model, prompt)

        # Display results
        st.header("Validation Results")

        if "error" in result:
            st.error(f"Validation failed: {result['error']}")
        else:
            # Status indicator
            if result["status"] == "All Good":
                st.success(f"Status: {result['status']}")
            else:
                st.error(f"Status: {result['status']}")

            # Create tabs for detailed results
            tab1, tab2, tab3 = st.tabs(["Extracted Text", "Master Text", "Comparison"])

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
                    # Calculate match percentage using difflib
                    matcher = difflib.SequenceMatcher(None, result["extracted_text"], result["master_text"])
                    match_percentage = round(matcher.ratio() * 100, 2)
                    st.metric("Match Percentage", f"{match_percentage}%")

                # Character-by-character comparison
                if result["comparison"] == "Mismatch":
                    st.subheader("Detailed Analysis")

                    extracted = result["extracted_text"]
                    master = result["master_text"]

                    st.write("Length Comparison:")
                    st.write(f"- Extracted text: {len(extracted)} characters")
                    st.write(f"- Master text: {len(master)} characters")

                    # Show all differences using difflib.ndiff
                    st.write("Text Differences:")
                    diff = list(difflib.ndiff(master, extracted))
                    diff_display = []
                    for i, d in enumerate(diff):
                        if d[0] == ' ':
                            continue  # skip matches
                        elif d[0] == '-':
                            diff_display.append(f"Position {i}: Missing in extracted: '{d[-1]}'")
                        elif d[0] == '+':
                            diff_display.append(f"Position {i}: Extra in extracted: '{d[-1]}'")
                        elif d[0] == '?':
                            continue  # skip markers
                    if diff_display:
                        for line in diff_display:
                            st.write(line)
                    else:
                        st.write("No character-level differences found.")

def defect_detection_page():
    """Defect Detection Tool Page"""
    st.title("🔍 Defect Detection Tool")
    st.markdown("---")
    
    # Sidebar for detection options
    st.sidebar.header("Detection Options")
    detection_type = st.sidebar.selectbox(
        "Select Detection Type",
        ["All Defects", "Scratches Only", "Dents & Cracks", "Surface Defects", "Quality Analysis", "Segmentation"]
    )
    
    sensitivity = st.sidebar.slider("Detection Sensitivity", 1, 10, 5)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Input Image")
        upload_tab, camera_tab = st.tabs(["Upload", "Camera"])
        
        uploaded_image = None
        with upload_tab:
            uploaded_image = st.file_uploader(
                "Upload image for defect detection",
                type=['jpg', 'jpeg', 'png'],
                key="defect_image_upload",
                help="Upload an image to detect scratches, dents, cracks, and other defects"
            )
        
        with camera_tab:
            camera_image = st.camera_input(
                "Capture image for defect detection",
                key="defect_image_camera"
            )
            if camera_image:
                uploaded_image = camera_image
        
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Input Image", use_container_width=True)
    
    with col2:
        st.header("Detection Results")
        
        if uploaded_image and st.button("Detect Defects", type="primary", use_container_width=True):
            with st.spinner("Analyzing image for defects..."):
                image = Image.open(uploaded_image)
                img_array = np.array(image)
                
                results = {}
                
                # Perform different types of detection based on selection
                if detection_type in ["All Defects", "Scratches Only"]:
                    scratch_contours, edges, closed = detect_scratches_simple(image)
                    results['scratches'] = {
                        'contours': scratch_contours,
                        'count': len(scratch_contours),
                        'edges': edges,
                        'closed': closed
                    }
                
                if detection_type in ["All Defects", "Dents & Cracks"]:
                    blobs, blurred = detect_blobs_simple(image)
                    results['dents_cracks'] = {
                        'blobs': blobs,
                        'count': len(blobs),
                        'blurred': blurred
                    }
                
                if detection_type in ["All Defects", "Surface Defects"]:
                    defects, cleaned = detect_surface_defects_simple(image)
                    results['surface_defects'] = {
                        'defects': defects,
                        'count': len(defects),
                        'cleaned': cleaned
                    }
                
                if detection_type in ["All Defects", "Quality Analysis"]:
                    quality_metrics = analyze_image_quality_simple(image)
                    results['quality'] = quality_metrics
                
                if detection_type == "Segmentation":
                    segmented_img = segment_image_kmeans(image, k=3)
                    results['segmentation'] = segmented_img
                
                # Display results
                if detection_type == "Segmentation":
                    st.subheader("Image Segmentation Result")
                    st.image(results['segmentation'], caption="Segmented Image (k-means)", use_container_width=True)
                    st.info("This is a simple k-means segmentation. For more advanced segmentation, consider using deep learning models.")
                else:
                    display_simple_results(image, results, detection_type, sensitivity)
        else:
            st.info("Upload an image and click 'Detect Defects' to analyze")

def display_simple_results(image, results, detection_type, sensitivity):
    """Display detection results with visualizations"""
    
    # Create tabs for different result types
    if detection_type == "All Defects":
        tabs = st.tabs(["Summary", "Scratches", "Dents & Cracks", "Surface Defects", "Quality"])
    else:
        tabs = st.tabs(["Results"])
    
    with tabs[0]:
        # Summary tab
        st.subheader("Detection Summary")
        
        total_defects = 0
        defect_summary = []
        
        if 'scratches' in results:
            total_defects += results['scratches']['count']
            defect_summary.append(f"Scratches: {results['scratches']['count']}")
        
        if 'dents_cracks' in results:
            total_defects += results['dents_cracks']['count']
            defect_summary.append(f"Dents/Cracks: {results['dents_cracks']['count']}")
        
        if 'surface_defects' in results:
            total_defects += results['surface_defects']['count']
            defect_summary.append(f"Surface Defects: {results['surface_defects']['count']}")
        
        # Overall status
        if total_defects == 0:
            st.success("✅ No defects detected!")
        elif total_defects <= 3:
            st.warning(f"⚠️ {total_defects} defects detected")
        else:
            st.error(f"❌ {total_defects} defects detected")
        
        # Display summary
        for defect_type in defect_summary:
            st.write(defect_type)
        
        # Quality metrics if available
        if 'quality' in results:
            st.subheader("Image Quality Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Brightness", f"{results['quality']['brightness']:.1f}")
            with col2:
                st.metric("Contrast", f"{results['quality']['contrast']:.1f}")
            with col3:
                st.metric("Sharpness", f"{results['quality']['sharpness']:.1f}")
            with col4:
                st.metric("Noise Level", f"{results['quality']['noise_level']:.1f}")
    
    # Detailed results tabs
    if detection_type == "All Defects" and len(tabs) > 1:
        with tabs[1]:  # Scratches tab
            if 'scratches' in results:
                st.subheader("Scratch Detection")
                st.write(f"Found {results['scratches']['count']} potential scratches")
                
                # Create visualization
                img_array = np.array(image)
                scratch_img = img_array.copy()
                cv2.drawContours(scratch_img, results['scratches']['contours'], -1, (0, 255, 0), 2)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image(scratch_img, caption="Detected Scratches", use_container_width=True)
                with col2:
                    st.image(results['scratches']['edges'], caption="Edge Detection", use_container_width=True)
        
        with tabs[2]:  # Dents & Cracks tab
            if 'dents_cracks' in results:
                st.subheader("Dent & Crack Detection")
                st.write(f"Found {results['dents_cracks']['count']} potential dents/cracks")
                
                # Create visualization
                img_array = np.array(image)
                blob_img = img_array.copy()
                
                for blob in results['dents_cracks']['blobs']:
                    cv2.drawContours(blob_img, [blob], -1, (255, 0, 0), 2)
                
                st.image(blob_img, caption="Detected Dents/Cracks", use_container_width=True)
        
        with tabs[3]:  # Surface Defects tab
            if 'surface_defects' in results:
                st.subheader("Surface Defect Detection")
                st.write(f"Found {results['surface_defects']['count']} surface defects")
                
                # Create visualization
                defect_img = np.array(image).copy()
                
                # Draw defects on original image
                cv2.drawContours(defect_img, results['surface_defects']['defects'], -1, (255, 0, 0), 2)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image(defect_img, caption="Surface Defects", use_container_width=True)
                with col2:
                    st.image(results['surface_defects']['cleaned'], caption="Defect Mask", use_container_width=True)
        
        with tabs[4]:  # Quality tab
            if 'quality' in results:
                st.subheader("Image Quality Analysis")
                
                # Create simple quality visualization
                gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Brightness Distribution**")
                    hist_values = gray.ravel()
                    st.bar_chart(pd.DataFrame(hist_values[::10], columns=['Pixel Values']))
                
                with col2:
                    st.write("**Image Statistics**")
                    st.write(f"Mean Brightness: {results['quality']['brightness']:.1f}")
                    st.write(f"Contrast: {results['quality']['contrast']:.1f}")
                    st.write(f"Sharpness: {results['quality']['sharpness']:.1f}")
                    st.write(f"Noise Level: {results['quality']['noise_level']:.1f}")
    
    # Export results
    st.markdown("---")
    with st.expander("Export Results"):
        if st.button("Export Detection Report"):
            # Create a simple report
            report_data = {
                'Detection Type': [detection_type],
                'Total Defects': [sum([results.get(k, {}).get('count', 0) for k in ['scratches', 'dents_cracks', 'surface_defects']])],
                'Scratches': [results.get('scratches', {}).get('count', 0)],
                'Dents/Cracks': [results.get('dents_cracks', {}).get('count', 0)],
                'Surface Defects': [results.get('surface_defects', {}).get('count', 0)]
            }
            
            if 'quality' in results:
                report_data.update({
                    'Brightness': [results['quality']['brightness']],
                    'Contrast': [results['quality']['contrast']],
                    'Sharpness': [results['quality']['sharpness']],
                    'Noise Level': [results['quality']['noise_level']]
                })
            
            df = pd.DataFrame(report_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV Report",
                data=csv,
                file_name="defect_detection_report.csv",
                mime="text/csv"
            )

def main():
    # Sidebar navigation
    st.sidebar.image(logo_path, width=150, caption="Godrej")
    # st.sidebar.title("\U0001F319 AI Moon Tools")  # Remove sidebar title
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Choose a Tool",
        ["OCR Validation", "Defect Detection"],
        index=0 if st.session_state.current_page == "OCR Validation" else 1
    )
    
    # Update session state
    st.session_state.current_page = page
    
    # Display selected page
    if page == "OCR Validation":
        ocr_validation_page()
    elif page == "Defect Detection":
        defect_detection_page()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About AI Moon
    A comprehensive AI-powered tool suite for:
    - **OCR Validation**: Extract and validate text from images
    - **Defect Detection**: Detect scratches, dents, cracks, and surface defects
    
    Built with Streamlit and OpenCV.
    """)

if __name__ == "__main__":
    main() 