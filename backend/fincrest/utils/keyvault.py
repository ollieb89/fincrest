import os
import logging

from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

logger = logging.getLogger(__name__)

# Load the Key Vault URL from environment variables.
# Ensure that AZURE_VAULT_URL is set in your Azure App Settings to point to your new Key Vault.
VAULT_URL = os.getenv("AZURE_VAULT_URL")
if not VAULT_URL:
    raise ValueError("❌ AZURE_VAULT_URL is missing. Please add it to your Azure App Settings.")

# Attempt to use ManagedIdentityCredential first.
# In local development or if the managed identity isn't available, fallback to DefaultAzureCredential.
try:
    credential = ManagedIdentityCredential()
    # Test if the credential can get a token from the vault scope.
    credential.get_token("https://vault.azure.net/.default")
except Exception as e:
    logger.warning("ManagedIdentityCredential unavailable, falling back to DefaultAzureCredential. Error: %s", e)
    credential = DefaultAzureCredential()

client = SecretClient(vault_url=VAULT_URL, credential=credential)

def get_secret(secret_name: str) -> str:
    """
    Retrieve a secret value from Azure Key Vault.

    Args:
        secret_name (str): The name of the secret to retrieve.

    Returns:
        str: The secret value, or None if retrieval fails.
    """
    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        logger.error("❌ Error retrieving secret %s: %s", secret_name, e)
        return None
