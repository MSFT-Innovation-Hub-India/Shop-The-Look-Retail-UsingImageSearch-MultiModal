// Types for Azure Storage operations with Default Credentials

export interface UploadResponse {
  message: string;
  image_url: string;
}

export interface StorageError {
  error: string;
}

export interface StorageConfig {
  storageAccountName: string;
  containerName: string;
}