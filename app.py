import streamlit as st
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import uuid
from response_generation import *
import requests
from intent_identification import *

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
    st.header('Results')
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
        st.image(image_url, caption="Uploaded Image (Preview)", width=200)
    except Exception as e:
        st.error(f"Error uploading image: {e}")

# Function to call inputoutput.py and capture its output
# def call_inputoutput(image_url, prompt):
#     try:
#         result = subprocess.run(['python', 'inputoutput.py'], input=f'{image_url}\n{prompt}', text=True, capture_output=True, check=True)
#         output_lines = result.stdout.splitlines()
#         openai_response = output_lines[-2]
#         url_response = output_lines[-1]
#         return openai_response, url_response
#     except subprocess.CalledProcessError as e:
#         st.error(f"An error occurred: {e}")
#         return None, None

# Display previous messages and results
for message in st.session_state.messages:
    with c.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(message["content"])
        if "image" in message and message["image"]:
            st.image(message["image"], width=200)
        if "results" in message and message["results"]:
            for result in message["results"]:
                st.image(result['url'], width=250)
                st.write(f"Name: {result['name']}")
                st.write(f"URL: {result['url']}")
                st.write("-" * 50)

# React to user input
if prompt := st.chat_input("How can I help?"):
    if image_url is not None:
        st.session_state.messages.append({"role": "user", "content": prompt, "image": image_url})

        with c.chat_message("user"):
            st.markdown(prompt)
            st.image(image_url, width=200)

        #################################################### 

        intent_result = identify_intent(prompt, image_url)

        params = {'image_url': image_url, 'text_query': intent_result}
        search_response = requests.post("http://localhost:8080/search", json=params)
        
        # Check if the request was successful
        search_response.raise_for_status()

        # Print the response from the server
        description_response = search_response.json()
        print(description_response)
        for i in range(0,3):
            url_response = description_response[i]['url']
            # url_response = description_response[0]['img']
            description_response_at_i = description_response[i]['name']

            openai_response = response_generation(description_response_at_i, prompt)
            if openai_response:
                # print(openai_response.choices[0].message.content)
                results = [{"name": openai_response, "url": url_response}]
                st.session_state.messages.append({"role": "assistant", "image": url_response, "content": openai_response.choices[0].message.content})

                with c.chat_message("assistant"):
                    st.image(results[0]['url'], width=200)
                    st.write(openai_response.choices[0].message.content)
                    # col1, col2, col3 = st.columns(3)
                    # for i, result in enumerate(results):
                    #     if(i == 0):
                    #         # with col1:
                    #             st.image(result['url'], width=200)
                    #             st.write(openai_response.choices[i].message.content)
                    #     elif(i == 1):
                    #         # with col2:
                    #             st.image(result['url'], width=200)
                    #             st.write(openai_response.choices[i].message.content)
                    #     elif(i == 2):
                    #         # with col3:
                    #             st.image(result['url'], width=200)
                    #             st.write(openai_response.choices[i].message.content)
                        # st.write(f"Name: {result['name']}")
                        # st.write(f"URL: {result['url']}")
                        # st.write("-" * 50)

                # Append the new results to the results history
                st.session_state.results.extend(results)
            else:
                st.session_state.messages.append({"role": "assistant", "content": "No results returned.", "results": []})
                with c.chat_message("assistant"):
                    st.markdown("No results returned.")

    else:
        st.session_state.messages.append({"role": "user", "content": prompt, "image": None})
        with c.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "assistant", "content": "No image provided. Please upload an image to get results.", "results": []})
        with c.chat_message("assistant"):
            st.markdown("No image provided. Please upload an image to get results.")
