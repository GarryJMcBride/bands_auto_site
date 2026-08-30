# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

B&S Autos is a single-page marketing site for a car garage with a "request a quote" form. A FastAPI backend serves a static HTML template (built on the Envato **Linoor** theme) and exposes one JSON API endpoint that validates, sanitises, stores, and (eventually) emails quote submissions. The project is a work in progress — much of the wiring is stubbed behind `TODO`s (see below).

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

**Request flow for a quote submission:**
1. `src/frontend/templates/index.html` renders the form (served at `/` by `read_homepage`).
2. `src/frontend/typescript/transferFormInput.ts` (compiled to `/dist/transferFormInput.js`) intercepts the submit event, sanitises input with **DOMPurify**, validates client-side, then `fetch()`-POSTs JSON to `/api/quote`.
3. `submit_quote` in `src/backend/app.py` re-validates/sanitises server-side via the `QuoteSubmission` Pydantic model, then stores to Postgres and (eventually) emails the business.

Client-side validation is convenience only — the **backend is the source of truth**. Validation rules are intentionally duplicated on both sides (name/email/phone/UK-registration/service regexes in `transferFormInput.ts` mirror the `field_validator`s in `app.py`); keep them in sync when changing either.

**Backend layout (`src/backend/`):**
- `app.py` — the live application: FastAPI app, CORS + `SecurityHeadersMiddleware`, `slowapi` rate limiting, the `QuoteSubmission` model with sanitisation (`sanitise` / `contains_injection`), asyncpg pool lifespan, `save_submission`, Gmail sending, and the `/api/quote` endpoint. **Most logic currently lives inline in this one file.**
- `routers/handle_form_inputs.py`, `config.py`, `schemas.py`, `classes.py`, `_typing.py` — placeholder/empty modules that inline `app.py` logic is meant to be extracted into (the router is imported but `app.include_router` is commented out). Wiring these up is pending work.
- `tests/test_db.py` — tests are entirely commented out.

**Frontend layout (`src/frontend/`):**
- `typescript/` — the only hand-written, type-checked JS source (`transferFormInput.ts`, `types.ts`, `classes.ts`). Compiles to `dist/`.
- `static/` — Linoor theme assets (CSS, fonts, legacy jQuery plugins). Themeable via `static/css/colors/` and `static/css/variables/` `:root` overrides.
- `templates/` — Jinja2 templates (`index.html`, `not-found.html`), served via Starlette `Jinja2Templates`.

Static mounts: `/static` → `src/frontend/static`, `/dist` → `src/frontend/dist`.

## Configuration & state

- Environment variables load from `.env` via `python-dotenv`. Key vars: `DATABASE_URL` (Postgres, used by asyncpg), `GMAIL_SCOPES`, `ENVIRONMENT` (`development` enables `DEBUG`). Several email vars (`BUSINESS_EMAIL`, `DELEGATED_EMAIL`, `SERVICE_ACCOUNT`) are referenced by `send_gmail` but currently commented out at module level — that code path is not yet functional.
- Postgres table DDL is the `CREATE_TABLE_SQL` string in `app.py` (`quote_submissions`). There is no migration tool.
- FastAPI docs are disabled (`docs_url`/`redoc_url`/`openapi_url` = `None`).

## Working in this repo

- The codebase is mid-refactor and littered with intentional `TODO`s and commented-out blocks (rate limits, lifespan, routers, Gmail, DB error handling). Before assuming a feature works, check whether its call is commented out. When completing a `TODO`, prefer moving inline `app.py` logic into the matching empty module (`schemas.py`, `config.py`, `routers/`) rather than adding more to `app.py`.
- After editing any `.ts` file, run `npm run build` — the app serves the compiled `dist/` output, not the TypeScript source.
- `docs/` contains deeper background: `architecture.md` (full flow + rationale for every legacy JS file), `development_journal.md`, and `site_content.md`. `todo.md` at the root tracks outstanding work.
