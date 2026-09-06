# Vehicle-Lookup Enrichment Plan (DVLA VES + DVSA MOT History)

Design doc for the feature described in `todo.md` → "## 6. Feature: Vehicle Info
from Registration". Not implemented yet — captured here so the design work
(including verified live API specs) isn't lost before work starts.

## Context

The quote form already collects and validates a UK vehicle registration
(`QuoteSubmission.registration` in `src/backend/schemas.py`). The goal is to
use that registration server-side to call two government APIs — DVLA's
Vehicle Enquiry Service (make/colour/fuel/tax/MOT status) and DVSA's MOT
History API (full MOT test history) — and append the results both to the row
saved in Postgres and to the notification email sent to the business, so the
mechanic sees vehicle details alongside the customer's request without
looking it up manually.

Verified live API specs (Sept 2026):
- **DVLA VES**: `POST https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles`, header `x-api-key`, body `{"registrationNumber": "AB12CDE"}`. 404 = not found, 429 = rate limited.
- **DVSA MOT History**: the old API-key-only version was deprecated Sept 1 2025. The current version needs OAuth2 client_credentials (Microsoft identity platform: `client_id`/`client_secret`/`scope`/tenant token URL) **plus** a separate `X-API-Key` header on every call; bearer token valid ~60 min. The exact single-vehicle lookup path wasn't confirmed from public docs (registration-gated) — the plan makes it a configurable env var so it can be corrected from `.env` alone once real developer-portal access confirms it, with no code change needed.

Both lookups are **best-effort enrichment**: if either API is down,
unconfigured, or returns an error, the quote submission must still save and
email successfully with that provider's data simply omitted.

## Approach

**Three new flat modules** (matching this repo's existing "one file per
external concern" convention, e.g. `mailer.py` — not a subpackage, since
there's one orchestrator with no sub-endpoints):
- `src/backend/dvla.py` — `async def lookup_vehicle(registration: str) -> dict | None`. Simple `x-api-key` POST via a per-call `httpx.AsyncClient`. Returns `None` (never raises) on missing API key, 404, any `httpx.HTTPError`, or unexpected exception.
- `src/backend/mot_history.py` — `async def lookup_vehicle(registration: str) -> dict | None`. Handles the OAuth2 client_credentials dance with an in-memory cached bearer token (module-level `_cached_token`/`_token_expires_at`/`asyncio.Lock`, refetched only when near expiry — not on every request), then GETs the vehicle with `Authorization: Bearer ...` + `X-API-Key`. Same never-raises contract as `dvla.py`. Lookup path built from an env-configurable template so the unconfirmed path can be fixed via `.env` alone.
- `src/backend/vehicle_lookup.py` — `async def gather_vehicle_details(registration: str) -> dict`, the only one of the three the router imports. Runs both providers concurrently via `asyncio.gather(..., return_exceptions=True)` and always returns `{"dvla": dict | None, "mot_history": dict | None}`, never raising, never `None` — this is the seam that keeps the router ignorant of DVLA/DVSA specifics, mirroring how it already treats `mailer.send_email` as a black box.

Kept as two separate keys (not merged into one flat dict) because each
provider can independently succeed/fail/be unconfigured, and their response
shapes don't overlap — flattening would obscure provenance and risk key
collisions given DVSA's shape isn't even fully confirmed yet.

**`config.py`** — new `os.getenv(...)` block per provider, following the
existing `SMTP_*` pattern exactly (plain module-level assignments under a
comment banner): `DVLA_VES_API_KEY`, `DVLA_VES_BASE_URL` (defaulted),
`DVLA_VES_TIMEOUT_SECONDS`; `DVSA_MOT_CLIENT_ID`, `DVSA_MOT_CLIENT_SECRET`,
`DVSA_MOT_API_KEY`, `DVSA_MOT_SCOPE_URL` (defaulted), `DVSA_MOT_TOKEN_URL`,
`DVSA_MOT_API_BASE_URL` (defaulted), `DVSA_MOT_LOOKUP_PATH_TEMPLATE`
(defaulted, e.g. `/registration/{registration}`), `DVSA_MOT_TIMEOUT_SECONDS`.
Absence of the relevant API key is each module's own "not configured, skip"
signal — no separate feature flag needed. No `.env.example` exists in this
repo today; not adding one as part of this change.

**Database** — `CREATE_TABLE_SQL` (`schemas.py`) gets a new nullable
`vehicle_details JSONB` column. Since `Database.ensure_schema()` currently
only runs `CREATE TABLE IF NOT EXISTS` (which never alters an existing
table) and this repo has no migration tool, add a
`schemas.MIGRATIONS_SQL = ["ALTER TABLE quote_submissions ADD COLUMN IF NOT EXISTS vehicle_details JSONB;"]`
list, change `Database.ensure_schema` (`classes.py`) to accept
`str | list[str]` and loop over statements, and update the one call site in
`app.py`'s `lifespan()` to
`await db.ensure_schema([schemas.CREATE_TABLE_SQL, *schemas.MIGRATIONS_SQL])`.
This is the smallest change that makes the column reach both fresh and
already-deployed databases with no manual step.

**Wiring it through the request flow** (`routers/handle_form_inputs.py`) —
in both `submit_quote_javascript_pipeline` and `submit_quote_python_pipeline`,
immediately after `QuoteSubmission` is built/validated:
```python
vehicle_details = await gather_vehicle_details(payload.registration)
submission_id = await update_database(payload, vehicle_details)
...
await send_email(payload, submission_id, vehicle_details)
```
`save_submission`/`update_database` gain a `vehicle_details: dict` parameter,
stored via `json.dumps(...)` into the new `$N::jsonb` INSERT param. No new
try/except needed around the lookup — `gather_vehicle_details` is
contractually non-raising. `QuoteSubmission` itself is **not** changed
(vehicle_details is server-fetched enrichment, not user input), so no
`Form(...)` field or client-side change is needed.

**Email** (`mailer.py`) — `build_email_body`/`build_email_html`/`send_email`
each gain an optional `vehicle_details: dict | None = None` parameter. A
shared private helper `_vehicle_detail_rows(vehicle_details) -> list[tuple[str, str]]`
extracts a curated, display-ready set of fields (DVLA: Make, Colour, Fuel
Type, Year, MOT Status, MOT Expiry, Tax Status, Tax Due Date; MOT History:
Model, Manufacture Date, Latest MOT Result/Expiry/Mileage from `motTests[0]`)
so the plain-text and HTML parts can't drift apart, matching the existing
pattern (the `rows` tuple list) already used for the customer fields.
Renders nothing when both providers came back empty. HTML values pass
through `html.escape(str(value))` for defense in depth, consistent with the
rest of the template.

**Testing** — use `unittest.mock.AsyncMock` to patch `httpx.AsyncClient`
calls rather than adding a new mocking dependency (e.g. `respx`), keeping
this repo's dependency footprint minimal per its existing conventions. New
test files: `test_dvla.py`, `test_mot_history.py` (including
token-cache-hit and expiry-refetch assertions), `test_vehicle_lookup.py`
(asserts the never-raises, always-both-keys contract), and an extension to
`mailer`/router tests confirming a submission still succeeds end-to-end when
both providers return `None`.

## Critical files
- `src/backend/config.py` — add the two new env-var blocks.
- `src/backend/dvla.py`, `src/backend/mot_history.py`, `src/backend/vehicle_lookup.py` — new.
- `src/backend/schemas.py` — `CREATE_TABLE_SQL` column + new `MIGRATIONS_SQL`.
- `src/backend/classes.py` — `Database.ensure_schema` accepts `str | list[str]`.
- `src/backend/app.py` — `lifespan()` call site update.
- `src/backend/mailer.py` — `_vehicle_detail_rows` + threaded `vehicle_details` param on all three functions.
- `src/backend/routers/handle_form_inputs.py` — `gather_vehicle_details` call + threaded param on `save_submission`/`update_database` and both endpoints.

## Documentation to update once implemented
`CLAUDE.md` (Backend layout + Configuration & state), `docs/architecture.md`
(flow + module table), `docs/pipeline-architecture-visual-diagram.md` (one
line under email), `todo.md` (check off the relevant "## 6" sub-tasks, note
the unconfirmed DVSA path).

## Verification (once implemented)
1. `uv run python -c "from src.backend import app"` — confirms nothing broke on import after all the signature changes.
2. Run the new unit tests (`uv run pytest src/backend/tests/test_dvla.py src/backend/tests/test_mot_history.py src/backend/tests/test_vehicle_lookup.py -v`) with both providers mocked at the `httpx` layer — cover success, 404, timeout, and not-configured cases for each.
3. With a clean `.env` (no new vars set at all): submit the form and confirm it still succeeds — 201/redirect-success, DB row has `vehicle_details = {"dvla": null, "mot_history": null}`, email sends with no "Vehicle Details" section.
4. Restart the app against a Postgres DB created *before* this change, to confirm the new `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` migration step runs cleanly with no manual intervention.
5. Once real DVLA/DVSA credentials exist: set `DVLA_VES_API_KEY` only first, confirm DVLA populates and DVSA is cleanly skipped; then add DVSA credentials, re-confirm the actual lookup path from the DVSA developer portal and correct the `DVSA_MOT_*` env vars if needed, and confirm both providers populate in the DB row and the email.
