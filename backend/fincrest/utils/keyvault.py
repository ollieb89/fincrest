import os
import logging
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the Key Vault URL from your environment variables.
VAULT_URL = os.getenv("AZURE_VAULT_URL")
if not VAULT_URL:
    raise ValueError("AZURE_VAULT_URL is not set. Please set it to your Key Vault URL (e.g., https://<your-key-vault-name>.vault.azure.net/).")

# Attempt to authenticate using ManagedIdentityCredential first.
try:
    credential = ManagedIdentityCredential()
    # Test the credential by requesting a token for the Key Vault default scope.
    credential.get_token("https://vault.azure.net/.default")
    logger.info("Connecting using ManagedIdentityCredential.")
except Exception as e:
    logger.warning("ManagedIdentityCredential unavailable, falling back to DefaultAzureCredential. Error: %s", e)
    credential = DefaultAzureCredential()

# Create the SecretClient to interact with the Key Vault.
client = SecretClient(vault_url=VAULT_URL, credential=credential)

def get_secret(secret_name: str) -> str:
    """
    Retrieve a secret value from Azure Key Vault.

    Args:
        secret_name (str): The name of the secret to retrieve.

    Returns:
        str: The secret value if successful; otherwise, None.
    """
    try:
        secret = client.get_secret(secret_name)
        logger.info("Secret '%s' retrieved successfully.", secret_name)
        return secret.value
    except Exception as ex:
        logger.error("Error retrieving secret '%s': %s", secret_name, ex)
        return None

if __name__ == "__main__":
    # Example usage: retrieve and print the secret named "DB-PASSWORD"
    secret_name = "DB-PASSWORD"  # Adjust this to match your secret's name in Key Vault.
    secret_value = get_secret(secret_name)
    if secret_value:
        logger.info("Retrieved secret value: %s", secret_value)
    else:
        logger.error("Failed to retrieve the secret.")
