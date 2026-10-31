"""Static audit of the generated website.

`python3 tools/build_site.py --audit` runs every check here after a build. The
audit reads only what GitHub Pages will actually serve (the files under
`website/`), so it catches problems that a template-level review would miss:
duplicate `@id`s, dangling structured-data references, a canonical that
disagrees with its sitemap entry, an image without alt text, a heading that
skips a level, a form field with no label, or a page that accidentally became
`noindex`.

Levels
------
FAIL  something that is wrong for a visitor, a crawler or the structured-data
      graph. The command exits non-zero.
WARN  a judgement call or a threshold that a human should look at (for example
      an unusually long meta description). The command still exits 0, so the
      warning is visible without blocking a deploy.

The audit is deliberately dependency-free and regex-based, matching the rest of
the toolchain: it is a safety net, not a replacement for the W3C validator or
Google's Rich Results Test, which are the authoritative checks after deploy.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

# Types that must never appear again: they describe a retail product listing
# with shipping, returns and customer ratings, none of which exist here.
FORBIDDEN_TYPES = {
    "Product",
    "IndividualProduct",
    "ProductModel",
    "Offer",
    "AggregateOffer",
    "AggregateRating",
    "Review",
    "MerchantReturnPolicy",
    "OfferShippingDetails",
}

REFERENCE_KEYS = ("@id", "item", "url", "mainEntityOfPage", "logo", "image")


class Report:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, str]] = []

    def fail(self, where: str, message: str) -> None:
        self.items.append(("FAIL", where, message))

    def warn(self, where: str, message: str) -> None:
        self.items.append(("WARN", where, message))

    def count(self, level: str) -> int:
        return sum(1 for item in self.items if item[0] == level)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def page_path(rel: str) -> str:
    """Map an output file to the URL path it is served at."""
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value)


def is_redirect(html: str) -> bool:
    return "http-equiv=\"refresh\"" in html


def single(pattern: str, html: str):
    match = re.search(pattern, html, re.S)
    return match.group(1).strip() if match else None


def all_matches(pattern: str, html: str) -> list[str]:
    return [m.group(1) for m in re.finditer(pattern, html, re.S)]


def walk_graph(node, result: list[dict]) -> None:
    """Collect every dict node in a JSON-LD structure."""
    if isinstance(node, dict):
        result.append(node)
        for value in node.values():
            walk_graph(value, result)
    elif isinstance(node, list):
        for value in node:
            walk_graph(value, result)


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_head(rel: str, html: str, canonical_path: str, report: Report, site_url: str) -> str | None:
    where = rel
    title = single(r"<title>(.*?)</title>", html)
    if not title:
        report.fail(where, "missing <title>")
    else:
        plain = strip_tags(title)
        if not 15 <= len(plain) <= 65:
            report.warn(where, f"title is {len(plain)} characters (target 15-65)")
    description = single(r'<meta name="description" content="([^"]*)"', html)
    if not description:
        report.fail(where, "missing meta description")
    elif not 60 <= len(description) <= 165:
        report.warn(where, f"meta description is {len(description)} characters (target 60-165)")
    if html.count('name="description"') > 1:
        report.fail(where, "more than one meta description")

    if not re.search(r'<html[^>]*\slang="[a-z]{2}', html):
        report.fail(where, "<html> is missing a lang attribute")

    canonical = single(r'<link rel="canonical" href="([^"]*)"', html)
    if not canonical:
        report.fail(where, "missing canonical link")
    elif canonical != site_url + canonical_path:
        report.fail(where, f"canonical {canonical} does not match served path {canonical_path}")

    robots = single(r'<meta name="robots" content="([^"]*)"', html)
    if not robots:
        report.fail(where, "missing robots meta")
    elif "noindex" in robots and not is_redirect(html) and rel != "404.html":
        report.fail(where, "public page is marked noindex")

    og = {
        key: single(rf'<meta property="og:{key}" content="([^"]*)"', html)
        for key in ("title", "description", "url", "image", "type", "site_name")
    }
    for key, value in og.items():
        if not value:
            report.fail(where, f"missing og:{key}")
    if og.get("url") and canonical and og["url"] != canonical:
        report.fail(where, "og:url does not match canonical")
    if single(r'<meta name="twitter:card" content="(.*?)" />', html) != "summary_large_image":
        report.warn(where, "twitter:card is not summary_large_image")

    # Render-blocking third-party resources must not come back.
    if "fonts.googleapis.com" in html or "fonts.gstatic.com" in html:
        report.fail(where, "page still requests Google Fonts")
    for match in re.finditer(r'<script src="([^"]+)"([^>]*)>', html):
        src, attrs = match.group(1), match.group(2)
        if " defer" not in attrs and " async" not in attrs and " type=\"module\"" not in attrs:
            report.warn(where, f"script {src} is render-blocking (no defer/async)")
    # Scroll-revealed content must be visible without JavaScript: the hidden
    # state is scoped to `.js`, which only the inline bootstrap adds.
    if 'class="no-js"' not in html:
        report.fail(where, "<html> is missing the no-js class (reveal fallback)")
    if 'replace("no-js","js")' not in html:
        report.warn(where, "missing the inline js bootstrap that enables reveal animation")
    if 'class="skip-link"' not in html:
        report.fail(where, "missing skip link")
    return canonical


def check_structured_data(rel: str, html: str, report: Report, site_url: str,
                          canonical: str | None) -> None:
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if len(blocks) != 1:
        report.fail(rel, f"expected exactly one JSON-LD block, found {len(blocks)}")
    if not blocks:
        return

    try:
        data = json.loads(blocks[0])
    except json.JSONDecodeError as exc:
        report.fail(rel, f"JSON-LD does not parse: {exc}")
        return

    if data.get("@context") != "https://schema.org":
        report.fail(rel, "JSON-LD @context is not https://schema.org")
    graph = data.get("@graph")
    if not isinstance(graph, list) or not graph:
        report.fail(rel, "JSON-LD has no @graph array")
        return

    nodes: list[dict] = []
    walk_graph(graph, nodes)

    for node in nodes:
        node_type = node.get("@type")
        type_names = node_type if isinstance(node_type, list) else [node_type]
        for name in type_names:
            if name in FORBIDDEN_TYPES:
                report.fail(rel, f"forbidden structured-data type {name} is back")

    defined = {node["@id"] for node in nodes if isinstance(node.get("@id"), str)}

    for node in nodes:
        for key in REFERENCE_KEYS:
            value = node.get(key)
            values = value if isinstance(value, list) else [value]
            for entry in values:
                if not isinstance(entry, str):
                    continue
                if entry.startswith("#"):
                    report.fail(rel, f"{key} uses a fragment-only reference {entry}")
                elif entry.startswith("/"):
                    report.fail(rel, f"{key} is not an absolute URL: {entry}")
                elif entry.startswith("http://"):
                    report.fail(rel, f"{key} is insecure http:// URL: {entry}")

    # Every {"@id": ...} used as a value must be defined in this page's graph.
    for node in nodes:
        for value in node.values():
            for entry in value if isinstance(value, list) else [value]:
                if isinstance(entry, dict) and set(entry.keys()) == {"@id"}:
                    if entry["@id"] not in defined:
                        report.fail(rel, f"dangling @id reference {entry['@id']}")

    types = [node.get("@type") for node in graph]
    if "Organization" not in types or "WebSite" not in types:
        report.fail(rel, "graph is missing the site-wide Organization/WebSite entities")

    for node in graph:
        if node.get("@type") == "Organization":
            logo = node.get("logo")
            logo_url = logo.get("url") if isinstance(logo, dict) else logo
            if not logo_url or logo_url.endswith(".svg"):
                report.fail(rel, "Organization logo must be a raster image URL")
        if node.get("@type") == "BreadcrumbList":
            items = node.get("itemListElement", [])
            positions = [item.get("position") for item in items]
            if positions != list(range(1, len(items) + 1)):
                report.fail(rel, "breadcrumb positions are not sequential")
            if items and "item" in items[-1]:
                report.warn(rel, "breadcrumb last item should omit the URL")
            if "<nav class=\"breadcrumbs\"" not in html:
                report.fail(rel, "BreadcrumbList published without visible breadcrumbs")

    page_kinds = {"WebPage", "AboutPage", "ContactPage", "CollectionPage", "FAQPage", "ItemPage"}
    if not any(node.get("@type") in page_kinds for node in graph):
        report.fail(rel, "graph has no WebPage-type node")


def check_content(rel: str, html: str, report: Report) -> None:
    headings = [(int(level), strip_tags(text)) for level, text in
                re.findall(r"<h([1-6])[^>]*>(.*?)</h\1>", html, re.S)]
    h1s = [text for level, text in headings if level == 1]
    if len(h1s) != 1:
        report.fail(rel, f"expected exactly one <h1>, found {len(h1s)}")
    previous = 0
    for level, text in headings:
        if previous and level > previous + 1:
            report.fail(rel, f"heading level jumps from h{previous} to h{level} ({text[:60]!r})")
        previous = level

    ids = re.findall(r'\sid="([^"]+)"', html)
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        report.fail(rel, f"duplicate id attribute(s): {', '.join(duplicates[:5])}")

    for tag in re.findall(r"<img\b[^>]*>", html):
        if " alt=" not in tag:
            report.fail(rel, f"image without alt attribute: {tag[:100]}")
        if " width=" not in tag or " height=" not in tag:
            report.warn(rel, f"image without width/height (layout shift risk): {tag[:100]}")

    # Form controls must be labelled, either explicitly (label[for]) or by
    # wrapping the control in a <label> (implicit association).
    label_for = set(re.findall(r'<label[^>]*\sfor="([^"]+)"', html))
    wrapped = [(m.start(), m.end()) for m in re.finditer(r"<label\b[^>]*>.*?</label>", html, re.S)]
    for match in re.finditer(r"<(?:input|select|textarea)\b[^>]*>", html):
        control = match.group(0)
        if 'type="hidden"' in control or 'type="submit"' in control:
            continue
        if "aria-label=" in control or "aria-labelledby=" in control:
            continue
        control_id = re.search(r'\sid="([^"]+)"', control)
        if control_id and control_id.group(1) in label_for:
            continue
        if any(start <= match.start() < end for start, end in wrapped):
            continue
        report.fail(rel, f"form control without an associated label: {control[:100]}")

    for opening, content in re.findall(r"(<button\b[^>]*>)(.*?)</button>", html, re.S):
        named = (
            strip_tags(content).strip()
            or "aria-label=" in opening
            or "aria-labelledby=" in opening
            or 'title="' in opening
        )
        if not named:
            report.fail(rel, f"button with no accessible name: {opening[:90]}")

    for match in re.finditer(r'<a\b[^>]*href="(http://[^"]+)"', html):
        report.fail(rel, f"insecure external link: {match.group(1)}")
    if re.search(r'<a\b[^>]*href="#"[^>]*>', html) or 'href="javascript:' in html:
        report.fail(rel, "placeholder or javascript: link")


def check_assets(rel: str, html: str, out: Path, report: Report) -> None:
    # Versioned assets must carry the hash of the file that is actually on disk,
    # otherwise a deploy could serve new HTML against a stale cached script.
    for ref, version in re.findall(r'(/(?:styles\.css|site\.js|config\.js))\?v=([0-9a-f]+)', html):
        target = out / ref.lstrip("/")
        if not target.exists():
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()[:8]
        if version != actual:
            report.fail(rel, f"stale version for {ref}: page says {version}, file is {actual}")

    for ref in re.findall(r'(?:href|src)="(/[^"#?]*)(?:\?[^"#]*)?"', html):
        target = out / ref.lstrip("/") if not ref.endswith("/") else out / ref.lstrip("/") / "index.html"
        if not target.exists():
            report.fail(rel, f"missing asset {ref}")
    if 'rel="preload"' in html and "as=\"font\"" in html:
        if "crossorigin" not in html.split('as="font"')[1][:80]:
            report.fail(rel, "font preload without crossorigin attribute")


def check_sitemap_robots(out: Path, pages: dict, redirects: dict, report: Report,
                         config, noindex_paths: set[str]) -> None:
    sitemap_file = out / "sitemap.xml"
    if not sitemap_file.exists():
        report.fail("sitemap.xml", "file is missing")
        return
    sitemap = sitemap_file.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>(.*?)</loc>", sitemap)

    expected = {page_path(rel) for rel in pages if rel != "404.html"}
    extra = [loc for loc in locs if loc.replace(config.SITE_URL, "") not in expected]
    if extra:
        report.fail("sitemap.xml", f"lists URLs that are not canonical pages: {extra[:3]}")
    listed = {loc.replace(config.SITE_URL, "") for loc in locs}
    absent = sorted(expected - listed)
    if absent:
        report.fail("sitemap.xml", f"canonical pages missing from sitemap: {absent[:5]}")
    for loc in locs:
        if not loc.startswith(config.SITE_URL):
            report.fail("sitemap.xml", f"non-absolute URL: {loc}")
    for path in listed & noindex_paths:
        report.fail("sitemap.xml", f"noindex page listed in sitemap: {path}")
    for rel in redirects:
        if page_path(rel) in listed:
            report.fail("sitemap.xml", f"legacy redirect listed in sitemap: {page_path(rel)}")

    robots = (out / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {config.SITE_URL}/sitemap.xml" not in robots:
        report.fail("robots.txt", "missing sitemap reference")
    for rule in re.findall(r"^Disallow:\s*(\S+)", robots, re.M):
        for loc in locs:
            if loc.replace(config.SITE_URL, "").startswith(rule):
                report.fail("robots.txt", f"Disallow {rule} blocks a sitemap URL")


def check_duplicates(canonicals: dict[str, str], titles: dict[str, str],
                     descriptions: dict[str, str], report: Report) -> None:
    for label, mapping in (("canonical", canonicals), ("title", titles),
                           ("description", descriptions)):
        seen: dict[str, list[str]] = {}
        for page, value in mapping.items():
            if value:
                seen.setdefault(value, []).append(page)
        for value, page_names in seen.items():
            if len(page_names) > 1:
                report.fail(page_names[0], f"duplicate {label} shared with {len(page_names) - 1} other page(s): {value[:70]}")


def check_secrets(out: Path, report: Report) -> None:
    patterns = {
        "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "AWS access key": r"AKIA[0-9A-Z]{16}",
        "GitHub token": r"gh[pousr]_[A-Za-z0-9]{36,}",
        "generic bearer token": r"Bearer\s+[A-Za-z0-9\-._~+/]{30,}",
    }
    for path in sorted(out.rglob("*")):
        if not path.is_file() or path.suffix in {".png", ".woff2", ".ico"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in patterns.items():
            if re.search(pattern, text):
                report.fail(str(path.relative_to(out)), f"possible {label} in a published file")

    for path in sorted(out.rglob("*")):
        name = path.name
        if name.startswith(".") and name not in {".nojekyll"}:
            report.fail(str(path.relative_to(out)), "unexpected dotfile published")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(out: Path, config, data, pages: dict, redirects: dict) -> int:
    report = Report()
    html_files = sorted(out.rglob("*.html"))

    canonicals: dict[str, str] = {}
    titles: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    noindex_paths: set[str] = set()

    for path in html_files:
        rel = str(path.relative_to(out))
        html = path.read_text(encoding="utf-8")

        if rel.startswith("downloads/"):
            # Downloadable report artefacts: not site pages, but they must stay
            # noindex and fully self-contained (no remote requests when a
            # visitor opens the saved file).
            if "noindex" not in html:
                report.fail(rel, "downloadable report must be noindex")
            for ref in re.findall(r'src="(https?://[^"]+)"', html):
                report.fail(rel, f"downloadable report loads a remote resource: {ref}")
            for ref in re.findall(r'<link[^>]+href="(https?://[^"]+)"', html):
                report.fail(rel, f"downloadable report loads a remote resource: {ref}")
            if "<script" in html:
                report.fail(rel, "downloadable report should not run scripts")
            continue

        expected_path = page_path(rel)
        if is_redirect(html):
            canonical = single(r'<link rel="canonical" href="([^"]*)"', html)
            if not canonical or canonical == config.SITE_URL + expected_path:
                report.fail(rel, "legacy redirect canonical must point at the new URL")
            if "noindex" not in html:
                report.fail(rel, "legacy redirect should be noindex")
            if 'http-equiv="refresh"' not in html:
                report.fail(rel, "legacy redirect without meta refresh")
            check_assets(rel, html, out, report)
            continue

        canonical = check_head(rel, html, expected_path, report, config.SITE_URL)
        if canonical:
            canonicals[rel] = canonical
        title = single(r"<title>(.*?)</title>", html)
        if title:
            titles[rel] = strip_tags(title)
        description = single(r'<meta name="description" content="([^"]*)"', html)
        if description:
            descriptions[rel] = description
        robots = single(r'<meta name="robots" content="([^"]*)"', html) or ""
        if "noindex" in robots:
            noindex_paths.add(expected_path)

        check_structured_data(rel, html, report, config.SITE_URL, canonical)
        check_content(rel, html, report)
        check_assets(rel, html, out, report)

    # Redirect targets must exist and be indexable.
    for rel in redirects:
        html = (out / rel).read_text(encoding="utf-8")
        target = single(r'http-equiv="refresh" content="0; url=(.*?)"', html)
        if not target:
            report.fail(rel, "redirect page has no refresh target")
        elif target + "index.html" not in pages and target.lstrip("/") + "index.html" not in pages:
            report.fail(rel, f"redirect target {target} is not a generated page")

    check_duplicates(canonicals, titles, descriptions, report)
    check_sitemap_robots(out, pages, redirects, report, config, noindex_paths)
    check_secrets(out, report)

    for level, where, message in report.items:
        print(f"  {level}  {where}: {message}")

    fails, warns = report.count("FAIL"), report.count("WARN")
    state = "FAILED" if fails else "passed"
    print(f"audit: {state} - {len(html_files)} pages, {fails} error(s), {warns} warning(s)")
    return 1 if fails else 0
