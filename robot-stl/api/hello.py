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
app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv(".env")

# Initialize Azure Blob Storage
connect_str = os.getenv("BLOB_CONNECTION_STRING")
container_name = os.getenv("BLOB_CONTAINER_NAME_IMG")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
speech_sub = os.getenv("AZURE_COMPUTER_VISION_KEY")

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


    return result.text

if __name__ == '__main__':
    app.run(port=5328)