import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Set Key Vault URL from environment variables or hardcoded (if needed)
KEY_VAULT_URL = os.getenv("AZURE_VAULT_URL", "https://fcvauult.vault.azure.net/")

# Authenticate with Managed Identity
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

def get_secret(secret_name):
    """Fetch secret from Azure Key Vault"""
    try:
        retrieved_secret = client.get_secret(secret_name)
        return retrieved_secret.value
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return None
