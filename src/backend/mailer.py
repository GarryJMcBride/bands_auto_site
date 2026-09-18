# mailer.py
"""Email building and sending for the B&S Autos web application.

Builds the plain-text and HTML parts of a notification email from a validated
submission (booking or enquiry) and sends it as a multipart/alternative message
over SMTP via aiosmtplib. Both submission types share the same HTML/plain-text
shell (`_render_html_shell`/`_render_plain_text`) — only the field rows and
the banner label differ — so the two pipelines can't drift apart in layout.
"""

from datetime import UTC, datetime
from email.message import EmailMessage
from pathlib import Path

import aiosmtplib

from src.backend import config
from src.backend.schemas import BookSubmission, EnquirySubmission

# The email header logo is sent as an inline CID attachment (see `send_book_email`),
# not a plain <img src="static/images/...">. This message travels over raw SMTP
# to an arbitrary mail client, not a browser with access to this app's /static
# mount, so a relative or site-relative path resolves to nothing on the
# recipient's end. Embedding the image as a MIME part referenced by Content-ID
# also renders immediately in Gmail/Outlook without the "load remote images?"
# prompt a normal http(s):// <img> would trigger.
LOGO_PATH = Path(__file__).resolve().parent.parent / "frontend" / "static" / "images" / "bands_logo_on_scroll.png"
LOGO_CID = "bands-logo-header"


def _render_field_rows_html(rows: list[tuple[str, str]]) -> str:
    """Build the inline-styled `<tr>` rows shared by every notification email.

    Pulled out so the booking and enquiry HTML builders can't render their
    field tables with subtly different styling — one row template, reused.
    """
    return "".join(
        f"""
        <tr>
          <td style="padding:12px 16px;border-bottom:1px solid #eee;color:#777;font-size:13px;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap;">{label}</td>
          <td style="padding:12px 16px;border-bottom:1px solid #eee;color:#222;font-size:15px;">{value}</td>
        </tr>"""
        for label, value in rows
    )


def _render_html_shell(banner_label: str, intro_text: str, rows_html: str, submission_id: str) -> str:
    """Wrap a notification email's field rows in the shared banner/table/footer
    layout (brand-red header with the logo, white content card, footer with
    submission ID + timestamp).

    Table-based layout with inline styles only — mail clients (Outlook/Gmail in
    particular) strip <style> blocks and ignore modern CSS, so nothing here can
    rely on a stylesheet. Shared by `build_book_email_html` (booking) and
    `build_enquiry_email_html` (enquiry) so both pipelines' emails stay
    visually identical apart from their content.

    Parameters
    ----------
    banner_label : str
        Text shown top-right of the red banner (e.g. "New Booking Request").
    intro_text : str
        One-line sentence introducing the field table.
    rows_html : str
        Pre-rendered `<tr>` markup from `_render_field_rows_html`.
    submission_id : str
        UUID string identifying the stored submission.

    Returns
    -------
    str
        Complete HTML email body.
    """
    submitted_at = datetime.now(UTC).strftime("%d %b %Y, %H:%M UTC")
    return f"""\
<!DOCTYPE html>
<html>
  <body style="margin:0;padding:0;background-color:#000000;font-family:Arial,Helvetica,sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#000000;padding:24px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background-color:#ffffff;border-radius:6px;overflow:hidden;">
            <tr>
              <td style="background-color:#ff0000;padding:20px 24px;">
                <!-- src="cid:{LOGO_CID}" matches the Content-ID send_book_email/send_enquiry_email
                     attach this part under via `add_related` — the mail client resolves it to the
                     inline image part, not a network fetch. -->
                <img src="cid:{LOGO_CID}" alt="B&amp;S Autos" height="28" style="display:inline-block;vertical-align:middle;border:0;">
                <span style="color:#ffe5df;font-size:13px;float:right;line-height:28px;">{banner_label}</span>
              </td>
            </tr>
            <tr>
              <td style="padding:24px;">
                <p style="margin:0 0 16px;color:#333;font-size:15px;">{intro_text}</p>
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #eee;border-radius:4px;overflow:hidden;">
                  {rows_html}
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:0 24px 24px;">
                <p style="margin:0;color:#999;font-size:12px;">Submission ID: {submission_id}</p>
                <p style="margin:4px 0 0;color:#999;font-size:12px;">Submitted at: {submitted_at}</p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""


def _render_plain_text(heading: str, submission_id: str, field_lines: str) -> str:
    """Build the plain-text shell shared by every notification email.

    Parameters
    ----------
    heading : str
        e.g. "New Booking Request".
    submission_id : str
        UUID string identifying the stored submission.
    field_lines : str
        Pre-formatted "Label : value" lines (one per line, already indented).

    Returns
    -------
    str
        Plain-text email body.
    """
    return f"""
    {heading} — {submission_id}

{field_lines}
    Submitted at: {datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")} UTC
    """


async def _attach_logo_and_send(message: EmailMessage) -> None:
    """Attach the shared logo as an inline CID part on the html sub-part, then
    send over SMTP. Shared tail end of `send_book_email`/`send_enquiry_email`.

    Parameters
    ----------
    message : EmailMessage
        Already has both the plain-text (`set_content`) and HTML
        (`add_alternative`) parts attached — this only adds the image and sends.
    """
    # Attach the logo to the *html* sub-part (not the top-level message) so it
    # becomes multipart/related nested inside the multipart/alternative html
    # branch — this is what makes `cid:` resolve inside that html body specifically,
    # rather than showing up as a separate top-level attachment on the email.
    html_part = message.get_payload()[1]
    html_part.add_related(LOGO_PATH.read_bytes(), maintype="image", subtype="png", cid=f"<{LOGO_CID}>")

    # Port 465 = implicit TLS; anything else (e.g. 587) = STARTTLS upgrade.
    use_tls = config.SMTP_PORT == 465
    await aiosmtplib.send(
        message,
        hostname=config.SMTP_HOST,
        port=config.SMTP_PORT,
        username=config.SMTP_USER,
        password=config.SMTP_PASS,
        use_tls=use_tls,
        start_tls=not use_tls,
    )


# ---- Book pipeline --------------------------------------------------


def build_book_email_body(data: BookSubmission, submission_id: str) -> str:
    """Build the plain-text part of the booking-notification email.

    Paired with `build_book_email_html` in `send_book_email`, which attaches
    both as a `multipart/alternative` message via `EmailMessage.set_content()`
    (this text part) + `.add_alternative()` (the HTML part). Deciding which
    part to show is entirely up to the receiving mail client, not this code:
    HTML-capable clients (Gmail, Outlook, Apple Mail, etc.) render the styled
    `build_book_email_html` part and never show this one, while clients that
    can't or won't render HTML — a plain-text mail reader, some
    accessibility/screen-reader setups, or a person viewing raw message
    source — fall back to this part automatically. That fallback is standard
    MIME behaviour, so no conditional logic is needed here.

    Parameters
    ----------
    data : BookSubmission
        Validated and sanitised submission data.
    submission_id : str
        UUID string identifying the stored submission.

    Returns
    -------
    str
        Plain-text email body.
    """
    field_lines = (
        f"    Name    : {data.username}\n"
        f"    Email   : {data.email}\n"
        f"    Phone   : {data.phone}\n"
        f"    Registration   : {data.registration}\n"
        f"    Service : {data.service.value}\n"
    )
    return _render_plain_text("New Booking Request", submission_id, field_lines)


def build_book_email_html(data: BookSubmission, submission_id: str) -> str:
    """Build the HTML part of the booking-notification email.

    Paired with `build_book_email_body` in `send_book_email`, which attaches
    both as a `multipart/alternative` message via `EmailMessage.set_content()`
    (the plain-text part) + `.add_alternative()` (this HTML part). This part
    is the one HTML-capable clients (Gmail, Outlook, Apple Mail, etc.) render;
    the plain-text part from `build_book_email_body` is the fallback shown by
    anything that can't or won't render HTML — the mail client picks
    automatically, per standard MIME rules, so no conditional logic is needed
    here.

    Parameters
    ----------
    data : BookSubmission
        Validated and sanitised submission data. Field values are already
        sanitised/HTML-escaped by the `BookSubmission` validators, so they're
        interpolated into the markup as-is (no double-escaping).
    submission_id : str
        UUID string identifying the stored submission.

    Returns
    -------
    str
        HTML email body.
    """
    rows_html = _render_field_rows_html(
        [
            ("Name", data.username),
            (
                "Email",
                f'<a href="mailto:{data.email}" style="color:#ff0000;text-decoration:none;">{data.email}</a>',
            ),
            (
                "Phone",
                f'<a href="tel:{data.phone}" style="color:#ff0000;text-decoration:none;">{data.phone}</a>',
            ),
            ("Registration", data.registration),
            ("Service", data.service.value),
        ]
    )
    return _render_html_shell(
        "New Booking Request",
        "A new Booking Request came in through the website from a visitor:",
        rows_html,
        submission_id,
    )


async def send_book_email(data: BookSubmission, submission_id: str) -> None:
    """Send a booking-notification email to the business over SMTP.

    Transport is async and fully configured from the environment file.

    Parameters
    ----------
    data : BookSubmission
        Validated and sanitised submission data.
    submission_id : str
        UUID string identifying the stored submission.

    Notes
    -----
    Switching the temporary "Gmail app-password mailbox" for a proper Email Sender Provider
    later requires no changes here.
    """
    message = EmailMessage()
    message["From"] = config.FROM_ADDR
    message["To"] = config.BUSINESS_EMAIL
    message["Subject"] = f"New Booking Request from {data.username}"
    message.set_content(build_book_email_body(data, submission_id))
    message.add_alternative(build_book_email_html(data, submission_id), subtype="html")
    await _attach_logo_and_send(message)


# ---- Enquiry pipeline --------------------------------------------------


def build_enquiry_email_body(data: EnquirySubmission, submission_id: str) -> str:
    """Build the plain-text part of the enquiry-notification email.

    Mirrors `build_book_email_body` — see that docstring for the MIME rationale,
    which applies identically here via `_render_plain_text`.
    """
    field_lines = (
        f"    Name    : {data.username}\n"
        f"    Email   : {data.email}\n"
        f"    Phone   : {data.phone}\n"
        f"    Subject : {data.subject}\n"
        f"    Message : {data.message}\n"
    )
    return _render_plain_text("New Enquiry Request", submission_id, field_lines)


def build_enquiry_email_html(data: EnquirySubmission, submission_id: str) -> str:
    """Build the HTML part of the enquiry-notification email.

    Mirrors `build_book_email_html` — see that docstring for the MIME rationale,
    which applies identically here via `_render_html_shell`.
    """
    rows_html = _render_field_rows_html(
        [
            ("Name", data.username),
            (
                "Email",
                f'<a href="mailto:{data.email}" style="color:#ff0000;text-decoration:none;">{data.email}</a>',
            ),
            (
                "Phone",
                f'<a href="tel:{data.phone}" style="color:#ff0000;text-decoration:none;">{data.phone}</a>',
            ),
            ("Subject", data.subject),
            ("Message", data.message),
        ]
    )
    return _render_html_shell(
        "New Enquiry Request",
        "A new Enquiry Request came in through the website from a visitor:",
        rows_html,
        submission_id,
    )


async def send_enquiry_email(data: EnquirySubmission, submission_id: str) -> None:
    """Send an enquiry-notification email to the business over SMTP.

    Mirrors `send_book_email` exactly apart from which builders it calls —
    see that function's docstring for transport details.
    """
    message = EmailMessage()
    message["From"] = config.FROM_ADDR
    message["To"] = config.BUSINESS_EMAIL
    message["Subject"] = f"New Enquiry Request from {data.username}"
    message.set_content(build_enquiry_email_body(data, submission_id))
    message.add_alternative(build_enquiry_email_html(data, submission_id), subtype="html")
    await _attach_logo_and_send(message)
