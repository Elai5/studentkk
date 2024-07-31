"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = get_asgi_application()


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from mysite import routing  # Replace 'your_app_name' with the actual name of your app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Get the default ASGI application
django_asgi_app = get_asgi_application()

# Define the ASGI application with routing
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Handle HTTP requests
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns  # Your WebSocket URL routing
            )
        )
    ),
})