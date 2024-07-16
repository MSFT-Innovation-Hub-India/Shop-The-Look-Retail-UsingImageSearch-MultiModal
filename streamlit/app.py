import streamlit as st
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import uuid
from response_generation import *
import requests
from intent_identification import *

# st.set_page_config(layout="wide")

page_bg_img="""
<style>

[data-testid="stSidebarContent"]{
background-image: linear-gradient(#FEAE84, #BC3232);
}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Load environment variables from .env file
load_dotenv(".env")
st.warning('WARNING: This is a pre-production version. Certain functionality may be limited. Use with caution', icon="⚠️")

col1, col2, col3 = st.columns(3)

with col1:
    st.write('')

with col2:
    st.image('logo.png', width=230)

with col3:
    st.write('')

# Initialize chat history and result history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "results" not in st.session_state:
    st.session_state.results = []
    
if "prompts" not in st.session_state:
    st.session_state.prompts = []
    
if "intents" not in st.session_state:
    st.session_state.intents = []

with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Result History</h2>", unsafe_allow_html=True)

c = st.container(height=350)

uploaded_file = st.file_uploader("Upload your image...", type=["jpg", "jpeg", "png"])

image_url = None

if uploaded_file is not None:
    st.write("")
    st.spinner("Image Preview Loading...")
    try:
        # Send the image file to the Flask endpoint
        files = {'file': uploaded_file}
        response = requests.post('http://localhost:8080/upload_image', files=files)

        if response.status_code == 200:
            # Display the image URL returned by the server
            response_data = response.json()
            image_url = response_data.get('image_url')
            
            st.image(image_url, caption="Image Preview", width=200)

        else:
            st.write(f"Error Uploading File. Status code: {response.status_code}")
            st.write(response.json())  # Print error message from server if available

    except Exception as e:
        st.write(f"Error uploading image: {str(e)}")

# Display previous messages and results
for message in st.session_state.messages:
     # Print the message dictionary for debugging
    #st.write(message)
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
        if "images" in message and message["images"]:
            cols = st.columns(3)
            for i in range(len(message["images"])):
                with cols[i % 3]:
                    st.image(message["images"][i], width=200, caption = f"₹{message['price'][i]}")

if 'search_response' not in st.session_state:
    st.session_state.search_response = None

def update_search_response(params, force_update=False):
    global search_response
    # Only update search_response if it is None or force_update is True
    if st.session_state.search_response is None or force_update:
        st.session_state.search_response = requests.post("http://localhost:8080/search", json=params)

if prompt := st.chat_input("How can I help?"):
    st.session_state.prompts.append(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "image": image_url})

    with c.chat_message("user"):
        st.markdown(prompt)
        if image_url is not None:   
            st.image(image_url, width=200)

    #################################################### 

    intent_result = identify_intent(prompt, image_url, json.dumps(st.session_state.prompts), json.dumps(st.session_state.intents))
    st.session_state.intents.append(intent_result)
    print(intent_result)
    
    
    if intent_result != "This is a follow up":
        force_update = True
    else:
        force_update = False
        
    
    params = {'image_url': image_url, 'text_query': intent_result}
    update_search_response(params, force_update)
    
    st.session_state.search_response.raise_for_status()

    description_response = st.session_state.search_response.json()
    
    if intent_result != "This is a follow up":
        new_objects = []
        url_responses = []
        price_response = []
        for i in range(3):
            url_responses.append(description_response[i]['url'])
            price_response.append(str(int(description_response[i]['price'])))

            description_response_new = {
                'name': description_response[i]['name']
            }
        
            new_objects.append(description_response_new)
        
        json_new_objects = json.dumps(new_objects)
        print("*********************")
        openai_response = response_generation(json_new_objects, prompt)
        
        if openai_response:
            for i in range(len(url_responses)):
                results = [{"name": None, "url": url_responses[i],"price":price_response[i]}]
                st.session_state.results.extend(results)
                
            with c.chat_message("assistant"):
                st.write(openai_response.choices[0].message.content)
                cols = st.columns(3)
                for i in range(3):
                    with cols[i % 3]:
                        st.image(url_responses[i], width=200, caption=f"₹{price_response[i]}")
                        

            st.session_state.messages.append({"role": "assistant", "content": openai_response.choices[0].message.content, "images": url_responses,"price": price_response})
                
    else:
        new_objects = []
        for i in range(3):
            description_response_new = {
                'name': description_response[i]['name']
            }
        
            new_objects.append(description_response_new)
        
        json_new_objects = json.dumps(new_objects)
        
        openai_response = response_generation(json_new_objects, prompt)
        
        if openai_response:
            results = [{"name": openai_response, "url": None}]
            st.session_state.messages.append({"role": "assistant", "image": None, "content": openai_response.choices[0].message.content,})

            with c.chat_message("assistant"):
                st.write(openai_response.choices[0].message.content)

            st.session_state.results.extend(results)
        
with st.sidebar:
    num_results = len(st.session_state.results)
    #st.write(st.session_state.results)
    if num_results > 0:
        cols = st.columns(3)
        for i, result in enumerate(st.session_state.results):
            with cols[i % 3]:
                if result["url"]:
                    st.image(result["url"], width=100, caption = f"₹{result['price']}")
