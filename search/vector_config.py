import os
from dotenv import load_dotenv

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

load_dotenv(".env")

AZURE_AI_VISION_API_KEY = os.getenv("AZURE_COMPUTER_VISION_KEY")
AZURE_AI_VISION_ENDPOINT = os.getenv("AZURE_COMPUTER_VISION_ENDPOINT")

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
        field_mappings=[FieldMapping(source_field_name="id", target_field_name="id"),
                        FieldMapping(source_field_name="price", target_field_name="price")],
        output_field_mappings=[
            FieldMapping(source_field_name="/document/descriptionVector", target_field_name="descriptionVector"),
            FieldMapping(source_field_name="/document/imageVector", target_field_name="imageVector"),
        ],
    )
    
    indexer_client.create_or_update_indexer(indexer)
    print(f"{indexer_name} created or updated.")
    
    indexer_client.run_indexer(indexer_name)
    print(f"{indexer_name} is running. If queries return no results, please wait a bit and try again.")
