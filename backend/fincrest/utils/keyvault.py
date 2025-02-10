from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Initialize Key Vault client
VAULT_URL = "https://fcvauult.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)

def get_secret(secret_name):
    """Retrieve secret from Azure Key Vault."""
    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return None
