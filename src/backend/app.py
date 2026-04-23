"""FASTAPI Framework and Main App Endpoints for B&S Auto Web Application.

This module defines the main FastAPI application, including the setup of static file serving,
template rendering, and the primary endpoints for the B&S Auto web application.

The application serves the homepage."""

import os
from dotenv import load_dotenv
from enum import Enum
import re
import html

from typing import AsyncGenerator
import logging
from pydantic import BaseModel
import base64
from contextlib import asynccontextmanager
from pydantic import BaseModel, EmailStr, field_validator, model_validator

from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from starlette.middleware.base import BaseHTTPMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import asyncpg

from src.backend.routers import handle_form_inputs

# Globals and Configurations
load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(
    ","
)  # Comma-separated list of allowed origins for CORS

db_pool = None

# ---- Logger Config --------------------------------------------------

# TODO: Move this to config.py and bring in
# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- FastAPI Config --------------------------------------------------


# FastAPI LifeSpan
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan function to manage startup and shutdown events for the FastAPI application."""
    global db_pool

    # Use A client for PostgreSQL - asyncpg - TODO: Move file and bring in connection to Database from else where
    do_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)

    logger.info("Database connection pool created")

    yield
    await do_pool.close()

    logger.info("Database connection pool closed")


# Rate Limiter for API endpoints - Security and traffic management
# ---------------
# Controls the number of requests to an API or server within a specific timeframe
limiter = Limiter(key_func=get_remote_address, default_limits=["5/hour"])

# Initialize FastAPI application
app = FastAPI(
    title="B&S Auto",
    description="A web application for B&S Auto to manage customer interactions and services.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    # debug=False;
)

# Attach the rate limiter to the FastAPI app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ---- Middleware & Security Config --------------------------------------------------

# Middleware Setup - Security and CORS
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    CORSMiddleware,  # CORS — only allow your own domain
    allow_origins=ALLOWED_ORIGINS,  # whitelist of trusted frontends
    allow_methods=["POST"],  # only POST requests are allowed cross-origin
    allow_headers=["Content-Type"],  # only this header is permitted
)


# Custom middleware to add security headers to all responses
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


app.add_middleware(SecurityHeadersMiddleware)


# ---- Endpoints, Routers and Static Files --------------------------------------------------

# Routers
app.include_router(handle_form_inputs.router)

# TODO: See todo.md for notes on updating the CSS paths as they require SCSS compile
# Mount static files so FASTAPI can serve them to the browser
# ---------------
# Static assets (HTML, CSS, jQuery) and compiled TypeScript output are mounted separately
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
app.mount("/dist", StaticFiles(directory="src/frontend/dist"), name="dist")

# Templates for rendering HTML templates, no serving as raw file like `.JS` or `.CSS`
templates = Jinja2Templates(directory="src/frontend/templates/")


# HTML Calls these Endpoints - Page navigation handled by HTML
# ---------------
# Endpoint for the index page
@app.get("/", response_class=HTMLResponse)
def read_homepage(request: Request) -> HTMLResponse:
    """Renders the homepage template."""

    logging.info("Homepage accessed")

    # TODO: Implement Jinja for this
    return templates.TemplateResponse("index.html", {"request": request})


# ---- Enums and Data Models --------------------------------------------------

class Service(str, Enum):
    # TODO: Change to actual B&S Services
    service    = "Website Development"
    graphic   = "Graphic Designing"
    marketing = "Digital Marketing"
    app_dev   = "App Development"


# ---- Sanitisation  --------------------------------------------------

# Patterns that suggest injection attempts
INJECTION_PATTERNS = [
    r"<[^>]*>",                          # HTML/XML tags
    r"javascript\s*:",                   # JS protocol
    r"on\w+\s*=",                        # HTML event handlers (onclick= etc)
    r"(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE)\s", # SQL keywords
    r"(\$\{|\{\{)",                      # Template injection
    r"(\.\.\/|\.\.\\)",                  # Path traversal
    r"(eval|exec|system|passthru)\s*\(", # Command injection
]

def contains_injection(value: str) -> bool:
    """Return True if the value contains any known injection pattern.
    
    Parameters
    ----------
    value: str
        Patterns defined in the INJECTION_PATTERNS
        
    Returns
    -------
    bool : True or False
        If True the pattern does contain injection pattern
        If False the pattern does not contain injection patterns
    """
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, value , re.IGNORECASE):
            return True
    return False

def sanitise(value: str) -> str:
    """Function to sanitise data if any characters that are not convential to simple
    form input.
    
    - Strip leading/trailing whitespace
    - Remove control characters
    - Escape HTML entities
    - Strip any remaining HTML tags

    Parameters
    ----------
    value : str
    
    Returns
    -------

    """
    value = value.strip()
    value = re.sub(r"[\x00-\x1F\x7F]", "", value)  # remove control characters
    value = html.escape(value)                       # encode & < > " '
    value = re.sub(r"<[^>]*>", "", value)           # strip remaining tags
    return value


# ---- Pydantic Schema --------------------------------------------------

# TODO: Find out why these functions are within a pydantic schema

class QuoteSubmission(BaseModel):
    username : str
    email : EmailStr
    phone : str
    registration : str
    service : Service
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = sanitise(v)
        if contains_injection(v):
            raise ValueError("Invalid characters in name.")
        if not re.match(r"^[a-zA-Z\s'\-]{2,64}$", v):
            raise ValueError("Name must be 2–64 characters, letters only.")
        return v    



###################################
###################################
###################################
###################################
###################################

# Test endpoint for quote submission - to be replaced with actual quote handling logic


# class QuoteSubmission(BaseModel):
#     username: str
#     email: str
#     phone: str
#     registration: str
#     service: str


# @app.post("/api/quote")
# async def submit_quote(payload: QuoteSubmission):
#     logger.info(f"Quote submitted: {payload}")
#     return {"message": "Received", "data": payload}


# fake_db = []


# @app.post("/api/quote")
# def submit(data: dict):
#     fake_db.append(data)
#     return {"status": "ok"}


# @app.get("/debug/db")
# def get_db():
#     return fake_db


# http://127.0.0.1:8000/debug/db
