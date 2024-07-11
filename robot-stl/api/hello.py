import cv2
import time

from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import uuid
from response_generation import *
import requests
from intent_identification import *
import azure.cognitiveservices.speech as speechsdk
import sys

from flask_cors import CORS
from flask import Flask
from flask import Flask, request, jsonify
from azure.search.documents.models import (
    HybridCountAndFacetMode,
    HybridSearch,
    SearchScoreThreshold,
    VectorizableTextQuery,
    VectorizableImageBinaryQuery,
    VectorizableImageUrlQuery,
    VectorSimilarityThreshold)
from vector_config import *
from data_configuration import *
from retrieval_configuration import *

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv(".env")

# Initialize Azure Blob Storage
connect_str = os.getenv("BLOB_CONNECTION_STRING")
container_name = os.getenv("BLOB_CONTAINER_NAME_IMG")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
speech_sub = os.getenv("AZURE_COMPUTER_VISION_KEY")
AZURE_AI_VISION_API_KEY = os.getenv("AZURE_COMPUTER_VISION_KEY")
AZURE_AI_VISION_ENDPOINT = os.getenv("AZURE_COMPUTER_VISION_ENDPOINT")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")
INDEX_NAME = "build-multimodal-demo"
SEARCH_SERVICE_API_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")

USE_AAD_FOR_SEARCH = False  # Set this to False to use API key for authentication

# Set Azure Search Credentials
azure_search_credential = authenticate_azure_search(api_key=SEARCH_SERVICE_API_KEY, use_aad_for_search=USE_AAD_FOR_SEARCH)

# Create a SearchIndexerClient instance
indexer_client = SearchIndexerClient(SEARCH_SERVICE_ENDPOINT, azure_search_credential)

# Call the function to create or update the data source
create_or_update_data_source(indexer_client, BLOB_CONTAINER_NAME, BLOB_CONNECTION_STRING, INDEX_NAME)

# Create index client and set up vector search configuration
index_client = SearchIndexClient(
    endpoint=SEARCH_SERVICE_ENDPOINT, credential=azure_search_credential
)
fields = create_fields()
vector_search = create_vector_search_configuration()

# Create the search index with the adjusted schema
create_search_index(index_client, INDEX_NAME, fields, vector_search)
print(f"Created index: {INDEX_NAME}")

# Create indexer client and skillset
client = SearchIndexerClient(
    endpoint=SEARCH_SERVICE_ENDPOINT, credential=azure_search_credential
)
skillset_name = f"{INDEX_NAME}-skillset"
text_embedding_skill = create_text_embedding_skill()
image_embedding_skill = create_image_embedding_skill()

create_skillset(client, skillset_name, text_embedding_skill, image_embedding_skill)
print(f"Created skillset: {skillset_name}")

indexer_client = SearchIndexerClient(
    endpoint=SEARCH_SERVICE_ENDPOINT, credential=azure_search_credential
)
data_source_name = f"{INDEX_NAME}-blob"
indexer_name = f"{INDEX_NAME}-indexer"

create_and_run_indexer(indexer_client, indexer_name, skillset_name, INDEX_NAME, data_source_name)

# Initialize the SearchClient
search_client = SearchClient(
    SEARCH_SERVICE_ENDPOINT,
    index_name=INDEX_NAME,
    credential=azure_search_credential,
)

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return "Hello, World!"

@app.route('/api/test', methods=['GET'])
def test():
    return "Test"

@app.route('/api/detect', methods=['GET'])
def detect_eyes():
    # Load the Haar cascade file for eye detection
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Start video capture from the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect eyes in the image for 3 seconds
        eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
        if(len(eyes)>0):
            delay=0
            while delay!=(3):
                eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
                if(len(eyes)>0):
                    time.sleep(1)
                    delay+=1
                else:
                    break
            if(delay==3):
                print("detected baby")
                cap.release()
                cv2.destroyAllWindows()
                return "eyes detected"

@app.route('/api/listen', methods=['GET'])
def listen():
    speech_config = speechsdk.SpeechConfig(subscription=speech_sub, region="northeurope")
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    speech_synthesizer_result = speech_synthesizer.speak_text_async("Hello, I am Ava. How can I help you today?").get()
    
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    result = speech_recognizer.recognize_once_async().get()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))

    identified_intent = identify_intent(result.text)

    return identified_intent

@app.route('/api/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text')
    speech_config = speechsdk.SpeechConfig(subscription=speech_sub, region="northeurope")
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    speech_synthesizer_result = speech_synthesizer.speak_text_async(text).get()
    return "Spoken"

@app.route('/api/search', methods = ['POST'])
def search():
    data = request.get_json()
    text_query = data.get('text_query')
    image_url = data.get('image_url')
    # Print received query and URL
    print(f"Received text query: {text_query}")
    print(f"Received image URL: {image_url}")

    text_vector_query = VectorizableTextQuery(
    text=text_query,
    k_nearest_neighbors=5,
    fields="descriptionVector",
    )

    text_image_vector_query = VectorizableTextQuery(
    text=text_query,
    k_nearest_neighbors=5,
    fields="imageVector",
    weight=50,
    )

    results = search_client.search(
        search_text=None, vector_queries=[text_vector_query, text_image_vector_query], top=3
    )

    response = []
    for result in results:        
        response.append({
            "id": result['id'],
            "name": result['description'],
            "score": result['@search.score'],
            "url": result['img'],
            "price": result['price']
        })
        
        # Print each result
        print(f"Name: {result['description']}")
        print(f"Score: {result['@search.score']}")
        print(f"URL: {result['img']}")
        print("-" * 50)

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5328)