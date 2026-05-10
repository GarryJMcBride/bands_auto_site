"""FASTAPI Framework and Main App Endpoints for B&S Autos Web Application.

This module defines the main FastAPI application, including the setup of static file serving,
template rendering, and the primary endpoints for the B&S Autos web application.

The application serves the homepage."""

import os
from dotenv import load_dotenv
from enum import Enum
import re
import html
from datetime import datetime, timezone

from typing import AsyncGenerator
import logging
from pydantic import BaseModel
import base64
from contextlib import asynccontextmanager
from pydantic import BaseModel, EmailStr, field_validator, model_validator
import uuid

from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.base import BaseHTTPMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import asyncpg

from src.backend.routers import handle_form_inputs

# Google Python Client and API
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText


# Globals and Configurations
load_dotenv()  # Load environment variables from .env file

# DATABASE_URL = os.getenv("DATABASE_URL")
# BUSINESS_EMAIL = os.getenv("BUSINESS_EMAIL")
# DELEGATED_EMAIL = os.getenv("DELEGATED_EMAIL")
# SERVICE_ACCOUNT = os.getenv("DATASERVICE_ACCOUNT")
# TODO: Configure ALLOWED_ORIGINS
# ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(
#     ","
# )  # Comma-separated list of allowed origins for CORS
# GMAIL_SCOPES = os.getenv("GMAIL_SCOPES")
DEBUG = os.getenv("ENVIRONMENT") == "development"


db_pool = None

# ---- Logger Config --------------------------------------------------

# TODO: Move this to config.py and bring in
# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- FastAPI Config --------------------------------------------------


# FastAPI LifeSpan
# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
#     """Lifespan function to manage startup and shutdown events for the FastAPI application."""
#     global db_pool

#     # Use A client for PostgreSQL - asyncpg - TODO: Move file and bring in connection to Database from else where
#     do_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)

#     logger.info("Database connection pool created")

#     yield
#     await do_pool.close()

#     logger.info("Database connection pool closed")


# Rate Limiter for API endpoints - Security and traffic management
# ---------------
# Controls the number of requests to an API or server within a specific timeframe
limiter = Limiter(key_func=get_remote_address, default_limits=["5/hour"])

# Initialize FastAPI application
app = FastAPI(
    title="B&S Autos",
    description="A web application for B&S Autos to manage customer interactions and services.",
    version="1.0.0",
    # lifespan=lifespan, TODO: Uncomment lifespan once DB Set up
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
app.add_middleware(
    CORSMiddleware,  # CORS — only allow your own domain
    # allow_origins=ALLOWED_ORIGINS,  # whitelist of trusted frontends
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

# Routers TODO: Uncomment when moving components to other files
# app.include_router(handle_form_inputs.router)

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
    return templates.TemplateResponse(request=request, name="index.html")


# ---- Enums and Data Models --------------------------------------------------


class Service(str, Enum):
    diagnostics = "Diagnostics"
    tyres = "Tyres"
    servicing = "Servicing"
    batteries = "Batteries"
    exhausts = "Exhausts"
    repairs = "Repairs"


# ---- Sanitisation  --------------------------------------------------

# Patterns that suggest injection attempts
INJECTION_PATTERNS = [
    r"<[^>]*>",  # HTML/XML tags
    r"javascript\s*:",  # JS protocol
    r"on\w+\s*=",  # HTML event handlers (onclick= etc)
    r"(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE)\s",  # SQL keywords
    r"(\$\{|\{\{)",  # Template injection
    r"(\.\.\/|\.\.\\)",  # Path traversal
    r"(eval|exec|system|passthru)\s*\(",  # Command injection
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
        if re.search(pattern, value, re.IGNORECASE):
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
    value = html.escape(value)  # encode & < > " '
    value = re.sub(r"<[^>]*>", "", value)  # strip remaining tags
    return value


# ---- Pydantic Schema --------------------------------------------------

# TODO: Find out why these functions are within a pydantic schema


class QuoteSubmission(BaseModel):
    username: str
    email: EmailStr
    phone: str
    registration: str
    service: Service

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = sanitise(v)
        if contains_injection(v):
            raise ValueError("Invalid characters in name.")
        if not re.match(r"^[a-zA-Z\s'\-]{2,64}$", v):
            raise ValueError("Name must be 2–64 characters, letters only.")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = sanitise(v).lower()
        if contains_injection(v):
            raise ValueError("Invalid characters in email.")
        if len(v) > 254:
            raise ValueError("Email must be 254 characters or fewer.")
        # EmailStr from Pydantic already validates format, so we just return the sanitized value
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = sanitise(v)
        if contains_injection(v):
            raise ValueError("Invalid characters in phone number.")
        if not re.match(r"^\+?[0-9\s\-\(\)]{7,20}$", v):
            raise ValueError(
                "Phone number must be 7-20 digits, may include +, spaces, - or ()."
            )
        return v

    @field_validator("registration")
    @classmethod
    def validate_registration(cls, v: str) -> str:
        v = sanitise(v).upper()
        if contains_injection(v):
            raise ValueError("Invalid characters in registration.")
        if len(v) > 7:
            raise ValueError("Registration must be 7 characters or fewer.")
        # UK format: AB12 CDE or AB12CDE
        if not re.match(r"^[A-Z]{2}[0-9]{2}\s?[A-Z]{3}$", v):
            raise ValueError("Invalid UK registration format (e.g. AB12 CDE).")
        return v

    @field_validator("service")
    @classmethod
    def validate_service(cls, v: str) -> str:
        # Enum already enforces the whitelist — this adds injection check
        if contains_injection(v):
            raise ValueError("Invalid service selection.")
        return v

    @model_validator(mode="after")
    def check_no_field_is_blank(self) -> "QuoteSubmission":
        """Belt-and-braces: ensure nothing slipped through as empty."""
        for field, value in self.__dict__.items():
            if isinstance(value, str) and not value.strip():
                raise ValueError(f"{field} must not be empty.")
        return self


# ---- Database Schema --------------------------------------------------

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS quote_submissions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username    VARCHAR(64)  NOT NULL,
    email       VARCHAR(254) NOT NULL,
    phone       VARCHAR(20)  NOT NULL,
    registration VARCHAR(7)   NOT NULL,
    service     VARCHAR(50)  NOT NULL,
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


async def save_submission(data: QuoteSubmission) -> str:
    """Insert a quote submission into the database PostgreSQL.

    Uses parameterized queries — no string concatenation, no SQL injection risk.
    Returns the generated UUID for the record.

    Parameters
    ----------
    data : QuoteSubmission
        The validated and sanitised quote submission data.

    Returns
    -------
    str
        The UUID of the newly created quote submission record.

    """
    submission_id = str(uuid.uuid4())
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO quote_submissions (id, username, email, phone, service, submitted_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            submission_id,
            data.username,
            data.email,
            data.phone,
            data.registration,
            data.service.value,
            data.registration,
            datetime.now(timezone.utc),
        )
        return submission_id


# ---- GMAIL API TODO: Configure GMAIL API --------------------------------------------------

# def build_email_body(data: QuoteSubmission, submission_id: str) -> str:
#     """First attempt at how the email body will look like when sent."""
#     return f"""
#     New Quote Request — {submission_id}

#     Name    : {data.username}
#     Email   : {data.email}
#     Phone   : {data.phone}
#     Registration   : {data.registration}
#     Service : {data.service.value}

#     Submitted at: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} UTC
#     """


# def send_gmail(data: QuoteSubmission, submission_id: str) -> None:
#     """
#     Send a notification email to the business via Gmail API.
#     Uses a service account — no stored passwords.

#     Parameters
#     ----------
#     data : QuoteSubmission
#         Sanitized Data.

#     submission_id : str
#         uuid string to identify the submissions.
#     """
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT, scopes=GMAIL_SCOPES
#     ).with_subject(DELEGATED_EMAIL)

#     service = build("gamil", "v1", credentials=credentials)

#     message = MIMEText(build_email_body(data, submission_id))
#     message["to"] = BUSINESS_EMAIL
#     message["subject"] = f"New Quote Request from {data.username}"

#     encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
#     service.users().messages().send(userId="me", body={"raw": encoded}).execute()

# ---- Endpoint --------------------------------------------------


@app.post("/api/quote", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # max 5 submissions per IP per minute
async def submit_quote(request: Request, payload: QuoteSubmission):
    """
    Receives, validates, sanitises, stores, and emails a quote submission.
    Pydantic handles validation — a 422 is returned automatically on failure.
    """
    try:
        # Save to PostgresSQL
        submission_id = await save_submission(payload)
        logger.info(f"submission saved: {submission_id}")

        # Send Gmail notificaition
        # send_gmail(payload, submission_id) # GMAIL NEED SET UP
        logger.info(f"Email send for submission: {submission_id}")

        return {
            "message": "Quote request received successfully.",
            "submission_id": submission_id,
        }

    except asyncpg.PostgresError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save submission. Please try again.",
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
