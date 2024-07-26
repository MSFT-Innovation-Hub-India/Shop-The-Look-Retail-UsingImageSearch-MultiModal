from response_generation import *
from transcription import *
from datetime import datetime
import requests
import os
import base64
import websocket

from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
CORS(app)

load_dotenv()

# ip_address = "10.11.175.16"
# getAudioFile = {"base64": ""}

# delete_audio_file = requests.delete('http://' + ip_address + '/api/audio', json={"FileName": "capture_HeyMisty.wav"})

# recordAudio = requests.post('http://' + ip_address + '/api/audio/keyphrase/start', json={"CaptureSpeech": True, "OverwriteExisting": True})

# if recordAudio.status_code == 200:
#     getAudioFile = requests.get('http://' + ip_address + '/api/audio?FileName=capture_HeyMisty.wav&Base64=true')

# audioFile = getAudioFile.json()
# audioFile = audioFile['result']['base64']

azure_speech_key = os.getenv("AZURE_COMPUTER_VISION_KEY")

@app.route('/transcribe', methods=['POST'])
def transcription():
    data = requests.json()
    audioFile = data['result']['base64']
    with open("audio.wav", "wb") as file:
        file.write(base64.b64decode(audioFile))
    
    transcribed_text = transcribe()
    return transcribed_text
    
# transcribed_text_result = requests.post('https://stl-project-ai-services.cognitiveservices.azure.com/speechtotext/transcriptions:transcribe?api-version=2024-05-15-preview', headers={"Ocp-Apim-Subscription-Key": azure_speech_key}, data={"audio": "audio.wav"})
# transcribed_text = transcribed_text_result['combinedPhrases']['text']

# transcribed_text = transcribe()

@app.route('/response', methods=['POST'])
def generate_response():
    data = requests.json()
    personName = data['name']
    transcribed_text = data['prompt']
    previous_prompts = []
    previous_responses = []
    with open("order_data.json", "r") as file:
        order_data = json.load(file)
    user_found = None
    for user in order_data.get('users', []):  # Safely get the 'users' list, default to empty list if not found
        if user.get('name') == personName:  # Safely get the 'name' from the user, default to None if not found
            user_found = user
            break
    response = response_generation(transcribed_text, datetime.today().strftime('%Y-%m-%d'), json.dumps(user_found['orders']), json.dumps(previous_prompts), json.dumps(previous_responses))
    return response
    
    
    

# personName = "Pranav"
# previous_prompts = []
# previous_responses = []

# with open("order_data.json", "r") as file:
#     order_data = json.load(file)
    
# # Find the user in the 'users' array
# user_found = None
# for user in order_data.get('users', []):  # Safely get the 'users' list, default to empty list if not found
#     if user.get('name') == personName:  # Safely get the 'name' from the user, default to None if not found
#         user_found = user
#         break
    
# response = response_generation(transcribed_text, datetime.today().strftime('%Y-%m-%d'), json.dumps(user_found['orders']), json.dumps(previous_prompts), json.dumps(previous_responses))
# print(response)    

# while True:
#     query = input("Enter your query: ")
#     if(query == "exit"):
#         break
#     else:
#         response = response_generation(query, datetime.today().strftime('%Y-%m-%d'), json.dumps(user_found['orders']), json.dumps(previous_prompts), json.dumps(previous_responses))
#         previous_responses.append(response)
#         previous_prompts.append(query)
#         print(response)

if __name__ == '__main__':
    app.run(port=5000)