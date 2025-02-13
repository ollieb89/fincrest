import os
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

logger = logging.getLogger(__name__)

class AzureVaultClient:
    """Client to fetch secrets from Azure Key Vault securely."""
    
    def __init__(self):
        self.vault_url = os.getenv("AZURE_VAULT_URL")
        if not self.vault_url:
            raise ValueError("AZURE_VAULT_URL is not set. Please set it in your Azure App Service settings to point to your new Key Vault.")
        # Authenticate using DefaultAzureCredential (this will utilize Managed Identity when available)
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)
    
    def get_secret(self, secret_name: str) -> str:
        """Fetch a secret from Azure Key Vault.
        
        Args:
            secret_name (str): The name of the secret to retrieve.
        
        Returns:
            str: The secret value, or None if retrieval fails.
        """
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            logger.error("Error fetching %s: %s", secret_name, e)
            return None
