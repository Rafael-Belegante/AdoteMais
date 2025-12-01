from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)

        # Proteções básicas
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("X-XSS-Protection", "1; mode=block")

        # Privacidade
        response.headers.setdefault("Referrer-Policy", "no-referrer")

        # Restringe APIs sensíveis do navegador por padrão
        response.headers.setdefault(
            "Permissions-Policy",
            "geolocation=(), microphone=(), camera=()"
        )

        # HSTS (só é efetivo em HTTPS; em HTTP é ignorado)
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=63072000; includeSubDomains; preload"
        )

        return response
