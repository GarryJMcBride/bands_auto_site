    This file should be merged with Architecture and documentation
    There will be some things done that have not been covered in here as they were done along the way**
    Reference and capture.

# Master Development TODO (Structured)

---

## 1. General Architecture & Setup

### Project Organisation

* [ ] Add these todos into **WND (Web Notes/Docs)**
  → Turn this into a reusable **“Website Development Process Checklist”**

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

* [ ] Install and configure TypeScript
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

* [ ] Validate full pipeline:

  * TypeScript → Build → FastAPI → Browser
  * Confirm no broken imports or missing files

---

## 5. CSS, UI & Styling

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
* [ ] Try to Penetrate Site with Scripts and other methods
* [ ] Scan Browser console for any passwords or risky data exposure
* [ ] Check out OWASP or other security methods defined by industry professionals
* [ ] Use the following:
    * Tokens
    * Sessions
    * API keys
    * Certs for HTTP and HTTPS for APIs
    * FastAPI Lifespan