# handle_form_inputs.py
"""Quote-submission endpoints for the B&S Autos web application.

Handles both submission paths — the JSON path used by transferFormInput.ts
when JavaScript is available, and the form-urlencoded no-JS fallback — plus
the database persistence they both share.
"""

import logging
import uuid
from datetime import datetime, timezone

import asyncpg
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from src.backend import config
from src.backend.classes import db
from src.backend.mailer import send_email
from src.backend.schemas import QuoteSubmission

logger = logging.getLogger(__name__)

router = APIRouter()


# ---- Database Operations --------------------------------------------------


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
    async with db.pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO quote_submissions (id, username, email, phone, registration, service, submitted_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            submission_id,
            data.username,
            data.email,
            data.phone,
            data.registration,
            data.service.value,
            datetime.now(timezone.utc),
        )
        return submission_id


async def update_database(payload: QuoteSubmission) -> str:
    """Updates the Database with the submission by the users.

    Takes save submission and receives SubmissionID.

    Parameters
    ----------
        payload : QuoteSubmission
            The data wrapped in pydantic class

    Returns
    -------
        submission_id : str
            The UUID of the newly created quote submission record
    """
    try:
        submission_id = await save_submission(payload)
        logger.info(f"Submission saved: {submission_id}")
        return submission_id
    except asyncpg.PostgresError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save submission to the database. Please try again later.",
        )


# ---- Endpoint --------------------------------------------------


@router.post("/api/quote-javascript-pipeline", status_code=status.HTTP_201_CREATED)
@config.limiter.limit("5/minute")  # max 5 submissions per IP per minute
async def submit_quote_javascript_pipeline(request: Request, payload: QuoteSubmission) -> dict:
    """Receive, validate, store, and email a quote submission (JSON path).

    Called by transferFormInput.ts via fetch() when JavaScript is available.
    Pydantic handles validation on `payload` — a 422 is returned automatically
    on failure, before this function body ever runs.

    Flow: validate -> store in Postgres -> notify the business by email. The
    submission is persisted first, so a failed notification email never loses
    a saved lead.

    Parameters
    ----------
    request : Request
        Not used directly in the function body — required as the first
        parameter so `@limiter.limit` can key rate limiting off the caller's
        IP address.
    payload : QuoteSubmission
        The validated, sanitised submission data.

    Returns
    -------
    dict
        A success message and the generated `submission_id`.

    Raises
    ------
    HTTPException
        500 if the confirmation email fails to send after the submission was
        already stored.
    """
    submission_id = await update_database(payload)

    try:
        await send_email(payload, submission_id)
        logger.info(f"Notification email sent for {submission_id}")
    except Exception as e:
        logger.error(f"Email send failed for {submission_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send confirmination email. Please try again later.",
        )

    return {
        "message": "Quote request received successfully.",
        "submission_id": submission_id,
    }


@router.post("/quote-python-pipeline")
@config.limiter.limit(
    "5/minute"
)  # same limit as /api/quote-javascript-pipeline — same endpoint, different transport
async def submit_quote_python_pipeline(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    registration: str = Form(...),
    service: str = Form(...),
) -> RedirectResponse:
    """Receive, validate, store, and email a quote submission (no-JS path).

    transferFormInput.ts intercepts the form's submit event and POSTs JSON to
    /api/quote-javascript-pipeline instead — but that only happens if
    JavaScript ran. A browser with JS disabled (or a page where the script
    failed to load) submits the form natively instead, as normal
    form-urlencoded fields, to whatever the <form>'s action/method are (see
    index.html). This endpoint is that target.

    Reuses the same QuoteSubmission validation and save/email logic as
    /api/quote-javascript-pipeline; the only difference is redirecting back
    to the page instead of returning JSON, since a plain HTML form submission
    expects a page in response, not a JSON body.

    Parameters
    ----------
    request : Request
        Not used directly in the function body — required as the first
        parameter so `@limiter.limit` can key rate limiting off the caller's
        IP address.
    username, email, phone, registration, service : str
        Raw form-urlencoded fields, unvalidated until passed into
        `QuoteSubmission` below.

    Returns
    -------
    RedirectResponse
        303 redirect to `/?submitted=success#booknow` on success, or
        `/?submitted=error#booknow` if validation, storage, or email sending
        failed — errors are swallowed here rather than raised, since a plain
        HTML form submission has no way to render a JSON error response.
    """
    try:
        payload = QuoteSubmission(
            username=username,
            email=email,
            phone=phone,
            registration=registration,
            service=service,
        )
        submission_id = await update_database(payload)
        await send_email(payload, submission_id)
    except Exception as e:
        logger.error(f"No-JS quote submission failed: {e}")
        return RedirectResponse(
            url="/?submitted=error#booknow", status_code=status.HTTP_303_SEE_OTHER
        )

    return RedirectResponse(
        url="/?submitted=success#booknow", status_code=status.HTTP_303_SEE_OTHER
    )
