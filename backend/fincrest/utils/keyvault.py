import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

VAULT_URL = os.getenv("AZURE_VAULT_URL", "https://fcvauult.vault.azure.net/")

credential = DefaultAzureCredential(
    exclude_interactive_browser_credential=True  # ✅ Ensures no interactive login
)
client = SecretClient(vault_url=VAULT_URL, credential=credential)

def get_secret(secret_name):
    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        print(f"❌ Error retrieving secret {secret_name}: {e}")
        return None
