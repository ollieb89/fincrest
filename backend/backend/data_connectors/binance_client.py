import asyncio
import json
import logging
import os
import websockets
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Initialize Azure Key Vault client
vault_url = os.getenv('AZURE_VAULT_URL')
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=vault_url, credential=credential)

# Retrieve secrets from Azure Key Vault
BINANCE_WS_URL = secret_client.get_secret('BINANCE_WS_URL').value
BINANCE_WS_USER = secret_client.get_secret('BINANCE_WS_USER').value

logger = logging.getLogger(__name__)


class BinanceMarketWebStream:
    """Handles Binance market data websockets."""

    def __init__(self, streams: list):
        # Use endpoint from Azure Key Vault
        self.ws_url = BINANCE_WS_URL
        self.streams = streams  # e.g., ["btcusdt@ticker", "ethusdt@trade"]
        self.connection = None

    async def subscribe(self):
        """Subscribe to the specified Binance market streams if required."""
        if not self.ws_url.startswith("wss://stream.binance.com:9443/ws/"):
            payload = {
                "method": "SUBSCRIBE",
                "params": self.streams,
                "id": 1
            }
            await self.connection.send(json.dumps(payload))
            logger.info("Subscribed to market streams: %s", self.streams)

    async def connect(self):
        """Establish the websocket connection and listen for messages."""
        try:
            # If single stream is an avgPrice stream, connect directly to individual endpoint
            if len(self.streams) == 1 and '@avgPrice' in self.streams[0]:
                endpoint = f"{BINANCE_WS_USER}/ws/{self.streams[0]}"
                async with websockets.connect(endpoint) as ws:
                    self.connection = ws
                    logger.info("Connected directly to avgPrice stream at %s", endpoint)
                    async for message in ws:
                        data = json.loads(message)
                        await self.handle_message(data)
            else:
                async with websockets.connect(self.ws_url) as ws:
                    self.connection = ws
                    await self.subscribe()
                    async for message in ws:
                        data = json.loads(message)
                        await self.handle_message(data)
        except Exception as e:
            logger.error("Market websocket connection error: %s", str(e))

    async def handle_message(self, message: dict):
        """Handle incoming market stream messages."""
        logger.info("Market stream message received: %s", message)
        # Add your processing logic here


class BinanceUserWebStream:
    """Handles Binance user data websockets."""

    def __init__(self, listen_key: str):
        # For user data stream, use the endpoint from Azure Key Vault and append the listen key
        self.ws_url = f"{BINANCE_WS_USER}/ws/{listen_key}"
        self.connection = None
        self.listen_key = listen_key

    async def connect(self):
        """Connect to the Binance user data stream using a listen key."""
        try:
            async with websockets.connect(self.ws_url) as ws:
                self.connection = ws
                logger.info("Connected to user data stream with listen key %s", self.listen_key)
                async for message in ws:
                    data = json.loads(message)
                    self.handle_message(data)
        except Exception as e:
            logger.error("User stream connection error: %s", str(e))
            # Reconnection or listen key renewal logic can be added here

    def handle_message(self, message: dict):
        """Handle incoming user stream messages."""
        logger.info("User stream message received: %s", message)
        # Process account updates, order changes, etc.
