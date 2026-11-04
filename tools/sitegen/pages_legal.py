"""Legacy URL redirects and the 404 page; legal copy lives in pages_relaunch_more."""
from __future__ import annotations
from . import config as C
from .ui import layout, btn, e, asset

def not_found() -> str:
    body=f"""<section class="section"><div class="wrap">
    <p class="eyebrow">404 / Page not found</p>
    <h1>There isn't a page at this address.</h1>
    <p class="lede">Start with the online assessment, explore what it checks,
    or read a recorded example while public scan access is being prepared.</p>
    <div class="hero-actions">{btn("/scan/","Check scan availability","primary","arrow")}
    {btn("/sample-report/","See the sample report","ghost")}</div>
    </div></section>"""
    return layout("/404.html","Page Not Found | SMB Scanner Lite",
      "This page does not exist. Explore the domain assessment, scan coverage and recorded sample report.",
      body,noindex=True)

def redirect(target: str,title: str) -> str:
    """A self-contained static redirect for legacy GitHub Pages URLs."""
    url=C.SITE_URL+target
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow">
<title>Moved — {e(title)} | {e(C.SITE_NAME)}</title>
<link rel="canonical" href="{e(url)}">
<meta http-equiv="refresh" content="0; url={e(target)}">
<link rel="stylesheet" href="{asset('/styles.css')}">
<link rel="stylesheet" href="{asset('/studio.css')}">
</head><body><main id="main" class="wrap section">
<p class="eyebrow">Moved</p><h1>The page has a new home.</h1>
<p><a class="btn btn-primary" href="{e(target)}">Continue to {e(title)}</a></p>
</main></body></html>"""
