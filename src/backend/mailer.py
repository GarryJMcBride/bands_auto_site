# mailer.py
"""Email building and sending for the B&S Autos web application.

Builds the plain-text and HTML parts of a quote-notification email from a
validated QuoteSubmission, and sends them as a multipart/alternative message
over SMTP via aiosmtplib.
"""

from datetime import datetime, timezone
from email.message import EmailMessage

import aiosmtplib

from src.backend import config
from src.backend.schemas import QuoteSubmission


def build_email_body(data: QuoteSubmission, submission_id: str) -> str:
    """Build the plain-text part of the quote-notification email.

    Paired with `build_email_html` in `send_email`, which attaches both as a
    `multipart/alternative` message via `EmailMessage.set_content()` (this text
    part) + `.add_alternative()` (the HTML part). Deciding which part to show is
    entirely up to the receiving mail client, not this code: HTML-capable clients
    (Gmail, Outlook, Apple Mail, etc.) render the styled `build_email_html` part
    and never show this one, while clients that can't or won't render HTML — a
    plain-text mail reader, some accessibility/screen-reader setups, or a person
    viewing raw message source — fall back to this part automatically. That
    fallback is standard MIME behaviour, so no conditional logic is needed here.

    Parameters
    ----------
    data : QuoteSubmission
        Validated and sanitised submission data.
    submission_id : str
        UUID string identifying the stored submission.

    Returns
    -------
    str
        Plain-text email body.
    """
    return f"""
    New Quote Request — {submission_id}

    Name    : {data.username}
    Email   : {data.email}
    Phone   : {data.phone}
    Registration   : {data.registration}
    Service : {data.service.value}

    Submitted at: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} UTC
    """


def build_email_html(data: QuoteSubmission, submission_id: str) -> str:
    """Build the HTML part of the quote-notification email.

    Table-based layout with inline styles only — mail clients (Outlook/Gmail in
    particular) strip <style> blocks and ignore modern CSS, so nothing here can
    rely on a stylesheet.

    Paired with `build_email_body` in `send_email`, which attaches both as a
    `multipart/alternative` message via `EmailMessage.set_content()` (the plain-
    text part) + `.add_alternative()` (this HTML part). This part is the one
    HTML-capable clients (Gmail, Outlook, Apple Mail, etc.) render; the plain-
    text part from `build_email_body` is the fallback shown by anything that
    can't or won't render HTML — the mail client picks automatically, per
    standard MIME rules, so no conditional logic is needed here.

    Parameters
    ----------
    data : QuoteSubmission
        Validated and sanitised submission data. Field values are already
        sanitised/HTML-escaped by the `QuoteSubmission` validators, so they're
        interpolated into the markup as-is (no double-escaping).
    submission_id : str
        UUID string identifying the stored submission.

    Returns
    -------
    str
        HTML email body.
    """
    submitted_at = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    rows = "".join(
        f"""
        <tr>
          <td style="padding:12px 16px;border-bottom:1px solid #eee;color:#777;font-size:13px;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap;">{label}</td>
          <td style="padding:12px 16px;border-bottom:1px solid #eee;color:#222;font-size:15px;">{value}</td>
        </tr>"""
        for label, value in (
            ("Name", data.username),
            ("Email", f'<a href="mailto:{data.email}" style="color:#df1e00;text-decoration:none;">{data.email}</a>'),
            ("Phone", f'<a href="tel:{data.phone}" style="color:#df1e00;text-decoration:none;">{data.phone}</a>'),
            ("Registration", data.registration),
            ("Service", data.service.value),
        )
    )

    return f"""\
<!DOCTYPE html>
<html>
  <body style="margin:0;padding:0;background-color:#f4f4f4;font-family:Arial,Helvetica,sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4;padding:24px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background-color:#ffffff;border-radius:6px;overflow:hidden;">
            <tr>
              <td style="background-color:#df1e00;padding:20px 24px;">
                <span style="color:#ffffff;font-size:20px;font-weight:bold;">B&amp;S Autos</span>
                <span style="color:#ffe5df;font-size:13px;float:right;line-height:28px;">New Quote Request</span>
              </td>
            </tr>
            <tr>
              <td style="padding:24px;">
                <p style="margin:0 0 16px;color:#333;font-size:15px;">A new quote request came in through the website:</p>
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #eee;border-radius:4px;overflow:hidden;">
                  {rows}
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


async def send_email(data: QuoteSubmission, submission_id: str) -> None:
    """Send a quote-notification email to the business over SMTP.

    Transport is async and fully configured from the environment file.

    Parameters
    ----------
    data : QuoteSubmission
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
    message["Subject"] = f"New Quote Request from {data.username}"
    message.set_content(build_email_body(data, submission_id))
    message.add_alternative(build_email_html(data, submission_id), subtype="html")

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
