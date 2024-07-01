import streamlit as st
import requests
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import uuid

# Load environment variables from .env file
load_dotenv(".env")

# Initialize Azure Blob Storage
connect_str = os.getenv("BLOB_CONNECTION_STRING")
container_name = os.getenv("BLOB_CONTAINER_NAME_IMG")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

st.title("🛍 Shop the Look")
st.caption("Upload an image and find similar items in our catalog")

# Initialize chat history and result history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "results" not in st.session_state:
    st.session_state.results = []

with st.sidebar:
    st.header('Result History')
    for result in st.session_state.results:
        st.image(result['url'], width=300)

c = st.container(height=550)

uploaded_file = st.file_uploader("Upload your image...", type=["jpg", "jpeg", "png"])

image_url = None

if uploaded_file is not None:
    image_id = uuid.uuid4().hex
    filename, file_extension = os.path.splitext(uploaded_file.name)
    filename = f"{image_id}{file_extension}"
    st.write(uploaded_file.name)

    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        blob_client.upload_blob(uploaded_file, overwrite=True)

        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=container_name,
            blob_name=filename,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )

        image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{filename}?{sas_token}"
        st.image(image_url, caption="Uploaded Image (Preview)", width=150)
    except Exception as e:
        st.error(f"Error uploading image: {e}")

def response_generator(image_url, prompt):
    try:
        params = {'image_url': image_url, 'text_query': prompt}
        response = requests.post("http://localhost:8080/search", json=params)

        if response.status_code == 200:
            results = response.json()
            return results
        else:
            st.error(f'Failed to retrieve from server. Status code: {response.status_code}')
    except Exception as e:
        st.error(f"Error: {e}")

    return []

# Display previous messages and results
for message in st.session_state.messages:
    with c.container():
        with st.chat_message("user" if message["role"] == "user" else "assistant"):
            st.markdown(message["content"])
            if "image" in message and message["image"]:
                st.image(message["image"], width=150)
            if "results" in message and message["results"]:
                for result in message["results"]:
                    st.image(result['url'], width=200)
                    st.write(f"Name: {result['name']}")
                    st.write(f"URL: {result['url']}")
                    st.write("-" * 50)

# React to user input
if prompt := st.chat_input("How can I help?"):
    if image_url is not None:
        st.session_state.messages.append({"role": "user", "content": prompt, "image": image_url})

        with c.container():
            with st.chat_message("user"):
                st.markdown(prompt)
                st.image(image_url, width=150)

                results = response_generator(image_url, prompt)

                st.session_state.messages.append({"role": "user", "content": prompt, "results": results})

        # Append the new results to the results history
        st.session_state.results.extend(results)

        with c.container():
            with c.chat_message("assistant"):
                for result in results:
                    st.image(result['url'], width=200)
                    st.write(f"Name: {result['name']}")
                    st.write(f"URL: {result['url']}")
                    st.write("-" * 50)
    else:
        st.session_state.messages.append({"role": "assistant", "content": "", "image": None})
        with c.chat_message("user"):
            st.markdown(prompt)

        # In case there is no image, just simulate empty results for now
        results = []

        st.session_state.messages.append({"role": "assistant", "content": "", "results": results})

        with c.chat_message("assistant"):
            st.markdown("No image provided. Please upload an image to get results.")
