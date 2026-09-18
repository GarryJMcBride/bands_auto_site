# validation.py
"""Generic input sanitisation and injection-detection helpers.

Domain-agnostic on purpose: these functions know nothing about
`BookSubmission` or any other specific form. Any Pydantic model in
`schemas.py` (current or future — e.g. the next form this repo gets hooked
up to) imports from here rather than defining its own copy, so the same
sanitisation rules apply uniformly across every form this backend serves.
"""

import html
import re

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


# ---- Shared field validators --------------------------------------------------
#
# Every form on this site collects a name/email/phone (currently BookSubmission
# and EnquirySubmission in schemas.py) — these live here, not on either model,
# so both `field_validator`s call the exact same rule instead of hand-copying
# the same regex into every new Pydantic model this backend ever grows.


def validate_name(value: str) -> str:
    """Sanitise and validate a person's name field.

    Shared by every form's `username`-style field. Raises ValueError with a
    user-facing message on failure, matching Pydantic's `field_validator`
    contract (the caller is expected to be one).
    """
    v = sanitise(value)
    if contains_injection(v):
        raise ValueError("Invalid characters in name.")
    if not re.match(r"^[a-zA-Z\s'\-]{2,64}$", v):
        raise ValueError("Name must be 2–64 characters, letters only.")
    return v


def validate_email_address(value: str) -> str:
    """Sanitise and validate an email address field.

    `EmailStr` (Pydantic) already validates the address *shape* before this
    runs — this only adds sanitisation, the injection check, and a length cap.
    """
    v = sanitise(value).lower()
    if contains_injection(v):
        raise ValueError("Invalid characters in email.")
    if len(v) > 254:
        raise ValueError("Email must be 254 characters or fewer.")
    return v


def validate_phone_number(value: str) -> str:
    """Sanitise and validate a UK-style phone number field."""
    v = sanitise(value)
    if contains_injection(v):
        raise ValueError("Invalid characters in phone number.")
    if not re.match(r"^\+?[0-9\s\-\(\)]{7,20}$", v):
        raise ValueError(
            "Phone number must be 7-20 digits, may include +, spaces, - or ()."
        )
    return v


def check_no_blank_string_fields(values: dict) -> None:
    """Belt-and-braces check: raise if any string field is blank/whitespace-only.

    Called from a `model_validator(mode="after")` on each Pydantic model with
    that model's own `self.__dict__` — shared here so every form's model gets
    the same guarantee without repeating the loop body.
    """
    for field, value in values.items():
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{field} must not be empty.")
