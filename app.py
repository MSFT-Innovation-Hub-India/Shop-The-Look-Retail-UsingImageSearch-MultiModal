import streamlit as st
import base64
import requests
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Initialize Azure Blob Storage
# Load environment variables from .env file
load_dotenv(".env")

# Get the values from environment variables
connect_str = os.getenv("CONNECT_STR")
container_name = os.getenv("CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

st.title("🛍 Shop the Look")
st.caption("Upload an image and find similar items in our catalog")

# Initialize a variable to store the image URL
image_url = None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

c = st.container()

uploaded_file = st.file_uploader("Upload your image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image.", width=200)

    # Upload the file to Azure Blob Storage
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=uploaded_file.name)
        blob_client.upload_blob(uploaded_file, overwrite=True)  # Ensure the blob is overwritten if it exists

        # Generate a SAS token for the uploaded image
        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=container_name,
            blob_name=uploaded_file.name,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )

        image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{uploaded_file.name}?{sas_token}"
        st.write(f"Image URL: {image_url}")

        # Display the image in Streamlit
        st.image(image_url, caption="Uploaded Image (Preview)", width=200)
    except Exception as e:
        st.error(f"Error uploading image: {e}")
else:
    st.warning('Please upload an image')

# React to user input
prompt = st.text_input("What is up?", key="prompt")

# Check if prompt has been entered and process it
if prompt:
    # Display user message in chat message container
    with c.chat_message("user"):
        st.write(prompt)
        if image_url is not None:  # Check if image_url is set
            st.image(image_url, width=100)
            
            # Send GET request to Flask server with image URL and text input
            try:
                params = {'image_url': image_url, 'text': prompt}
                response = requests.post("http://localhost:8080/upload", data=params)
                
                if response.status_code == 200:
                    st.success('Successfully retrieved from server')
                else:
                    st.error(f'Failed to retrieve from server. Status code: {response.status_code}')
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error('Please upload an image')
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "image": image_url if uploaded_file else None})
