# ---- DEPRECATED ----
# ---- USE APP.PY INSTEAD ----


import os

from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    AIServicesVisionParameters,
    AIServicesVisionVectorizer,
    AIStudioModelCatalogName,
    AzureMachineLearningVectorizer,
    AzureOpenAIVectorizer,
    AzureOpenAIModelName,
    AzureOpenAIParameters,
    BlobIndexerDataToExtract,
    BlobIndexerParsingMode,
    CognitiveServicesAccountKey,
    DefaultCognitiveServicesAccount,
    ExhaustiveKnnAlgorithmConfiguration,
    ExhaustiveKnnParameters,
    FieldMapping,
    HnswAlgorithmConfiguration,
    HnswParameters,
    IndexerExecutionStatus,
    IndexingParameters,
    IndexingParametersConfiguration,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    ScalarQuantizationCompressionConfiguration,
    ScalarQuantizationParameters,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SearchIndexer,
    SearchIndexerDataContainer,
    SearchIndexerDataIdentity,
    SearchIndexerDataSourceConnection,
    SearchIndexerSkillset,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    SimpleField,
    VectorSearch,
    VectorSearchAlgorithmKind,
    VectorSearchAlgorithmMetric,
    VectorSearchProfile,
    VisionVectorizeSkill
)
from azure.search.documents.models import (
    HybridCountAndFacetMode,
    HybridSearch,
    SearchScoreThreshold,
    VectorizableTextQuery,
    VectorizableImageBinaryQuery,
    VectorizableImageUrlQuery,
    VectorSimilarityThreshold,
)
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
# from IPython.display import Image, display, HTML
from openai import AzureOpenAI
import pandas as pd


# Load environment variables
load_dotenv()

# Configuration
AZURE_AI_VISION_API_KEY = os.getenv("AZURE_COMPUTER_VISION_KEY")
AZURE_AI_VISION_ENDPOINT = os.getenv("AZURE_COMPUTER_VISION_ENDPOINT")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")
INDEX_NAME = "build-multimodal-demo"
SEARCH_SERVICE_API_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")

# print(AZURE_AI_VISION_API_KEY)

# User-specified parameter
USE_AAD_FOR_SEARCH = False  # Set this to False to use API key for authentication

def authenticate_azure_search(api_key=SEARCH_SERVICE_API_KEY, use_aad_for_search=False):
    if use_aad_for_search:
        print("Using AAD for authentication.")
        credential = DefaultAzureCredential()
    else:
        print("Using API keys for authentication.")
        if api_key is None:
            raise ValueError("API key must be provided if not using AAD for authentication.")
        credential = AzureKeyCredential(api_key)
    return credential

azure_search_credential = authenticate_azure_search(api_key=SEARCH_SERVICE_API_KEY, use_aad_for_search=USE_AAD_FOR_SEARCH)

def create_or_update_data_source(indexer_client, container_name, connection_string, index_name):
    """
    Create or update a data source connection for Azure AI Search.
    """
    container = SearchIndexerDataContainer(name=container_name)
    data_source_connection = SearchIndexerDataSourceConnection(
        name=f"{index_name}-blob",
        type="azureblob",
        connection_string=connection_string,
        container=container
    )
    try:
        indexer_client.create_or_update_data_source_connection(data_source_connection)
        print(f"Data source '{index_name}-blob' created or updated successfully.")
    except Exception as e:
        raise Exception(f"Failed to create or update data source due to error: {e}")

# Create a SearchIndexerClient instance
indexer_client = SearchIndexerClient(SEARCH_SERVICE_ENDPOINT, azure_search_credential)

# Call the function to create or update the data source
create_or_update_data_source(indexer_client, BLOB_CONTAINER_NAME, BLOB_CONNECTION_STRING, INDEX_NAME)

def create_fields():
    """Creates the fields for the search index based on the specified schema."""
    return [
        SimpleField(
            name="id", type=SearchFieldDataType.String, key=True, filterable=True
        ),
        SearchField(name="description", type=SearchFieldDataType.String, searchable=True),
        SearchField(name="img", type=SearchFieldDataType.String, searchable=True),
        SearchField(
            name="descriptionVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=1024,
            vector_search_profile_name="myHnswProfile",
            stored=False,
        ),
        SearchField(
            name="imageVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=1024,
            vector_search_profile_name="myHnswProfile",
            stored=False,
        ),
    ]


def create_vector_search_configuration():
    """Creates the vector search configuration."""
    return VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="myHnsw",
                parameters=HnswParameters(
                    m=4,
                    ef_construction=400,
                    ef_search=500,
                    metric=VectorSearchAlgorithmMetric.COSINE,
                ),
            )
        ],
        compressions=[
            ScalarQuantizationCompressionConfiguration(
                name="myScalarQuantization",
                rerank_with_original_vectors=True,
                default_oversampling=10,
                parameters=ScalarQuantizationParameters(quantized_data_type="int8"),
            )
        ],
        vectorizers=[
            AIServicesVisionVectorizer(
                name="myAIServicesVectorizer",
                kind="aiServicesVision",
                ai_services_vision_parameters=AIServicesVisionParameters(
                    model_version="2023-04-15",
                    resource_uri=AZURE_AI_VISION_ENDPOINT,
                    api_key=AZURE_AI_VISION_API_KEY,
                ),
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="myHnswProfile",
                algorithm_configuration_name="myHnsw",
                compression_configuration_name="myScalarQuantization",
                vectorizer="myAIServicesVectorizer",
            )
        ],
    )


def create_search_index(index_client, index_name, fields, vector_search):
    """Creates or updates a search index."""
    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search,
    )
    index_client.create_or_update_index(index=index)


index_client = SearchIndexClient(
    endpoint=SEARCH_SERVICE_ENDPOINT, credential=azure_search_credential
)
fields = create_fields()
vector_search = create_vector_search_configuration()

# Create the search index with the adjusted schema
create_search_index(index_client, INDEX_NAME, fields, vector_search)
print(f"Created index: {INDEX_NAME}")

def create_text_embedding_skill():
    return VisionVectorizeSkill(
        name="text-embedding-skill",
        description="Skill to generate embeddings for text via Azure AI Vision",
        context="/document",
        model_version="2023-04-15",
        inputs=[InputFieldMappingEntry(name="text", source="/document/description")],
        outputs=[OutputFieldMappingEntry(name="vector", target_name="descriptionVector")],
    )

def create_image_embedding_skill():
    return VisionVectorizeSkill(
        name="image-embedding-skill",
        description="Skill to generate embeddings for image via Azure AI Vision",
        context="/document",
        model_version="2023-04-15",
        inputs=[InputFieldMappingEntry(name="url", source="/document/img")],
        outputs=[OutputFieldMappingEntry(name="vector", target_name="imageVector")],
    )

def create_skillset(client, skillset_name, text_embedding_skill, image_embedding_skill):
    skillset = SearchIndexerSkillset(
        name=skillset_name,
        description="Skillset for generating embeddings",
        skills=[text_embedding_skill, image_embedding_skill],
        cognitive_services_account=CognitiveServicesAccountKey(
            key=AZURE_AI_VISION_API_KEY,
            description="AI Vision Multi Service Account in North Europe",
        ),
    )
    client.create_or_update_skillset(skillset)

client = SearchIndexerClient(
    endpoint=SEARCH_SERVICE_ENDPOINT, credential=azure_search_credential
)
skillset_name = f"{INDEX_NAME}-skillset"
text_embedding_skill = create_text_embedding_skill()
image_embedding_skill = create_image_embedding_skill()

create_skillset(client, skillset_name, text_embedding_skill, image_embedding_skill)
print(f"Created skillset: {skillset_name}")

def create_and_run_indexer(indexer_client, indexer_name, skillset_name, index_name, data_source_name):
    indexer = SearchIndexer(
        name=indexer_name,
        description="Indexer to index documents and generate embeddings",
        skillset_name=skillset_name,
        target_index_name=index_name,
        data_source_name=data_source_name,
        parameters=IndexingParameters(
            configuration=IndexingParametersConfiguration(
                parsing_mode=BlobIndexerParsingMode.DELIMITED_TEXT,
                query_timeout=None,
            ),
        ),
        field_mappings=[FieldMapping(source_field_name="id", target_field_name="id")],
        output_field_mappings=[
            FieldMapping(source_field_name="/document/descriptionVector", target_field_name="descriptionVector"),
            FieldMapping(source_field_name="/document/imageVector", target_field_name="imageVector"),
        ],
    )

    indexer_client.create_or_update_indexer(indexer)
    print(f"{indexer_name} created or updated.")
    
    def index_exists(index_client, index_name):
        try:
            index_client.get_index(index_name)
            return True
        except Exception:
            return False
        
    # if not index_exists(index_client, index_name):
    # indexer_client.run_indexer(indexer_name)
    # print(f"{indexer_name} is running. If queries return no results, please wait a bit and try again.")

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
query = "jacket of the same style as the image"
text_vector_query = VectorizableTextQuery(
    text=query,
    k_nearest_neighbors=5,
    fields="descriptionVector",
)

text_image_vector_query = VectorizableTextQuery(
    text=query,
    k_nearest_neighbors=5,
    fields="imageVector",
    # weight=100,
)

# Define the image query
image_vector_query = VectorizableImageUrlQuery(  # Alternatively, use VectorizableImageBinaryQuery
    # url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # Image of a Red Nike Running Shoe
    # url = "https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/18198270/2022/7/12/282737f5-b38e-4c6e-89ad-745630638d3c1657628613069-Biba-Women-Kurtas-9431657628612606-4.jpg",
    url = "https://stlprojectstorage.blob.core.windows.net/image/Fashion1.jpeg?se=2024-06-26T12%3A19%3A26Z&sp=r&sv=2024-05-04&sr=b&sig=yNQP0QtfvQCWLPzAJTTWND4g9vYjipuO5E7%2BoiJb3Bs%3D",
    k_nearest_neighbors=5,
    fields="imageVector",
    weight=100,
)

# Perform the search
results = search_client.search(
    search_text=None, vector_queries=[text_vector_query, image_vector_query, text_image_vector_query], top=3
)
# if results is not None:
#     print(results[0])

# Print the results
for result in results:
    print(f"Name: {result['description']}")
    print(f"Score: {result['@search.score']}")
    print(f"URL: {result['img']}")
    # display(HTML(f'<img src="{result["img"]}" style="width:200px;"/>'))
    print("-" * 50)