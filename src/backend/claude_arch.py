# ─── Imports ──────────────────────────────────────────────────────────────────

import re
import html
import uuid
import logging
from datetime import datetime, timezone
from enum import Enum
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Config ───────────────────────────────────────────────────────────────────

# Move these to environment variables / .env in production
DATABASE_URL       = "postgresql://user:password@localhost/dbname"  # 👈 replace
BUSINESS_EMAIL     = "yourbusiness@gmail.com"                       # 👈 replace
GMAIL_SCOPES       = ["https://www.googleapis.com/auth/gmail.send"]
SERVICE_ACCOUNT    = "service_account.json"                         # 👈 replace
ALLOWED_ORIGINS    = ["https://yourdomain.com"]                     # 👈 replace

# ─── Database ─────────────────────────────────────────────────────────────────

db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create and close the database connection pool on startup/shutdown."""
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
    logger.info("Database pool created.")
    yield
    await db_pool.close()
    logger.info("Database pool closed.")

# ─── Rate Limiter ─────────────────────────────────────────────────────────────

limiter = Limiter(key_func=get_remote_address)

# ─── App Setup ────────────────────────────────────────────────────────────────

app = FastAPI(
    lifespan=lifespan,
    debug=False,  # Never True in production
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# HTTPS redirect — enforce encrypted transport
app.add_middleware(HTTPSRedirectMiddleware)

# CORS — only allow your own domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

# ─── Security Headers Middleware ──────────────────────────────────────────────

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"]   = "default-src 'self'"
        response.headers["X-Content-Type-Options"]    = "nosniff"
        response.headers["X-Frame-Options"]           = "DENY"
        response.headers["Referrer-Policy"]           = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# ─── Enums ────────────────────────────────────────────────────────────────────

class Service(str, Enum):
    web_dev   = "Website Development"
    graphic   = "Graphic Designing"
    marketing = "Digital Marketing"
    app_dev   = "App Development"

# ─── Sanitisation ─────────────────────────────────────────────────────────────

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
    """Return True if the value contains any known injection pattern."""
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, value, re.IGNORECASE):
            return True
    return False

def sanitise(value: str) -> str:
    """
    - Strip leading/trailing whitespace
    - Remove control characters
    - Escape HTML entities
    - Strip any remaining HTML tags
    """
    value = value.strip()
    value = re.sub(r"[\x00-\x1F\x7F]", "", value)  # remove control characters
    value = html.escape(value)                       # encode & < > " '
    value = re.sub(r"<[^>]*>", "", value)           # strip remaining tags
    return value

# ─── Pydantic Schema ──────────────────────────────────────────────────────────

class QuoteSubmission(BaseModel):
    username : str
    email    : EmailStr
    phone    : str
    service  : Service

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
        if len(v) > 254:  # RFC 5321 max email length
            raise ValueError("Email address is too long.")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = sanitise(v)
        if contains_injection(v):
            raise ValueError("Invalid characters in phone number.")
        if not re.match(r"^\+?[\d\s\-()]{7,20}$", v):
            raise ValueError("Invalid phone number format.")
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

# ─── Database Schema ──────────────────────────────────────────────────────────

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS quote_submissions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username    VARCHAR(64)  NOT NULL,
    email       VARCHAR(254) NOT NULL,
    phone       VARCHAR(20)  NOT NULL,
    service     VARCHAR(50)  NOT NULL,
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

async def save_submission(data: QuoteSubmission) -> str:
    """
    Insert a validated submission into PostgreSQL.
    Uses parameterized queries — no string concatenation, no SQL injection risk.
    Returns the generated UUID for the record.
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
            data.service.value,
            datetime.now(timezone.utc),
        )
    return submission_id

# ─── Gmail API ────────────────────────────────────────────────────────────────

def build_email_body(data: QuoteSubmission, submission_id: str) -> str:
    return f"""
    New Quote Request — {submission_id}

    Name    : {data.username}
    Email   : {data.email}
    Phone   : {data.phone}
    Service : {data.service.value}

    Submitted at: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} UTC
    """

def send_gmail(data: QuoteSubmission, submission_id: str) -> None:
    """
    Send a notification email to the business via Gmail API.
    Uses a service account — no stored passwords.
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT, scopes=GMAIL_SCOPES
    )
    service = build("gmail", "v1", credentials=credentials)

    message = MIMEText(build_email_body(data, submission_id))
    message["to"]      = BUSINESS_EMAIL
    message["subject"] = f"New Quote Request from {data.username}"

    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(
        userId="me",
        body={"raw": encoded}
    ).execute()

# ─── Endpoint ─────────────────────────────────────────────────────────────────

@app.post("/api/quote", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # max 5 submissions per IP per minute
async def submit_quote(request: Request, payload: QuoteSubmission):
    """
    Receives, validates, sanitises, stores, and emails a quote submission.
    Pydantic handles validation — a 422 is returned automatically on failure.
    """
    try:
        # Save to PostgreSQL
        submission_id = await save_submission(payload)
        logger.info(f"Submission saved: {submission_id}")

        # Send Gmail notification
        send_gmail(payload, submission_id)
        logger.info(f"Email sent for submission: {submission_id}")

        return {
            "message"       : "Quote request received successfully.",
            "submission_id" : submission_id,
        }

    except asyncpg.PostgresError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save submission. Please try again."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )