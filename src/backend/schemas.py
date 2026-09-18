# schemas.py
""" "Defines Pydantic models for data validation and serialization in the B&S Autos web application.

These models represent the structure of data for customer interactions, service requests, and other relevant
entities in the application.

They ensure that incoming data is validated and structured correctly before being processed by the application logic."""

import re

from pydantic import BaseModel, EmailStr, field_validator, model_validator

from src.backend._typing import Service
from src.backend.validation import (
    check_no_blank_string_fields,
    contains_injection,
    sanitise,
    validate_email_address,
    validate_name,
    validate_phone_number,
)

# ---- Pydantic Schemas --------------------------------------------------


class BookSubmission(BaseModel):
    username: str
    email: EmailStr
    phone: str
    registration: str
    service: Service

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return validate_name(v)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return validate_email_address(v)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        return validate_phone_number(v)

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
    def check_no_field_is_blank(self) -> "BookSubmission":
        """Belt-and-braces: ensure nothing slipped through as empty."""
        check_no_blank_string_fields(self.__dict__)
        return self


class EnquirySubmission(BaseModel):
    """The "Not Sure What Your Vehicle Needs?" enquiry form (`#contact-form`
    in index.html) — a free-text alternative to BookSubmission for customers
    who don't know which service they need yet."""

    username: str
    email: EmailStr
    phone: str
    subject: str
    message: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return validate_name(v)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return validate_email_address(v)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        return validate_phone_number(v)

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, v: str) -> str:
        v = sanitise(v)
        if contains_injection(v):
            raise ValueError("Invalid characters in subject.")
        if not (2 <= len(v) <= 128):
            raise ValueError("Subject must be 2–128 characters.")
        return v

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        v = sanitise(v)
        if contains_injection(v):
            raise ValueError("Invalid characters in message.")
        if not (2 <= len(v) <= 2000):
            raise ValueError("Message must be 2–2000 characters.")
        return v

    @model_validator(mode="after")
    def check_no_field_is_blank(self) -> "EnquirySubmission":
        """Belt-and-braces: ensure nothing slipped through as empty."""
        check_no_blank_string_fields(self.__dict__)
        return self


# ---- Database Schemas --------------------------------------------------

CREATE_BOOK_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS book_submissions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username    VARCHAR(64)  NOT NULL,
    email       VARCHAR(254) NOT NULL,
    phone       VARCHAR(20)  NOT NULL,
    registration VARCHAR(7)   NOT NULL,
    service     VARCHAR(50)  NOT NULL,
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

CREATE_ENQUIRY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS enquiry_submissions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username    VARCHAR(64)  NOT NULL,
    email       VARCHAR(254) NOT NULL,
    phone       VARCHAR(20)  NOT NULL,
    subject     VARCHAR(128) NOT NULL,
    message     TEXT         NOT NULL,
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""
