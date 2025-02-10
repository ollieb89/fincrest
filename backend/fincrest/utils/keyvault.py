from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import logging

logger = logging.getLogger(__name__)

# Get Key Vault URL from environment
VAULT_URL = os.getenv("AZURE_VAULT_URL", "https://fcvauult.vault.azure.net/")

if not VAULT_URL:
    raise ValueError("❌ AZURE_VAULT_URL is missing. Add it in Azure environment variables.")

# Use Managed Identity if in Azure, fallback to DefaultAzureCredential locally
credential = ManagedIdentityCredential() if "WEBSITE_HOSTNAME" in os.environ else DefaultAzureCredential()

# Initialize Secret Client
client = SecretClient(vault_url=VAULT_URL, credential=credential)

def get_secret(secret_name):
    """Retrieve secret from Azure Key Vault."""
    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        logger.error(f"❌ Error retrieving secret {secret_name}: {e}")
        return None
