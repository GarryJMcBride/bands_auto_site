# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

B&S Autos is a single-page marketing site for a car garage with a "book your vehicle in" form. A FastAPI backend serves a static HTML template (built on the Envato **Linoor** theme) and exposes two endpoints — a JSON API and a form-encoded fallback — that both validate, sanitise, store, and email booking submissions. (The theme's own markup/CSS classes still say "quote" throughout — e.g. `class="get-quote-section"` — left as-is since it's presentational and unrelated to the underlying "book"-named data model.) The project is a work in progress — much of the wiring is stubbed behind `TODO`s (see below).

Python is managed with **uv**; frontend interactivity is written in **TypeScript** compiled with `tsc`. The bulk of the theme's JavaScript is legacy jQuery shipped as static, unmanaged files under `src/frontend/static/js/` (not in `package.json`).

## Commands

Python (run from repo root, with `.venv` activated):

```bash
uv sync                 # install deps from uv.lock
uv sync --no-dev        # install without dev deps
uv lock --upgrade       # refresh the lockfile
python main.py          # start Uvicorn on localhost:8000 (entry point)
uvicorn src.backend.app:app --reload   # dev server with auto-reload
pytest                  # run Python tests
pytest src/backend/tests/test_db.py    # run a single test file
```

Database utility scripts (run from repo root; they read `DATABASE_URL` from `.env`):

```bash
python -m scripts.db_migrate           # dry run: diff schemas.py against the live DB
python -m scripts.db_migrate --apply   # add missing tables/columns (additive only)
python -m scripts.db_query tables      # tables + row counts (also: describe <t>, head <t> -n 5)
python -m scripts.db_query sql "SELECT ..."   # ad-hoc query, read-only unless --write
```

TypeScript / frontend:

```bash
npm ci                  # clean install from package-lock.json
npm run build           # tsc: compile src/frontend/typescript -> src/frontend/dist
npm run watch           # tsc --watch
npx vitest              # run JS/TS tests (vitest is configured but no test files exist yet)
```

SCSS (theme styles are committed as compiled CSS; recompile when editing `.scss`):

```bash
npx sass --watch src/frontend/static/css/style.scss src/frontend/static/css/style.css
```

## Architecture

**Request flow for a booking submission** — the form (`id="book-form"` in `index.html`, still inside the theme's `class="get-quote-section"` block) works with or without JavaScript, via two independent paths that converge on the same backend model:
1. `src/frontend/templates/index.html` renders the form (served at `/` by `read_homepage`), with `action="/book-python-pipeline" method="post"` as its native fallback target.
2. **With JS**: `src/frontend/typescript/bookForm.ts` (compiled to `/dist/bookForm.js`) intercepts the submit event, sanitises input with **DOMPurify** (via `sanitise.ts`), validates client-side, then `fetch()`-POSTs JSON to `/api/book-javascript-pipeline` (`submit_book_javascript_pipeline` in `routers/handle_book_inputs.py`), which shows a success/error message in-page.
3. **Without JS** (or if the JS fails to load — see gotcha below): the browser falls through to its native form submission, `POST /book-python-pipeline` (`submit_book_python_pipeline` in `routers/handle_book_inputs.py`), which accepts the same fields as `Form(...)` and redirects back to `/?book_submitted=success` or `?book_submitted=error` for the server-rendered banner.
4. Both endpoints build the exact same `BookSubmission` Pydantic model and call the same `update_book_database()`/`send_book_email()` helpers — there's no separate validation path to keep in sync for the backend half.

Client-side validation is convenience only — the **backend is the source of truth**. Validation rules are intentionally duplicated on both sides (name/email/phone/UK-registration/service regexes in `bookForm.ts`/`enquiryForm.ts` mirror the `field_validator`s in `schemas.py`, though the JS versions are deliberately looser on registration/email); keep the *shapes* roughly in sync when changing either, but never rely on the JS copy for security.

**Gotcha:** DOMPurify is vendored (not bundled — see `docs/development_journal.md` → "Email Sending pipeline") as `static/js/vendor/dompurify/purify.es.mjs`, loaded via an import map in `index.html`. A `.mjs` file served with the wrong `Content-Type` (e.g. `text/plain`, which Python's `mimetypes` can default to on some OSes) makes the browser silently refuse to run the whole module — no console error, no bad status code — and the form quietly falls back to the no-JS path. `app.py` explicitly registers `mimetypes.add_type("text/javascript", ".mjs")` on startup to prevent this; don't remove it.

**Backend layout (`src/backend/`):** the modularisation this section used to describe as "pending work" is done — `app.py` is now just app wiring, with each concern split into its own module. There are now two parallel form pipelines (booking and enquiry) sharing this same structure — see `docs/pipeline-architecture-visual-diagram.md` for the full breakdown of both:
- `app.py` — FastAPI instance (docs disabled), `lifespan()` (connects the asyncpg pool via `classes.Database`/`db.connect()`, runs `CREATE_BOOK_TABLE_SQL`/`CREATE_ENQUIRY_TABLE_SQL` via `db.ensure_schema()`, closes the pool on shutdown), CORS + `SecurityHeadersMiddleware`, the shared `slowapi` rate limiter attached to `app.state.limiter`, `app.include_router()` for both `handle_book_inputs.router` and `handle_enquiry_inputs.router` (live, not commented out), the `mimetypes.add_type(".mjs")` gotcha (must run before the `/static` mount — see below), the `/static`/`/dist` static mounts, and the `GET /` `read_homepage` route (reads `?book_submitted=`/`?enquiry_submitted=` for the no-JS success/error banners).
- `config.py` — env-loaded settings (`DATABASE_URL`, `DEBUG`, SMTP/email vars), the module logger, and the shared `limiter` (`slowapi.Limiter`) instance — defined here (a dependency-free leaf module) so both `app.py` and the routers can import the same instance without a circular import.
- `classes.py` — `SecurityHeadersMiddleware` (adds `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection` to every response) and `Database`, a thin asyncpg pool wrapper (`connect()`, `close()`, `ensure_schema()`), exposed as the `db` singleton both routers import.
- `_typing.py` — the `Service` enum (`Diagnostics`, `Tyres`, `Servicing`, `Batteries`, `Exhausts`, `Repairs`) — booking-specific.
- `schemas.py` — the `BookSubmission` and `EnquirySubmission` Pydantic models (per-field `field_validator`s that call into `validation.py`, plus a `model_validator` belt-and-braces blank check each), and `CREATE_BOOK_TABLE_SQL`/`CREATE_ENQUIRY_TABLE_SQL` (the `book_submissions`/`enquiry_submissions` table DDL, executed once at lifespan startup).
- `validation.py` — `sanitise()` / `contains_injection()` (+ `INJECTION_PATTERNS`), plus shared field validators (`validate_name`, `validate_email_address`, `validate_phone_number`, `check_no_blank_string_fields`) — generic helpers both `BookSubmission` and `EnquirySubmission` call into. Deliberately form-agnostic and kept separate from `schemas.py` specifically so a future form's Pydantic model — or a copy of this repo reused for another client site — can reuse them without depending on `BookSubmission`. See `docs/development_journal.md` → "Splitting sanitisation out of schemas.py into validation.py".
- `mailer.py` — booking and enquiry email building/sending in one module. `build_book_email_body()`/`build_book_email_html()`/`send_book_email()` (booking) and `build_enquiry_email_body()`/`build_enquiry_email_html()`/`send_enquiry_email()` (enquiry) share a common layout via `_render_html_shell()`/`_render_plain_text()`/`_render_field_rows_html()` (the header logo is embedded as an inline CID attachment rather than a `static/images/...` path — see `docs/development_journal.md` → "Implementing images to the html email file") and a shared `_attach_logo_and_send()` tail that assembles a `multipart/alternative` `EmailMessage` and sends it via `aiosmtplib.send()` using `config`'s SMTP settings.
  - Each `send_*_email` sends a `multipart/alternative` message: its `*_html` builder (styled, brand-coloured table layout) as the primary part plus its `*_body` builder (plain text) as the fallback part, via `EmailMessage.set_content()` + `.add_alternative()`. This isn't a JS-vs-no-JS fallback — it's MIME negotiation the *mail client* does automatically: HTML-capable clients (Gmail, Outlook, Apple Mail, etc.) render the styled version, and anything that can't or won't render HTML (plain-text clients, some accessibility tools, an admin reading raw source) gets the plain-text part instead. Both parts of a given pipeline are built from the same sanitised submission fields, so keep them in sync when changing one.
- `routers/handle_book_inputs.py` — `save_book()` (parameterized `INSERT` via `db.pool.acquire()`), `update_book_database()` (wraps `asyncpg.PostgresError` as an `HTTPException(500)`), and both POST endpoints — `submit_book_javascript_pipeline` (JSON, `201` / `HTTPException`) and `submit_book_python_pipeline` (form fields, `303` redirect either way).
- `routers/handle_enquiry_inputs.py` — mirrors `handle_book_inputs.py` exactly for the enquiry form (`save_enquiry()`, `update_enquiry_database()`, `submit_enquiry_javascript_pipeline`, `submit_enquiry_python_pipeline`), kept as a separate module so each form's pipeline can be read, tested, and changed independently.
- `tests/test_db.py` — tests are entirely commented out.

**Frontend layout (`src/frontend/`):**
- `typescript/` — the only hand-written, type-checked JS source: `bookForm.ts` and `enquiryForm.ts` (one per form, each with its own client-side validation), sharing `sanitise.ts` (DOMPurify wrapper) and `formFeedback.ts` (error/banner rendering), plus `types.ts` and `classes.ts`. Compiles to `dist/`.
- `static/` — Linoor theme assets (CSS, fonts, legacy jQuery plugins). Themeable via `static/css/colors/` and `static/css/variables/` `:root` overrides. Also holds `static/js/vendor/dompurify/purify.es.mjs` — DOMPurify's official build, copied in manually (not via a bundler) since there isn't one; see the gotcha above. Note: the theme's own class names (e.g. `get-quote-section`) still say "quote" and are left as-is — only the underlying form id/data model was renamed to "book".
- `templates/` — Jinja2 templates (`index.html`, `not-found.html`), served via Starlette `Jinja2Templates`. `index.html` reads `book_submitted`/`enquiry_submitted` context vars (set by `read_homepage` from the `?book_submitted=`/`?enquiry_submitted=` query params) to show a success/error banner for the no-JS fallback path of each form.

Static mounts: `/static` → `src/frontend/static`, `/dist` → `src/frontend/dist`.

## Configuration & state

- Environment variables load from `.env` via `python-dotenv`. Key vars: `DATABASE_URL` (Postgres, used by asyncpg), `ENVIRONMENT` (`development` enables `DEBUG`), and SMTP settings (`config.py`): `SMTP_HOST`/`SMTP_PORT`/`SMTP_USER`/`SMTP_PASS`, `FROM_ADDR` (sender), `BUSINESS_EMAIL` (recipient). Email sending is functional (`send_book_email`/`send_enquiry_email` via `aiosmtplib`), but currently points at a **temporary personal Gmail app-password mailbox**, not a production ESP — see `todo.md` → `## 12. Email Delivery` before relying on it long-term. `FROM_ADDR` must match/be authorised by whatever account `SMTP_USER` authenticates as, or the send will be rejected.
- Postgres table DDL is `CREATE_BOOK_TABLE_SQL` (`book_submissions`) and `CREATE_ENQUIRY_TABLE_SQL` (`enquiry_submissions`) in `schemas.py`, executed automatically in `lifespan()` (`app.py`) on every startup via `db.ensure_schema()`. Because `CREATE TABLE IF NOT EXISTS` never alters an existing table, a column added to `schemas.py` won't reach an already-created database on its own — run `python -m scripts.db_migrate --apply` (`scripts/db_migrate.py`) to add it. It diffs `schemas.py`'s DDL (run in a throwaway scratch schema) against the live tables, applies only additive changes (missing tables/columns), and reports — never applies — dropped/changed columns and new `NOT NULL` columns without a `DEFAULT` on populated tables. `scripts/db_query.py` holds the read-oriented query helpers; both share `scripts/_db.py`, whose `DDL_STATEMENTS` list must include any new `CREATE_*_TABLE_SQL`.
- FastAPI docs are disabled (`docs_url`/`redoc_url`/`openapi_url` = `None`).

## Working in this repo

- The codebase still has intentional `TODO`s and commented-out blocks in places (CORS `allow_origins`, `Pydantic` settings vs raw `os.getenv`). Before assuming a feature works, check whether its call is commented out — but don't assume the reverse either: lifespan (DB pool + table creation), the router, email sending, and the `schemas.py`/`validation.py` split are all fully wired and functional now, not stubs. `app.py` is meant to stay limited to app wiring — new logic belongs in whichever module already owns that concern (or a new one, following the `validation.py` precedent — a domain-agnostic helper module split out specifically so it's reusable if/when this repo becomes a starting point for another form or another client site), not back inline in `app.py`.
- After editing any `.ts` file, run `npm run build` — the app serves the compiled `dist/` output, not the TypeScript source.
- `docs/` contains deeper background: `architecture.md` (full flow + rationale for every legacy JS file), `development_journal.md`, and `site_content.md`. `todo.md` at the root tracks outstanding work.
