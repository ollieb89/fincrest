import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

# Load credentials from environment
VAULT_URL = os.getenv("AZURE_VAULT_URL", "https://fcvauult.vault.azure.net/")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID")

# Authenticate using Service Principal
credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
client = SecretClient(vault_url=VAULT_URL, credential=credential)

def get_secret(secret_name):
    """Retrieve secret from Azure Key Vault."""
    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        print(f"❌ Error retrieving secret {secret_name}: {e}")
        return None
