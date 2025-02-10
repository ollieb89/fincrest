"""
ASGI config for fincrest project.

It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter  # For WebSockets

# Ensure correct settings are used in production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fincrest.settings.production')

# Define ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Default HTTP requests
    # "websocket": AuthMiddlewareStack(URLRouter(websocket_routes)),  # Uncomment if using WebSockets
})
