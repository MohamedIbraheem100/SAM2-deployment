import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import base64
import requests 
import json
import io

st.title("SAM2 Segmentation: Select Two Points on Image")

uploaded_file = st.file_uploader(
    "Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    # Save points
    if "points" not in st.session_state:
        st.session_state.points = []

    st.subheader("Click on TWO points")

    value = streamlit_image_coordinates(image)

    if value and len(st.session_state.points) < 2:
        st.session_state.points.append((value["x"], value["y"]))

    # Draw points on copy
    output_image = image.copy()
    draw = ImageDraw.Draw(output_image)

    for i, point in enumerate(st.session_state.points):
        x, y = point
        r = 8
        draw.ellipse((x-r, y-r, x+r, y+r), fill="red")
        draw.text((x+10, y+10), f"P{i+1}", fill="red")

    st.subheader("Image with Points")
    # st.image(output_image, use_container_width=True)
    st.image(output_image, width='stretch')

    # # Show coordinates
    # if len(st.session_state.points) > 0:
    #     st.write("Selected Coordinates:")
    #     for i, point in enumerate(st.session_state.points):
    #         st.write(f"Point {i+1}: X = {point[0]}, Y = {point[1]}")

    # #  Show original image again
    # st.subheader("Image without background")
    # st.image(image, use_container_width=True)

    # # Reset button
    # if st.button("Reset"):
    #     st.session_state.points = []
# إرسال الصورة + النقاط لـ FastAPI عند اختيار نقطتين
    if len(st.session_state.points) == 2:
        # Base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        img_base64 = f"data:image/png;base64,{img_str}"
        
         #  debug: 
        st.write("Base64 length:", len(img_base64))
        st.write("Points:", st.session_state.points)

        # POST request
        payload = {"image_base64": img_base64, "points": st.session_state.points}
        response = requests.post("http://127.0.0.1:8010/segment", json=payload)

        if response.status_code == 200:
            st.subheader("Segmented Images")
            segmented_images = response.json()["segmented_images"]
            for i, img_b64 in enumerate(segmented_images):
                img_data = base64.b64decode(img_b64)
                segmented_img = Image.open(io.BytesIO(img_data))
                st.image(segmented_img, caption=f"Segmented for Point {i+1}", use_container_width=True)
        else:
            st.error(f"API Error: {response.text}")

    # زر Reset
    if st.button("Reset"):
        st.session_state.points = []