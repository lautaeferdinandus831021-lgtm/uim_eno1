"""
DEV ONLY: Auto-login middleware
Creates a default user and auto-authenticates all requests.
REMOVE IN PRODUCTION!
"""
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.security import create_access_token


class DevAutoLoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip non-API routes
        path = request.url.path
        if path in ("/health", "/metrics", "/docs", "/redoc", "/openapi.json"):
            return await call_next(request)

        # If no auth header, inject dev token
        if "authorization" not in request.headers:
            token = create_access_token(1, "dev@bgbot.local")
            request.scope["headers"].append(
                (b"authorization", f"Bearer {token}".encode())
            )

        return await call_next(request)
