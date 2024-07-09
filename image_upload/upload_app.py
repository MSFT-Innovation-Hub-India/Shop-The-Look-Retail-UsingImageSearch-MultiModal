import streamlit as st
import requests

# Define the Flask endpoint URL
UPLOAD_URL = "http://localhost:5003/upload_image"  # Replace with your actual endpoint URL

st.title('Image Uploader')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.write("")
    st.write("Uploading...")

    try:
        # Send the image file to the Flask endpoint
        files = {'file': uploaded_file}
        response = requests.post(UPLOAD_URL, files=files)

        if response.status_code == 200:
            st.write("Upload successful!")
            # Display the image URL returned by the server
            response_data = response.json()
            image_url = response_data.get('image_url')
            
            st.image(image_url, caption="Uploaded Image (Preview)", width=200)

            st.write(f"Image URL: {image_url}")

        else:
            st.write(f"Upload failed. Status code: {response.status_code}")
            st.write(response.json())  # Print error message from server if available

    except Exception as e:
        st.write(f"Error uploading image: {str(e)}")
