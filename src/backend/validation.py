# validation.py
"""Generic input sanitisation and injection-detection helpers.

Domain-agnostic on purpose: these functions know nothing about
`QuoteSubmission` or any other specific form. Any Pydantic model in
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
