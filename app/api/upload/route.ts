import { NextRequest, NextResponse } from 'next/server';
import { BlobServiceClient } from '@azure/storage-blob';
import { DefaultAzureCredential } from '@azure/identity';
import { UploadResponse, StorageError } from '../../types/storage';

export async function POST(request: NextRequest): Promise<NextResponse<UploadResponse | StorageError>> {
  try {
    // Get the uploaded file from the form data
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json({ error: 'No file provided' }, { status: 400 });
    }

    // Get environment variables
    const storageAccountName = process.env.AZURE_STORAGE_ACCOUNT_NAME;
    const containerName = process.env.BLOB_CONTAINER_NAME || process.env.BLOB_CONTAINER_NAME_IMG;

    if (!storageAccountName || !containerName) {
      return NextResponse.json(
        { error: 'Missing required environment variables: AZURE_STORAGE_ACCOUNT_NAME, BLOB_CONTAINER_NAME' },
        { status: 500 }
      );
    }

    // Create BlobServiceClient using DefaultAzureCredential
    const credential = new DefaultAzureCredential();
    const blobServiceClient = new BlobServiceClient(
      `https://${storageAccountName}.blob.core.windows.net`,
      credential
    );

    // Get container client
    const containerClient = blobServiceClient.getContainerClient(containerName);

    // Generate unique blob name
    const timestamp = Date.now();
    const fileName = file.name.replace(/[^a-zA-Z0-9.-]/g, '_'); // Sanitize filename
    const blobName = `uploads/${timestamp}_${fileName}`;

    // Get block blob client
    const blockBlobClient = containerClient.getBlockBlobClient(blobName);

    // Convert file to buffer
    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    // Upload the file
    await blockBlobClient.upload(buffer, buffer.length, {
      blobHTTPHeaders: {
        blobContentType: file.type,
      },
    });

    // Return the blob URL
    const imageUrl = blockBlobClient.url;

    return NextResponse.json({ 
      message: 'File uploaded successfully',
      image_url: imageUrl 
    });

  } catch (error) {
    console.error('Error uploading file to Azure Blob Storage:', error);
    return NextResponse.json(
      { error: 'Failed to upload file' },
      { status: 500 }
    );
  }
}