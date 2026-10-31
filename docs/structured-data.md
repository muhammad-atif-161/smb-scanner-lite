# Structured data: what the site publishes, and why

This document records the structured-data architecture of smbscannerlite.me,
the reasoning behind every type that is published or deliberately not
published, and how to re-validate it after a deploy.

Source of truth: `tools/sitegen/schema.py` (node builders) and
`tools/sitegen/ui.py` → `layout()` (graph assembly). No page hand-writes
JSON-LD any more; `tools/build_site.py --audit` fails the build if a forbidden
type, a relative URL, a dangling `@id` or a duplicated block appears.

---

## 1. What each page publishes now

Every page publishes exactly **one** `<script type="application/ld+json">`
containing one `@graph`:

| Part | Type | `@id` | Present on |
|------|------|-------|------------|
| Site-wide | `Organization` | `https://smbscannerlite.me/#organization` | every page |
| Site-wide | `WebSite` | `https://smbscannerlite.me/#website` | every page |
| Page | `WebPage` | `<canonical>#webpage` | every page |
| Page (role-specific) | `FAQPage` | … | `/faq/` |
| Page (role-specific) | `AboutPage` | … | `/about/` |
| Page (role-specific) | `ContactPage` | … | `/contact/`, `/request-assessment/` |
| Page (role-specific) | `CollectionPage` | … | `/resources/` |
| Subject | `SoftwareApplication` | `…/#software` | `/` only |
| Subject | `Report` | `<canonical>#report` | `/sample-report/` |
| Subject | `Article` | `<canonical>#article` | the eight `/resources/*` articles |
| Subject | `TechArticle` | `<canonical>#article` | `/methodology/`, `/docs/` |
| Subject | `ItemList` | `<canonical>#itemlist` | `/capabilities/` |
| Navigation | `BreadcrumbList` | `<canonical>#breadcrumb` | every page with visible breadcrumbs (24) |

Totals after remediation: 26 pages, 26 JSON-LD blocks, 115 nodes — 26
`Organization`, 26 `WebSite`, 21 `WebPage`, 4 role-specific page types, 8
`Article`, 2 `TechArticle`, 1 `Report`, 1 `ItemList`, 1 `SoftwareApplication`,
24 `BreadcrumbList`.

The `Organization` and `WebSite` nodes carry the same `@id` and the same facts
on every page, so the site describes one consistent set of entities instead of
26 unrelated documents. Every `{"@id": …}` reference used on a page is defined
in that page's own graph (the audit enforces this), so a consumer that parses a
single page never sees a dangling reference.

---

## 2. What was removed, and why

### `Product` + `Offer` on `/acquisition/`

The page offers a **complete software project for sale** — source, engine,
documentation, handover — at a negotiable price, with terms that also exist on
a marketplace listing. It was marked up as a retail `Product` with an `Offer`
(`price: 2999`, `availability: InStock`).

Search Console then asked, correctly, for the properties a merchant listing
needs:

| Search Console issue | Why it could not be fixed honestly |
|----------------------|------------------------------------|
| Missing field `image` | There is no product photograph. A stock or decorative image would misrepresent the item. |
| Invalid object type for `brand` | `brand` is a `Brand`; the value was `Organization`. Fixable in isolation, but it only matters for a listing Google cannot index as a merchant listing anyway. |
| Missing `shippingDetails` | Nothing is shipped. It is a one-off transfer of a software project, not a physical parcel. |
| Missing `hasMerchantReturnPolicy` | There is no return policy for a project acquisition, and inventing one would create a term that does not exist in the sale. |

`/acquisition/` is not a merchant storefront and there is no checkout. Scenario
B (complete the merchant listing) was therefore rejected: it would have
required inventing a product image, shipping terms and a return policy.
Scenario A (remove inappropriate markup) was applied. The page keeps a
`WebPage` node whose `about` is the software, and the price and terms remain in
the visible copy where they are already stated with their context.

**Consequence:** `/acquisition/` is no longer eligible for the merchant-listing
or product-snippet experiences, and no rich result is claimed for it. It
remains eligible for ordinary blue links and for the breadcrumb treatment of a
normal page.

### `offers` on the homepage `SoftwareApplication`

The homepage described the free public sandbox edition with
`offers: {price: "0", priceCurrency: "USD"}`. That is factually true, but the
Software app rich result needs `aggregateRating` or `review` as well, and the
site has no ratings and no customers who have left reviews. Publishing the
offer kept the entity in Google's product reporting with warnings that could
only be cleared by fabricating ratings. The `offers` node was removed; the
`SoftwareApplication` node itself stays because it accurately describes what
the site is about.

### `SoftwareApplication` on `/demo/`

The demo page publishes a *recording* of an assessment. It does not distribute
an application, and it had a second `SoftwareApplication` node with a different
name (`… recorded assessment demo`) and no `@id`. That duplicated and muddied
the application entity. It is now a plain `WebPage` whose `about` points at the
software.

### `Product`-snippet warnings (`review`, `aggregateRating`)

No review or rating data exists, is displayed, or will be invented. Both
affected items (`/acquisition/` and the homepage application node) are
addressed by removing the offer-bearing markup described above, so there is no
longer a product-snippet item that needs a rating to be eligible.

### `Organization.logo` pointing at an SVG

Google's logo documentation requires a raster image (at least 112×112) and does
not accept SVG. The entity now points at `/logo-512.png`, a 512×512 PNG
rendered from the same `logo.svg` artwork (which stays as the favicon and the
header mark). `apple-touch-icon.png` (180×180) was added for the same reason:
iOS does not use SVG touch icons.

---

## 3. What is deliberately **not** published

* **No `AggregateRating`, `Review`, `Offer`, `Product`, `MerchantReturnPolicy`
  or `OfferShippingDetails`** anywhere. `tools/sitegen/audit.py` treats these
  as forbidden types and fails the build if one returns.
* **No `SearchAction`/`potentialAction`** on `WebSite`: the site has no search
  function, so a sitelinks search box would be a dead control.
* **No `Person` entity with invented credentials, no `EducationalOccupational
  Credential`, no `Award`, no `sameAs` beyond the real GitHub profile and
  repository.**
* **No per-article `image`.** There are no article illustrations, and using the
  generic Open Graph card as each article's image would imply an image that is
  not on the page. Articles may therefore show a smaller (or no) image in
  Article enhancements — an accepted limitation rather than a fabrication.
* **No `FAQPage` rich result expectation.** The markup is valid and describes
  visible question/answer pairs, but since August 2023 Google only shows FAQ
  rich results for authoritative government and health sites. It is kept for
  accuracy and for consumers other than Google's rich results.
* **No structured data on `/404.html` beyond the site entities and a `WebPage`
  node** (that page is `noindex`).

---

## 4. Eligibility after remediation (honest expectations)

| Feature | Eligible? | Notes |
|---------|-----------|-------|
| Breadcrumbs | Yes | 24 pages with visible breadcrumbs and matching `BreadcrumbList`; display is not guaranteed. |
| Article / TechArticle | Yes (limited) | Truthful metadata, no `image`; may not receive a large image treatment. |
| Software app | No | Requires `aggregateRating`/`review`. Markup is descriptive; no rich result is claimed. |
| FAQ | No | Rich result restricted by Google policy to government/health sites. |
| Merchant listing / product snippet | N/A | Merchant markup removed. The reports will empty out after re-crawl. |
| Merchant listing on `/acquisition/` | No (by decision) | A project sale is not a retail product; see §2. |

Valid markup is not a promise of a rich result: Google decides display.

---

## 5. Validation

Local, on every build:

```bash
python3 tools/build_site.py --check --audit
```

The audit parses every JSON-LD block, checks the `@context`, absolute URLs,
`@id` resolution, breadcrumb positions, forbidden types, one block per page and
the raster logo URL.

After deploy, on the live URLs (these need a browser, so they run on your
machine, not in the build):

1. **Rich Results Test** — <https://search.google.com/test/rich-results>
   * `https://smbscannerlite.me/` → expect no rich-result types other than
     breadcrumbs; no errors.
   * `https://smbscannerlite.me/acquisition/` → expect *no* product or
     merchant-listing items.
   * `https://smbscannerlite.me/faq/` → FAQ markup valid, rich result unlikely.
   * `https://smbscannerlite.me/sample-report/` → `Report` is not a Google
     rich-result type; no errors expected.
2. **Schema Markup Validator** — <https://validator.schema.org> — check that
   `Organization`, `WebSite`, `WebPage` and page-specific nodes resolve and that
   no `@id` is dangling.
3. **Search Console** — *Merchant listings* and *Product snippets* reports.
   After the next crawl, the items disappear (the report should show **no items
   detected**, not six "valid" items). Use **Validate fix** only after a crawl
   has picked up the new HTML; validation can take days to weeks and cannot be
   completed from a local build.
