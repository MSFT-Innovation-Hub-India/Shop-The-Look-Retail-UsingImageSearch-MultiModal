# Migration Guide: Connection String to Managed Identity

This guide explains how to migrate from connection string-based authentication to Azure Managed Identity for blob storage access.

## Overview

The application has been updated to use **Azure Managed Identity** instead of connection strings for authenticating with Azure Blob Storage. This provides better security by eliminating the need to store sensitive credentials.

## What Changed

### Environment Variables

**Removed:**
- `BLOB_CONNECTION_STRING` - No longer needed

**Added:**
- `BLOB_STORAGE_ACCOUNT_NAME` - The name of your storage account (e.g., "mystorageaccount")
- `AZURE_SUBSCRIPTION_ID` - Your Azure subscription ID
- `AZURE_RESOURCE_GROUP` - The resource group containing your storage account

### Code Changes

1. **search/search.py**
   - Replaced `BlobServiceClient.from_connection_string()` with managed identity authentication
   - Updated SAS token generation to use user delegation keys instead of account keys
   - Now uses `DefaultAzureCredential` for authentication

2. **search/data_configuration.py**
   - Updated data source connection to use ResourceId-based connection string
   - Added validation for required environment variables

## Setup Instructions

### Step 1: Enable Managed Identity

#### For Azure App Service:
1. Go to your App Service in Azure Portal
2. Navigate to **Identity** > **System assigned**
3. Set Status to **On**
4. Click **Save**
5. Note down the **Object (principal) ID** for the next step

#### For Azure Functions or other services:
Follow the same process in the Identity section of your service.

### Step 2: Assign RBAC Roles

#### On Storage Account:
The application's managed identity needs the following roles:

1. **Storage Blob Data Contributor**
   ```bash
   az role assignment create \
     --assignee <managed-identity-object-id> \
     --role "Storage Blob Data Contributor" \
     --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>
   ```

2. **Storage Blob Delegator**
   ```bash
   az role assignment create \
     --assignee <managed-identity-object-id> \
     --role "Storage Blob Delegator" \
     --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>
   ```

#### For Azure AI Search Indexer:
The search service's managed identity needs:

1. Enable managed identity on your Azure AI Search service
2. Assign **Storage Blob Data Reader** role:
   ```bash
   az role assignment create \
     --assignee <search-service-managed-identity-object-id> \
     --role "Storage Blob Data Reader" \
     --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>
   ```

### Step 3: Update Environment Variables

Update your `.env` file or application configuration:

```bash
# Remove this line:
# BLOB_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...

# Add these lines:
BLOB_STORAGE_ACCOUNT_NAME=yourstorageaccount
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=your-resource-group
```

Keep these existing variables:
```bash
BLOB_CONTAINER_NAME=your-container-name
BLOB_CONTAINER_NAME_IMG=your-images-container-name
```

### Step 4: Deploy and Test

1. Deploy your application with the updated code
2. Test the image upload functionality
3. Verify that the Azure AI Search indexer can access the blob storage

## Local Development

For local development and testing:

1. Install Azure CLI if not already installed
2. Login to Azure:
   ```bash
   az login
   ```
3. Ensure your Azure account has the same RBAC roles assigned
4. Set the environment variables in your local `.env` file
5. Run the application

The `DefaultAzureCredential` will automatically use your Azure CLI credentials for local development.

## Troubleshooting

### Issue: "AuthorizationPermissionMismatch" error
**Solution:** Ensure the managed identity has the required RBAC roles assigned. It may take a few minutes for role assignments to propagate.

### Issue: "AZURE_SUBSCRIPTION_ID must be set" error
**Solution:** Add the `AZURE_SUBSCRIPTION_ID` and `AZURE_RESOURCE_GROUP` environment variables to your configuration.

### Issue: Local development fails with authentication error
**Solution:** 
- Run `az login` to authenticate with Azure CLI
- Ensure your Azure account has the necessary RBAC roles
- Check that you're logged in to the correct Azure subscription: `az account show`

### Issue: Image upload works but indexer fails
**Solution:** Ensure the Azure AI Search service's managed identity has the "Storage Blob Data Reader" role on the storage account.

## Benefits of Managed Identity

1. **Improved Security**: No credentials stored in code or configuration
2. **Automatic Credential Rotation**: Azure manages credential lifecycle
3. **Simplified Operations**: No need to manage and rotate connection strings
4. **Audit Trail**: Better tracking of access through Azure Activity Log
5. **Principle of Least Privilege**: Fine-grained access control through RBAC

## Rollback Instructions

If you need to rollback to connection string authentication:

1. Revert the code changes in `search/search.py` and `search/data_configuration.py`
2. Add back the `BLOB_CONNECTION_STRING` environment variable
3. Remove the new environment variables (`BLOB_STORAGE_ACCOUNT_NAME`, `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`)
4. Deploy the previous version

## Additional Resources

- [Azure Managed Identity Documentation](https://docs.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview)
- [Azure Storage RBAC Roles](https://docs.microsoft.com/azure/storage/common/storage-auth-aad-rbac-portal)
- [DefaultAzureCredential](https://docs.microsoft.com/python/api/azure-identity/azure.identity.defaultazurecredential)
