import streamlit as st
import base64
import requests
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import uuid 
# Load environment variables from .env file
load_dotenv(".env")

# Initialize Azure Blob Storage
connect_str = "DefaultEndpointsProtocol=https;AccountName=stlprojectstorage;AccountKey=W/hJZzTvxeC1FsCDC70If3W9rxA0Wo3e/uO9EAItdXe8v8duNZSEFgGCuImR0+hv95grfmpT0cE++AStymGoWQ==;EndpointSuffix=core.windows.net"
container_name = "image"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

st.title("🛍 Shop the Look")
st.caption("Upload an image and find similar items in our catalog")

# Initialize a variable to store the image URL
# image_url = None

# Initialize chat history and result history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "results" not in st.session_state:
    st.session_state.results = []

with st.sidebar:
    st.header('Result History')
    for result in st.session_state.results:
        st.image(result['url'], width=300)
        st.write("-" * 50)

c = st.container(height=550)

uploaded_file = st.file_uploader("Upload your image...", type=["jpg", "jpeg", "png"])

image_url = None

if uploaded_file is not None:
    image_id = uuid.uuid4().hex
    filename, file_extension = os.path.splitext(uploaded_file.name)
    filename = f"{image_id}{file_extension}"
    st.write(uploaded_file.name)
    # Upload the file to Azure Blob Storage

    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        blob_client.upload_blob(uploaded_file, overwrite=True)  # Ensure the blob is overwritten if it exists

        # Generate a SAS token for the uploaded image
        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=container_name,
            blob_name=filename,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )

        image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{filename}?{sas_token}"
        st.write(f"Image URL: {image_url}")

        # Display the image in Streamlit
        st.image(image_url, caption="Uploaded Image (Preview)", width=200)
    except Exception as e:
        st.error(f"Error uploading image: {e}")

def response_generator():

    try:
        params = {'image_url': image_url, 'text_query': prompt}
        response = requests.post("http://localhost:8080/search", json=params)  # Send as JSON
                
        if response.status_code == 200:
            results = response.json()
            st.success('Successfully retrieved from server')
                    
                    # Display search results and save them to session state
            for result in results:
                response = st.image(result['url'], width=100), st.write(f"Name: {result['name']}"), st.write(f"URL: {result['url']}"), st.write("-" * 50), st.session_state.results.append(result)
        else:
            st.error(f'Failed to retrieve from server. Status code: {response.status_code}')
    except Exception as e:
        st.error(f"Error: {e}")

    #Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "image": image_url})

# Display previous messages
for message in st.session_state.messages:
    with c.chat_message(message["role"]):
        st.write(message["content"])
        # if message["image"]:
        #     st.image(message["image"], width=100)
        if image_url:
            st.image(image_url)

# React to user input
if prompt := st.chat_input("What is up?"):
    if image_url is not None:  # Check if image_url is set
            st.image(image_url, width=100)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with c.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with c.chat_message("assistant"):
                response = response_generator()
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
