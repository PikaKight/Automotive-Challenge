import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Parking Spot Finder", page_icon="🅿️", layout="centered")

# Title and subtitle
st.title("🚗 Smart Parking Spot Finder")
st.markdown("### Welcome to your AI-powered parking assistant!")
st.markdown("Upload an image, and we'll help you find the best available parking spot.")

# File uploader for image input
uploaded_file = st.file_uploader("Upload a picture of the parking lot", type=["jpg", "png", "jpeg"])

# Placeholders for processing message and results
status_placeholder = st.empty()
image_placeholder = st.empty()

if uploaded_file is not None:
    status_placeholder.markdown(
        """
        <div style="display: flex; align-items: center;">
            <span style="margin-right: 10px;">Processing...</span>
            <img src="https://i.gifer.com/ZZ5H.gif" width="30"/>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Send POST request with the image
    backend_url = "http://localhost:5000/get-parking-spots"
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}

    try:
        response = requests.post(backend_url, files=files)

        if response.status_code == 200:
            result = response.json()
            processed_file_url = result.get("processed_image")  # Get the correct processed image URL
            print(processed_file_url)

            if processed_file_url:
                status_placeholder.markdown("### ✅ The following parking spots are available:")
                image_placeholder.image(processed_file_url, caption="Processed Parking Lot", use_column_width=True)
            else:
                status_placeholder.markdown("### ❌ Error: Processed image not found on server.")

        else:
            status_placeholder.markdown("### ❌ Something went wrong while processing the image.")
            st.write(response.json())

    except requests.exceptions.RequestException as e:
        status_placeholder.markdown("### ❌ Failed to connect to the backend.")
        st.write(e)
