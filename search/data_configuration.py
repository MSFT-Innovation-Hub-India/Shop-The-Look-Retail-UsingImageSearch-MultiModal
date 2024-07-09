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