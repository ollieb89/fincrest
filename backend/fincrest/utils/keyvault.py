import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Load Key Vault details
VAULT_URL = os.getenv("AZURE_VAULT_URL", "https://fcvauult.vault.azure.net/")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID")

if not CLIENT_ID or not CLIENT_SECRET or not TENANT_ID:
    raise ValueError("❌ Azure credentials are missing. Set AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_TENANT_ID.")

# Authenticate with Key Vault
credential = ClientSecretCredential(tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
client = SecretClient(vault_url=VAULT_URL, credential=credential)

def get_secret(secret_name):
    """Retrieve secret from Azure Key Vault."""
    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        logger.error(f"❌ Error retrieving secret {secret_name}: {e}")
        return None
