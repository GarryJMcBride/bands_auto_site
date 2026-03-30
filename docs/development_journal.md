# Development Journal

TODO: Add links to URLS for tools and resources

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
# TODO: Change this code snipped to reflect actual page names from B&S Auto Site
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

## API Calls to an Email Exchange

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

## Installing and Configurating TypeScript

Install TypeScript

```bash
npm init -y          # skip if you already have a package.json
npm install --save-dev typescript
npx tsc --init       # generates tsconfig.json
```

Notes:
- Once installed, an autogenerated `tsconfig.json` file will be created in the root folder
- Configurations need set inside `tsconfig.json`: https://www.typescriptlang.org/tsconfig/
    - Covered notes in `tools.md` going further into detail regarding what configurations were made
- 






####################################################
####################################################
####################################################
####################################################
####################################################
####################################################


<br>

# Documentation of Tools

## Abstract - Overview of Architecture

Built upon top of **Linoor** template, this repo uses mostly static `JavaScript | JQuery` files, that mostly focus on Browswer compatibility, responsiveness, UI Elements, etc etc.

It does not include any dependencies through `NPM (Node Package Manager)`. However any `JavaScript` functionality or libraries from this point onwards implemented by myself will use `NPM` as static files can become out of date quickly, and require much more manual handling.

TODO: Implement Architecture over view for Form submission

## Tools Used for Development - Table of Contents

| Tool         | Purpose                                     
|--------------|---------------------------------------------
| <br>
| **FRONTEND**
| `Node.js`  | Runs JavaScript outside the browser - Locally on Server
| `JQuery-UI`    | jQuery UI Widget - https://jqueryui.com/
| `TS/JS`    | Web Languages - TypeScript compiles to JavaScript
| `Bootstrap`    | Responsive Design - Automated Screen size adjustments
| <br>
| **BACKEND**
| `python`   | Python Language
| `uv` | Package Manager
| `uvicorn` | Server gateway for asyncronous Framework (FastAPI)
| `FastAPI` | Asyncronous Framework
| <br>
| **Testing**
| `pytest` | Python Language Testing
| `vitest` | JavaScript Language Testing
| <br>
| **Note Worthly Scripts/Settings**
| **JQuery** - Used as static files for UI Interaction and Browser support
| `respond.js` | A CSS media query polyfill for old IE browsers, it uses XHR internally just to read your CSS files and parse media queries. 
| `jquery.js` | Core jQuery |
| `popper.min.js` | Tooltip/dropdown positioning (Bootstrap dependency) |
| `bootstrap.min.js` | Bootstrap UI framework |
| `TweenMax.js` | GSAP animations |
| `jquery-ui.js` | Legacy UI widgets |
| `jquery.fancybox.js` | Lightbox/modal images |
| `owl.js` | Carousel/slider |
| `mixitup.js` | Filter/sort animations |
| `knob.js` | Circular dial UI elements |
| `validate.js` | Client-side form validation only |
| `appear.js` | Trigger events when elements scroll into view |
| `wow.js` | Scroll-triggered CSS animations |
| `jarallax.min.js` | Parallax scrolling |
| `jquery.easing.min.js` | Animation easing functions |
| `custom-script.js` | Template's own glue code |
| <br>
| **TypeScript Configurations**
| `tsconfig.json` | Master configuration for TypeScript |




---

<br>

# Some Scripts worth notes

    TODO: Consider adding this information to the actual scripts at the top of them

## validate.js

**jQuery Validation Plugin** is a client-side form validation library. It checks that form fields are filled in correctly *before* submission like:

- Required fields aren't empty
- Email addresses are in a valid format
- Phone numbers match a pattern
- Fields meet minimum/maximum length rules

It essentially adds error messages and prevents the form from submitting if the inputs don't pass the rules. **It does not send any data anywhere** — it's purely a gatekeeper on the frontend.

**WARNING**: It's version `1.11.0` from **2013** — over 12 years old. The current version is 1.21.x. Not a critical issue since it's just validation, but worth noting.


### How it is included

**Not** a managed dependency and does not appear in `package.json`. It is a static file (`src/js/respond.js`) stored directly in the repository

## respond.js

https://github.com/scottjehl/Respond/tree/master

### Summary

A CSS media query polyfill for old IE browsers, it uses XHR internally just to read your CSS files and parse media queries. A fast and lightweight polyfill specifically for min-width and max-width CSS3 media queries. It is commonly used to bring responsive design capabilities to Internet Explorer 6–8

While modern browsers have broad support for CSS media queries, polyfills are used to enable support for legacy browsers (like IE8) or to provide access to newer features like range syntax

### How it is included

**Not** a managed dependency and does not appear in `package.json`. It is a static file (`src/js/respond.js`) stored directly in the repository


    TODO: Remove `respond.js` and use modern alternatives/methods

    "Respond.js is a legacy polyfill for IE8 that causes performance lag and CORS issues by re-fetching and parsing CSS via JavaScript.

    It is now considered obsolete technical debt; modern best practices favor native CSS features or "graceful degradation" over supporting outdated browsers.



## jquery-ui.js

https://jqueryui.com/

### Summary

jQuery UI is a curated set of user interface interactions, effects, widgets, and themes built on top of the jQuery JavaScript Library.

jQuery UI is a legacy JavaScript library built on top of jQuery that provides UI widgets, interactions, and effects such as datepickers, sliders, dialogs, and drag-and-drop. It is now largely considered outdated, superseded by modern frameworks and lighter alternatives.

### How it is included

**Not** a managed dependency and does not appear in `package.json`. It is a static file (`src/js/jquery-ui.js`) stored directly in the repository.

A pre-built distribution of v1.12.1 (2016), included as part of the original Envato Market template. This was common practice at the time. It receives no automatic updates and must be managed manually.

> ⚠️ v1.12.1 is a nine-year-old release with known XSS vulnerabilities and should be replaced if the project is modernised.

### Modern alternatives

- **Alpine.js** — lightweight interactivity, no build step
- **Floating UI** — modern positioning utilities
- **Radix UI / Headless UI** — accessible component primitives for React/Vue
- **SortableJS** — drag-and-drop without jQuery
- **Native browser APIs** — many jQuery UI features are now available natively in modern browsers

---

## tsconfig.json

Configures the TypeScript compiler — which files to check, strictness rules, and output format.

Key settings:
- **Strict mode** — catches bugs, prevents accidental `undefined` errors, flags unused params/variables, enforces return types
- **ESNext + esModuleInterop** — modern modules with safe handling of older CommonJS libraries
- **DOM libs** — TypeScript understands `window`, `document`, `$`
- **JSX ready** — configured for React, works fine with plain HTML/jQuery now
- **Separate output** — source and compiled files kept in distinct folders
- **Case-sensitive filenames + skip external lib errors** — avoids deployment issues

### Types: jQuery vs Vitest

**jQuery** > needs `npm install -D @types/jquery`
- Written before TypeScript existed, so ships no type definitions
- Lets you use `$` globally in `.ts` files without importing
- Note: the jQuery static files already in the project are downloaded UI assets — unrelated to this install

**Vitest** > no `@types` install needed
- Modern, written in TypeScript, ships its own types
- Only add `"vitest/globals"` to `tsconfig.json` if you want `describe`/`it` available globally without imports

```bash
{
  "compilerOptions": {
    ...,
    "types": ["vitest/globals", "jquery"],
    ...,
}
```