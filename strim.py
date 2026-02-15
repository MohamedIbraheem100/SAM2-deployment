
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

st.title("Select Two Points on Image")

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
    st.image(output_image, use_container_width=True)

    # Show coordinates
    if len(st.session_state.points) > 0:
        st.write("Selected Coordinates:")
        for i, point in enumerate(st.session_state.points):
            st.write(f"Point {i+1}: X = {point[0]}, Y = {point[1]}")

    # ✅ Show original image again
    st.subheader("Image without background")
    st.image(image, use_container_width=True)

    # Reset button
    if st.button("Reset"):
        st.session_state.points = []
