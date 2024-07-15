import os
from flask import Flask, request, jsonify
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.models import (
    HybridCountAndFacetMode,
    HybridSearch,
    SearchScoreThreshold,
    VectorizableTextQuery,
    VectorizableImageBinaryQuery,
    VectorizableImageUrlQuery,
    VectorSimilarityThreshold,
)
from dotenv import load_dotenv

from vector_config import *
from data_configuration import *
from retrieval_configuration import *

# Load environment variables
load_dotenv(".env")
app = Flask(__name__)


# Configuration
AZURE_AI_VISION_API_KEY = os.getenv("AZURE_COMPUTER_VISION_KEY")
AZURE_AI_VISION_ENDPOINT = os.getenv("AZURE_COMPUTER_VISION_ENDPOINT")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")
INDEX_NAME = "build-multimodal-demo"
SEARCH_SERVICE_API_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")

# User-specified parameter
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

# Define the text query
@app.route('/search', methods=['POST'])
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

    if image_url is not None:
        image_vector_query = VectorizableImageUrlQuery(
            url=image_url,
            k_nearest_neighbors=5,
            fields="imageVector",
        )

        results = search_client.search(
            search_text=None, vector_queries=[text_vector_query, image_vector_query, text_image_vector_query], top=3
        )
    else:
        results = search_client.search(
            search_text=None, vector_queries=[text_vector_query, text_image_vector_query], top=3
        )

    response = []
    for result in results:
        response.append({
            "name": result['description'],
            "score": result['@search.score'],
            "url": result['img'],
            "price": result['price']
        })
        
        # Print each result
        print(f"Name: {result['description']}")
        print(f"Score: {result['@search.score']}")
        print(f"URL: {result['img']}")
        print(f"Price: {result['price']}")
        print("-" * 50)

    return jsonify(response)

# Print a message indicating the server is running
print("Flask server is running...")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)