"""Shared layout, components and icons for the generated website.

No template engine: pages are composed from small functions that return HTML
strings. Keeping it dependency-free means `python3 tools/build_site.py` is the
whole toolchain.
"""

from __future__ import annotations

import html
import json

from . import config as C
from . import schema as structured


# ---------------------------------------------------------------------------
# Icons (24x24, stroke based, decorative unless a title is supplied)
# ---------------------------------------------------------------------------

_PATHS = {
    "arrow": '<path d="M4 12h15"/><path d="M13 6l6 6-6 6"/>',
    "arrow-up-right": '<path d="M8 16L16 8"/><path d="M9.5 8H16v6.5"/>',
    "chevron": '<path d="M6 9.5l6 6 6-6"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.4-3 7.6-7 9-4-1.4-7-4.6-7-9V6l7-3z"/><path d="M9 12.2l2.2 2.2L15.4 10"/>',
    "shield-alert": '<path d="M12 3l7 3v6c0 4.4-3 7.6-7 9-4-1.4-7-4.6-7-9V6l7-3z"/><path d="M12 8v5"/><circle cx="12" cy="16.2" r="0.9" fill="currentColor" stroke="none"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17"/><path d="M12 3.5c2.5 2.4 3.8 5.3 3.8 8.5S14.5 18.1 12 20.5C9.5 18.1 8.2 15.2 8.2 12S9.5 5.9 12 3.5z"/>',
    "mail": '<rect x="3" y="6" width="18" height="12" rx="2.5"/><path d="M4 8.5l8 5.5 8-5.5"/>',
    "lock": '<rect x="4.5" y="10.5" width="15" height="9.5" rx="2.5"/><path d="M8 10.5V8a4 4 0 018 0v2.5"/>',
    "server": '<rect x="3.5" y="4" width="17" height="7" rx="2"/><rect x="3.5" y="13" width="17" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01"/>',
    "network": '<rect x="9" y="3" width="6" height="5" rx="1.5"/><rect x="2.5" y="16" width="6" height="5" rx="1.5"/><rect x="15.5" y="16" width="6" height="5" rx="1.5"/><path d="M12 8v4M5.5 16v-4h13v4"/>',
    "list": '<path d="M9 6.5h11M9 12h11M9 17.5h11"/><path d="M4 6.5l1 1 1.6-1.6"/><path d="M4 12l1 1 1.6-1.6"/><path d="M4 17.5l1 1 1.6-1.6"/>',
    "chart": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16v-3.5M12.5 16V8M17 16v-6"/>',
    "gauge": '<path d="M4 17a8.5 8.5 0 1116 0"/><path d="M12 17l4-5"/>',
    "file": '<path d="M14 3.5H7.5A2.5 2.5 0 005 6v12a2.5 2.5 0 002.5 2.5h9A2.5 2.5 0 0019 18V8.5L14 3.5z"/><path d="M14 3.5V9h5"/>',
    "code": '<path d="M9 8l-4 4 4 4"/><path d="M15 8l4 4-4 4"/>',
    "terminal": '<rect x="3" y="4.5" width="18" height="15" rx="2.5"/><path d="M7.5 9.5l2.5 2.5-2.5 2.5"/><path d="M12.5 14.5H16"/>',
    "check": '<path d="M4 12.5l4.5 4.5L20 6.5"/>',
    "check-circle": '<circle cx="12" cy="12" r="8.5"/><path d="M8.2 12.3l2.5 2.5 5-5.4"/>',
    "alert": '<path d="M12 4.5l8.5 15h-17l8.5-15z"/><path d="M12 10v4"/><circle cx="12" cy="16.6" r="0.9" fill="currentColor" stroke="none"/>',
    "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5"/><circle cx="12" cy="7.8" r="0.9" fill="currentColor" stroke="none"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "copy": '<rect x="8.5" y="8.5" width="11" height="11" rx="2"/><path d="M15.5 8.5V6.5a2 2 0 00-2-2h-7a2 2 0 00-2 2v7a2 2 0 002 2h2"/>',
    "download": '<path d="M12 4v10"/><path d="M8 10.5l4 4 4-4"/><path d="M5 19h14"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.5"/><path d="M12 4v2M12 18v2M4 12h2M18 12h2"/>',
    "eye": '<path d="M2.5 12s3.5-6.5 9.5-6.5S21.5 12 21.5 12s-3.5 6.5-9.5 6.5S2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "scale": '<path d="M12 4v16"/><path d="M6 8h12"/><path d="M6 8L3 15h6L6 8z"/><path d="M18 8l-3 7h6l-3-7z"/><path d="M8 20h8"/>',
    "bell": '<path d="M6.5 17V11a5.5 5.5 0 1111 0v6"/><path d="M5 17h14"/><path d="M10 20h4"/>',
    "layers": '<path d="M12 3.5l8 4.5-8 4.5-8-4.5 8-4.5z"/><path d="M4 12.5l8 4.5 8-4.5"/><path d="M4 16.5l8 4.5 8-4.5"/>',
    "key": '<circle cx="8.5" cy="12" r="3.5"/><path d="M12 12h8"/><path d="M17 12v3M20 12v2.5"/>',
    "route": '<circle cx="6" cy="7" r="2.5"/><circle cx="18" cy="17" r="2.5"/><path d="M6 9.5v3A3.5 3.5 0 009.5 16h6"/>',
    "fingerprint": '<path d="M12 4.5c-4.1 0-7.5 3.4-7.5 7.5 0 1.6.5 3 1.3 4.2"/><path d="M12 8a4 4 0 014 4c0 2.4-.6 4.6-1.6 6.5"/><path d="M9.6 19.2A9 9 0 018 17.5"/><path d="M12 11.5c.9 0 1.5.7 1.5 1.5 0 2-.5 3.9-1.3 5.5"/>',
    "bolt": '<path d="M13 3L5.5 13h5L10 21l7.5-10h-5L13 3z"/>',
    "book": '<path d="M4 5.5A2 2 0 016 3.5h13v15H6a2 2 0 00-2 2v-15z"/><path d="M19 18.5v3H6a2 2 0 01-2-2"/>',
    "scale-doc": '<rect x="4" y="3.5" width="16" height="17" rx="2.5"/><path d="M8 8.5h8M8 12h8M8 15.5h5"/>',
    "user": '<circle cx="12" cy="8.5" r="3.5"/><path d="M5 20c0-3.3 3.1-6 7-6s7 2.7 7 6"/>',
    "sparkle": '<path d="M12 3.5l1.8 5.2 5.2 1.8-5.2 1.8L12 17.5l-1.8-5.2L5 10.5l5.2-1.8L12 3.5z"/>',
    "link": '<path d="M10.5 13.5a3.5 3.5 0 004.9 0l3-3a3.5 3.5 0 00-4.9-5l-1.6 1.6"/><path d="M13.5 10.5a3.5 3.5 0 00-4.9 0l-3 3a3.5 3.5 0 004.9 5l1.6-1.6"/>',
    "external": '<path d="M14 4h6v6"/><path d="M20 4l-8.5 8.5"/><path d="M18 14v4.5A2.5 2.5 0 0115.5 21h-9A2.5 2.5 0 014 18.5v-9A2.5 2.5 0 016.5 7H11"/>',
}


def icon(name: str, size: int = 20, cls: str = "") -> str:
    paths = _PATHS.get(name, _PATHS["shield"])
    cls_attr = f' class="{cls}"' if cls else ""
    return (
        f'<svg{cls_attr} viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
        'aria-hidden="true" stroke="currentColor" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round">{paths}</svg>'
    )


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def e(value: object) -> str:
    """Escape text for HTML."""
    return html.escape(str(value), quote=True)


def jsonld(data: object) -> str:
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        + "</script>"
    )


# ---------------------------------------------------------------------------
# Versioned static assets
# ---------------------------------------------------------------------------
# GitHub Pages serves every file with `cache-control: max-age=600` and does not
# allow custom headers, so a deploy can leave a visitor on a stale stylesheet
# for up to ten minutes. The builder therefore appends a short content hash to
# the CSS/JS/configuration URLs: when a file changes, its URL changes, and the
# browser fetches it immediately instead of reusing the cached copy.
_ASSET_VERSIONS: dict[str, str] = {}


def set_asset_versions(mapping: dict[str, str]) -> None:
    _ASSET_VERSIONS.clear()
    _ASSET_VERSIONS.update(mapping)


def asset(path: str) -> str:
    version = _ASSET_VERSIONS.get(path)
    return f"{path}?v={version}" if version else path


def btn(href: str, label: str, variant: str = "primary", icon_name: str = "", external: bool = False) -> str:
    classes = f"btn btn-{variant}"
    icon_html = icon(icon_name, 18, "btn-icon") if icon_name else ""
    rel = ' rel="noopener"' if external else ""
    target = ' target="_blank"' if external else ""
    return f'<a class="{classes}" href="{e(href)}"{rel}{target}>{icon_html}<span>{e(label)}</span></a>'


def pill(text: str, tone: str = "info", mono: bool = False) -> str:
    mono_cls = " mono" if mono else ""
    return (
        f'<span class="pill pill-{tone}{mono_cls}"><span class="dot dot-{tone}" aria-hidden="true"></span>{e(text)}</span>'
    )


def eyebrow(text: str) -> str:
    return f'<p class="eyebrow">{e(text)}</p>'


def section_head(kicker: str, heading: str, lede: str = "", align: str = "left") -> str:
    lede_html = f'<p class="section-lede">{lede}</p>' if lede else ""
    return (
        f'<div class="section-head reveal" data-align="{align}">'
        f"{eyebrow(kicker)}<h2>{heading}</h2>{lede_html}</div>"
    )


def breadcrumbs(items) -> str:
    """items: [(label, href|None), ...] - last item is the current page."""
    parts = []
    for label, href in items:
        if href:
            parts.append(f'<li><a href="{e(href)}">{e(label)}</a></li>')
        else:
            parts.append(f'<li><span aria-current="page">{e(label)}</span></li>')
    return (
        '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>'
        + "".join(parts)
        + "</ol></nav>"
    )


def cta_band(title: str, text: str, primary=("/demo/", "Open the recorded demo"), secondary=("/sample-report/", "View a sample report")) -> str:
    return f"""
<section class="section">
  <div class="wrap">
    <div class="cta-band reveal">
      <div class="cta-band-text">
        <h2>{title}</h2>
        <p>{text}</p>
      </div>
      <div class="cta-band-actions">
        {btn(primary[0], primary[1], "primary", "arrow")}
        {btn(secondary[0], secondary[1], "ghost")}
      </div>
    </div>
  </div>
</section>"""


def notice(text: str, tone: str = "info", title: str = "", icon_name: str = "info") -> str:
    title_html = f"<strong>{title}</strong>" if title else ""
    return (
        f'<div class="notice notice-{tone} reveal">{icon(icon_name, 18, "notice-icon")}'
        f'<div class="notice-body">{title_html}<p>{text}</p></div></div>'
    )


# ---------------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------------

def nav_html(active: str) -> str:
    links = []
    for key, label, href in C.NAV:
        current = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="{href}"{current}>{e(label)}</a>')
    panel_links = []
    for key, label, href in C.NAV:
        current = ' aria-current="page"' if key == active else ""
        panel_links.append(f'<a href="{href}"{current}>{e(label)}</a>')
    return f"""
<a class="skip-link" href="#main">Skip to content</a>
<header class="nav" data-nav>
  <div class="wrap nav-inner">
    <a class="brand" href="/" aria-label="{C.SITE_NAME} home">
      <img src="/logo.svg" width="32" height="32" alt="" />
      <span class="brand-text">SMB Scanner <span class="brand-lite">Lite</span></span>
    </a>
    <nav class="nav-links" aria-label="Primary">
      {''.join(links)}
    </nav>
    <div class="nav-actions">
      <a class="btn btn-primary btn-sm" href="/demo/">{icon('bolt', 16, 'btn-icon')}<span>Try the Demo</span></a>
      <button class="nav-toggle" type="button" data-nav-toggle aria-label="Open menu" aria-expanded="false" aria-controls="nav-panel">
        <span data-nav-open>{icon('menu', 22)}</span>
        <span data-nav-close hidden>{icon('x', 22)}</span>
      </button>
    </div>
  </div>
</header>
<div class="nav-panel" id="nav-panel" data-nav-panel hidden>
  <nav class="nav-panel-links" aria-label="Mobile">
    {''.join(panel_links)}
  </nav>
  <div class="nav-panel-foot">
    <a class="btn btn-primary" href="/demo/">{icon('bolt', 16, 'btn-icon')}<span>Try the Demo</span></a>
    <a class="btn btn-ghost" href="/request-assessment/">Request an assessment</a>
  </div>
</div>"""


def footer_html() -> str:
    columns = []
    for title, links in C.FOOTER_COLUMNS:
        items = []
        for label, href in links:
            external = href.startswith("http")
            attrs = ' rel="noopener" target="_blank"' if external else ""
            items.append(f'<li><a href="{e(href)}"{attrs}>{e(label)}</a></li>')
        columns.append(f'<div class="foot-col"><h3>{e(title)}</h3><ul>{"".join(items)}</ul></div>')
    return f"""
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand-col">
        <a class="foot-brand" href="/">
          <img src="/logo.svg" width="30" height="30" alt="" />
          <span>SMB Scanner <span class="brand-lite">Lite</span></span>
        </a>
        <p class="foot-desc">An evidence-first external security posture assessment for small and medium businesses. 22 controls, a 0&ndash;100 score and an A&ndash;F grade &mdash; with the observation behind every conclusive finding. The public edition is restricted to five approved test domains.</p>
        <p class="foot-meta"><span class="mono">v{C.PRODUCT_VERSION}</span> &middot; {e(C.EDITION)}</p>
        <div class="foot-mails">{''.join(f'<a class="foot-mail" href="mailto:{e(address)}">{icon("mail", 16)}<span>{e(address)}</span></a>' for address in C.CONTACT_EMAILS)}</div>
      </div>
      {''.join(columns)}
    </div>
    <div class="foot-bottom">
      <p>&copy; <span data-year>2026</span> {e(C.AUTHOR)} &middot; {e(C.SITE_NAME)} &middot; Built in Rawalpindi, Pakistan.</p>
      <p class="foot-bottom-links">
        <a href="/privacy/">Privacy</a>
        <a href="/terms/">Terms</a>
        <a href="/responsible-use/">Responsible use</a>
        <a href="{C.REPO_URL}" rel="noopener" target="_blank">GitHub</a>
      </p>
    </div>
  </div>
</footer>
<div class="toast-region" id="toastRegion" aria-live="polite" aria-atomic="false"></div>"""


def layout(
    path: str,
    title: str,
    description: str,
    body: str,
    *,
    active: str = "",
    crumbs=None,
    schema=None,
    page_type: str = "WebPage",
    page_extra: dict | None = None,
    og_type: str = "website",
    noindex: bool = False,
    extra_head: str = "",
    body_class: str = "",
) -> str:
    canonical = C.SITE_URL + path
    robots = (
        "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    )
    og_image = f"{C.SITE_URL}/og-image.png"

    # One @graph per page: site entities, a page node typed to the page's role,
    # page-specific nodes, and a BreadcrumbList only where breadcrumbs are
    # rendered. See tools/sitegen/schema.py for the rules and the reasoning.
    schema_html = jsonld(
        structured.graph(
            path,
            title,
            description,
            kind=page_type,
            extras=schema,
            crumbs=crumbs,
            page_extra=page_extra,
        )
    )
    crumb_html = breadcrumbs(crumbs) if crumbs else ""

    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8" />
<script>document.documentElement.className=document.documentElement.className.replace("no-js","js");</script>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{e(title)}</title>
<meta name="description" content="{e(description)}" />
<link rel="canonical" href="{canonical}" />
<meta name="robots" content="{robots}" />
<meta name="author" content="{e(C.AUTHOR)}" />
<meta name="theme-color" content="#080B14" />
<meta name="generator" content="SMB Scanner Lite static site builder" />
<meta property="og:site_name" content="{C.SITE_NAME}" />
<meta property="og:type" content="{og_type}" />
<meta property="og:title" content="{e(title)}" />
<meta property="og:description" content="{e(description)}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{og_image}" />
<meta property="og:image:alt" content="SMB Scanner Lite — a dark navy assessment report showing a posture score of 86 out of 100, grade B, with evidence-backed findings." />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:locale" content="en_US" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{e(title)}" />
<meta name="twitter:description" content="{e(description)}" />
<meta name="twitter:image" content="{og_image}" />
<link rel="icon" href="/logo.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180" />
<link rel="alternate" type="application/json" href="/data/recorded-assessment.json" title="Recorded assessment data (JSON)" />
<link rel="stylesheet" href="{asset('/styles.css')}" />
<link rel="preload" href="/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin />
<link rel="preload" href="/fonts/space-grotesk-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin />
{extra_head}
{schema_html}
</head>
<body class="{body_class}">
{nav_html(active)}
<main id="main">
{crumb_html}
{body}
</main>
{footer_html()}
<script src="{asset('/config.js')}" defer></script>
<script src="{asset('/site.js')}" defer></script>
</body>
</html>
"""
