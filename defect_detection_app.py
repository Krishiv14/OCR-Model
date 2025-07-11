import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io
import matplotlib.pyplot as plt
from skimage import feature, filters, morphology, measure
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
import pandas as pd

def init_page_config():
    """Initialize page configuration"""
    st.set_page_config(
        page_title="Defect Detection Tool",
        page_icon="🔍",
        layout="wide"
    )

def detect_scratches(image):
    """Detect scratches using edge detection and morphological operations"""
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

def detect_dents_cracks(image):
    """Detect dents and cracks using blob detection"""
    # Convert to grayscale
    gray = rgb2gray(np.array(image))
    
    # Apply Gaussian blur
    blurred = filters.gaussian(gray, sigma=1)
    
    # Apply Laplacian of Gaussian for blob detection
    blobs = feature.blob_log(blurred, max_sigma=30, num_sigma=10, threshold=0.1)
    
    # Filter blobs based on size
    valid_blobs = []
    for blob in blobs:
        y, x, r = blob
        if 5 < r < 50:  # Filter by radius
            valid_blobs.append(blob)
    
    return valid_blobs, blurred

def detect_surface_defects(image):
    """Detect general surface defects using texture analysis"""
    # Convert to grayscale
    gray = rgb2gray(np.array(image))
    
    # Apply local binary pattern for texture analysis
    lbp = feature.local_binary_pattern(gray, P=8, R=1, method='uniform')
    
    # Calculate texture statistics
    hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 10), range=(0, 9))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)
    
    # Detect anomalies using threshold
    threshold = np.percentile(lbp, 95)
    defect_mask = lbp > threshold
    
    # Morphological operations to clean up the mask
    kernel = morphology.disk(3)
    defect_mask = morphology.binary_opening(defect_mask, kernel)
    defect_mask = morphology.binary_closing(defect_mask, kernel)
    
    # Find connected components
    labels = measure.label(defect_mask)
    regions = measure.regionprops(labels)
    
    # Filter regions by area
    valid_regions = [region for region in regions if region.area > 100]
    
    return valid_regions, lbp, defect_mask

def analyze_image_quality(image):
    """Analyze overall image quality and detect potential issues"""
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
    
    # Detect noise using high-frequency components
    f_transform = np.fft.fft2(gray)
    f_shift = np.fft.fftshift(f_transform)
    magnitude_spectrum = np.log(np.abs(f_shift) + 1)
    
    # Calculate noise level
    noise_level = np.std(magnitude_spectrum)
    
    return {
        'brightness': brightness,
        'contrast': contrast,
        'sharpness': sharpness,
        'noise_level': noise_level
    }

def main():
    init_page_config()
    
    st.title("🔍 Defect Detection Tool")
    st.markdown("---")
    
    # Sidebar for detection options
    st.sidebar.header("Detection Options")
    detection_type = st.sidebar.selectbox(
        "Select Detection Type",
        ["All Defects", "Scratches Only", "Dents & Cracks", "Surface Defects", "Quality Analysis"]
    )
    
    sensitivity = st.sidebar.slider("Detection Sensitivity", 1, 10, 5)
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Input Image")
        upload_tab, camera_tab = st.tabs(["📁 Upload", "📷 Camera"])
        
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
                    scratch_contours, edges, closed = detect_scratches(image)
                    results['scratches'] = {
                        'contours': scratch_contours,
                        'count': len(scratch_contours),
                        'edges': edges,
                        'closed': closed
                    }
                
                if detection_type in ["All Defects", "Dents & Cracks"]:
                    blobs, blurred = detect_dents_cracks(image)
                    results['dents_cracks'] = {
                        'blobs': blobs,
                        'count': len(blobs),
                        'blurred': blurred
                    }
                
                if detection_type in ["All Defects", "Surface Defects"]:
                    regions, lbp, defect_mask = detect_surface_defects(image)
                    results['surface_defects'] = {
                        'regions': regions,
                        'count': len(regions),
                        'lbp': lbp,
                        'mask': defect_mask
                    }
                
                if detection_type in ["All Defects", "Quality Analysis"]:
                    quality_metrics = analyze_image_quality(image)
                    results['quality'] = quality_metrics
                
                # Display results
                display_results(image, results, detection_type, sensitivity)
        else:
            st.info("Upload an image and click 'Detect Defects' to analyze")

def display_results(image, results, detection_type, sensitivity):
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
                    y, x, r = blob
                    cv2.circle(blob_img, (int(x), int(y)), int(r), (255, 0, 0), 2)
                
                st.image(blob_img, caption="Detected Dents/Cracks", use_container_width=True)
        
        with tabs[3]:  # Surface Defects tab
            if 'surface_defects' in results:
                st.subheader("Surface Defect Detection")
                st.write(f"Found {results['surface_defects']['count']} surface defects")
                
                # Create visualization
                defect_img = np.array(image).copy()
                mask = results['surface_defects']['mask']
                
                # Overlay defects on original image
                defect_img[mask] = [255, 0, 0]  # Red overlay for defects
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image(defect_img, caption="Surface Defects", use_container_width=True)
                with col2:
                    st.image(mask, caption="Defect Mask", use_container_width=True)
        
        with tabs[4]:  # Quality tab
            if 'quality' in results:
                st.subheader("Image Quality Analysis")
                
                # Create quality visualization
                fig, axes = plt.subplots(2, 2, figsize=(10, 8))
                
                # Brightness histogram
                gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
                axes[0, 0].hist(gray.ravel(), bins=256, alpha=0.7)
                axes[0, 0].set_title('Brightness Distribution')
                axes[0, 0].set_xlabel('Pixel Value')
                axes[0, 0].set_ylabel('Frequency')
                
                # Contrast analysis
                axes[0, 1].imshow(gray, cmap='gray')
                axes[0, 1].set_title('Grayscale Image')
                axes[0, 1].axis('off')
                
                # Sharpness analysis
                laplacian = cv2.Laplacian(gray, cv2.CV_64F)
                axes[1, 0].hist(laplacian.ravel(), bins=50, alpha=0.7)
                axes[1, 0].set_title('Sharpness Distribution')
                axes[1, 0].set_xlabel('Laplacian Value')
                axes[1, 0].set_ylabel('Frequency')
                
                # Noise analysis
                f_transform = np.fft.fft2(gray)
                f_shift = np.fft.fftshift(f_transform)
                magnitude_spectrum = np.log(np.abs(f_shift) + 1)
                axes[1, 1].imshow(magnitude_spectrum, cmap='gray')
                axes[1, 1].set_title('Frequency Domain')
                axes[1, 1].axis('off')
                
                plt.tight_layout()
                st.pyplot(fig)
    
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

if __name__ == "__main__":
    main() 