# Development Journal

TODO: Add links to URLS for tools and resources

## Using a Static website template from Envato
Utilising a static web template from `envato` marketplace are sometimes packaged by the developers in different ways. Links between files are sometimes different, have not seen one using a Backend framework yet, or frontend framework. Currently most have used static `HTML, CSS and JS` files use relative paths to find eachother.

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

> Some folder are higher or deeper and call either Fonts or Images from `../../` or `/fonts`

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

## Implementing a Frontend Framework

TODO: TBD

## Installing and configuring a Database

## API Calls to an Email Exchange

## Security

*See = sorceror\Self-Development\Research and Findings\Application Development\How to secure a Web App from simple attacks and keep it secure.md

## Server Gateway (Uvicorn)

FastAPI is an ASGI (Asynchronous Server Gateway Interface) framework. Unlike older Python web frameworks (like Flask) which are WSGI, FastAPI is built around Python's async/await and needs a server that can handle asynchronous connections. Uvicorn is that server.

It's a lightning-fast ASGI server that acts as the bridge between incoming HTTP requests and your FastAPI app. Without it, your FastAPI app has no way to actually listen on a port and serve traffic. Uvicorn handles TCP/HTTP — FastAPI handles routing.

- Flask needs a WSGI server (like Gunicorn or Waitress).
- FastAPI needs an ASGI server (like Uvicorn or Hypercorn).

## Testing Functionality on Testing Envrionment (T-800/T-X)

## Installing and Configurating TypeScript

Install Type Script

```bash
npm init -y          # skip if you already have a package.json
npm install --save-dev typescript
npx tsc --init       # generates tsconfig.json
```

Notes:
- Once installed, an autogenerated `tsconfig.json` file will be created in the root folder
- 

What was configured in `tsconfig.json`?

`tsconfig.json` = Master configuration file for the TypeScript compiler (tsc).It tells TypeScript which files to check, how strictly to enforce rules, and how to transform your modern code into JavaScript that the browser or Node.js can actually run.

I configured `tsconfig.json` to handle modern day TypeScript/JavaScript implementation. I have added settings for dealing with older style JavaScript modules, and also being ready for a framework like `react`. It will handle simple HTML, CSS and JQuery files just now.

I had to install `@types` for TypeScript JQuery so that I can use `$` globally in the `.ts` files without needing to import JQuery.

What was configured in `tsconfig.json`?
- React Ready: Set up for React (jsx) but fully supports your current HTML/jQuery projects.
- Modern Modules: Uses the latest standards (ESNext) while safely handling older libraries (esModuleInterop). Handles `commonJS` vs `ES Modules`.
- Browser Support: Includes DOM libraries so TypeScript understands window, document, and jQuery.
- High Strictness: Enforces "strict mode" to catch hidden bugs and prevent accidental undefined errors.
- Clean Folders: Automatically organises your project by separating source files from compiled output.
- Reliable Builds: Prevents crashes in deployment by enforcing case-sensitive file naming and skipping external library errors.
- Coding: No unsed Params, Variables and strict checking on `function return types`
- Enabled types for `vitest` and `jquery`

TypeScript `types[]` - Vitest and jquery types
- You install `@types` packages for libraries that were written in plain JavaScript and don't include their own type definitions.

- Had to sperately installed `npm install -D @types/jquery`
    - Legacy Code: jQuery was created long before TypeScript
    - Its source code doesn't contain the type information TypeScript needs to understand what `$` or `.ajax()` are.
    - Currently the sit uses `JQuery` static files that were downloaded for UI Styling. 
    - It doesn't need this type install, but I have placed it here incase I use any JQuery within TypeScript logic.

- Do not need to install `@types` for `vitest`
    - Built-in Types: Unlike jQuery, Vitest is a modern tool written in TypeScript. 
    - It ships with its own type definitions included in the main vitest package.
    - Once you `npm install -D vitest`, the types are already in your node_modules. 
    - You only need to add "vitest/globals" to your `tsconfig.json` if you want to use global functions like describe and it without importing them in every file.

```bash
{
  "compilerOptions": {
    ...,
    "types": ["vitest/globals", "jquery"],
    ...,
}
```