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
| ----------------------------------- | ------------------------ |
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

**Does the frontend's architecture affect backend security? No.** `/api/book-javascript-pipeline` is a public endpoint — it can't tell whether a request came from `bookForm.ts`, curl, or Postman, so nothing about the frontend's structure, framework, or even its presence changes what `BookSubmission`'s validators, `sanitise()`/`contains_injection()`, or the `slowapi` rate limiter do. They run identically on every request regardless of origin.

**Does the form work with JS disabled?** It didn't, until now. `#book-form` had no `action`/`method`, so with the JS listener gone the browser fell back to its default native submission — a `GET /` with every field appended as a query string, which FastAPI's `/` route just ignores. Nothing reached the database or the email step; a no-JS user could not submit the form at all (annoying, but not a security hole — see above).

**Fix — progressive enhancement (`app.py` + `index.html`):**
- `#book-form` now has `action="/book-python-pipeline" method="post"`, a real fallback target for a native browser POST.
- New `POST /book-python-pipeline` endpoint accepts the fields as `Form(...)` (needs the `python-multipart` package — added via `uv add python-multipart`), builds the same `BookSubmission`, and reuses `update_book_database()`/`send_book_email()` unchanged. Since a plain HTML form expects a page back, not JSON, it redirects (`303`) to `/?book_submitted=success#booknow` or `/?book_submitted=error#booknow` instead of returning a JSON body.
- `read_homepage()` reads that `?book_submitted=` query param and passes it to the template, which shows a plain `<p class="form-success-message">`/`<p class="form-error-message">` banner above the form (same unstyled-for-now convention as the JS's existing per-field `.form-error-message` spans).
- `/api/book-javascript-pipeline` (JSON, used by `bookForm.ts` when JS runs) is untouched — `/book-python-pipeline` is a separate, parallel path for the no-JS case only.

**How would a malicious user actually attack this?** Exactly as guessed: skip the page and the JS entirely and POST straight at the endpoint —
```bash
curl -X POST http://localhost:8000/api/book-javascript-pipeline \
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

**Frontend sanitization uses DOMPurify** (`sanitise.ts`, shared by `bookForm.ts`/`enquiryForm.ts`) — strips all HTML tags/attributes from each field (`ALLOWED_TAGS: []`) before the regex validators run, so `<script>` etc. never even reaches validation. This is separate from and unaware of the backend's own sanitisation (`sanitise()` / `contains_injection()` in `validation.py`, which does `html.escape` + strips tags + checks injection patterns) — each layer is independent, per the "backend doesn't trust the frontend" rule above. See `## Email Sending pipeline` for the DOMPurify vendoring workaround (no bundler, so it isn't a plain `npm install` away in the browser).



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
CREATE TABLE book_submissions (
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

1. **HTML** — `#book-form` (`index.html`, `novalidate`) holds the raw fields: `username`, `email`, `phone`, `registration`, `service`. (This form was originally named "quote" throughout — see "Splitting the enquiry form into its own pipeline" and the "Update 'Quote' to 'Book'" todo item; renamed to `book`/`Book*` everywhere except the theme's own untouched HTML/CSS class names.)
2. **JS** (`transferFormInput.ts` → compiled `dist/transferFormInput.js`, later split into `bookForm.ts`/`sanitise.ts`/`formFeedback.ts` — see below) — `submit` listener does `preventDefault()`, sanitises each field with DOMPurify, validates format/required-ness client-side (convenience only), then `fetch("/api/book-javascript-pipeline", {method: "POST", body: JSON})`.
3. **Python** (`app.py`, `POST /api/book-javascript-pipeline`) — FastAPI parses the body into `BookSubmission` (Pydantic), which independently re-sanitises/re-validates every field (this is the real gate, not the JS). `submit_book_javascript_pipeline()` then:
   - `save_book()` — parameterized `INSERT` into `book_submissions` via the `asyncpg` pool.
   - `send_book_email()` — builds a `multipart/alternative` message (styled HTML via `build_book_email_html` + plaintext via `build_book_email_body`, see "HTML email body + plain-text fallback" below) and sends it with `aiosmtplib`, creds from `config.py`/`.env` (`SMTP_HOST/PORT/USER/PASS`, `FROM_ADDR`, `BUSINESS_EMAIL`).
   - Returns `201` + `submission_id` only if both the DB write and the email send succeed; either failing raises a `500` (DB write happens first, so a failed send doesn't lose the saved lead).
4. **Database** — single `book_submissions` table. DDL (`CREATE_BOOK_TABLE_SQL`) now runs automatically in `lifespan()` on app startup (previously wasn't wired up anywhere, so the table didn't exist).

### DOMPurify vendoring workaround (no bundler)

This project has no bundler (webpack/esbuild/vite) — `npm run build` is plain `tsc`, which only compiles `.ts` → `.js`. It does **not** resolve/inline `node_modules` packages for the browser. So `import DOMPurify from "dompurify"` in `transferFormInput.ts` (this form's original, pre-split TypeScript file — see above) can't just work off `npm install` like it would in a bundled app — the browser has no way to reach into `node_modules`.

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

Fixing the missing vendor file above wasn't the whole story — even with the file present, the browser refused to run it, and *every* form submission in testing was silently hitting the no-JS `/book-python-pipeline` fallback instead of the JS `fetch` path, for a completely different reason.

**Why MIME types matter for JS/modules at all:** every HTTP response includes a `Content-Type` header (e.g. `text/css`, `image/png`, `application/javascript`) telling the browser what kind of content it just downloaded, so it knows how to handle it. A `<script>` tag doesn't care much about the exact value as long as it's *some* JS-flavoured type — but `<script type="module">` (and `import`/`import()`) is stricter: the spec requires the response to be one of a specific allow-list of JavaScript MIME types, or the module load is rejected outright, with no code ever running. `text/plain`, `application/octet-stream`, etc. are not on that list.

**Where DOMPurify comes in:** `purify.es.mjs` is fetched as a *module* (via the import map — see above), not a plain `<script src>`. FastAPI's `StaticFiles` mount doesn't hardcode a `Content-Type` per file — it asks Python's built-in `mimetypes` module to guess one from the file extension. `mimetypes` reads from the OS's own MIME registry (on Windows, effectively the registry; on Linux, files like `/etc/mime.types`), and `.mjs` — being a newer, less universal extension than plain `.js` — isn't always registered there. On this machine it wasn't, so `mimetypes` fell back to `text/plain`.

**Why it failed *silently*:** `SecurityHeadersMiddleware` (`app.py`) already adds `X-Content-Type-Options: nosniff` to every response — a deliberate security header that tells the browser "trust the Content-Type I gave you, don't try to guess a better one from the file's actual bytes." That's the header doing exactly its job; it just collided with `mimetypes` guessing wrong. The combination (wrong type + nosniff) makes the browser reject the module fetch with no console error and no network-level failure visible in a normal check — `curl` and the Network tab both showed a clean `200`, which is why this took real browser testing (via `claude-in-chrome`, dynamically `import()`-ing the file directly) to actually surface, rather than curl/status-code checks alone.

**Fix** (`app.py`): register the MIME type explicitly, once, at startup, so it doesn't depend on the host OS's registry at all:
```python
import mimetypes

mimetypes.add_type("text/javascript", ".mjs")
```
Placed before the `/static` mount. This means the exact same code behaves identically on Windows, Linux, in CI, wherever — no dependency on what that machine's `mimetypes` happens to already know.

**Real-world proof the no-JS fallback earns its keep:** by the time this MIME bug was discovered, several genuine test submissions (username "Garry") had already landed correctly in `book_submissions` — sent *before* the bug above was even found or fixed. That's not a contradiction: the `POST /book-python-pipeline` fallback and the form's `action="/book-python-pipeline" method="post"` were already wired up by then. So the actual sequence was: click submit → the browser tries to run `transferFormInput.js` → it fails silently (this exact MIME bug, undiscovered at the time) → `preventDefault()` never runs → the browser falls through to its native form submission → which now had a real, working target instead of nowhere. The data never touched DOMPurify or `fetch` — it went in as plain form-urlencoded fields, validated and saved entirely server-side. Good demonstration of why the fallback is worth having as a genuinely independent path: the "enhanced" JS layer was silently dead the whole time, and the fallback caught it without anyone noticing until later.

### HTML email body + plain-text fallback for non-HTML recipients

The booking-notification email used to be `build_email_body()` — an all-plaintext `f"""..."""` string, i.e. raw field values dumped into the message with no formatting (`build_email_body`/`build_email_html`/`send_quote_email` were later renamed to `build_book_email_body`/`build_book_email_html`/`send_book_email` — see the "Update 'Quote' to 'Book'" rename). Replaced with a styled version while keeping a fallback for recipients that can't (or won't) render HTML:

- `build_book_email_html()` (`mailer.py`) — a table-based HTML layout (brand red `#ff0000` header, field table, footer with submission ID + timestamp) using **inline styles only**, no `<style>` block. This is a deliberate email-HTML constraint, not a stylistic choice: major clients (Outlook especially, but also Gmail's clipping/stripping behaviour) ignore or strip `<style>` tags and much of modern CSS (flexbox/grid, custom properties) in mail bodies — inline `style="..."` attributes on table cells is still the most reliably-supported approach across clients.
- `build_book_email_body()` — kept as-is, the original plaintext version.
- `send_book_email()` wires both together as a single MIME message (see "Splitting the enquiry form into its own pipeline" below — this later became the booking-specific half of `mailer.py`, mirrored by `send_enquiry_email()`):
  ```python
  message.set_content(build_book_email_body(data, submission_id))  # text/plain
  message.add_alternative(
      build_book_email_html(data, submission_id), subtype="html"
  )  # text/html
  ```
  `EmailMessage.set_content()` + `.add_alternative()` produces a `multipart/alternative` message containing both parts. This is standard MIME, not app-specific logic: the **mail client**, not this code, decides which part to render — an HTML-capable client shows the styled `text/html` part, anything that only understands plaintext (a terminal mail reader, some accessibility/screen-reader setups, viewing raw source) falls back to the `text/plain` part automatically. No conditional logic needed on the send side; the fallback is inherent to the MIME format.
- Both parts read from the same sanitised `BookSubmission` fields (already `html.escape`'d by the Pydantic validators before this point), so values are interpolated into the HTML as-is — no double-escaping, and no injection risk since sanitisation already ran.
- Verified by rendering `build_book_email_html()`'s output to a static file and viewing it in a real browser tab (via `claude-in-chrome`) rather than trusting the string concatenation — confirmed header colour, table layout, and `mailto:`/`tel:` links all render correctly.

### Still using a temporary mailbox, not a real ESP

Email currently goes out over `smtp.gmail.com` using a personal Gmail account + app password (`SMTP_USER`/`SMTP_PASS` in `.env`) — this only exists to prove the send pipeline works end-to-end, it is **not** the intended long-term setup. `FROM_ADDR` and `BUSINESS_EMAIL` are also both pointed at that same throwaway test mailbox right now.

A real Email Service Provider (Resend / Amazon SES, per the comments already in `config.py`/`.env`) is more robust and secure than relaying through a personal Gmail account:
- Scoped API key / SMTP credential instead of a personal mailbox password.
- Proper domain verification (SPF/DKIM/DMARC) so mail reliably lands in the inbox instead of getting bounced or spam-filtered (Gmail's relay is picky about the `From` domain matching the authenticated account — already bit us once).
- `send_email()` was written provider-agnostic on purpose, so this swap should only touch `.env`, not `app.py`. See `todo.md` → `## 12. Emai         Delivery` for the concrete steps.

### Implementing images to the html email file

Wanted the B&S Autos logo (`bands_logo_no_scroll.png`) in the red header banner of `build_email_html()`, but a plain `<img src="static/images/bands_logo_no_scroll.png">` — the pattern used everywhere else in `index.html` — doesn't work here. That path only resolves because a *browser* is loading it from this app's own `/static` mount at `http://this-host/static/...`. An email travels over raw SMTP to an arbitrary mail client on the recipient's machine, which has no concept of this app's server or its static mount at all — a relative path resolves to nothing, and even the full `https://` URL would depend on the site being publicly deployed and reachable, which it isn't yet in dev.

The fix is to embed the image *inside* the email itself as a MIME part, referenced from the HTML by a `Content-ID` instead of a URL — the same mechanism every "logo in the email header" you've ever received actually uses:

```python
message.set_content(build_email_body(data, submission_id))
message.add_alternative(build_email_html(data, submission_id), subtype="html")
html_part = message.get_payload()[1]
html_part.add_related(
    LOGO_PATH.read_bytes(), maintype="image", subtype="png", cid=f"<{LOGO_CID}>"
)
```
and in the HTML:
```html
<img src="cid:bands-logo-header" alt="B&amp;S Autos" height="28">
```

Things worth remembering about this:
- `add_related()` must be called on the **html sub-part** (`message.get_payload()[1]`), not on the top-level `message`. Calling it on the top level would attach the image as a separate top-level `multipart/mixed` attachment (a normal file attachment) instead of nesting it as `multipart/related` inside the html branch of the `multipart/alternative` — which is what actually makes a bare `cid:` reference resolve inside that html body.
- The `Content-ID` header value needs angle brackets (`<bands-logo-header>`), but the `cid:` reference in the `<img src>` does not (`cid:bands-logo-header`) — this is RFC 2392 syntax, easy to get backwards. Verified by building the message with stdlib `email.message.EmailMessage` and inspecting `message.as_string()` directly rather than trusting it blind — confirmed `Content-ID: <bands-logo-header>`, `Content-Type: image/png`, and `Content-Disposition: inline` all show up in the right place before wiring it in.
- Chose CID embedding over hosting the image at a real URL once deployed, even though that would also work: CID-embedded images render immediately in Gmail/Outlook/Apple Mail with no click-through, since they're already part of the downloaded message rather than a remote fetch the client may block by default ("images are hidden — display images below?"). It also means the email doesn't silently break if the image is ever moved/renamed on the live site after being sent.
- `LOGO_PATH` is resolved once with `pathlib.Path(__file__).resolve().parent.parent / "frontend" / "static" / "images" / "bands_logo_no_scroll.png"` — reading the file happens lazily inside `_attach_logo_and_send()` (`mailer.py`), not at import time, so `build_email_html()` stays a pure string-building function with no file I/O of its own. (`_attach_logo_and_send()` is the shared tail both `send_quote_email()` and `send_enquiry_email()` call into — see "Splitting the enquiry form into its own pipeline" below.)

See `todo.md` → `## 11. Tests` — an automated test asserting the CID/image part shows up in the built message is still outstanding.

## Redirect-after-POST: why no-JS submissions round-trip through `/`

`read_homepage()` (`GET /` in `app.py`) never receives a form submission directly — it only ever sees a `GET` with a query string. The actual submissions are handled entirely by the POST endpoints (`submit_book_python_pipeline`, `submit_enquiry_python_pipeline` in the `routers/` modules). The reason `/` is involved at all comes down to what a plain HTML `<form>` can and can't do without JavaScript:

- A JS-driven submission (`fetch()`) can show a success/error message in-page without navigating anywhere.
- A native `<form method="post">` submission can't — the browser always navigates to whatever the POST handler returns. It has no equivalent of `fetch()`'s "stay on the page and update a div."

So the no-JS POST handlers do their real work (validate, save to Postgres, send the notification email), then respond with a **303 redirect** back to `/?book_submitted=success` (or `...=error`, and `?enquiry_submitted=...` for the enquiry form) instead of returning HTML themselves. The browser follows that redirect as a fresh `GET /`, which is what actually lands in `read_homepage()` — it just reads the flag back off the query string to decide which banner the template should render next to the right form.

Using `303 See Other` specifically (rather than the POST handler just returning a rendered page directly) also avoids the browser's "confirm form resubmission" prompt if the user refreshes afterward — refreshing a redirected `GET` just re-fetches `/`, not the original POST.

Two separate query params (`book_submitted` / `enquiry_submitted`) exist because both the booking and enquiry forms live on the same page — one shared flag couldn't tell the template which form's banner to show.

## Splitting sanitisation out of schemas.py into validation.py

`schemas.py` had carried a `# TODO: Find out why these functions are within a pydantic schema` comment since early on, sitting right above `BookSubmission` (named `QuoteSubmission` at the time — see "Update 'Quote' to 'Book'" below). `INJECTION_PATTERNS`, `contains_injection()`, and `sanitise()` lived in the same file as the Pydantic model, called from inside its `field_validator`s.

That was fine while there was exactly one form and one Pydantic model in the whole app. It stops being fine once a second form gets hooked up (planned soon) and, further out, once this FastAPI backend gets reused as a starting point for other client sites — the goal being explicit reuse across projects, not just across forms in this one repo.

**The distinction that matters:** `sanitise()`/`contains_injection()` know nothing about `BookSubmission` — they operate on plain strings and have no opinion about names, emails, or vehicle registrations. `BookSubmission` itself, by contrast, is entirely specific to this one form on this one site. Keeping them in the same file meant you couldn't reuse one without dragging the other along — a new form's schema, or a copy of this repo for a different client, would have to either duplicate the sanitisation functions or import them out of a file that's conceptually "just this site's form model."

**Fix:** moved `INJECTION_PATTERNS`, `contains_injection()`, and `sanitise()` verbatim into a new `src/backend/validation.py`, with `schemas.py` now just `from src.backend.validation import contains_injection, sanitise` and calling them from its `field_validator`s exactly as before. `schemas.py` is left holding only `BookSubmission` (the domain-specific model) and `CREATE_BOOK_TABLE_SQL` (the DB DDL) — no logic changes, pure move + import update, verified by re-running a `BookSubmission(...)` construction and importing `src.backend.app` afterwards to confirm nothing else referenced the old location (nothing did — `sanitise`/`contains_injection` were only ever imported from within `schemas.py` itself).

The `# TODO` comment is gone — this was the answer to it. See `docs/pipeline-architecture-visual-diagram.md` for the updated module table (now a separate "Sanitisation" row for `validation.py` alongside "Schema" for `schemas.py`).

## Splitting the enquiry form into its own pipeline

The `validation.py` split above was explicitly preparing for this: `#contact-form` ("Not Sure What Your Vehicle Needs?") is the second form on the site, alongside the original booking form (still `QuoteSubmission`/`quoteForm.ts`/etc. at the time this split happened — see "Update 'Quote' to 'Book'" below for the later rename). Rather than bolt its handling onto the existing booking-only files, it got its own pipeline, mirroring the booking form's structure end to end:

- **Frontend**: `enquiryForm.ts` (new) mirrors `quoteForm.ts`'s structure (since renamed to `bookForm.ts`) — its own `EnquiryFormData` validation (subject/message length checks instead of registration/service), `fetch()`-POSTs to `/api/enquiry-javascript-pipeline`. The booking form's old `transferFormInput.ts` was split too — its DOMPurify wrapper became `sanitise.ts` and its error/banner rendering became `formFeedback.ts`, both now shared by `quoteForm.ts`/`bookForm.ts` and `enquiryForm.ts` rather than living inside one form's file.
- **Backend router**: `routers/handle_enquiry_inputs.py` (new) mirrors `handle_form_inputs.py` (since renamed to `handle_book_inputs.py`) function-for-function — `save_enquiry()`, `update_enquiry_database()`, `submit_enquiry_javascript_pipeline` (JSON), `submit_enquiry_python_pipeline` (form, `303` redirect to `?enquiry_submitted=...`).
- **Schema**: `EnquirySubmission` added to `schemas.py` alongside `QuoteSubmission` (since renamed to `BookSubmission`), plus `CREATE_ENQUIRY_TABLE_SQL` alongside `CREATE_TABLE_SQL` (since renamed to `CREATE_BOOK_TABLE_SQL`) — both DDLs run in `lifespan()` (`app.py`) on startup. `EnquirySubmission` reuses the same shared field validators from `validation.py` (`validate_name`, `validate_email_address`, `validate_phone_number`, `check_no_blank_string_fields`) that `QuoteSubmission`/`BookSubmission` uses — this is exactly the reuse the `validation.py` split was for.
- **Email**: `mailer.py` grew a parallel set of builders — `build_enquiry_email_body`/`build_enquiry_email_html`/`send_enquiry_email` alongside the existing `build_email_body`/`build_email_html`/`send_quote_email` (since renamed to `build_book_email_body`/`build_book_email_html`/`send_book_email`). Rather than duplicate the HTML/plain-text layout itself, the shared visual shell was pulled out into `_render_html_shell()`, `_render_plain_text()`, and `_render_field_rows_html()` — both pipelines' emails call into these, so they can't visually drift apart even though their field content differs. The inline-CID logo attach + SMTP send tail (`_attach_logo_and_send()`) is likewise shared, called by both `send_quote_email()`/`send_book_email()` and `send_enquiry_email()`.
- **`app.py`**: now includes both routers (`app.include_router(handle_form_inputs.router)` and `handle_enquiry_inputs.router` — the former since renamed to `handle_book_inputs.router`), and `read_homepage()` reads two independent query flags — `?submitted=` (since renamed to `?book_submitted=`) and `?enquiry_submitted=` — since both forms live on the same page and need independently-shown banners. See `docs/development_journal.md` -> "Redirect-after-POST" (above) for why that redirect round-trip exists at all.

**Why duplicate rather than generalise into one "submission" abstraction:** the two forms' data shapes only overlap on name/email/phone — everything else (registration/service vs. subject/message, the resulting DB columns, the resulting email content) is genuinely different per form. A forced shared `Submission` base class or generic router factory would have added a layer of indirection to save a modest amount of boilerplate, at the cost of making either form harder to change independently. Splitting cleanly by file (one router, one schema, one set of email builders per form) keeps each pipeline simple to read top-to-bottom, while `validation.py` and the `mailer.py` shell functions still capture everything that's genuinely shared.

See `docs/pipeline-architecture-visual-diagram.md` for the full updated diagram and module table covering both pipelines.

## Update "Quote" to "Book"

The template's own theme markup calls this form "Quote" (`class="get-quote-section"`, `<!--Get Quote Section-->`, etc.) but its actual purpose on B&S Autos is booking a vehicle in for work — the page copy already says "Book Your Vehicle In" and the section anchor is `id="booknow"`. Everywhere the code used "quote"/"Quote" as an identifier (not as prebuilt theme markup) was renamed to "book"/"Book" for clarity, per the todo item this closes:

- **Schema**: `QuoteSubmission` -> `BookSubmission`; `CREATE_TABLE_SQL` -> `CREATE_BOOK_TABLE_SQL`; table `quote_submissions` -> `book_submissions`.
- **Router**: `routers/handle_form_inputs.py` -> `routers/handle_book_inputs.py`; `save_submission()` -> `save_book()`; `update_database()` -> `update_book_database()`; `submit_quote_javascript_pipeline` -> `submit_book_javascript_pipeline`; `submit_quote_python_pipeline` -> `submit_book_python_pipeline`; endpoints `/api/quote-javascript-pipeline` -> `/api/book-javascript-pipeline` and `/quote-python-pipeline` -> `/book-python-pipeline`.
- **Mailer**: `build_email_body`/`build_email_html`/`send_quote_email` -> `build_book_email_body`/`build_book_email_html`/`send_book_email`.
- **Frontend**: `quoteForm.ts` -> `bookForm.ts`; `QuoteFormData` -> `BookFormData`; `validateQuoteFormData`/`handleQuoteFormSubmit`/`submitQuoteData` -> `validateBookFormData`/`handleBookFormSubmit`/`submitBookData`.
- **Template**: `index.html`'s `id="quote-form"` -> `id="book-form"`, its `action`/script `src` updated to match, and the Jinja `submitted` context var -> `book_submitted` (mirroring `enquiry_submitted`'s naming for the enquiry form).

**What was deliberately left alone:** the Linoor theme's own HTML/CSS — `class="get-quote-section"`, `class="get-quote-two"`, the `<!--Get Quote Section-->` comments — since these are presentational, come from the prebuilt template, and renaming them would mean tracking divergence from the vendor theme's CSS for no functional benefit. Only the underlying form id and the entire Python/TypeScript data model were renamed; the visible theme markup still says "quote" and that's fine.

## Commenting out `validate.js`'s leftover Contact Form Validation call

While auditing template bloat (see `docs/frontend-bloat-audit.md`), one of the "probably dead, will confirm" vendored plugins turned out to still be live and worth flagging on its own.

### What it was doing

`custom-script.js` (~line 956, now commented out) ran this on every page load:
```js
if ($("#contact-form").length) {
  $("#contact-form").validate({
    rules: {
      username: { required: true },
      email: { required: true, email: true },
      phone: { required: true },
      subject: { required: true },
      message: { required: true }
    }
  });
}
```
This is the **jQuery Validation Plugin** (`validate.js`, v1.11.0, 2013) — a client-side "are these fields filled in / roughly the right shape" checker. It's purely presence/format checking: it never sanitises anything, never strips or escapes content, and has no concept of injection patterns.

### How it wires up to `custom-script.js` — the jQuery plugin pattern

There's no explicit call between the two files — the connection is entirely through shared global state:

1. **Load order**: `index.html` loads `validate.js` *before* `custom-script.js` (both plain classic `<script>` tags, no modules).
2. **`validate.js` extends jQuery's prototype**: it does `jQuery.extend(jQuery.fn, { validate: function(t){...} })`. `jQuery.fn` is `jQuery.prototype` — every `$(...)`-wrapped element inherits from it. This bolts a `.validate()` method onto *every* jQuery object, site-wide, the moment `validate.js` executes. Standard jQuery plugin pattern.
3. **`custom-script.js` just calls the method that now exists**: `$("#contact-form").validate({...})` is nothing more than "wrap the form, call the method `validate.js` attached earlier." Neither file imports or references the other directly.
4. **What `.validate()` itself does under the hood**: it calls `this.submit(function(t){...})` — jQuery's shorthand for `form.addEventListener("submit", handler)` — registering its *own* native submit listener on the form, entirely independently of anything `enquiryForm.ts` does.

### Why it looked dead but wasn't

`docs/architecture.md` already claims *"Removed form Validation... from `custom-script` as its now handled by TypeScript"* — and most of the template's other jQuery widgets genuinely are dead (see the audit doc's version table: `mixitup.js`, `knob.js`, `appear.js`, `jquery.fancybox.js`, `isotope.js`, `nouislider.*` all target elements that don't exist in `index.html`). This one looked like it should belong in that same "removed/dead" bucket, since the intent was clearly to hand validation over to TypeScript entirely.

But `#contact-form` isn't template leftover — it's the *real*, live ID of the enquiry form (`#requestcall` section), the same element `enquiryForm.ts` attaches its own `submit` listener to. So unlike every other "dead" plugin in the audit, this one's trigger selector genuinely matches something on the page — it was actually running on every load, just never noticed because it doesn't visibly error or obviously misbehave. It's a live conflict, not dead code, which is exactly why it's called out separately from the rest of the audit's "unused plugin" list.

### `validate.js` vs. this repo's actual sanitisation/validation pipeline

| | `validate.js` | This repo's pipeline |
|---|---|---|
| Checks | Presence only (`required: true`) + basic email format | Full: sanitise (strip HTML/control chars, `html.escape`), injection-pattern detection, length bounds, name/phone/UK-reg regex, blank-check |
| Sanitises input? | No — never touches/cleans the value, only validates presence/shape | Yes — `DOMPurify` (`sanitise.ts`) client-side, `sanitise()`/`contains_injection()` + Pydantic validators server-side (`validation.py`) |
| Security value | None — a UX convenience layer only | This is the actual security boundary — `validation.py` is what's trusted |
| Trust model | Assumes it even runs (client-side, bypassable) | Backend never trusts the client; re-validates every field regardless of what the JS did |

It's strictly weaker than and redundant with what's already in place, contributes zero sanitisation, and its only real effect was the interference risk above — a submit-handler race with `enquiryForm.ts` on the same form, with no upside.

### Current state: commented out, not deleted

Per `todo.md` → `## 13. Frontend Bloat Audit`, the call site in `custom-script.js` has been **commented out** (not removed) for now, with a note pointing back to `docs/frontend-bloat-audit.md`'s "Priority finding" section. Full removal of the file (`validate.js`, its `<script src>` tag) is tracked in that same audit doc/todo, pending confirmation via a real browser test of whether it was actually breaking `enquiryForm.ts`'s `fetch()` path or just quietly running alongside it.

## UI plumbing: `formFeedback.ts`

`src/frontend/typescript/formFeedback.ts` is pure DOM-rendering plumbing shared by `bookForm.ts` and `enquiryForm.ts` — it has no validation logic of its own and makes no network calls. It's the "how do I show/hide feedback" layer both forms call into *after* they've already validated or submitted.

Four exported functions:
- `displayErrors(errors, form)` — takes the `{fieldName: message}` object each form's `validate*FormData()` produces, and for each entry inserts a `<span class="form-error-message" role="alert">` immediately after that input, plus `aria-invalid="true"` on the input for screen readers. Calls `clearErrors()` first so repeated invalid submits don't stack duplicate spans.
- `clearErrors(form)` — removes all `.form-error-message` spans and `aria-invalid` attributes from the form.
- `showSubmitMessage(form, type, message)` — after a `fetch()` call resolves, inserts one `<p class="form-success-message">`/`.form-error-message` directly above the `<form>` (`insertAdjacentElement("beforebegin", ...)`), with `role="status"`.
- `clearSubmitMessage(form)` — removes that banner before showing a new one.

**Why it's a separate shared file rather than living inside each form's `.ts`:** both forms need identical DOM behaviour (same classes, same accessibility attributes, same insertion point), so duplicating this in `bookForm.ts` and `enquiryForm.ts` would risk them drifting apart the first time one form's error styling/behaviour changes and the other doesn't. Same rationale as `sanitise.ts` and `validation.py` elsewhere in this repo — shared, form-agnostic behaviour gets pulled into its own module rather than copy-pasted.

**One namespacing detail worth calling out:** `submitMessageId()` derives the banner's element id from `${form.id}-submit-message` rather than a fixed constant, specifically because both `#book-form` and `#contact-form` live on the same page at once — a shared fixed id would mean one form's success message could get clobbered by (or clobber) the other's error message.

### Is `index.html` involved in this? Yes, in three concrete ways

1. **`form.id` must exist and be unique** — `showSubmitMessage`/`clearSubmitMessage` key their banner's id off `form.id`. This is exactly why the booking form is `id="book-form"` and the enquiry form is `id="contact-form"` (see "Update 'Quote' to 'Book'" above) — without a real, distinct id per form, the two forms' submit banners would collide.
2. **`<input name="...">` attributes must match the validators' field names** — `displayErrors()` looks up each erroring field via `form.elements.namedItem(field)`, so the `name` attributes already in `index.html` (`username`, `email`, `phone`, `registration`/`service` for booking; `subject`/`message` for enquiry) are the contract `formFeedback.ts` depends on. Rename an input's `name` in the HTML without updating the corresponding `*FormData` type/validator, and its errors silently stop appearing.
3. **The CSS class names are shared with the server-rendered no-JS banner already in `index.html`** — the Jinja templates render `<p class="form-success-message">`/`<p class="form-error-message">` for the `?book_submitted=`/`?enquiry_submitted=` no-JS fallback case (see "Redirect-after-POST" above). `formFeedback.ts` deliberately reuses those exact same class names for its JS-created elements, so a user sees the same-looking message regardless of whether JS ran or the no-JS fallback fired. Currently **neither** version actually has CSS backing them (`grep`ed `style.scss` — no `.form-error-message`/`.form-success-message` rules exist), so both render as unstyled browser-default text; styling either would style both automatically since they share the class names.

What `index.html` does **not** need for this: no pre-built empty placeholder `<div>`s for errors/messages. `formFeedback.ts` creates every element on the fly with `document.createElement(...)` and positions it relative to the real `<input>`/`<form>` elements already in the markup, rather than targeting a fixed container that would need to pre-exist in the template.

## Closing the submit-to-response feedback gap

Once client-side validation passes, `clearErrors(form)` runs immediately, but the success/error banner (`showSubmitMessage`) only appears once `fetch()` resolves — leaving a silent window, for however long the network round-trip takes, where the form shows neither an error nor a success state. Nothing told the user their click had registered, and nothing stopped a slow connection plus an impatient double-click from firing the request twice.

**Fix** (`submitBookData` in `bookForm.ts`, mirrored in `submitEnquiryData` in `enquiryForm.ts`): grab the form's submit button before the `fetch()` call, disable it and swap its `.btn-title` span text to "Submitting…", then restore both in a `finally` block so the button resets whether the request succeeds, fails, or throws.

**Gotcha:** the initial version selected the button with `form.querySelector('button[type="submit"]')`, which worked for `#book-form` (`<button type="submit" ...>`) but silently found nothing on `#contact-form`, whose button has no explicit `type` attribute at all (`<button class="theme-btn btn-style-one">`). A bare `<button>` inside a `<form>` still submits it — the browser defaults its type to `submit` — but the CSS attribute selector `[type="submit"]` only matches an attribute that's literally present in the markup, not the browser's implicit default. Fixed by selecting on `form.querySelector("button")` alone, which is safe here since each form has exactly one button.
