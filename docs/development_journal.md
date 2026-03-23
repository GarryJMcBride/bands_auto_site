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