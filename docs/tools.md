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
| **Note Worthly Scripts/Settings**
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
| **BACKEND**
| `python`   | Python Language
| `uv` | Package Manager

---

<br>

# Scripts

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