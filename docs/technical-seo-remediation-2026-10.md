# Technical SEO, structured data and performance remediation — October 2026

Repository: `muhammad-atif-161/smb-scanner-lite` · Site: <https://smbscannerlite.me>
Branch: `arena/7f92d23e-smb-scanner-lite` · Scope: the statically generated site in
`website/` and the generator in `tools/`.

This document is the audit, the plan, the implementation record and the
verification evidence for the Search Console and Lighthouse issues that were
reported. It deliberately separates **what was measured** from **what could not
be measured here** and from **what needs the deployed site or Google's own
validation**.

---

## 0. Honest statement of what this environment could and could not verify

| Capability | Available here? | Consequence for this report |
|------------|-----------------|-----------------------------|
| Read/write the repository, run the generator | Yes | All source and generated-HTML findings below are first-hand. |
| Parse and validate every JSON-LD block | Yes | Structured-data inventory, `@id` graph and policy checks are measured. |
| HTML conformance validator (`html-validate`, recommended ruleset) | Yes | 0 errors after the fixes; see §5.3. |
| Headless DOM test of `site.js` (jsdom) | Yes | Navigation, reveal, tabs, accordions, forms checked; see §5.4. |
| Lighthouse / Chrome Performance traces | **No** — no browser engine and no way to install one (the sandbox can only reach package registries, not browser download hosts) | **No before/after Lighthouse score, LCP, CLS or TBT numbers are reported.** All performance figures below are static measurements (bytes, request counts, blocking chains, code paths). |
| Fetch the live site (`https://smbscannerlite.me`) | **No** — outbound access is restricted to package registries and GitHub | Deployed response headers, live HTML and live structured data are **not** verified here. §7 gives the exact commands to do it. |
| Google Rich Results Test / Search Console validation | **No** | Rich-result eligibility is reasoned from documentation, not demonstrated. |

Everything that follows is either measured on this machine or explicitly
labelled as inference.

---

## 1. Phase 1 — Baseline audit

### 1.1 What the site is, architecturally

* Zero-dependency Python generator: `tools/build_site.py` + `tools/sitegen/`
  (`config`, `data`, `snippets`, `ui`, `pages_*`).
* 26 pages, 7 legacy redirect stubs, 1 downloadable standalone HTML report,
  `sitemap.xml`, `robots.txt`, `config.js`, `data/recorded-assessment.json` and
  four report downloads are all produced by the same build.
* Deployed by `.github/workflows/deploy-pages.yml` → GitHub Pages, static
  upload, no build step on the runner. Committed output in `website/`.
* Design system: one stylesheet (`website/styles.css`), one script
  (`website/site.js`), runtime configuration (`website/config.js`).
* Build baseline: `python3 tools/build_site.py --check` → *"built 26 pages, 7
  redirects"*, *"link check: 34 pages, all internal links resolve"*. No warnings,
  no errors. The generator itself was healthy; the problems were in what it
  emitted.

### 1.2 Structured-data inventory (baseline)

25 JSON-LD blocks, one per page except `/404.html`, 46 nodes:

| Type | Count | Where |
|------|-------|-------|
| `BreadcrumbList` | 24 | most pages |
| `Article` | 8 | knowledge base |
| `ContactPage` | 2 | `/contact/`, `/request-assessment/` |
| `SoftwareApplication` | 2 | `/` (with `Offer`), `/demo/` |
| `TechArticle` | 2 | `/methodology/`, `/docs/` |
| `AboutPage`, `CollectionPage`, `FAQPage`, `ItemList`, `Report` | 1 each | as named |
| **`Product`** | **1** | **`/acquisition/`, with an `Offer` (price 2999 USD, `InStock`)** |
| `WebSite`, `Organization` | 1 each | **homepage only** |

### 1.3 Root causes, issue by issue

#### A. Merchant listings — "missing `image`" (critical), "missing `shippingDetails`", "invalid object type for `brand`", "missing `hasMerchantReturnPolicy`" (4 items)

**Root cause.** `/acquisition/` published a `Product` node with an `Offer`:

```python
# tools/sitegen/pages_contact.py (before)
schema={
    "@type": "Product",
    "name": "SMB Scanner Lite — complete project acquisition",
    "brand": {"@type": "Organization", "name": C.SITE_NAME},   # brand is a Brand
    "offers": {"@type": "Offer", "price": "2999", "priceCurrency": "USD",
               "availability": "https://schema.org/InStock", ...},
}
```

* It described a **business asset sale** (the whole project, transferred with
  handover) as a retail product.
* `brand` was typed `Organization`; the schema.org domain for `brand` is
  `Brand`, which is exactly the "invalid object type" Search Console reported.
* There is no product image, no shipping and no return policy — none of which
  can be invented truthfully for a software project sale.

**Was the warning valid?** Yes, on all four counts, and the warning was a
symptom rather than the disease: the markup claimed a merchant listing that
does not exist.

**Which of the reported items?** The repository contains exactly **one**
`Product` item, so a count of four items means Google saw the same markup on
four crawled URLs (for example `/acquisition/` and `/acquisition` variants, a
mobile crawl, or the previous deploy still in the index). Because the markup is
removed entirely, the count is moot after re-crawl: there is no merchant
markup left anywhere for Google to count. This mapping is **inference**, not
something that could be observed from here.

**Decision.** Scenario A — remove the inappropriate merchant markup. Scenario B
(complete the listing with `image`, `shippingDetails`, `hasMerchantReturnPolicy`)
was rejected because every missing property would have had to be fabricated.
Full reasoning: [`docs/structured-data.md`](structured-data.md) §2.

#### B. Product snippets — "missing `review`", "missing `aggregateRating`" (2 items)

**Root cause.** Two offer-bearing nodes with no rating data:

1. `/acquisition/` `Product` + `Offer` (above).
2. Homepage `SoftwareApplication` with `offers: {price: "0", priceCurrency:
   "USD"}`. The Software app / product treatment requires `aggregateRating` or
   `review`; the site has neither, and no visitor has ever been asked to leave
   one.

**Was the warning valid?** Structurally yes. It is unanswerable by design: the
only honest fix is to stop claiming an offer, not to invent a rating.

**Remediation.** `/acquisition/` no longer publishes a product; the homepage
`SoftwareApplication` no longer publishes `offers`. No `review`,
`aggregateRating` or hidden rating text was added anywhere. `Review`,
`AggregateRating` and `Offer` are now on the build's forbidden-type list
(`tools/sitegen/audit.py`).

#### C. Site-wide structured-data architecture

Found by auditing the whole graph, not just the six reported items:

| Problem | Detail | Fix |
|---------|--------|-----|
| Site entities existed on one page only | `Organization`/`WebSite` were defined on `/` and nowhere else, so 24 pages described themselves with no publisher, no site and no stable `@id` | Shared `Organization` + `WebSite` nodes with stable `@id`s emitted on every page by `layout()` |
| No page node anywhere | Pages were described by `Article`/`ItemList`/`Product` nodes only; a page that is not an article had no `WebPage` | Every page now emits a `WebPage`-family node with `url`, `name`, `description`, `isPartOf`, `inLanguage`, `breadcrumb` |
| Conflicting application entities | Two `SoftwareApplication` nodes (homepage `#software`; `/demo/` with a different name and no `@id`) | One `SoftwareApplication` with `@id …/#software` on `/`; `/demo/` is a `WebPage` whose `about` is the software |
| Invalid property types | `brand: Organization`; `author: Organization` where a person wrote the article; `Organization.logo` as an SVG (Google requires raster) | `brand` gone with the product; article authors are `Person`; logo is a 512×512 PNG |
| Duplicate large schema blocks in templates | Full `WebSite`/`Organization`/`SoftwareApplication` literal in `pages_home.py` | Builders in `tools/sitegen/schema.py`; no page writes JSON-LD by hand |
| `BreadcrumbList` not addressable | 24 breadcrumb nodes with no `@id`, no link from the page node | `@id = <canonical>#breadcrumb`, referenced from the page node |
| Unused import `jsonld` in `pages_trust.py` | Dead code from an earlier approach | Removed |

#### D. Render-blocking resources (~740 ms potential saving)

**Measured baseline (homepage, cache-cold):**

| Resource | Origin | Blocking? | Size |
|----------|--------|-----------|------|
| HTML document | 1st party | — | 57.7 KB (12.4 KB gzip) |
| `https://fonts.googleapis.com/css2?family=Inter…&family=JetBrains+Mono…&family=Space+Grotesk…` | **3rd party** | **yes** | small file, ~750 ms reported by Lighthouse |
| `/styles.css` | 1st party | yes | 62.9 KB (11.3 KB gzip) |
| `/config.js` | 1st party | **yes** (classic script, no `defer`) | 1.5 KB |
| `/site.js` | 1st party | no (`defer`) | 30.6 KB (8.3 KB gzip) |
| Font files (up to 8: Inter 400/500/600, JetBrains Mono 400/500, Space Grotesk 500/600/700) | **3rd party** `fonts.gstatic.com` | after the CSS hop | ~160 KB total |

Plus `<link rel="preconnect">` to `fonts.googleapis.com` and
`fonts.gstatic.com`.

**Root cause.** Three typefaces were loaded from Google Fonts, so the critical
chain was: HTML → third-party CSS → third-party font files, in series with
`/styles.css`. Two extra origins, two preconnects, one extra blocking
stylesheet, and a synchronous `config.js` at the end of the body.

**Not the root cause.** The stylesheet itself: 11.3 KB gzipped, one same-origin
request, used by all 26 pages. Splitting it into "critical" and "deferred" CSS
would duplicate rules across 26 pages, add a flash-of-unstyled-content risk and
save little. It was left as a single blocking stylesheet *by decision*, and the
external font chain — the part that actually crossed the network twice — was
removed.

#### E. Largest Contentful Paint — 2,520 ms element render delay, 0 ms TTFB

**Analysis.** TTFB of 0 ms means the document was served from cache or a local
proxy; the 2,520 ms is entirely element render delay. Three code facts explain
how that delay reaches the largest text:

1. **Nothing could paint until two stylesheets arrived**, one of them a
   third-party request that in turn ordered the font files (D above).
2. **The hero was invisible by design.** `.hero-rise` (the eyebrow, the `<h1>`,
   the lede, the actions, the meta row) started at `opacity: 0` and animated
   in over 0.7 s with per-child delays, and `animation-fill-mode: forwards`
   (not `both`), so the pre-animation state was the invisible base rule.
3. **Below-fold content was also invisible** until `site.js` ran and an
   `IntersectionObserver` added `.is-visible` (238 `.reveal` elements).

Chrome does not count a fully transparent element as painted. With the hero
transparent at first paint, the largest *painted* text could be the header
brand (`SMB Scanner Lite`) — which matches the element Lighthouse reported —
and LCP then moved to the hero only once the font chain had resolved and the
animation had run. That is a coherent explanation for a ~2.5 s render delay
with a cached document, but it is **an inference from the code and the reported
diagnostics; it was not confirmed with a trace in this environment** (§7 shows
how to confirm it in DevTools).

**Root causes addressed:** the third-party font chain (D), the `opacity: 0`
start state of above-the-fold content (E2), and the synchronous `config.js`.
Below-fold reveal animation was left in place, because it cannot affect LCP.

#### F. Forced reflow at `site.js:87`

```js
// website/site.js, before (line 87, column 49 = window.scrollY)
var syncNav = function () {
  nav.classList.toggle("is-scrolled", window.scrollY > 8);
};
syncNav();
window.addEventListener("scroll", syncNav, { passive: true });
```

Two problems, in this order:

1. `syncNav()` ran during initialisation, **after** the reveal loop had written
   a `--reveal-delay` inline style to all 238 `.reveal` elements. Those writes
   invalidate style; the `window.scrollY` read immediately requires an up-to-date
   layout, so the whole document was laid out synchronously during startup.
   Lighthouse attributes that to the reading line (87:49).
2. Even after load, every scroll event toggled a class and then read the scroll
   offset — a read-after-write in the same frame, on the main thread, for every
   scroll tick.

**Fix.** A 1×8 px `.scroll-sentinel` pinned to the top of the document is
observed by an `IntersectionObserver`; the class is applied only when the state
actually changes. No layout read remains in the scroll path. The per-element
stagger writes were replaced by six `:nth-child` rules in CSS, so no inline
style is written at startup at all. A `requestAnimationFrame`-throttled scroll
handler was *not* used: it would still read `scrollY` 60 times a second to
achieve what the observer gets for free.

The resize handler was also reordered (`if (!panel.hidden && innerWidth > 1080)`)
so it does not read layout when the mobile panel is closed.

#### G. Cache lifetime — 22 KiB, ~10 minutes

**Root cause: the host, not the site.** GitHub Pages serves every file with
`Cache-Control: max-age=600` and offers no way to override response headers
(no `_headers` support, no server config). The reported "10 minutes" is exactly
that platform default. No repository change can raise it.

**What was done instead.** The build appends a content hash to the three
unhashed, frequently-changing URLs:

```html
<link rel="stylesheet" href="/styles.css?v=c8f893d1" />
<script src="/config.js?v=…" defer></script>
<script src="/site.js?v=…" defer></script>
```

The URL changes when the file changes, so a returning visitor can never be
served a stale stylesheet from the ten-minute window. The Lighthouse
"cache lifetime" audit will still report ~10 minutes for these assets: that is
a hosting limitation, reported honestly rather than papered over.

`config.js` was treated deliberately: it contains only public runtime values
(contact address, form endpoint, allowlist, data URL) that are already rendered
into the HTML, so versioning it is safe and nothing sensitive is cached.

#### H. Smaller findings from the site-wide audit

| Finding | Status |
|---------|--------|
| Downloadable report had unescaped `&` (4 HTML conformance errors) | Fixed — all interpolated values escaped |
| `apple-touch-icon` pointed at an SVG (iOS ignores it) | Fixed — 180×180 PNG |
| `Organization.logo` was an SVG (Google requires raster) | Fixed — 512×512 PNG |
| Privacy policy said fonts were loaded from Google Fonts | **Fixed** — policy text updated, `POLICY_VERSION` bumped to `2026.10-sandbox-v2` |
| Terms §7 referenced Google Fonts | Fixed |
| 20 page titles and 14 meta descriptions outside the usual length targets | **Deliberately unchanged** — see §6 |
| 404 page had no structured data | Now gets site entities + `WebPage`; still `noindex` |
| Content could stay invisible if `site.js` failed | `.reveal`'s hidden state is now scoped to `.js`, added by a one-line inline bootstrap; without that class every section is simply visible. The `<noscript>` patch is gone. |
| Sitemap, robots, canonicals, legacy redirects, heading order, alt text, `og:*`, internal links | Audited, no defects found; now enforced by `--audit` |
| `logo.svg` gradient on a zero-height path never renders (in any browser) | **Not changed** — a pre-existing artwork quirk; fixing it would alter the mark |

---

## 2. Phase 2 — Remediation plan (prioritised)

| # | Problem | Files | Change | Risk | Verification |
|---|---------|-------|--------|------|--------------|
| 1 | Merchant/product markup misrepresenting an asset sale | `pages_contact.py`, `pages_home.py`, new `schema.py`, `ui.py` | Remove `Product`/`Offer`; keep accurate types; one graph per page | Low (loses product-snippet eligibility that could not be used legitimately) | `--audit` forbidden-type check; Rich Results Test after deploy |
| 2 | Site-wide entity graph inconsistent | `schema.py`, all `pages_*` | Site entities with stable `@id`s + page node on every page | Low | `--audit` graph checks |
| 3 | Third-party blocking font chain | `ui.py`, `styles.css`, new `website/fonts/` | Self-host 8 latin WOFF2 faces (SIL OFL), `font-display: swap`, preload the two above-the-fold faces, drop both preconnects | Medium (visual regression if metrics differ) | Byte/request comparison; visual check; licence file |
| 4 | LCP delay | `styles.css` (hero), `ui.py` | Hero entrance becomes transform-only (no `opacity: 0`); fonts preloaded; `config.js` deferred | Low (subtle motion change) | Manual visual check; trace after deploy |
| 5 | Forced reflow | `site.js`, `styles.css` | Sentinel + `IntersectionObserver`; CSS stagger; resize ordering | Medium (header state, mobile panel) | jsdom smoke test (§5.4) |
| 6 | Cache lifetime | `build_site.py`, `ui.py` | Content-hash query strings on CSS/JS/config | Low | Hash changes on edit; no stale files |
| 7 | HTML conformance, touch icon, logo | `build_site.py`, `schema.py`, new PNGs | Escape values; PNG icons | Low | `html-validate`; image inspection |
| 8 | Privacy/terms text accuracy | `pages_legal.py`, `config.py` | Describe self-hosted assets; bump policy version | Low | Read the diff; policy page renders |

---

## 3. Phase 3 — Implementation

### 3.1 Files added

| File | Purpose |
|------|---------|
| `tools/sitegen/schema.py` | All structured-data builders and the design rules (no merchant markup, no ratings, stable `@id`s). |
| `tools/sitegen/audit.py` | 20+ static checks over the built site (structured data, head/canonical/robots, headings, labels, links, assets, sitemap/robots consistency, secrets, forbidden types). Wired to `--audit`. |
| `website/fonts/*.woff2` (8 files) | Self-hosted latin subsets of Inter 400/500/600, Space Grotesk 500/600/700, JetBrains Mono 400/500 — the exact weights the CSS uses. |
| `website/fonts/OFL.txt` | Copyright notices + full SIL OFL 1.1 text (redistribution requirement). |
| `website/logo-512.png`, `website/apple-touch-icon.png` | Raster logo for `Organization.logo` (Google requires raster) and for iOS. |
| `docs/structured-data.md` | Structured-data report: retained/removed types, reasoning, eligibility, validation. |
| `docs/technical-seo-remediation-2026-10.md` | This document. |

### 3.2 Files modified

| File | Change |
|------|--------|
| `tools/sitegen/ui.py` | Head rewritten (no Google Fonts, font preloads, PNG icons, versioned asset URLs, no-js bootstrap); `layout()` now builds one `@graph` from site entities + page node + page extras + breadcrumbs; `config.js`/`site.js` deferred; asset-version plumbing; `<noscript>` style hack and dead `crumb_schema()` removed. |
| `tools/sitegen/pages_home.py` | Inline `WebSite`/`Organization`/`SoftwareApplication` literal replaced by `schema.software_application()`, page node gains `mainEntity`; `offers` removed. |
| `tools/sitegen/pages_contact.py` | `Product`/`Offer` removed from `/acquisition/`; `ContactPage` nodes now come from the shared builder. |
| `tools/sitegen/pages_product.py` | `ItemList`, `Report`, `TechArticle` via builders; demo page no longer declares a second application entity. |
| `tools/sitegen/pages_resources.py` | `Article` nodes via builder with `mainEntityOfPage`; index page is a `CollectionPage`. |
| `tools/sitegen/pages_trust.py` | `FAQPage` main entity built from the same data the page renders; `AboutPage` via `page_type`; unused `jsonld` import removed. |
| `tools/sitegen/pages_legal.py` | Privacy §6 rewritten (no third-party requests), terms §7 updated, effective date, redirect stubs use the versioned stylesheet. |
| `tools/sitegen/config.py` | `POLICY_VERSION` → `2026.10-sandbox-v2` with the reason recorded. |
| `tools/build_site.py` | `config_js_source()` split out; `apply_asset_versions()`; escape values in the downloadable report; `--audit` flag. |
| `website/styles.css` | §0 self-hosted `@font-face` (8 faces, `font-display: swap`, unicode-range); `.scroll-sentinel`; hero entrance transform-only; CSS reveal stagger; reveal hidden-state scoped to `.js`. |
| `website/site.js` | Sentinel + `IntersectionObserver` nav state; CSS-based stagger (no inline writes); resize ordering; comments explaining why. |
| `README.md` | Documents self-hosting, `--audit`, and the new docs. |
| `website/**/*.html`, `website/sitemap.xml`, `website/data/recorded-assessment.json`, `website/downloads/*.html` | Regenerated by the build (no hand edits). |

### 3.3 What was deliberately *not* done

* No framework, no bundler, no new runtime dependency. The generator is still
  standard-library Python; the site is still plain HTML/CSS/JS on GitHub Pages.
* No service worker (it would add a cache-invalidation problem, not solve one).
* No critical-CSS inlining: it would duplicate rules across 26 pages for a
  12.9 KB gzip same-origin file.
* No font subsetting beyond the latin subset the licensed packages ship, and no
  `font-display: optional` (it can leave a page permanently in fallback fonts).
* No title/description rewrites (see §6).
* No change to any scanning behaviour, allowlist, consent logic, form handling
  or `site.contact.json`.

---

## 4. Phase 4/5 — Local verification

### 4.1 Build and internal consistency

```
$ python3 tools/build_site.py --check --audit
built 26 pages, 7 redirects into /home/user/smb-scanner-lite/website
link check: 34 pages, all internal links resolve
audit: passed - 34 pages, 0 error(s), 30 warning(s)
```

All 26 pages, 7 redirects, sitemap, robots, config, data and downloads are
regenerated. The 30 warnings are all title/description length notices (§6).

### 4.2 Structured data

* 26 blocks (was 25), 115 nodes (was 46), every block parses.
* `Product`, `Offer`, `Review`, `AggregateRating`, `MerchantReturnPolicy`,
  `OfferShippingDetails`: **0 occurrences** (enforced).
* Every `@id` reference on a page resolves inside that page's graph
  (enforced by the audit).
* Every `url`/`item`/`logo`/`mainEntityOfPage` value is an absolute `https://`
  URL (enforced).
* `BreadcrumbList` items are sequential (1..n), the last item has no URL, and
  every breadcrumb list has visible breadcrumbs above it (enforced).
* `Organization.logo` is `/logo-512.png` (512×512 PNG, verified by reading the
  file back).

### 4.3 HTML conformance

`html-validate` (v9, `html-validate:recommended`) over all 34 HTML files, with
only stylistic rules disabled (`void-style`, `attr-quotes`,
`attribute-boolean-style`, `no-trailing-whitespace`, `no-inline-style`,
`long-title`, `require-sri`):

```
✖ 0 problems
```

Before the fixes it reported 4 `no-raw-characters` errors in the downloadable
report (now escaped).

### 4.4 JavaScript behaviour (jsdom)

A jsdom harness evaluated `config.js` + `site.js` against 12 representative
pages (home, demo, FAQ, capabilities, sample report, request-assessment,
contact, acquisition, privacy, docs, methodology, an article) and asserted:

* no runtime errors on load;
* `document.documentElement` carries the `no-js` class from the server-rendered
  HTML, and the inline bootstrap is present in `<head>` (so a browser with
  JavaScript blocked or a failed `site.js` shows every section rather than a
  page of invisible panels);
* `.scroll-sentinel` inserted and observed; simulated intersection toggles
  `.nav.is-scrolled` on and off;
* reveal observer registered for every `.reveal` element and elements become
  visible; **no inline `--reveal-delay` written**;
* mobile panel: starts closed, opens on click, `aria-expanded` flips, focus
  moves into the panel, `Escape` closes it;
* tab groups switch (`aria-selected`, one visible panel);
* expand-all / collapse-all works;
* footer year filled.

```
smoke: all checks passed
```

### 4.5 Self-hosted font coverage

The eight WOFF2 files are the `latin` subsets. To make sure that subsetting
cannot silently change the design, every non-ASCII character on all 34
generated HTML files was checked against the `unicode-range` declared in
`styles.css`: **0 characters fall outside the shipped ranges** (the site uses
`—`, `·`, `–`, `©`, `…`, `→`-free ASCII arrows and similar). Nothing will fall
back to a system font because of subsetting. Characters outside the ranges would
fall back exactly as they did with Google's `latin` subset before.

### 4.6 Assets and routes

The scanner's own test suite is untouched and still passes
(`PYTHONPATH=src python3 -m unittest discover -s tests`; it needs `PYTHONPATH=src`
because the package is not pip-installed here — a pre-existing requirement).

Served from a local static server, all 200: `/`, `/styles.css?v=…`,
`/site.js?v=…`, `/config.js`, each font, `/fonts/OFL.txt`, `/logo-512.png`,
`/apple-touch-icon.png`, `/sitemap.xml`, `/robots.txt`, `/demo/`, `/faq/`.
Font files are served as `font/woff2`; the stylesheet resolves all 8 `url()`
references; CSS braces balance (510/510).

---

## 5. Performance: measured before/after (static), and limits

### 5.1 Measured on this machine

| Metric | Before | After | Note |
|--------|--------|-------|------|
| Render-blocking stylesheets | **2** (Google Fonts CSS + `/styles.css`) | **1** (`/styles.css`) | |
| Blocking scripts in `<head>`/body-end | **1** (`config.js`, no `defer`) | **0** | both scripts deferred |
| Third-party origins contacted | **2** (`fonts.googleapis.com`, `fonts.gstatic.com`) | **0** | |
| `preconnect` hints | 2 | 0 (obsolete, removed) | no unused hints added |
| Font requests | from a CDN, behind a blocking CSS hop | 8 same-origin faces, 2 preloaded, rest on demand, `font-display: swap` | same families and weights → no visual change from weights |
| `styles.css` | 62,962 B raw / 11,250 B gzip | 69,192 B raw / 12,890 B gzip | +1.6 KB gzip: the `@font-face` rules |
| `site.js` | 30,559 B raw / 8,340 B gzip | 31,989 B raw / 8,815 B gzip | +475 B gzip: sentinel logic + comments |
| `config.js` | 1,514 B | 1,514 B | now deferred |
| Inline style writes at startup | **238** (`--reveal-delay` on every `.reveal`) | **0** | |
| Layout reads in the scroll path | 1 per scroll event | **0** | IntersectionObserver |
| Above-fold text hidden at first paint | hero (`opacity: 0`) | **nothing** | |
| Asset URL freshness | fixed URLs, 10-min TTL | content-hashed URLs | |

### 5.2 What this should do to the reported diagnostics (inference)

* **Render-blocking (~740 ms):** the third-party stylesheet and its preconnects
  are gone. The remaining blocking request is one 12.9 KB gzip same-origin
  stylesheet. Expect a large reduction, not zero — the first-party stylesheet
  must still arrive before paint.
* **LCP element render delay (2,520 ms):** the two serialised cross-origin hops
  are removed, the two faces that affect the hero are preloaded, and the hero
  text now paints opaque in the first frame instead of waiting for an opacity
  animation. Expect a substantial improvement; the exact number depends on the
  connection and cannot be produced here.
* **Forced reflow (~69 ms + 49 ms unattributed):** the `scrollY` read that
  Lighthouse pinned to `site.js:87` no longer exists, and the 238 startup style
  writes are gone.
* **Cache lifetime (~22 KiB):** will still be reported, because GitHub Pages
  fixes `max-age=600`. The staleness *risk* is fixed; the TTL cannot be.

### 5.3 How to produce the numbers this environment could not

Run on a machine with Chrome (both form factors, 3+ runs, report the median):

```bash
# Lab runs against production
npx lighthouse https://smbscannerlite.me/ --form-factor=mobile \
  --throttling-method=simulate --output=json --output=html \
  --output-path=./lh-mobile-after
npx lighthouse https://smbscannerlite.me/ --preset=desktop \
  --output=json --output=html --output-path=./lh-desktop-after

# Repeat for /acquisition/, /demo/, /faq/ and one article
```

To confirm the LCP element and its dependency chain, open DevTools →
Performance → record a reload with network throttling ("Slow 4G") and CPU 4×,
then read *Timings* → **LCP** and the *Critical request chain* panel. Check that
the LCP element is now the hero `<h1>` or the header brand and that it paints
within the first ~1 s at that throttling, with no font request before it.

Field data (CrUX) will only move once there is enough real traffic; a site this
size may never clear the 75th-percentile reporting threshold. That is a data
limitation, not a code one.

---

## 6. Phase 6 — Deployment and regression

### 6.1 Deployment

Deployment still happens through `.github/workflows/deploy-pages.yml` (static
upload of `website/` on push to `main`). Nothing in the workflow changed: no
build step was added, no secret, no service. The generated output is committed,
as before.

**This branch has not been deployed and the live site was not reachable from
this environment**, so no live header, live HTML or live rich-result check has
been performed. After merging, run:

```bash
# Headers: confirm the platform TTL and that fonts are served from the origin
curl -sI https://smbscannerlite.me/styles.css | grep -i -E 'cache-control|content-type'
curl -sI https://smbscannerlite.me/fonts/inter-latin-400-normal.woff2

# Confirm no third-party references remain in the deployed HTML
curl -s https://smbscannerlite.me/ | grep -c 'fonts.googleapis.com'   # expect 0

# Confirm the merchant markup is gone from the live acquisition page
curl -s https://smbscannerlite.me/acquisition/ | grep -c '"@type":"Product"'   # expect 0
```

Then: Rich Results Test on `/`, `/acquisition/`, `/faq/`, `/sample-report/`
(see `docs/structured-data.md` §5), and Search Console → **Validate fix** for
both reports. Validation is not complete until Google re-crawls; the items
should disappear rather than become "valid", because the markup is gone.

### 6.2 Regression checklist

| Area | Method | Result |
|------|--------|--------|
| All 26 pages generate | build output | pass |
| Internal links (34 files, every `href`/`src`/`#anchor`) | `--check` | pass |
| Legacy redirects (7) | audit: `noindex`, canonical → target, target exists | pass |
| Sitemap = canonical indexable pages, redirects/404 excluded | audit | pass |
| `robots.txt` sitemap reference, `Disallow: /downloads/` blocks nothing in the sitemap | audit | pass |
| Canonical/`og:url` agree with served path on every page | audit | pass |
| One `<h1>` per page, no skipped heading levels | audit | pass |
| Every `<img>` has `alt` + dimensions | audit (2 images: logo in header/footer, both decorative `alt=""`) | pass |
| Form controls labelled (explicit `label[for]` or wrapping `<label>`) | audit | pass |
| Navigation, mobile panel, Escape, focus management | jsdom smoke | pass |
| Tabs, accordions, copy-to-clipboard wiring, footer year | jsdom smoke | pass |
| Enquiry forms still compose/POST exactly as before | unchanged code path; smoke test exercises page load | pass (behaviour untouched) |
| Privacy policy reachable, text now accurate | `/privacy/` regenerated | pass |
| Sample reports and downloads (HTML/JSON/CSV/TXT) | regenerated; audit checks the HTML artefact is `noindex` and self-contained | pass |
| Capability catalogue, methodology, docs | regenerated; schema validated | pass |
| Public demo restrictions unchanged | `config.ALLOWED_DOMAINS` untouched; `/data/recorded-assessment.json` unchanged in content | pass |
| No secrets in published files | audit scans for private keys/tokens/`ghp_`/`AKIA`/bearer tokens and unexpected dotfiles | pass |
| Design identity | same tokens, fonts (same families/weights), spacing, colours; only the hero entrance lost its fade | reviewed |
| Reduced motion | `.reveal`/`.hero-rise` still forced visible; animation durations collapsed | unchanged |

### 6.3 Response header reality check

| Asset | Intended policy | What GitHub Pages actually sends |
|-------|-----------------|----------------------------------|
| `/styles.css?v=`, `/site.js?v=`, `/config.js?v=` | long-lived immutable | `max-age=600` (platform default, not configurable) |
| `/fonts/*.woff2` | long-lived immutable | `max-age=600` |
| `/logo-512.png`, `/apple-touch-icon.png` | long-lived | `max-age=600` |
| HTML | short | `max-age=600` |

The only way to set real cache headers is to put a CDN or another host in front
of GitHub Pages — an infrastructure decision with a cost/approval implication,
therefore listed as a recommendation (§8, #2) rather than implemented.

---

## 7. Deliverable A — Root-cause summary

| Reported issue | Valid? | Cause | Code change? | Verified by |
|----------------|--------|-------|--------------|-------------|
| Merchant: missing `image` | Yes | `Product` on `/acquisition/` describing a project sale | Markup removed | audit forbidden-type check |
| Merchant: missing `shippingDetails` | Yes | Same; nothing is shipped | Markup removed | audit |
| Merchant: invalid `brand` type | Yes | `brand: Organization` instead of `Brand` | Markup removed | audit |
| Merchant: missing `hasMerchantReturnPolicy` | Yes | Same; no return policy exists | Markup removed | audit |
| Product snippet: missing `review` | Yes | Offer-bearing nodes, no reviews exist | Offers removed | audit |
| Product snippet: missing `aggregateRating` | Yes | Same, no ratings exist | Offers removed | audit |
| Render-blocking ~740 ms | Yes | Google Fonts CSS + 8 fonts on 2 extra origins, blocking | Fonts self-hosted, preloaded, preconnects dropped | static request audit |
| LCP render delay 2,520 ms | Yes | Serialised cross-origin font chain + hero at `opacity: 0` | Font chain removed, hero paints opaque immediately | code + inference (§1.3 E) |
| Forced reflow `site.js:87` | Yes | `window.scrollY` read after 238 style writes, plus per-scroll read/write | Sentinel + observer; CSS stagger | jsdom smoke + code |
| Cache lifetime ~22 KiB | Partly | Host sets `max-age=600`; site cannot change it | Content-hashed URLs (correctness, not TTL) | build output; §6.3 |
| Site-wide schema gaps | — | Found by audit, not reported | Shared builders, page nodes, raster logo | audit |

---

## 8. Deliverable F — Outstanding issues

1. **No Lighthouse/lab numbers before or after.** No browser engine here. Use
   §5.3. Until then, the performance claims in §5.2 are inferences, and the
   static measurements in §5.1 are the hard evidence.
2. **No live verification.** The deployed HTML, headers, fonts and rich results
   were not checked from this environment (§6.1 has the commands).
3. **Cache TTL remains 10 minutes.** Needs a different host or a CDN in front of
   GitHub Pages (see §9, #2). Local mitigation (hashed URLs) is in place.
4. **30 title/description length warnings.** 20 titles exceed ~65 characters and
   14 descriptions exceed ~165, so SERP snippets will be truncated. Left alone
   because the brief requires preserving existing metadata and because editing
   them is a content/SEO judgement about pages that are already indexed. The
   audit keeps reporting them so the decision stays visible.
5. **FAQ markup earns no rich result** (Google policy since Aug 2023) and
   **`SoftwareApplication` cannot earn the software-app rich result** without
   ratings. Both are documented rather than "fixed" with invented data.
6. **Articles have no `image` property.** Adding one would require real
   illustrations per article.
7. **The hero no longer fades in** (it slides 12 px). This is a deliberate,
   documented visual change to keep the largest text out of an `opacity: 0`
   state. If the fade is wanted back, it must not start from full transparency.
8. **`logo.svg` has a gradient painted on a zero-height path** that no browser
   renders. Harmless (the mark still looks intentional) but it means the left
   half of the scan line never appears. Fixing it changes the logo artwork and
   was left out of scope.
9. **Search Console cannot be validated from here**, and validation only counts
   after Google re-crawls. The items should disappear, not turn "valid".
10. **A future Content-Security-Policy must account for the inline bootstrap.**
    The one-line `no-js` → `js` script in `<head>` is inline; under a strict CSP
    it needs a SHA-256 hash (or nonce) rather than `unsafe-inline`. It is listed
    here so that the CSP in recommendation #2 does not silently break the
    reveal fallback.
11. **`sitemap.xml` `lastmod` changes on every build** (build date), which makes
    the sitemap diff noisy but is not incorrect.

---

## 9. Deliverable G — Next three highest-value improvements

1. **Measure, then decide.** Run Lighthouse (mobile + desktop, 3 runs, median)
   and a DevTools trace on production for `/`, `/acquisition/` and `/demo/`.
   Effort: ~1 hour. Risk: none. Everything else in this list is guesswork until
   that exists — and it will show whether the remaining blocking stylesheet or
   the hero's blurred radial background (`.hero::before` with `filter: blur(10px)`
   over a 620 px tall element) is the next real cost.
2. **Move to a host that allows response headers** (GitHub Pages + Cloudflare
   proxy, Netlify, or Cloudflare Pages). Effort: 1–2 hours plus a DNS change.
   Risk: medium (deployment change). It is the only way to fix cache lifetimes
   honestly, and it would also enable HSTS, `X-Content-Type-Options`,
   `Referrer-Policy` and a real CSP — none of which a security project should
   be missing. This needs your approval because it changes infrastructure.
3. **Add a small build-time content check to the audit for *content* quality**
   — canonical URLs that are orphaned from internal links, keyword-bearing
   titles, and description lengths — then make the 30 existing warnings a
   deliberate, reviewed change in one pass. Effort: 1–2 hours. Risk: low (title
   changes can shift rankings politely). This is the largest remaining SEO
   gain, but it is a content decision, not a bug.

Deliberately **not** recommended: converting the stylesheet to async loading,
inlining critical CSS per page, adding a service worker, adding analytics, or
splitting `site.js` — each costs maintenance or correctness for no measured
user benefit at this size.
