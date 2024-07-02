import streamlit as st
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import uuid
from response_generation import *
import requests
from intent_identification import *

# st.set_page_config(layout="wide")

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
                
if 'search_response' not in st.session_state:
    st.session_state.search_response = None

def update_search_response(params, force_update=False):
    global search_response
    # Only update search_response if it is None or force_update is True
    if st.session_state.search_response is None or force_update:
        st.session_state.search_response = requests.post("http://localhost:8080/search", json=params)


if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt, "image": image_url})

    with c.chat_message("user"):
        st.markdown(prompt)
        if image_url is not None:
            st.image(image_url, width=200)

    #################################################### 

    intent_result = identify_intent(prompt, image_url)
    # print(intent_result)
    
    
    if intent_result != "This is a follow up":
        force_update = True
    else:
        force_update = False
        
    # print(force_update)
        
    params = {'image_url': image_url, 'text_query': intent_result}
    update_search_response(params, force_update)
    
    # print("**********************")
    # print(st.session_state.search_response.json()[0]['name'])
    # print("**********************")

    # Check if the request was successful   
    st.session_state.search_response.raise_for_status()

    # Print the response from the server
    description_response = st.session_state.search_response.json()
    # print(description_response)
    print("################################")
    
    if intent_result != "This is a follow up":
        new_objects = []
        st.session_state.url_responses = []
        for i in range(0,3):
            st.session_state.url_responses.append(description_response[i]['url'])
            # url_response = description_response[0]['img']
            # description_response_at_i = description_response[i]['name']

            # openai_response = response_generation(description_response_at_i, prompt)
            description_response_new = {
                'name': description_response[i]['name']
            }
        
            new_objects.append(description_response_new)
        
        json_new_objects = json.dumps(new_objects)
        openai_response = response_generation(json_new_objects, prompt)
        if openai_response:
            # print(openai_response.choices[0].message.content)
            for i in range(len(st.session_state.url_responses)):
                results = [{"name": None, "url": st.session_state.url_responses[i]}]
                st.session_state.results.extend(results)
            # results = [{"name": openai_response, "url": url_responses}]
            st.session_state.messages.append({"role": "assistant", "content": openai_response.choices[0].message.content, "images": st.session_state.url_responses})

            with c.chat_message("assistant"):
                # st.image(results[0]['url'], width=200)
                st.write(openai_response.choices[0].message.content)
                cols = st.columns(3)
                for i in range(3):
                    with cols[i % 3]:
                        st.image(st.session_state.url_responses[i], width=200)

            # Append the new results to the results history
            st.session_state.results.extend(results)
                
    else:
        new_objects = []
        for i in range(0,3):
            description_response_new = {
                'name': description_response[i]['name']
            }
        
            new_objects.append(description_response_new)
        
        json_new_objects = json.dumps(new_objects)
            
        # print(json_new_objects)
        # print("################################")
        openai_response = response_generation(json_new_objects, prompt)
        
        if openai_response:
            # print(openai_response.choices[0].message.content)
            results = [{"name": openai_response, "url": None}]
            st.session_state.messages.append({"role": "assistant", "image": None, "content": openai_response.choices[0].message.content})

            with c.chat_message("assistant"):
                # st.image(results[0]['url'], width=200)
                st.write(openai_response.choices[0].message.content)

            # Append the new results to the results history
            st.session_state.results.extend(results)
        
with st.sidebar:
    num_results = len(st.session_state.results)
    if num_results > 0:
        cols = st.columns(3)
        for i, result in enumerate(st.session_state.results):
            with cols[i % 3]:
                if result["url"]:
                    st.image(result["url"], width=100)