# PR Summary: Fix quote form pipeline + add no-JS fallback

## Problem

The quote form was silently broken end-to-end: submitting it just reloaded the page with the form data appended to the URL as a query string, and nothing ever reached the database or the business inbox.

## Root causes (found in order)

- `static/js/vendor/dompurify/purify.es.mjs` (vendored, since there's no bundler) was missing entirely, so `transferFormInput.ts`'s DOMPurify import failed and the whole module never executed, leaving the submit handler unattached.
- The importmap entry for `"dompurify"` was missing a leading slash, which is invalid per the import map spec and gets silently nulled by the browser.
- `.mjs` files were being served with `Content-Type: text/plain` (Python's `mimetypes` doesn't know the extension on this OS); combined with the existing `X-Content-Type-Options: nosniff` header, the browser refused to execute the module with no visible error at all. Now registered explicitly via `mimetypes.add_type` in `app.py`.
- `quote_submissions` was never actually created — `CREATE_TABLE_SQL` existed but nothing executed it. Now runs in `lifespan()` on startup.
- `transferFormInput.ts` had a hardcoded `http://127.0.0.1:8000/api/quote` fetch target, a different origin than the app's actual `localhost:8000`, which CORS (no `allow_origins` configured) would have blocked anyway. Now a relative `/api/quote`.
- The `"tyres"` `<option>` didn't match the `"Tyres"` casing required by `VALID_SERVICES` (frontend) and the `Service` enum (backend).
- `validate_registration` counted the space in `"AB12 CDE"`-style plates before stripping it, rejecting valid UK registrations and, once relaxed, letting 8-character values overflow the `VARCHAR(7)` column.

## Changes

- Vendored the missing DOMPurify build, fixed the importmap path, and registered the `.mjs` MIME type explicitly so module loading no longer depends on the host OS's MIME registry.
- Wired `CREATE_TABLE_SQL` into `lifespan()` so the database table always exists on startup.
- Fixed the frontend fetch URL, the `"Tyres"` option casing, and the registration validator's space handling.
- Added a no-JS fallback: `POST /quote` accepts the form fields via `Form(...)`, builds the same `QuoteSubmission` Pydantic model used by `/api/quote`, and redirects back to `/` with `?submitted=success|error` for a server-rendered banner. The form now has a real `action`/`method` so it degrades gracefully instead of doing a broken native `GET` when JS fails to load.
- Added a matching success/error message on the JS path (`transferFormInput.ts`), closing a pre-existing TODO where it only `console.log`ged.
- Added `python-multipart` as a dependency (required by FastAPI's `Form(...)`).
- Updated `CLAUDE.md` and `docs/development_journal.md` to reflect the corrected architecture (SMTP replaced the Gmail API before this work even started, but the docs still described the old approach).
- Updated `todo.md` with follow-up items surfaced along the way: ESP migration, bundler adoption, rate limiter behind a reverse proxy, credential rotation, TLS/HSTS/CSP.

## Test plan

- [x] Submitted the form with JS enabled — confirmed `fetch` POST to `/api/quote`, no page reload, success banner shown, row saved to Postgres.
- [x] Submitted the form with JS disabled — confirmed native POST to `/quote`, redirect with `?submitted=success`, same validation/save/email path.
- [x] Verified `quote_submissions` table is created automatically on a fresh startup.
- [x] Verified UK registrations with a space (e.g. `"GA54 MCB"`) validate and store correctly without overflowing the column.
- [x] Verified `.mjs` now serves with a JS `Content-Type` and the DOMPurify module loads without error in a real browser.
