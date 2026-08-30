# config.py
""" "Configuration module for the B&S Autos web application.

This module manages application settings, and other configuration-related tasks for the B&S Autos web application."""

import os

from dotenv import load_dotenv

# Load .env here too — config is imported before app.py runs its own load_dotenv(),
# and load_dotenv() is idempotent, so calling it in both places is safe.
load_dotenv()

# ---- SMTP / Email config --------------------------------------------------
# Everything the mail transport needs is read from the environment. This is a
# TEMPORARY Gmail "middle" mailbox (app password) used only to prove the send
# pipeline works end-to-end. It will be swapped for a proper ESP (Resend /
# Amazon SES) later — that swap must only touch .env, never this code, so keep
# provider specifics (e.g. smtp.gmail.com) out of the logic and in SMTP_HOST.
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_ADDR = os.getenv("FROM_ADDR")

# Destination inbox for quote notifications (the business owner).
BUSINESS_EMAIL = os.getenv("BUSINESS_EMAIL")
