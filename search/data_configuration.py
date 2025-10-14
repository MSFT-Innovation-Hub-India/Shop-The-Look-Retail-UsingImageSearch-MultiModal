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
import os

def create_or_update_data_source(indexer_client, container_name, storage_account_name, index_name):
    """
    Create or update a data source connection for Azure AI Search using Managed Identity.
    Requires AZURE_SUBSCRIPTION_ID and AZURE_RESOURCE_GROUP environment variables to be set.
    """
    container = SearchIndexerDataContainer(name=container_name)
    
    # Get subscription ID and resource group from environment variables
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    
    if not subscription_id or not resource_group:
        raise ValueError(
            "AZURE_SUBSCRIPTION_ID and AZURE_RESOURCE_GROUP environment variables must be set "
            "for managed identity authentication with blob storage."
        )
    
    # Use managed identity for blob storage connection
    # ResourceId format enables managed identity authentication
    connection_string = (
        f"ResourceId=/subscriptions/{subscription_id}"
        f"/resourceGroups/{resource_group}"
        f"/providers/Microsoft.Storage/storageAccounts/{storage_account_name};"
    )
    
    data_source_connection = SearchIndexerDataSourceConnection(
        name=f"{index_name}-blob",
        type="azureblob",
        connection_string=connection_string,
        container=container
    )
    try:
        indexer_client.create_or_update_data_source_connection(data_source_connection)
        print(f"Data source '{index_name}-blob' created or updated successfully with managed identity.")
        print(f"Using storage account: {storage_account_name}")
        print(f"Resource: /subscriptions/{subscription_id}/resourceGroups/{resource_group}")
    except Exception as e:
        raise Exception(f"Failed to create or update data source due to error: {e}")
    
def create_fields():
    """Creates the fields for the search index based on the specified schema."""
    return [
        SimpleField(
            name="id", type=SearchFieldDataType.String, key=True, filterable=True
        )
        ,SearchField(name="description", type=SearchFieldDataType.String, searchable=True),
        SearchField(name="img", type=SearchFieldDataType.String, searchable=True),
        SearchField(
            name="descriptionVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=1024,
            vector_search_profile_name="myHnswProfile",
            stored=False,
        ),
        SimpleField(
            name="price", type=SearchFieldDataType.Double, filterable=True
        ),
        SearchField(
            name="imageVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=1024,
            vector_search_profile_name="myHnswProfile",
            stored=False,
        ),
    ]