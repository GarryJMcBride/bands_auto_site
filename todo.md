    This file should be merged with Architecture and documentation
    There will be some things done that have not been covered in here as they were done along the way**
    Reference and capture.

# Master Development TODO (Structured)

---

## 1. General Architecture & Setup

### Project Organisation

* [ ] Add these todos into **WND (Web Notes/Docs)**
  → Turn this into a reusable **“Website Development Process Checklist”**

  - Use commit history from github to add todos for process
  - Use already predefined check list for Takmadoon

### Architecture

* [ ] Create diagram of architecture, including frontend and backend notes such as packages or libraries, JQUERY, and bootstrap

### FastAPI Integration

* [ ] Fix static file paths for FastAPI:

  * Replace all `../../` relative paths in HTML
  * Mount static directories correctly in `app.py`
  * Ensure CSS, JS, and images resolve properly when served via FastAPI
    → Reference: *“relative paths in fastapi” + your browser notes*

* [ ] Define a **standard development workflow**:

  * Decide how to run FastAPI during development (instead of VS Code Live Server)
  * Ensure frontend + backend work together consistently

### Python Tooling

* [x] Create a `main()` entry point for running Uvicorn
* [ ] Install and configure:

  * `ruff` (linting)
  * `pylance` (type checking / IntelliSense)

### Static Assets

* [ ] Move `/images` into FastAPI `static/` directory

  * Ensure it is tracked correctly (currently ignored / misplaced)
  * Fix any broken references after moving

---

### Add Error handling from the server to the frontend

[ ] Implement warnings on the frontend from the server for HTTPExceptions

## 2. Frontend Architecture (JavaScript / TypeScript)

### JavaScript & API Integration

* [ ] Implement JavaScript API call:

  * Send form data → FastAPI backend
  * Handle response (success/failure feedback)

### jQuery Evaluation

* [ ] Decide strategy for jQuery usage:

  * Option A: Keep jQuery for UI only (static behaviour)
  * Option B: Replace with modern JavaScript
* [ ] If keeping:

  * Separate **UI scripts (jQuery)** from **logic scripts (TS/JS API calls)**

---

## 3. TypeScript Setup & Build Pipeline

### Initial Setup

* [x] Install and configure TypeScript
* [ ] Define compilation workflow:

  * Run compiler separately OR integrate into dev server
  * Output compiled JS into correct folders

### Project Structure

* [ ] Organise scripts:

  * Move jQuery → dedicated `/jquery` folder
  * Use `/js` or `/dist` as TypeScript output target

### FastAPI Integration

* [ ] Configure Uvicorn/dev workflow to:

  * Automatically compile TypeScript when server starts (or via watcher)

### Vite / Bundler Understanding

* [ ] Investigate role of **Vite**:

  * How it handles bundling, imports, and dev server
  * Whether it replaces manual TypeScript compilation
* [ ] Summarise findings into `Development_journal.md`:

  * TS + bundler workflow
  * Whether HTML should directly reference scripts or bundled output
  * Strategy for handling legacy jQuery files
* [ ] Fix DOMPurify's non-bundled setup — currently manually copied from
  `node_modules/dompurify/dist/purify.es.mjs` to
  `static/js/vendor/dompurify/purify.es.mjs` and wired via an import map in
  `index.html`, because there's no bundler to resolve `node_modules` packages
  for the browser. Fragile (already broke once when the vendor file went
  missing and silently killed the whole form-handling module — see
  `Development_journal.md` → `## Email Sending pipeline`). A bundler would let
  `import DOMPurify from "dompurify"` just work off `npm install`.

---

## 4. TypeScript Paths & Imports

* [ ] Define import strategy:

  * Avoid deep relative paths (`../../../`)
  * Prefer `baseUrl` and aliases

* [ ] Update `tsconfig.json`:

  * `"baseUrl": "./src"`
  * Optional alias:

    ```json
    "paths": { "@/*": ["*"] }
    ```

* [ ] Refactor imports across project:

  * Use cleaner absolute or simplified relative paths

* [ ] Ensure build output works:

  * Compiled files resolve correctly in `/dist`
  * Compatible with FastAPI static serving

* [ ] Introduce bundler (if needed):

  * Handle alias resolution
  * Produce browser-ready assets
  * Would remove the manual DOMPurify vendoring workaround (see section 3)

* [ ] Validate full pipeline:

  * TypeScript → Build → FastAPI → Browser
  * Confirm no broken imports or missing files

---

## 5. HTML, CSS, UI & Styling

### Understanding Current Setup

* [ ] Learn how CSS is structured:

  * Variables
  * Theme system
  * Template overrides

* [ ] Investigate:

  * SCSS usage
  * Bootstrap integration
  * jQuery-driven UI behaviour
  * Animations (fades, transitions)

### Cleanup (Low Priority)

* [ ] Reduce CSS bloat:

  * Rename unclear class names to meaningful ones
  * Remove unused styles

* [ ] Remove template override system:

  * Delete:

    * `css/colours`
    * `cssvariables`
  * Simplify styling approach

* [ ] Remove all references to Linoor on html index.html as it uses different content for mobile responsiveness

---

## 6. Feature: Vehicle Info from Registration

### Goal

Allow users to submit only a registration number and automatically retrieve vehicle details.

### Tasks

* [ ] Build form:

  * Input: vehicle registration only
  * Keep UX minimal (per client request)

* [ ] Backend integration:

  * Call external API to fetch vehicle data
  * Process and validate response

* [ ] Email system:

  * Send collected data to client (Brian)
  * Include:

    * User details
    * Vehicle details

* [ ] Security considerations:

  * Protect API keys and backend endpoints
    * Wrap API calls in clients
    * Wrap API calls with certs, tokens or other
    * Uvicorn defaults to 127.0.0.1 (localhost)
    * Uvicorn defaults to 127.0.0.1 for security, but SSL requires a full https:// path because network requests
      * Add full paths to localhost (127.0.0.1) for internal apis 
      * Currently we just give uvicorn a port number and it knows where to look. SSL and security need full path
  * Ensure safe handling of vehicle data
    *(Note: Reg lookups are public, but API usage must still be secured)*

* [ ] Match email format:

  * Use template from:
    `Takmadoon/B&S Autos/Template from Book my Mechanic`

---

## 7. Feature: User Testimonials

### Basic Version (No Accounts)

* [ ] Create submission system:

  * Users submit reviews
  * Stored in database

* [ ] Admin moderation:

  * Accept or reject reviews before display

### External Integration विचार

* [ ] Investigate pulling reviews from external platforms:

  * Example: “Book My Garage”
  * Options:

    * API (preferred)
    * Scraping (fallback, less reliable)

---

## 8. Deployment (VPS & Multi-Site Setup)

### Architecture Decisions

* [ ] Decide structure:

  * Separate FastAPI app per site

* [ ] Static file handling:

  * Ensure sites don’t conflict when mounting `/static`
  * Confirm isolation between projects

### Infrastructure Questions

* [ ] Database strategy:

  * Shared vs separate databases per site

* [ ] Networking:

  * Multiple sites on port 443 (via reverse proxy like Nginx)
  * TLS termination, HSTS, and Content-Security-Policy headers — these belong at
    the reverse proxy/CDN layer (Nginx/Cloudflare), not in `app.py`. Not yet set
    up anywhere; needed before going live.

* [ ] Future scalability:

  * Create a **core FastAPI base setup**
  * Allow reuse across multiple client sites

### .bashrc file

* [ ] Add Alias and Short cuts into this bash file

---

## 9. Client-Side Validation (Frontend)

### Form Validation

* [ ] Add constraints:

  * Max lengths
  * Required fields

* [ ] Improve UX:

  * Show success/failure messages clearly
  * Prevent duplicate submissions
  * Harden the `?submitted=success|error` banner on `/` (no-JS fallback, `app.py`):
    currently a plain query param anyone can set without submitting anything —
    purely cosmetic today, but should move to a signed/session-based flash
    message if this ever needs to mean more than "show a message"

### Behaviour & Edge Cases

* [ ] Understand **AJAX** (async requests without reload)

* [ ] Decide fallback:

  * What happens if JavaScript is disabled?

* [ ] Data handling:

  * Clear form after submission
  * Avoid retaining sensitive data client-side

* [ ] Debug validation issues:

  * Investigate why form is inheriting validation rules unexpectedly
  * Review existing custom JS scripts

---

## 10. Security

* [ ] Add honeypot field or rate limiting on the form endpoint to stop spam
      - Add a honeypot field to the form schema (hidden field bots fill in, humans don't —
        reject silently if populated).
      - Add IP-based rate limiting on the submission endpoint (e.g. via `slowapi` or
        equivalent — check what's already in the project's dependencies first).
* [ ] Fix `slowapi`'s IP detection for production: `get_remote_address` (`app.py`)
      reads the direct peer IP. Once behind a reverse proxy/load balancer for TLS
      termination, every request will appear to come from the proxy's IP unless
      `X-Forwarded-For` is explicitly trusted — silently turning the per-IP rate
      limit into one shared global limit. Needs fixing once deployment topology
      (which reverse proxy, how many hops) is known.
* [ ] Rotate credentials in `.env` before going live — real DB password and Gmail
      app password currently in there are the ones used throughout local dev/
      debugging (some were even echoed into chat sessions while troubleshooting).
      Generate fresh ones for production.
* [ ] Try to Penetrate Site with Scripts and other methods
* [ ] Scan Browser console for any passwords or risky data exposure
* [ ] Check out OWASP or other security methods defined by industry professionals
* [ ] Use the following:
    * Tokens
    * Sessions
    * API keys
    * Certs for HTTP and HTTPS for APIs
    * FastAPI Lifespan

## 11. Tests
- Write an integration test that calls the email-sending function against the
  temporary SMTP config and asserts no exception is raised.
- Write unit tests for the Pydantic validation (reject injection attempts, reject
  honeypot-filled submissions, accept valid submissions).

## 12. Email Delivery — Move off temporary Gmail mailbox to a proper ESP

* [ ] Replace the temporary Gmail app-password mailbox (`SMTP_HOST=smtp.gmail.com`
  in `.env`, used only to prove the SMTP send pipeline works end-to-end) with a
  real Email Service Provider (e.g. Resend or Amazon SES).
  * By design this should only touch `.env` — `send_email()` in `app.py` is
    written provider-agnostic (see comment in `config.py`), so no code changes
    should be needed, only new `SMTP_HOST`/`SMTP_PORT`/`SMTP_USER`/`SMTP_PASS`
    (or an API-key based ESP client if not doing SMTP relay).
* [ ] Fix `FROM_ADDR` — must be an address the sending provider is actually
  authorised to send as (domain-verified), not an arbitrary personal address.
  Gmail's relay will reject/bounce/spam-filter mail otherwise.
* [ ] Set up domain verification (SPF / DKIM / DMARC) for whatever domain
  `FROM_ADDR` uses once on a real ESP — needed for reliable inbox delivery,
  not just "the send call didn't error."
* [ ] Decide final `BUSINESS_EMAIL` (currently pointed at the same temporary
  test mailbox) once ready to go live.
* [ ] An ESP is also more secure than a personal Gmail app password long-term —
  scoped API keys instead of a mailbox credential, provider-side deliverability/
  spam handling, and no dependency on one person's personal Google account.

