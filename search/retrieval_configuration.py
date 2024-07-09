from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def authenticate_azure_search(api_key, use_aad_for_search=False):
    if use_aad_for_search:
        print("Using AAD for authentication.")
        credential = DefaultAzureCredential()
    else:
        print("Using API keys for authentication.")
        if api_key is None:
            raise ValueError("API key must be provided if not using AAD for authentication.")
        credential = AzureKeyCredential(api_key)
    return credential

