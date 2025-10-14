
# Shop the Look

A Generative AI powered solution that implements Shop the Look capabilities for Retail users


## Features

- Light/dark mode toggle
- Live previews
- Fullscreen mode
- Cross platform


## Tech Stack

**Client:** Streamlit

**Server:** Flask

**Azure Services:** Azure AI Search, Azure OpenAI, Azure AI Vision

**Deployment:** Azure App Service


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`AZURE_OPENAI_ENDPOINT`

`AZURE_OPENAI_API_KEY`

`AZURE_OAI_DEPLOYMENT`

`AZURE_COMPUTER_VISION_ENDPOINT`

`AZURE_COMPUTER_VISION_KEY`

`BLOB_STORAGE_ACCOUNT_NAME` - The name of your Azure Storage Account (e.g., "mystorageaccount")

`BLOB_CONTAINER_NAME` - The blob container name for indexer data source

`BLOB_CONTAINER_NAME_IMG` - The blob container name for uploaded images

`AZURE_SEARCH_ADMIN_KEY`

`AZURE_SEARCH_SERVICE_ENDPOINT`


### Managed Identity Configuration

This application uses **Azure Managed Identity** for authentication with Azure Blob Storage instead of connection strings. Ensure that:

1. The application's managed identity (system-assigned or user-assigned) has the following RBAC roles assigned on the storage account:
   - **Storage Blob Data Contributor** - For reading and writing blobs
   - **Storage Blob Delegator** - For generating user delegation SAS tokens

2. For Azure AI Search indexer to access blob storage, the search service's managed identity must also have:
   - **Storage Blob Data Reader** - For reading blobs during indexing
   
3. Update the ResourceId in `data_configuration.py` with your actual subscription ID and resource group name




## Authors

- [@goy4l](https://www.github.com/goy4l)
- [@ashwinchandra08](https://www.github.com/ashwinchandra08)
- [@tanishqatp](https://www.github.com/tanishqatp)
- [@YohanTheNohan](https://www.github.com/YohanTheNohan)
- [@AutisticCoder-9000](https://github.com/AutisticCoder-9000)