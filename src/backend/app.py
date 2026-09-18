"""FASTAPI Framework and Main App Endpoints for B&S Autos Web Application.

This module defines the main FastAPI application, including the setup of static file serving,
template rendering, and the primary endpoints for the B&S Autos web application.

The application serves the homepage."""

import logging
import mimetypes
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.templating import Jinja2Templates

from src.backend import config, schemas
from src.backend.classes import SecurityHeadersMiddleware, db
from src.backend.routers import handle_book_inputs, handle_enquiry_inputs

# Globals and Configurations
# TODO: Use Pydantic settings instead to being ENV variables in
load_dotenv()  # Load environment variables from .env file

logger = logging.getLogger(__name__)

# ---- FastAPI Config --------------------------------------------------


# FastAPI LifeSpan
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan function to manage startup and shutdown events for the FastAPI application."""
    await db.connect()

    logger.info("Database connection pool created")

    # If any database schema setup is needed, it can be done here
    await db.ensure_schema(schemas.CREATE_BOOK_TABLE_SQL)
    await db.ensure_schema(schemas.CREATE_ENQUIRY_TABLE_SQL)

    logger.info(
        "Database schema ensured (book_submissions, enquiry_submissions tables)"
    )

    yield
    await db.close()

    logger.info("Database connection pool closed")


# Initialize FastAPI application
app = FastAPI(
    title="B&S Autos",
    description="A web application for B&S Autos to manage customer interactions and services.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    # debug=False;
)

# Attach the rate limiter to the FastAPI app
app.state.limiter = config.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ---- Middleware & Security Config --------------------------------------------------

# Middleware Setup - Security and CORS
app.add_middleware(
    CORSMiddleware,  # CORS — only allow your own domain
    # allow_origins=ALLOWED_ORIGINS,  # whitelist of trusted frontends
    allow_methods=["POST"],  # only POST requests are allowed cross-origin
    allow_headers=["Content-Type"],  # only this header is permitted
)

app.add_middleware(SecurityHeadersMiddleware)


# ---- Endpoints, Routers and Static Files --------------------------------------------------

app.include_router(handle_book_inputs.router)
app.include_router(handle_enquiry_inputs.router)

# TODO: See todo.md for notes on updating the CSS paths as they require SCSS compile
# Mount static files so FASTAPI can serve them to the browser
# ---------------
# .mjs isn't in every system's mimetypes registry (observed serving as text/plain on
# Windows) — StaticFiles guesses Content-Type from this registry, and combined with
# SecurityHeadersMiddleware's X-Content-Type-Options: nosniff, a wrong type makes the
# browser silently refuse to execute it as a module. Register it explicitly so the
# vendored DOMPurify build (static/js/vendor/dompurify/purify.es.mjs) always serves
# with a real JS MIME type regardless of the host OS's registry.
mimetypes.add_type("text/javascript", ".mjs")

# Static assets (HTML, CSS, jQuery) and compiled TypeScript output are mounted separately
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
app.mount("/dist", StaticFiles(directory="src/frontend/dist"), name="dist")

# Templates for rendering HTML templates, no serving as raw file like `.JS` or `.CSS`
templates = Jinja2Templates(directory="src/frontend/templates/")


# Endpoint for the index page
# ---------------
# Page navigation handled by HTML
@app.get("/", response_class=HTMLResponse)
def read_homepage(request: Request) -> HTMLResponse:
    """Renders the homepage template."""

    logger.info("Homepage accessed")

    # This route serves every "/" visit, not just the no-JS fallback — the
    # query flag is only present when a no-JS form redirected here after POSTing.
    # See docs/development_journal.md -> "Redirect-after-POST".
    book_submitted = request.query_params.get("book_submitted")
    enquiry_submitted = request.query_params.get("enquiry_submitted")

    # TODO: Implement Jinja for this
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "book_submitted": book_submitted,
            "enquiry_submitted": enquiry_submitted,
        },
    )
