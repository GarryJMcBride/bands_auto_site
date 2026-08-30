# Development Journal

TODO: Add links to URLS for tools and resources

## Mounting Folders and Understanding Paths - FASTAPI Server

When you write:
```bash
# pythonStaticFiles(directory="src/frontend/static")
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
```
You're just telling FastAPI: "when someone requests a static file, go look for it in this folder." That's it. The files live in your repo, on your disk, in that folder. FastAPI just reads them from there and sends them to the browser when requested.

So when a browser requests http://localhost:8000/static/style.css, FastAPI:

- Goes to src/frontend/static/ on your disk
- Finds style.css
- Sends it to the browser

The file never moves. FastAPI just knows where to look.

The mounting is about URLs, not file paths. Without mounting, there's no way for a browser to request a file. A browser doesn't have access to your disk — it can only make HTTP requests like `GET /something`.

Mounting creates that bridge:
|Browser requests:          FastAPI looks on disk at:
/static/style.css    >     src/frontend/static/style.css

Without the mount, `/static/style.css` would just return a 404 — FastAPI has no idea what to do with that URL.

The browser speaks URLs, your disk speaks file paths. They're two completely different address systems. Mounting is just you defining the translation between them:

Absolute/relative paths are for your Python code to find files on disk. They're useless to a browser sitting on someone else's computer, which has no knowledge of your server's file system at all.

| File on disk                        | URL in browser          |
| ----------------------------------- | ----------------------- |
| `src/frontend/static/js/app.js`     | `thisSite/static/js/app.js`     |
| `src/frontend/static/css/style.css` | `thisSite/static/css/style.css` |

## Previous trial with PHP/PHPMailer vs Modern Day web development

**PHP (PHPMailer) Flow**

* Form > PHP script > SMTP (email sent immediately)
* No DB by default
* Tight coupling (form = email trigger)
* Vulnerable to spam if unprotected
* Manual HTML email formatting (client inconsistencies)
* Older way of doing web development

**Modern (Python / Node.js + APIs)**

* Form > Backend > DB > Email API (Gmail / Outlook)
* Decoupled (store first, send later)
* APIs handle delivery + better formatting consistency
* Easier validation, logging, retries, scaling

## Laying a Static website template from Envato onto a FASTAPI Framework
Utilising a static web template from `envato` marketplace are sometimes packaged by the developers in different ways. Links between files are sometimes different, have not seen one using a Backend framework yet, or frontend framework. Currently most site templates I have come across have used static `HTML, CSS and JS` files with relative paths to find eachother in the packaged REPO they exist in.

```bash
# Example of Paths before template edited

# HTML finds JavaScript
<script src="../js/jquery.js"></script>

# HTML finds CSS Style sheets
<link href="../css/bootstrap.min.css" rel="stylesheet">

# HTML finds HTML
<li class="dropdown"><a href="index-main.html">Home</a>

# HTML finds Images
<img src="../images/update-26-02-2021/resources/feature-3-1.jpg" alt="">

# CSS finds Images
background-image: url(../images/background/home-portfolio-bg-1-1.png);

# CSS Finds local font files
src: url("../fonts/fa-brands-400.eot");
 
```

TODO: revamp this content below to highlight how using FASTAPI Endpoints changes the use of relative paths and requires mounting of static files. Everything on the web is a request, but Python has been chosen to serve the frontend to the DOM, or browser sever. Relative links are now risky as the endpoints can change the paths behind the screens, best to use absolute paths for files that will be pushed or made static by FASTAPI. *See chatGPT `relative paths in fastapi` and `understanding the browser 1 and 2`

###########################################
###########################################
###########################################
###########################################
###########################################

Content to fix:

## Changing Requests to the Browser due to FastAPI use

### Synopsis

Linoor template that was used as a boilerplate for this project is a static HTML, CSS and JavaScript website. The decision to use `FastAPI` for the backend has led to changes all over the REPO. One of the most vital one is the handling of Requests.

### Body

In the HMTL pages `<a href="thisPage.html">thisPage</a>` is a `GET /` reqeust to the browser from HTML. This common practice for static websites as its a simple request to the Browser for `thisPage.html`.

With the implementation/use of `FastAPI`, the requests are now handled by the Python Framework, and now we use `<a href="/thisPage">thisPage</a>` which is a call to the `FastAPI` Endpoint. 

```bash
# TODO: Change this code snipped to reflect actual page names from B&S Autos Site
# HTML
<a href="/thisPage">thisPage</a>

# Python - FastAPI
@app.get("/thisPage")
def homepage_endpoint():
    return templates.TemplateResponse("homepage.html", {"request": request})
    return HTMLResponse(login_html)
```

<br>

Why do static sites always default to the first page being index.html? Can we choose any?
- With FastAPI and other frameworks, the developer explicitly decide what page the user sees first, and FastAPI returns that to the browser when it hits your site. When someone goes to your site, the browser automatically requests `GET /`, which is now served by FastAPI.
- "/" is the “entry point”, index.html is NOT required to be the first page. The “first page” is whatever route handles. That / route is your “index”, even if no index.html exists. In FastAPI, "/" replaces index.html conceptually, but it’s just a route, not a file.
- `<a href="about.html">` is still a request. The browser sends a GET request for that file; the only difference is whether the server serves a static file or passes the request to something like FastAPI.
- Every page no matter where its accessed from is a REQUEST to the brower. The Browser always needs a request, you just define what type of request.

<br>

What will happen if I do a FastAPI call for the "/" page which will be "index.html" but I leave the navbar links as `<a href="about.html">`
- It will likely break (404 error) unless you explicitly serve that file and return 404 as the FastAPI expects to be the main method serving requests for pages.

### Summary

1. User types domain
2. Browser requests "/"
3. FastAPI checks: "Do I have a route for /?"
4. Your code runs
5. Response sent back (HTML / redirect / JSON)
6. Browser renders it

###########################################
###########################################
###########################################
###########################################
###########################################

## Decide on Languages
### Type Safety
#### Python
- Type annotations for Python to compile at Run time to help with Data and Robust code
#### JavaScript
- TypeScript used for type safety for JavaScript backend logic.
- `.ts` files compile to `.js` at runtime, collected in a file that holds all links to `.js` files.
#### JavaScript (QJuery)
JQuery already in static website template file from Envato for UI Behaviour. This is JavaScript, but only for behaviour, transitons and movements of UI elements. 

Plan to use JavaScript for some backend communcating logic, which will be compiled from TypeScript. Will leave `JQuery` files to stay static and seperate from logic JavaScript files to seperate the UI from the partial backend architecture.

> Wanted to clarify this as same langauge used in different aspects of application

## Code Presentation
### SCSS
- Use `SASS` to structure, format and tidy `CSS` code. SASS compiles `.scss` files to `.css`.
- `.scss` files allow nesting, variables and modular files imported, keeps `.css` from bloating up REPO.

### Folder Structure
TODO: Add Folder Structure

## User Interface Interaction/Behaviour
- `JQuery` used for UI Behaviour
    - Should be seperated from `JavaScript` for backend functionality calls to python or other settings

## Set up Developer Environment in IDE

- Install `git` and create REPO connection with remote on `github`
- Have `README.md`
- Install `python` on local OS
- Install `node.js` on local OS
- Create `python` virtual environment
- Pip Install `uv` for Python Package Dependencies
- Initiate `uv` and see created `pyproject.toml` and `uv.lock`
- Initiate `package.json` or install `npm` packages that already exist
    - If frontend web template `package.json` may include packages
    - If not then JavaScipt/JQuery will be static
- Create `docs` folder for Code and Development Documentation
- Install and configure TypeScript 

## Deciding on a Backend Framework

Options for backend frameworks are vast and broad. First the correct language needs to be chosen, and then a framework can be defined. Using `JavaScript` frameworks for the backend would make sense as the front end is written in `JS`. Python vs JavaScript for the back end can be experimental, and sites can be build with both and they can be weighed/compared. 

For now we use Python in the backend and `FastAPI` as a starting point. FastAPI is good for light UI web project and heavy API calls to the Backend. If advanving. It covers other aspects like security, user validation amongst others. Python also works good with most Databases. FastAPI can be used for a simple website with forms. While it is primarily marketed as an API framework, it includes built-in tools to serve HTML pages and process standard form data.

- Use FastAPI if: You plan to eventually add complex features like WebSockets, want automatic data validation (via Pydantic), or want to use the same backend for a mobile app later.

- Use Flask if: You want the simplest possible setup for a "classic" website. Flask has more "website-specific" extensions (like Flask-Login or Flask-WTF) that handle things like user sessions and form security out of the box.

If wanting to experiment, consider using more heavier advanced frameworks if needed like `Django` or `Flask`.

**Why Use a Framework (FastAPI)**

* Handles HTTP requests properly
* Routing (`/submit`, `/home`)
* Validation (Pydantic)
* Security + structure
* Avoids manual request parsing (scripts = messy/unscalable)

**Serving HTML (index.html vs FastAPI)**

* Static hosting: `index.html` auto-served first
* With FastAPI:
  * FastAPI decides routes (`GET /`)
  * Can serve `index.html` or templates
* Browser still renders HTML/JS
* FastAPI = backend controller, not DOM

## Implementing a Frontend Framework

TODO: TBD

## Installing and configuring a Database

## Security

*See = sorceror\Self-Development\Research and Findings\Application Development\How to secure a Web App from simple attacks and keep it secure.md

-------------
Keep it simple and layered:
1. **Input validation & sanitization** – Only allow expected data types, lengths, and characters.
2. **Escape outputs** – Prevent XSS/HTML injection by escaping user content before rendering.
4. **Parameterized queries** – For databases, avoid SQL injection.
5. **Use roles & least privilege** – Don’t run scripts with admin rights; isolate services.
6. **WAF / server rules** – Block common attack patterns and unwanted characters.
7. **Protect All endpoints from potential abuse** - You don’t need full login/auth if the form is public, but don’t leave it wide open to bots.
In short: **never trust user input**, validate, sanitize, and isolate.

TODO: Browser Console - Explore browser console and check you are not leaving any breadcrumbs or access for hackers via data or ways in

### Data Validation - client-side (frontend) and server-side (backend)

Why Doing Both is Robust
Better UX + Security: Frontend validation improves usability; backend validation ensures security and integrity.
Redundant checks catch more mistakes: Even if the frontend misses a subtle issue, the backend will catch it.
Easier debugging and logging: Backend validation can log suspicious or malformed requests, useful for detecting attack patterns.

**Embrace the repeated logic — it's intentional and each layer has a distinct purpose.**
- Frontend validation — "Is this what we expected?" — guides the honest user to submit correct data with instant friendly feedback
- Backend validation — "Can we trust this?" — treats everything as hostile regardless of where it came from

**What good frontend validation buys you in practice**
- User types abc in the phone field > JS catches it instantly, no server request made
- User forgets to select a service > JS highlights it before they even click submit
- User pastes something with <script> tags > stripped before it goes anywhere
- Reduces noise on your FastAPI logs from malformed but innocent requests

Think of it like airport security — the ticket check at the entrance (frontend) stops normal errors quickly, but the metal detector and baggage scan (backend) catch anything that slips through or comes with malicious intent.

**Frontend validation is a courtesy, not a shield.**
- For genuine users it's invaluable — instant feedback and friendly error messages guide honest people to submit correct data without frustration.
- For a hacker it's invisible. They send raw HTTP requests directly to your API, bypassing the browser entirely. Your JavaScript never even runs.
- Both layers are essential — they just solve different problems for completely different audiences.

**Delete Data from frontend once purpose served**
After receiving a successful response from your backend, explicitly reset the form with form.reset() and clear any variables holding the submitted values from memory. Never assume the browser handles this for you. The data has served its purpose the moment FastAPI receives it — clear it immediately and treat lingering form data as a liability.

#### Data Validation and Security - Relationship Between the Frontend and Backend: TODO: Should help out with SOWAW task for understanding the browser

**The Backend does not, and should not trust the Frontend, Security lives in FastAPI, not the browser.**

- How do hackers or anyone web dev see your api endpoints in the server?

Frontend (JS, fetch, forms) is just a convenience layer. the backend is publicly reachable if it’s on the internet. 
- Looking at Network tab in browser dev tools (while JS is ON once)
- Viewing your frontend source code
- Guessing common routes (`/api/login`, `/submit`, `/users`)
- Using tools like:
    - curl
    - Postman
    - Burp Suite
- Crawling/scanning your site automatically

Turning off JavaScript doesn’t protect you. API must assume anyone can hit it directly.

In DevTools:
- Network tab > shows every request (URLs, payloads, headers)
- Console > shows JS logs (not as useful for endpoints)
- Sources > your JS code (can reveal endpoints)

- How can someone send malicious requests?

Because HTTP is open. Instead of your frontend `fetch("/api/contact"` and sending JSON, an attacher could `curl` inside using `https://yoursite.com/api/contact` and push JSON data or other data that has a command like run a script or `"Content-Type: application/json"`. Thousands of these could be sent at one time, this is why we should use a rate limiter in Python.

They’re not using your UI. They’re talking directly to FastAPI. Hackers do not waste time wiuth UIs.

#### Data Validation and Security - Python
#### Data Validation and Security - JavaScript

**Does the frontend's architecture affect backend security? No.** `/api/quote-javascript-pipeline` is a public endpoint — it can't tell whether a request came from `transferFormInput.ts`, curl, or Postman, so nothing about the frontend's structure, framework, or even its presence changes what `QuoteSubmission`'s validators, `sanitise()`/`contains_injection()`, or the `slowapi` rate limiter do. They run identically on every request regardless of origin.

**Does the form work with JS disabled?** It didn't, until now. `#quote-form` had no `action`/`method`, so with the JS listener gone the browser fell back to its default native submission — a `GET /` with every field appended as a query string, which FastAPI's `/` route just ignores. Nothing reached the database or the email step; a no-JS user could not submit the form at all (annoying, but not a security hole — see above).

**Fix — progressive enhancement (`app.py` + `index.html`):**
- `#quote-form` now has `action="/quote-python-pipeline" method="post"`, a real fallback target for a native browser POST.
- New `POST /quote-python-pipeline` endpoint accepts the fields as `Form(...)` (needs the `python-multipart` package — added via `uv add python-multipart`), builds the same `QuoteSubmission`, and reuses `update_database()`/`send_email()` unchanged. Since a plain HTML form expects a page back, not JSON, it redirects (`303`) to `/?submitted=success#booknow` or `/?submitted=error#booknow` instead of returning a JSON body.
- `read_homepage()` reads that `?submitted=` query param and passes it to the template, which shows a plain `<p class="form-success-message">`/`<p class="form-error-message">` banner above the form (same unstyled-for-now convention as the JS's existing per-field `.form-error-message` spans).
- `/api/quote-javascript-pipeline` (JSON, used by `transferFormInput.ts` when JS runs) is untouched — `/quote-python-pipeline` is a separate, parallel path for the no-JS case only.

**How would a malicious user actually attack this?** Exactly as guessed: skip the page and the JS entirely and POST straight at the endpoint —
```bash
curl -X POST http://localhost:8000/api/quote-javascript-pipeline \
  -H "Content-Type: application/json" \
  -d '{"username":"...","email":"...","phone":"...","registration":"...","service":"Tyres"}'
```
This already works today and always will, for any public endpoint — it's not something the frontend can prevent. It's exactly why backend validation exists independently of whatever the JS already checked.


## Deployment on VPS

See `Finding a VPS` and `Modern Hosting Options` on ChatGPT

## Server Gateway (Uvicorn)

FastAPI is an ASGI (Asynchronous Server Gateway Interface) framework. Unlike older Python web frameworks (like Flask) which are WSGI, FastAPI is built around Python's async/await and needs a server that can handle asynchronous connections. Uvicorn is that server.

It's a lightning-fast ASGI server that acts as the bridge between incoming HTTP requests and your FastAPI app. Without it, your FastAPI app has no way to actually listen on a port and serve traffic. Uvicorn handles TCP/HTTP — FastAPI handles routing.

- Flask needs a WSGI server (like Gunicorn or Waitress).
- FastAPI needs an ASGI server (like Uvicorn or Hypercorn).

**Why Uvicorn**

* ASGI server > runs FastAPI
* Async support (non-blocking tasks)
* Production-ready, fast

**Workers:**

* Small app: `1` worker fine
* Scale: ~`(CPU cores × 2) + 1`

## Testing Functionality on Testing Envrionment (T-800/T-X)

## Installing TypeScript

Install TypeScript

```bash
npm init -y          # skip if you already have a package.json
npm install --save-dev typescript
npx tsc --init       # generates tsconfig.json
```

Notes:
- Once installed, an autogenerated `tsconfig.json` file will be created in the root folder
- Configurations need set inside `tsconfig.json`: https://www.typescriptlang.org/tsconfig/
    - Covered notes in `Some Scripts worth notes` going further into detail regarding what configurations were made
    - Important for clarity... sets environment to call JQUERY commands inside typescript files
- `Typescript` has to compiled to JavaScript, Need to keep logic JavaScript serated
    - Can manually compile before push to live instance
    - Can compile at runtime with bundler so manual intervention is not needed
- Need to mount JavaScript files (compiled) from TypeScript so that FASTAPI can serve them to the browser
    - Done in `app.py`
    - Kept seperate from `static` folder which contains `HTML, CSS and JQUERY`
    - Wanted to use another folder to keep compiled code seperate
    - Appears in a `/dist` folder



## Sanatizing and Validating Data

Data is sanitized on the frontend and backend. Backend Uses Pydantic from Python, and functions to check for patterns, characters and sets limited on character amount of expected input of data in form.

Frontend end does the same, this can be turned off by the browser, server santiitizing and validating is most important on server. I'm doing both just for that added layer of security. If JavaScript turned off, the server still validates data.

**Frontend sanitization uses DOMPurify** (`transferFormInput.ts`) — strips all HTML tags/attributes from each field (`ALLOWED_TAGS: []`) before the regex validators run, so `<script>` etc. never even reaches validation. This is separate from and unaware of the backend's own sanitisation (`sanitise()` / `contains_injection()` in `app.py`, which does `html.escape` + strips tags + checks injection patterns) — each layer is independent, per the "backend doesn't trust the frontend" rule above. See `## Email Sending pipeline` for the DOMPurify vendoring workaround (no bundler, so it isn't a plain `npm install` away in the browser).



## Claude Boilerplate for JavaScipt(TS) and Python

### Configuration with Database

**`DATABASE_URL`**
The connection string to your PostgreSQL database. Contains the username, password, host, and database name. Sensitive because it's the key to all your stored data.

### GMAIL API

#### Environment Variables

**`SERVICE_ACCOUNT`**
The path to your Google service account JSON file. This is how your app authenticates with the Gmail API without using a password — Google issues a credential file instead.

**`GMAIL_SCOPES`**
Tells the Gmail API exactly what permissions your app needs — in this case only the ability to send email, nothing else. Google uses scopes to limit what an authenticated app can actually do.

**`DELEGATED_EMAIL`**
The Gmail address the service account sends email as. Service accounts don't have their own Gmail inbox — they need to impersonate a real Google account to send mail. Without this the Gmail API call will fail.

### Endpoint Exposure

**`ALLOWED_ORIGINS`**
The domains allowed to talk to your API. Which brings us to —

### What is CORS?

CORS stands for **Cross Origin Resource Sharing**. It's a browser security rule that blocks a website from making requests to a different domain unless that domain explicitly says it's allowed.

For example without CORS configured:
- `https://yourdomain.com` tries to call `https://yourapi.com/api/quote`
- The browser blocks it because the domains differ

`ALLOWED_ORIGINS` tells FastAPI which domains are permitted to call your API. Anyone not on that list gets blocked at the browser level.

## Installing and Setting up POSTGRES

### 1. Install PostgreSQL

Download the installer from:
```
https://www.postgresql.org/download/windows/
```
Run it and note down:
- The **password** you set for the `postgres` superuser
- The **port** (default `5432`)

---

### 2. Add PostgreSQL to your PATH

During installation check **"Add to PATH"** or add it manually:
```
C:\Program Files\PostgreSQL\16\bin
```

---

### 3. Connect to PostgreSQL

Open a terminal:
```bash
psql -U postgres
```
Enter your password when prompted.

---

### 4. Create your database and user

```sql
CREATE DATABASE bands_auto;
CREATE USER bands_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE bands_auto TO bands_user;
\c bands_auto
GRANT ALL ON SCHEMA public TO bands_user;
```

---

### 5. Create your submissions table

```sql
CREATE TABLE quote_submissions (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username     VARCHAR(64)  NOT NULL,
    email        VARCHAR(254) NOT NULL,
    phone        VARCHAR(20)  NOT NULL,
    registration VARCHAR(7)   NOT NULL,
    service      VARCHAR(50)  NOT NULL,
    submitted_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
```

---

### 6. Update your `.env`

```env
DATABASE_URL="postgresql://bands_user:yourpassword@localhost:5432/bands_auto"
```

---

### 7. Test the connection in Python

```bash
pip install asyncpg
```

```python
import asyncio
import asyncpg
import os


async def test():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    print("Connected successfully")
    await conn.close()


asyncio.run(test())
```

## Installing ClaudeCode Native Installer to Windows OS

**Claude Code – Windows Install Guide**

### 1. **Install Git for Windows** (recommended, not required): https://git-scm.com/downloads/win — defaults are fine.

### 2. **Open PowerShell** (not CMD) and run:
```powershell
irm https://claude.ai/install.ps1 | iex
```

### 3. **Add it to PATH** (the installer sometimes doesn't do this automatically):
```powershell
[Environment]::SetEnvironmentVariable("Path", "$env:Path;$env:USERPROFILE\.local\bin", "User")
```
Close and reopen PowerShell.

### 4. **Verify:**
```powershell
claude --version
```

### 5. **Authenticate:** run `claude` in any folder, follow the OAuth prompt (Claude Pro/Max/Team account or API key).

### 6. **If using Git Bash too**, make sure `~/.bashrc` exists and includes:
```bash
export PATH="$PATH:/c/Users/<yourname>/.local/bin"
```
Then `source ~/.bashrc` or open a new window.

### 7. **Keep config out of repos:** store project instructions in `~/.claude/CLAUDE.md` (global) rather than a per-repo `.claude/CLAUDE.md`, or add `.claude/` to `.gitignore` if you do want repo-level config.

That's the whole path — no npm/npx needed, since the native installer is self-contained.

## Email Sending pipeline

See Claude conversation regarding using advanced GMAIL logic that is more suited for a pool of 500 email users... rather than a simple SMPT email send as its just brian alone in the the business.

The important work is done with honeypots, Rate limiting, validation, sanitization, cleaning etc. The GMAIL API is advanced but is more suited for a larger scale orgaziation.

- Decide and change architecture.
- Capture the simple architecture and note what GMAIL API could be used for in the future
    - GMAIL api comes with alot of "meta" security layers like tokens etc.
    - This is overkill for a simple send email to personal email address

### Pipeline (as built)

1. **HTML** — `#quote-form` (`index.html`, `novalidate`) holds the raw fields: `username`, `email`, `phone`, `registration`, `service`.
2. **JS** (`transferFormInput.ts` → compiled `dist/transferFormInput.js`) — `submit` listener does `preventDefault()`, sanitises each field with DOMPurify, validates format/required-ness client-side (convenience only), then `fetch("/api/quote-javascript-pipeline", {method: "POST", body: JSON})`.
3. **Python** (`app.py`, `POST /api/quote-javascript-pipeline`) — FastAPI parses the body into `QuoteSubmission` (Pydantic), which independently re-sanitises/re-validates every field (this is the real gate, not the JS). `submit_quote_javascript_pipeline()` then:
   - `save_submission()` — parameterized `INSERT` into `quote_submissions` via the `asyncpg` pool.
   - `send_email()` — builds a plaintext message (`build_email_body`) and sends it with `aiosmtplib`, creds from `config.py`/`.env` (`SMTP_HOST/PORT/USER/PASS`, `FROM_ADDR`, `BUSINESS_EMAIL`).
   - Returns `201` + `submission_id` only if both the DB write and the email send succeed; either failing raises a `500` (DB write happens first, so a failed send doesn't lose the saved lead).
4. **Database** — single `quote_submissions` table. DDL (`CREATE_TABLE_SQL`) now runs automatically in `lifespan()` on app startup (previously wasn't wired up anywhere, so the table didn't exist).

### DOMPurify vendoring workaround (no bundler)

This project has no bundler (webpack/esbuild/vite) — `npm run build` is plain `tsc`, which only compiles `.ts` → `.js`. It does **not** resolve/inline `node_modules` packages for the browser. So `import DOMPurify from "dompurify"` in `transferFormInput.ts` can't just work off `npm install` like it would in a bundled app — the browser has no way to reach into `node_modules`.

Fix: treat DOMPurify like the rest of this repo's third-party JS (jQuery, Owl Carousel, etc. under `static/js/`) — vendor it as a committed static file rather than building it:
- Copied `node_modules/dompurify/dist/purify.es.mjs` → `src/frontend/static/js/vendor/dompurify/purify.es.mjs` (served via the existing `/static` mount). Unmodified file, straight from the official `dompurify` npm package (`^3.3.3`, already in `package.json`) — `npm install` had already put it in `node_modules`, just copied as-is.
- `index.html` has an import map pointing the bare specifier at that file:
  ```html
  <script type="importmap">
  { "imports": { "dompurify": "static/js/vendor/dompurify/purify.es.mjs" } }
  </script>
  <script type="module" src="dist/transferFormInput.js"></script>
  ```
- Gotcha: this vendor file had gone missing, which broke `import DOMPurify` — and a failed top-level import silently kills the *entire* ES module, so the `submit` listener never attached and the form fell back to a native browser GET-with-querystring submission (no error shown to the user, nothing reaching FastAPI at all). Worth remembering if the form ever "does nothing" again — check the console for a module/import error first.

### Second DOMPurify gotcha: `.mjs` served with the wrong MIME type

Fixing the missing vendor file above wasn't the whole story — even with the file present, the browser refused to run it, and *every* form submission in testing was silently hitting the no-JS `/quote-python-pipeline` fallback instead of the JS `fetch` path, for a completely different reason.

**Why MIME types matter for JS/modules at all:** every HTTP response includes a `Content-Type` header (e.g. `text/css`, `image/png`, `application/javascript`) telling the browser what kind of content it just downloaded, so it knows how to handle it. A `<script>` tag doesn't care much about the exact value as long as it's *some* JS-flavoured type — but `<script type="module">` (and `import`/`import()`) is stricter: the spec requires the response to be one of a specific allow-list of JavaScript MIME types, or the module load is rejected outright, with no code ever running. `text/plain`, `application/octet-stream`, etc. are not on that list.

**Where DOMPurify comes in:** `purify.es.mjs` is fetched as a *module* (via the import map — see above), not a plain `<script src>`. FastAPI's `StaticFiles` mount doesn't hardcode a `Content-Type` per file — it asks Python's built-in `mimetypes` module to guess one from the file extension. `mimetypes` reads from the OS's own MIME registry (on Windows, effectively the registry; on Linux, files like `/etc/mime.types`), and `.mjs` — being a newer, less universal extension than plain `.js` — isn't always registered there. On this machine it wasn't, so `mimetypes` fell back to `text/plain`.

**Why it failed *silently*:** `SecurityHeadersMiddleware` (`app.py`) already adds `X-Content-Type-Options: nosniff` to every response — a deliberate security header that tells the browser "trust the Content-Type I gave you, don't try to guess a better one from the file's actual bytes." That's the header doing exactly its job; it just collided with `mimetypes` guessing wrong. The combination (wrong type + nosniff) makes the browser reject the module fetch with no console error and no network-level failure visible in a normal check — `curl` and the Network tab both showed a clean `200`, which is why this took real browser testing (via `claude-in-chrome`, dynamically `import()`-ing the file directly) to actually surface, rather than curl/status-code checks alone.

**Fix** (`app.py`): register the MIME type explicitly, once, at startup, so it doesn't depend on the host OS's registry at all:
```python
import mimetypes
mimetypes.add_type("text/javascript", ".mjs")
```
Placed before the `/static` mount. This means the exact same code behaves identically on Windows, Linux, in CI, wherever — no dependency on what that machine's `mimetypes` happens to already know.

**Real-world proof the no-JS fallback earns its keep:** by the time this MIME bug was discovered, several genuine test submissions (username "Garry") had already landed correctly in `quote_submissions` — sent *before* the bug above was even found or fixed. That's not a contradiction: the `POST /quote-python-pipeline` fallback and the form's `action="/quote-python-pipeline" method="post"` were already wired up by then. So the actual sequence was: click submit → the browser tries to run `transferFormInput.js` → it fails silently (this exact MIME bug, undiscovered at the time) → `preventDefault()` never runs → the browser falls through to its native form submission → which now had a real, working target instead of nowhere. The data never touched DOMPurify or `fetch` — it went in as plain form-urlencoded fields, validated and saved entirely server-side. Good demonstration of why the fallback is worth having as a genuinely independent path: the "enhanced" JS layer was silently dead the whole time, and the fallback caught it without anyone noticing until later.

### Still using a temporary mailbox, not a real ESP

Email currently goes out over `smtp.gmail.com` using a personal Gmail account + app password (`SMTP_USER`/`SMTP_PASS` in `.env`) — this only exists to prove the send pipeline works end-to-end, it is **not** the intended long-term setup. `FROM_ADDR` and `BUSINESS_EMAIL` are also both pointed at that same throwaway test mailbox right now.

A real Email Service Provider (Resend / Amazon SES, per the comments already in `config.py`/`.env`) is more robust and secure than relaying through a personal Gmail account:
- Scoped API key / SMTP credential instead of a personal mailbox password.
- Proper domain verification (SPF/DKIM/DMARC) so mail reliably lands in the inbox instead of getting bounced or spam-filtered (Gmail's relay is picky about the `From` domain matching the authenticated account — already bit us once).
- `send_email()` was written provider-agnostic on purpose, so this swap should only touch `.env`, not `app.py`. See `todo.md` → `## 12. Email Delivery` for the concrete steps.