from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

class AzureVaultClient:
    """Client to fetch secrets from Azure Key Vault securely."""

    def __init__(self):
        self.vault_url = os.getenv("AZURE_VAULT_URL")
        if not self.vault_url:
            raise ValueError("AZURE_VAULT_URL is not set. Check your Azure App Service settings.")

        # Authenticate using Managed Identity or Service Principal
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)

    def get_secret(self, secret_name: str):
        """Fetch a secret from Azure Key Vault."""
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            print(f"Error fetching {secret_name}: {str(e)}")
            return None
