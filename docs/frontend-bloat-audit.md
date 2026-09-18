# Frontend Bloat Audit — Envato/Linoor Template Cleanup

## Why this exists

This site started from the Envato **Linoor** marketplace template, which ships every
plugin/widget/CSS component the theme's demo pages use — regardless of which ones this
particular single-page site actually needs. Nothing here has been trimmed yet. This doc
is the tracked checklist for finding and removing that dead weight safely, plus the one
genuine security item hiding in it: jQuery UI 1.12.1's known XSS CVEs.

**Audit method used below:** for each vendored plugin, grep its trigger selector/class
(read out of its `custom-script.js` init block) against `src/frontend/templates/index.html`.
No match = the plugin's code never runs on this page — safe to delete the plugin file, its
`<script src>`/`<link>` tag, its CSS if any, and its dead init block in `custom-script.js`.
A match = it's live; leave it alone (or handle separately, as with jQuery UI below).

All findings below were verified by grep against the current `index.html` and
`custom-script.js` — this isn't guesswork, it's checked. Re-verify after any HTML
changes before deleting, since a removed/renamed element could flip a "live" plugin to
"dead" or vice versa.

## Version table (`src/frontend/static/js/`)

| File                                             | Version           | Status                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------ | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `jquery.js`                                      | **3.5.0**         | Core jQuery — already patched. This is the exact release that fixed CVE-2020-11022/11023 (`htmlPrefilter` XSS). Not the vulnerable piece.                                                                                                                                                                                                      |
| `jquery-ui.js`                                   | **1.12.1** (2016) | **The outdated/vulnerable piece.** ~9 years old, has known XSS CVEs. Only `.selectmenu()` is actually invoked (see below) — small surface, but still worth patching/replacing.                                                                                                                                                                 |
| `TweenMax.js` (GSAP)                             | 2.1.2 (2019)      | **Live** — drives the custom cursor follower effect (`custom-script.js:294-307`, targets `.custom-cursor__overlay`, present in `index.html`).                                                                                                                                                                                                  |
| `owl.js` (Owl Carousel)                          | 2.3.4 (2018)      | **Live** — banner and testimonial carousels (`owl-carousel` classes throughout `index.html`).                                                                                                                                                                                                                                                  |
| `jarallax.min.js`                                | 1.12.4            | **Live** — parallax section (`data-jarallax` on the section around `index.html:266`).                                                                                                                                                                                                                                                          |
| `wow.js`                                         | 1.0.1 (2014)      | **Live** — `wow fadeIn*` classes widespread in `index.html`.                                                                                                                                                                                                                                                                                   |
| `jquery.easing.min.js`                           | 1.3               | **Live** — easing helper used by the above animations.                                                                                                                                                                                                                                                                                         |
| `validate.js` (jQuery Validation Plugin)         | 1.11.0 (2013)     | **Live — see priority finding below.** Still wired to `#contact-form` (the real enquiry form) via `custom-script.js:957-975`.                                                                                                                                                                                                                  |
| `mixitup.js`                                     | 2.1.10 (2015)     | **Dead.** Triggers on `.filter-list` (`custom-script.js:952-953`) — no `.filter-list` element exists in `index.html`.                                                                                                                                                                                                                          |
| `knob.js` (jQuery Knob)                          | 1.2.11 (2012)     | **Dead.** Only called from inside the `.dial` `.appear()` handler (`custom-script.js:818-853`) — no `.dial` element exists.                                                                                                                                                                                                                    |
| `appear.js`                                      | ~2012-2014        | **Dead.** All three call sites (`.count-bar`, `.count-box`, `.dial` — `custom-script.js:776-853`) target elements that don't exist in `index.html`.                                                                                                                                                                                            |
| `jquery.fancybox.js` + `jquery.fancybox.min.css` | 3.2.10            | **Dead.** Triggers on `.lightbox-image` (`custom-script.js:941-944`) — no such element exists.                                                                                                                                                                                                                                                 |
| `isotope.js`                                     | —                 | **Dead — not even loaded.** No `<script src="...isotope...">` tag exists in `index.html` at all, despite a whole filter/portfolio block in `custom-script.js:1107-1152` (`.post-filter`, `.filter-layout`, `.portfolio-masonary__filters`) that calls `.isotope(...)`. Both the unreferenced file and the dead-reference code block should go. |
| `nouislider.min.js`                              | —                 | **Dead — not even loaded.** No `<script src>` tag in `index.html`. The matching init code (`custom-script.js:100-122`, targets `#range-slider-price`/`.range-slider-price`) has no matching element either — doubly dead.                                                                                                                      |

## Priority finding: `validate.js` is still active on the real enquiry form

Unlike everything else flagged dead above, this one is a **live conflict**, not just
unused weight, and should be looked at before the rest of the cleanup:

- `custom-script.js:957-975` runs `$("#contact-form").validate({...})` on page load.
- `#contact-form` is not template leftover — it's the actual enquiry form's real ID
  (`src/frontend/templates/index.html`, the `#requestcall` section), the same form
  `enquiryForm.ts` attaches its own `submit` listener to.
- `docs/architecture.md` already claims _"Removed form Validation... from
  `custom-script` as its now handled by TypeScript"_ — but that removal apparently
  never actually happened for this specific call site; the jQuery Validation Plugin
  init is still present and still targets the live form.
- **Why this matters:** two independent submit-time handlers are now attached to the
  same form — jQuery Validation Plugin's own submit interception, and
  `enquiryForm.ts`'s `preventDefault()` + `fetch()` handler. Depending on execution
  order and what the jQuery plugin's default `submitHandler` does on a passing
  validation (by default it calls the native `form.submit()`, which does **not**
  dispatch a `'submit'` event and would bypass `enquiryForm.ts`'s listener entirely),
  this could mean the enquiry form's JS fetch path silently never runs — the exact
  "legacy jQuery code silently breaks the real JS pipeline" failure mode this repo
  already hit once before with the DOMPurify `.mjs` MIME-type bug (see
  `docs/development_journal.md`).
- [ ] **Verify in a real browser** (e.g. via `claude-in-chrome`) whether submitting
      `#contact-form` with valid data actually hits `/api/enquiry-javascript-pipeline`
      (Network tab) or falls through to a native/no-JS-style submission instead.
- [ ] If it does interfere: remove the `$("#contact-form").validate({...})` block from
      `custom-script.js` (validation is already handled server-side by
      `EnquirySubmission` and client-side by `enquiryForm.ts` — this plugin call is
      redundant even if it isn't actively breaking anything).

## Checklist

### 1. jQuery UI — CVE remediation

- [x] Confirm core `jquery.js` is 3.5.0+ (already patched) — no action needed, documented here so it isn't re-flagged.
- [ ] Decide jQuery UI's fate: it's only used for `.selectmenu()` on the booking form's service `<select>` (`custom-script.js:928-932`, targets `.custom-select-box`, `index.html:336`). Options:
  - Upgrade to a patched jQuery UI release (check current jQuery UI release notes for the CVEs that affect 1.12.1 and confirm a later 1.x release fixes them without breaking `.selectmenu()`'s markup/API).
  - Or drop jQuery UI entirely and replace the styled dropdown with a lighter alternative — a plain native `<select>` with custom CSS, or one of the modern options already listed in `docs/architecture.md` (Alpine.js, Floating UI, Radix/Headless UI).
- [ ] Remove the dead `.datepicker()` init in `custom-script.js:936-938` regardless of the above — no `.date-picker` element exists, it's pure dead weight either way.
- [ ] Once resolved, trim or delete `jquery-ui.css` accordingly (see CSS section below).

### 2. Dead JS plugin removal (confirmed dead above — delete file, script tag, CSS, and init block)

- [ ] `mixitup.js`
- [ ] `knob.js`
- [ ] `appear.js` (also removes the `.count-bar`/`.count-box`/`.dial` init blocks in `custom-script.js:776-853`)
- [ ] `jquery.fancybox.js` + `jquery.fancybox.min.css` (also removes `custom-script.js:941-944`)
- [ ] `isotope.js` (unreferenced file) + the dead `.post-filter`/`.filter-layout`/`.portfolio-masonary__filters` block, `custom-script.js:1107-1152`
- [ ] `nouislider.min.js`, `nouislider.min.css`, `nouislider.pips.css` (all unreferenced) + the dead `#range-slider-price` block, `custom-script.js:~95-122`
- [ ] Dead `.tabs-box` click-handler block in `custom-script.js` (no `.tabs-box` element in `index.html`) — not a vendored plugin, just inline dead code, low priority

### 3. CSS bloat audit

- [ ] `rtl.css`/`rtl.scss` — no `dir="rtl"`, language switcher, or any RTL-related markup found in `index.html`. Confirm no plan for multi-language support, then remove both the `<link>` and the SCSS partial.
- [ ] `jquery-ui.css` — once jQuery UI's fate (section 1) is decided: trim to just the `.ui-selectmenu-*`/`.ui-menu`/`.ui-widget` rules if kept, or delete entirely if replaced.
- [ ] Icon systems: both `flaticon-*` and `fa*/fab fa-*` classes are in active use (7 distinct icons each, confirmed by grep) — **not** a clear-cut duplicate to eliminate; consolidating to one system would mean re-mapping icons both ways for a purely cosmetic/maintenance win. Low priority, note only.
- [ ] General unused-selector sweep on `style.scss` once the above are resolved — a large fraction of the ~15,000-line stylesheet is Linoor theme sections/pages this single-page site never renders (e.g. `.trusted-section`, `.agency-section` spotted during an earlier grep for `.featured-block`) — worth a dedicated pass with a CSS-usage tool (e.g. PurgeCSS) rather than manual review given the file's size.

### 4. Process notes for whoever does this work

- Re-verify each "dead" finding above against the _current_ `index.html` before deleting anything — a class name could have changed since this audit was written.
- After any CSS change: recompile with `npx sass --watch src/frontend/static/css/style.scss src/frontend/static/css/style.css` (per `CLAUDE.md`) before testing.
- After any JS/CSS removal: manually test in a real browser — carousels (banner + testimonials), the parallax section, the FAQ accordion, the custom-cursor effect, and **both forms' full submit flow** (JS path and no-JS fallback) are the interactive surfaces most likely to break silently, per this repo's own history of silent JS/CSS failures (see `docs/development_journal.md`'s DOMPurify `.mjs` MIME-type gotcha).
- Do this incrementally — one plugin or CSS block per commit — so a regression is easy to bisect rather than buried in one large deletion.
- Once files are actually deleted, update `docs/architecture.md`'s "Note Worthly Scripts/Settings" table so it stops describing files that no longer exist.
