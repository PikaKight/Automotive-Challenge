import streamlit as st
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Parking Spot Finder", page_icon="🅿️", layout="centered")

# Title and subtitle
st.title("🚗 Smart Parking Spot Finder")
st.markdown("### Welcome to your AI-powered parking assistant!")
st.markdown("Upload an image, and we'll help you find the best available parking spot.")

# File uploader for image input
uploaded_file = st.file_uploader("Upload a picture of the parking lot", type=["jpg", "png", "jpeg"])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Parking Lot Image", use_column_width=True)
    st.success("Image uploaded successfully! Processing...")
