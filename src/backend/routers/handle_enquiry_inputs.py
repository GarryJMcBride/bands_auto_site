# handle_enquiry_inputs.py
"""Vehicle-enquiry endpoints for the B&S Autos web application.

Mirrors `handle_form_inputs.py`'s structure exactly, one file per form: the
JSON path used by enquiryForm.ts when JavaScript is available, and the
form-urlencoded no-JS fallback, plus the database persistence they both
share. See `handle_form_inputs.py` for the pattern this was copied from —
kept as a separate module (rather than folded into that one) so each form's
pipeline can be read, tested, and changed independently.
"""

import logging
import uuid
from datetime import UTC, datetime

import aiosmtplib
import asyncpg
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from src.backend import config
from src.backend.classes import db
from src.backend.mailer import send_enquiry_email
from src.backend.schemas import EnquirySubmission

logger = logging.getLogger(__name__)

router = APIRouter()


# ---- Database Operations --------------------------------------------------


async def save_enquiry(data: EnquirySubmission) -> str:
    """Insert a vehicle enquiry into the database PostgreSQL.

    Uses parameterized queries — no string concatenation, no SQL injection risk.
    Returns the generated UUID for the record.

    Parameters
    ----------
    data : EnquirySubmission
        The validated and sanitised enquiry data.

    Returns
    -------
    str
        The UUID of the newly created enquiry record.
    """
    submission_id = str(uuid.uuid4())
    async with db.pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO enquiry_submissions (id, username, email, phone, subject, message, submitted_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            submission_id,
            data.username,
            data.email,
            data.phone,
            data.subject,
            data.message,
            datetime.now(UTC),
        )
        return submission_id


async def update_enquiry_database(payload: EnquirySubmission) -> str:
    """Updates the Database with the enquiry submitted by the user.

    Parameters
    ----------
    payload : EnquirySubmission
        The data wrapped in the pydantic class

    Returns
    -------
    submission_id : str
        The UUID of the newly created enquiry record
    """
    try:
        submission_id = await save_enquiry(payload)
        logger.info(f"Enquiry saved: {submission_id}")
        return submission_id
    except asyncpg.PostgresError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save enquiry to the database. Please try again later.",
        )


# ---- Endpoint --------------------------------------------------


@router.post("/api/enquiry-javascript-pipeline", status_code=status.HTTP_201_CREATED)
@config.limiter.limit("5/minute")  # max 5 submissions per IP per minute
async def submit_enquiry_javascript_pipeline(
    request: Request, payload: EnquirySubmission
) -> dict:
    """Receive, validate, store, and email a vehicle enquiry (JSON path).

    Called by enquiryForm.ts via fetch() when JavaScript is available.
    Pydantic handles validation on `payload` — a 422 is returned automatically
    on failure, before this function body ever runs.

    Flow: validate -> store in Postgres -> notify the business by email. The
    enquiry is persisted first, so a failed notification email never loses a
    saved lead.

    Parameters
    ----------
    request : Request
        Not used directly in the function body — required as the first
        parameter so `@limiter.limit` can key rate limiting off the caller's
        IP address.
    payload : EnquirySubmission
        The validated, sanitised enquiry data.

    Returns
    -------
    dict
        A success message and the generated `submission_id`.

    Raises
    ------
    HTTPException
        500 if the notification email fails to send after the enquiry was
        already stored.
    """
    submission_id = await update_enquiry_database(payload)

    try:
        await send_enquiry_email(payload, submission_id)
        logger.info(f"Notification email sent for {submission_id}")
    except (aiosmtplib.SMTPException, OSError) as e:
        logger.error(f"Email send failed for {submission_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send confirmination email. Please try again later.",
        )

    return {
        "message": "Enquiry received successfully.",
        "submission_id": submission_id,
    }


@router.post("/enquiry-python-pipeline")
@config.limiter.limit(
    "5/minute"
)  # same limit as /api/enquiry-javascript-pipeline — same endpoint, different transport
async def submit_enquiry_python_pipeline(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
) -> RedirectResponse:
    """Receive, validate, store, and email a vehicle enquiry (no-JS path).

    enquiryForm.ts intercepts the form's submit event and POSTs JSON to
    /api/enquiry-javascript-pipeline instead — but that only happens if
    JavaScript ran. A browser with JS disabled (or a page where the script
    failed to load) submits the form natively instead, as normal
    form-urlencoded fields, to whatever the <form>'s action/method are (see
    index.html). This endpoint is that target.

    Reuses the same EnquirySubmission validation and save/email logic as
    /api/enquiry-javascript-pipeline; the only difference is redirecting back
    to the page instead of returning JSON, since a plain HTML form submission
    expects a page in response, not a JSON body.

    Parameters
    ----------
    request : Request
        Not used directly in the function body — required as the first
        parameter so `@limiter.limit` can key rate limiting off the caller's
        IP address.
    username, email, phone, subject, message : str
        Raw form-urlencoded fields, unvalidated until passed into
        `EnquirySubmission` below.

    Returns
    -------
    RedirectResponse
        303 redirect to `/?enquiry_submitted=success#requestcall` on success,
        or `/?enquiry_submitted=error#requestcall` if validation, storage, or
        email sending failed — errors are swallowed here rather than raised,
        since a plain HTML form submission has no way to render a JSON error
        response.
    """
    try:
        payload = EnquirySubmission(
            username=username,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
        )
        submission_id = await update_enquiry_database(payload)
        await send_enquiry_email(payload, submission_id)
    except Exception as e:  # noqa: BLE001 — deliberate top-level boundary: a plain
        # HTML form has no way to render a JSON error, so any failure at any stage
        # (validation, DB, or email) must still redirect to the error banner
        # instead of surfacing an unhandled 500 to a non-JS browser. Already logged.
        logger.error(f"No-JS enquiry submission failed: {e}")
        # 303 -> read_homepage() (app.py) renders the error banner from ?enquiry_submitted=
        return RedirectResponse(
            url="/?enquiry_submitted=error#requestcall",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    # 303 -> read_homepage() (app.py) renders the success banner from ?enquiry_submitted=
    return RedirectResponse(
        url="/?enquiry_submitted=success#requestcall",
        status_code=status.HTTP_303_SEE_OTHER,
    )
