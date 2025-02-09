import os

# Retrieve environment variables
BINANCE_WS_URL = os.getenv('BINANCE_WS_URL')
BINANCE_WS_USER = os.getenv('BINANCE_WS_USER')
AZURE_VAULT_URL = os.getenv('AZURE_VAULT_URL')

# Log the locations of these variables
print(f"BINANCE_WS_URL is set to: {BINANCE_WS_URL}")
print(f"BINANCE_WS_USER is set to: {BINANCE_WS_USER}")
print(f"AZURE_VAULT_URL is set to: {AZURE_VAULT_URL}")