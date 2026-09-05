# classes.py
"""Shared classes for the B&S Autos web application: the security-headers
middleware and the Postgres connection-pool wrapper used across the app."""

from typing import Optional

import asyncpg
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.backend import config


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses.

    This middleware enhances security by adding headers that prevent MIME type sniffing,
    clickjacking, and cross-site scripting (XSS) attacks.

    Headers added:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: DENY
    - X-XSS-Protection: 1; mode=block
    """

    # Add security headers to all responses to enhance security against common web vulnerabilities
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response


class Database:
    """Thin wrapper around an asyncpg connection pool.

    Replaces the old module-level `db_pool = None` + `global db_pool` pattern in
    app.py: the pool itself is created/closed by `connect()`/`close()` (called from
    the FastAPI lifespan), while other modules (e.g. routers/handle_form_inputs.py)
    import the `db` singleton below and read `db.pool` directly — no `global`
    statement needed anywhere, since only the attribute is mutated, not the object.
    """

    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        """Create the connection pool. Called once at app startup."""
        self.pool = await asyncpg.create_pool(self.dsn, min_size=1, max_size=10)

    async def close(self) -> None:
        """Close the connection pool. Called once at app shutdown."""
        await self.pool.close()

    async def ensure_schema(self, ddl: str) -> None:
        """Run schema-setup DDL (e.g. CREATE TABLE IF NOT EXISTS) against the pool."""
        async with self.pool.acquire() as conn:
            await conn.execute(ddl)


# Module-level singleton — constructed at import time, but `db.pool` stays None
# until `Database.connect()` is awaited from the FastAPI lifespan.
db = Database(config.DATABASE_URL)
