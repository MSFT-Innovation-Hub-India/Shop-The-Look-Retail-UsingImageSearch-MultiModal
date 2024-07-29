from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import uuid
import requests
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv(".env")

# Initialize Azure Speech SDK
speech_sub = os.getenv("AZURE_COMPUTER_VISION_KEY")
speech_config = speechsdk.SpeechConfig(subscription=speech_sub, region="northeurope")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name = 'en-US-AvaMultilingualNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def from_mic(speech_config):
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = speech_recognizer.recognize_once_async().get()
    print(result.text)
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    return None

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return jsonify({"message": "Speech synthesis completed"}), 200
    else:
        return jsonify({"error": "Speech synthesis failed"}), 500

@app.route('/listen', methods=['POST'])
def listen():
    print("Receieved request")
    recognized_text = from_mic(speech_config)
    if recognized_text:
        return jsonify({"text": recognized_text}), 200
    return jsonify({"error": "No speech detected"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
