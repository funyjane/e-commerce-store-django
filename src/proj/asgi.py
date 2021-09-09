"""
ASGI config for proj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""


from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from main.routing import websockets

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(websockets),
    }
)
