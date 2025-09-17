
# Shop the Look

A Multi modal Generative AI powered solution that implements Shop the Look capabilities for Retail users

## Function Features
- Users can upload an image and search for matching apparal
- Users can upload an image, point to a particular item in the image using natural language and search for matching items. This involves the gpt-4o multi modal capabilities to describe the item being pointed to, create an enriched search prompt and use Azure AI Search to return matching items from the Catalog
- Showcase how catalog enrichment can be done on the fly, by using gpt-4o model to generate a compelling description of each item in the catalog search results, based on the image of the items


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

`AZURE_STORAGE_ACCOUNT_NAME` (Required for Azure Default Credentials storage access)

`BLOB_CONTAINER_NAME`

`AZURE_SEARCH_ADMIN_KEY`

`AZURE_SEARCH_SERVICE_ENDPOINT`

`BLOB_CONTAINER_NAME_IMG`

### Migration to Azure Default Credentials

The application now uses Azure Default Credentials for storage account authentication instead of connection strings. This enables:
- Support for Managed Identity in Azure Container Apps
- Enhanced security by eliminating connection string management
- Seamless integration with Azure RBAC

When deploying to Azure Container Apps with Managed Identity:
1. Assign the Managed Identity the "Storage Blob Data Contributor" role on the storage account
2. Set the `AZURE_STORAGE_ACCOUNT_NAME` environment variable
3. Remove any `BLOB_CONNECTION_STRING` environment variables (deprecated)

### Deployment Notes

For local development, ensure you're authenticated with Azure CLI:
```bash
az login
```

For Container Apps deployment with Managed Identity:
```bash
# Enable system-assigned managed identity
az containerapp identity assign --name your-app --resource-group your-rg

# Grant storage permissions
az role assignment create \
  --assignee <managed-identity-principal-id> \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/<subscription-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-account>
```




## Authors

- [@goy4l](https://www.github.com/goy4l)
- [@ashwinchandra08](https://www.github.com/ashwinchandra08)
- [@tanishqatp](https://www.github.com/tanishqatp)
- [@YohanTheNohan](https://www.github.com/YohanTheNohan)
- [@AutisticCoder-9000](https://github.com/AutisticCoder-9000)
