import streamlit as st
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(page_title="Image Coordinate Detector", layout="wide")

# Title
st.title("📍 Image Object Coordinate Detector")

# Initialize session state
if 'coordinates' not in st.session_state:
    st.session_state.coordinates = []
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []

# Sidebar for uploading images
with st.sidebar:
    st.header("Upload Images")

    # Main image upload
    main_image = st.file_uploader("Upload Main Image", type=[
                                  'png', 'jpg', 'jpeg', 'webp'])

    # Additional images upload
    other_images = st.file_uploader(
        "Upload Additional Images",
        type=['png', 'jpg', 'jpeg', 'webp'],
        accept_multiple_files=True
    )

    # Clear coordinates button
    if st.button("Clear Coordinates"):
        st.session_state.coordinates = []
        st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if main_image is not None:
        # Load and display the main image
        image = Image.open(main_image)

        st.subheader("Main Image (Click to get coordinates)")

        # Get image dimensions
        img_width, img_height = image.size

        # Convert image to base64 for HTML
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Create clickable image with JavaScript
        html_code = f"""
        <div style="position: relative; display: inline-block;">
            <img id="clickable-image" src="data:image/png;base64,{img_str}" 
                 style="max-width: 100%; height: auto; cursor: crosshair;"
                 onclick="getCoordinates(event)">
        </div>
        
        <script>
        function getCoordinates(event) {{
            var img = document.getElementById('clickable-image');
            var rect = img.getBoundingClientRect();
            
            // Get click position relative to image
            var x = event.clientX - rect.left;
            var y = event.clientY - rect.top;
            
            // Calculate actual image coordinates (accounting for scaling)
            var scaleX = {img_width} / rect.width;
            var scaleY = {img_height} / rect.height;
            
            var actualX = Math.round(x * scaleX);
            var actualY = Math.round(y * scaleY);
            
            // Send coordinates back to Streamlit
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: {{x: actualX, y: actualY}}
            }}, '*');
        }}
        </script>
        """

        # Use streamlit-javascript component alternative
        # Since we can't directly use JavaScript, we'll use streamlit_image_coordinates
        try:
            from streamlit_image_coordinates import streamlit_image_coordinates

            # Display image and get coordinates on click
            coords = streamlit_image_coordinates(image, key="image_coords")

            if coords is not None:
                x, y = coords["x"], coords["y"]
                st.session_state.coordinates.append((x, y))
                st.rerun()

        except ImportError:
            st.warning(
                "⚠️ For click functionality, install: `pip install streamlit-image-coordinates`")
            st.image(image, use_container_width=True)

            # Manual coordinate input as fallback
            st.subheader("Manual Coordinate Input")
            col_x, col_y, col_add = st.columns([1, 1, 1])
            with col_x:
                x_coord = st.number_input(
                    "X Coordinate", min_value=0, max_value=img_width, value=0)
            with col_y:
                y_coord = st.number_input(
                    "Y Coordinate", min_value=0, max_value=img_height, value=0)
            with col_add:
                if st.button("Add Coordinate", use_container_width=True):
                    st.session_state.coordinates.append((x_coord, y_coord))
                    st.rerun()
    else:
        st.info("👆 Please upload a main image from the sidebar")

with col2:
    st.subheader("Recorded Coordinates")

    if st.session_state.coordinates:
        for idx, (x, y) in enumerate(st.session_state.coordinates, 1):
            st.write(f"**Point {idx}:** X={x}, Y={y}")

        # Export coordinates
        if st.button("📋 Copy Coordinates"):
            coords_text = "\n".join(
                [f"{x},{y}" for x, y in st.session_state.coordinates])
            st.code(coords_text, language="text")
    else:
        st.info("Click on the image to record coordinates")

    # Display image dimensions
    if main_image is not None:
        st.divider()
        st.write(f"**Image Size:** {img_width} x {img_height} pixels")

# Display additional images
if other_images:
    st.divider()
    st.subheader("Additional Images")

    # Create columns for additional images
    cols = st.columns(min(len(other_images), 3))

    for idx, uploaded_file in enumerate(other_images):
        with cols[idx % 3]:
            img = Image.open(uploaded_file)
            st.image(img, caption=uploaded_file.name, use_container_width=True)
            st.caption(f"Size: {img.size[0]} x {img.size[1]} pixels")

# Instructions
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    ### Instructions:
    
    1. **Upload Main Image**: Use the sidebar to upload the image you want to analyze
    2. **Click on Objects**: Click anywhere on the image to record coordinates
    3. **View Coordinates**: All clicked coordinates appear in the right panel
    4. **Upload Additional Images**: Upload other images for comparison or reference
    5. **Clear Coordinates**: Use the button in the sidebar to reset all coordinates
    
    ### Installation Note:
    For automatic click-to-coordinate functionality, install:
    ```bash
    pip install streamlit-image-coordinates
    ```
    
    Without this package, you can use manual coordinate input instead.
    """)
