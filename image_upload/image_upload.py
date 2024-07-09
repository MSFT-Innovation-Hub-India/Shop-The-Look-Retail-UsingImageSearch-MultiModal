import uuid
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Load environment variables from .env file
load_dotenv(".env")

# Initialize Azure Blob Storage
connect_str = os.getenv("BLOB_CONNECTION_STRING")
container_name = os.getenv("BLOB_CONTAINER_NAME_IMG")
#blob_service_client = BlobServiceClient.from_connection_string(connect_str)

def initialize_blob_service(connect_str):
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    return blob_service_client

def generate_image_url(blob_service_client, container_name, filename):
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=filename,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{filename}?{sas_token}"
    return image_url

@app.route('/upload_image', methods=['POST'])
def upload_image_endpoint():
    uploaded_file = request.files.get('file')

    if not uploaded_file:
        return jsonify({'error': 'No file provided'}), 400

    try:
        # Initialize the blob service client
        blob_service_client = initialize_blob_service(connect_str)
        
        # Process the uploaded file
        image_id = uuid.uuid4().hex
        filename, file_extension = os.path.splitext(uploaded_file.filename)
        filename = f"{image_id}{file_extension}"

        # Upload the file to Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        blob_client.upload_blob(uploaded_file, overwrite=True)

        # Generate the SAS token and image URL
        image_url = generate_image_url(blob_service_client, container_name, filename)

        return jsonify({'image_url': image_url, 'filename': uploaded_file.filename})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5003, debug=True)
