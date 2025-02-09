import logging
import os
from binance.client import Client
from binance.streams import BinanceSocketManager
from binance.exceptions import BinanceAPIException
from backend.apps.config.azure_vault import AzureVaultClient  # Fetch credentials from Azure

logger = logging.getLogger(__name__)

# ✅ Fetch API Keys from Azure Vault
vault_client = AzureVaultClient()
BINANCE_API_KEY = vault_client.get_secret("BINANCE_API_KEY")
BINANCE_API_SECRET = vault_client.get_secret("BINANCE_API_SECRET")

# ✅ Initialize Binance Client
try:
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    logger.info("Binance Client successfully initialized.")
except BinanceAPIException as e:
    logger.error(f"Error initializing Binance Client: {e}")
    client = None


class BinanceMarketData:
    """Handles market data streaming using Binance WebSockets."""

    def __init__(self, pairs=["btcusdt", "ethusdt"]):
        """Initialize WebSocket Manager for Binance market streams."""
        self.client = client
        self.pairs = pairs
        self.bsm = BinanceSocketManager(client)
        self.sockets = {}

    def start_stream(self):
        """Start WebSocket streams for each trading pair."""
        if not self.client:
            logger.error("Binance Client is not initialized. Check API keys.")
            return
        
        for pair in self.pairs:
            stream = self.bsm.trade_socket(pair)
            self.sockets[pair] = stream
            logger.info(f"Starting WebSocket for: {pair}")

        self.bsm.start()

    def stop_stream(self):
        """Stop all active WebSocket streams."""
        self.bsm.stop_socket()
        logger.info("All Binance WebSockets stopped.")


class BinanceUserStream:
    """Handles Binance User Data WebSocket Stream."""
    
    def __init__(self):
        """Initialize WebSocket for user account updates."""
        self.client = client
        self.bsm = BinanceSocketManager(client)
        self.user_socket = None

    def start_stream(self):
        """Start user WebSocket stream."""
        if not self.client:
            logger.error("Binance Client is not initialized. Check API keys.")
            return

        self.user_socket = self.bsm.user_socket()
        self.bsm.start()
        logger.info("User WebSocket Stream started.")

    def stop_stream(self):
        """Stop the user WebSocket stream."""
        if self.user_socket:
            self.bsm.stop_socket(self.user_socket)
            logger.info("User WebSocket Stream stopped.")
