# Testing Azure Default Credentials Implementation

## Local Testing

To test the Azure Default Credentials implementation locally:

1. **Install Azure CLI** and login:
   ```bash
   az login
   ```

2. **Set up environment variables** in `.env.local`:
   ```bash
   AZURE_STORAGE_ACCOUNT_NAME=your-storage-account-name
   BLOB_CONTAINER_NAME=your-container-name
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

4. **Test the upload endpoint**:
   ```bash
   curl -X POST http://localhost:3000/api/upload \
     -F "file=@path/to/your/image.jpg" \
     -H "Content-Type: multipart/form-data"
   ```

## Container Apps Deployment Testing

1. **Deploy with Managed Identity**:
   ```bash
   # Enable system-assigned managed identity
   az containerapp identity assign \
     --name your-app \
     --resource-group your-rg

   # Get the managed identity principal ID
   PRINCIPAL_ID=$(az containerapp identity show \
     --name your-app \
     --resource-group your-rg \
     --query principalId -o tsv)

   # Grant storage permissions
   az role assignment create \
     --assignee $PRINCIPAL_ID \
     --role "Storage Blob Data Contributor" \
     --scope "/subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{storage-account}"
   ```

2. **Set environment variables** in Container App:
   ```bash
   az containerapp env set \
     --name your-app \
     --resource-group your-rg \
     --set-env-vars AZURE_STORAGE_ACCOUNT_NAME=your-storage-account-name \
                    BLOB_CONTAINER_NAME=your-container-name
   ```

## Expected Behavior

- **Success Response**: `{"message": "File uploaded successfully", "image_url": "https://storage.blob.core.windows.net/..."}`
- **Error Response**: `{"error": "Missing required environment variables..."}`
- **Authentication**: Uses Azure Default Credentials chain (Managed Identity in Container Apps, Azure CLI locally)

## Troubleshooting

1. **"DefaultAzureCredential failed to retrieve a token"**: 
   - Ensure Managed Identity is enabled and has proper permissions
   - Locally, ensure `az login` is completed

2. **"Missing required environment variables"**:
   - Verify `AZURE_STORAGE_ACCOUNT_NAME` and `BLOB_CONTAINER_NAME` are set

3. **"Container not found"**:
   - Ensure the blob container exists in the storage account
   - Verify the container name matches the environment variable