import os
import logging
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

# Configure logging
logger = logging.getLogger(__name__)

# Load Key Vault URL from environment
VAULT_URL = os.getenv("AZURE_VAULT_URL")

if not VAULT_URL:
    raise ValueError("❌ AZURE_VAULT_URL is missing. Add it in Azure App Settings.")

# 🔴 FIXED: Use Managed Identity
credential = ManagedIdentityCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)

def get_secret(secret_name):
    """Retrieve secret from Azure Key Vault."""
    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        logger.error(f"❌ Error retrieving secret {secret_name}: {e}")
        return None
