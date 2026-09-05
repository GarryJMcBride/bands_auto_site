# schemas.py
""" "Defines Pydantic models for data validation and serialization in the B&S Autos web application.

These models represent the structure of data for customer interactions, service requests, and other relevant
entities in the application.

They ensure that incoming data is validated and structured correctly before being processed by the application logic."""

import re
import html

from pydantic import BaseModel, EmailStr, field_validator, model_validator

from src.backend._typing import Service

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
        if len(v.replace(" ", "")) > 7:
            raise ValueError("Registration must be 7 characters or fewer.")
        # UK format: AB12 CDE or AB12CDE
        if not re.match(r"^[A-Z]{2}[0-9]{2}\s?[A-Z]{3}$", v):
            raise ValueError("Invalid UK registration format (e.g. AB12 CDE).")
        return v.replace(" ", "")

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
