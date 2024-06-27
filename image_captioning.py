import json
import os
from uuid import uuid4

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient

# Get environment variables for Azure AI Vision
try:
    endpoint = os.getenv("AZURE_COMPUTER_VISION_ENDPOINT")
    key = os.getenv("AZURE_COMPUTER_VISION_KEY")
    connection_string = os.getenv("BLOB_CONNECTION_STRING")
    container_name = os.getenv("BLOB_CONTAINER_NAME")
    # container_name = "vector-sandbox"
except KeyError as e:
    print(f"Missing environment variable: {str(e)}")
    print("Set them before running this sample.")
    exit()

# Create an Image Analysis client
client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Setup for Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

def get_caption(image_url):
    """
    Get a caption for the image using Azure AI Vision.
    """
    try:
        result = client.analyze_from_url(
            image_url=image_url,
            visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
            gender_neutral_caption=False
        )
        if result.caption is not None:
            return result.caption.text
        else:
            return "No caption available"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error generating caption"

def generate_json_objects():
    json_objects = []

    # Iterate over the blobs in the container
    for blob in container_client.list_blobs():
        image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob.name}"
        caption = get_caption(image_url)

        json_object = {"id": str(uuid4()), "imageUrl": image_url, "caption": caption}
        json_objects.append(json_object)

    return json_objects

def write_to_file(json_objects):
    # Write the updated JSON to a file
    with open("build-demo.json", "w") as json_file:
        json.dump(json_objects, json_file, indent=4)

json_objects = generate_json_objects()
write_to_file(json_objects)