"""Central configuration for the SMB Scanner Lite website build.

Everything that is repeated across pages (site identity, navigation, footer,
contact routes, structured data defaults) lives here so that a change is made
once. The generated HTML is what GitHub Pages serves from `website/`.
"""

from __future__ import annotations

SITE_NAME = "SMB Scanner Lite"
SITE_TAGLINE = "Evidence-First External Security Posture Assessment"
SITE_URL = "https://smbscannerlite.me"
AUTHOR = "Muhammad Atif"
AUTHOR_URL = "https://github.com/muhammad-atif-161"
REPO_URL = "https://github.com/muhammad-atif-161/smb-scanner-lite"
LISTING_URL = "https://www.sideprojectors.com/project/104650/smb-scanner"

# ---------------------------------------------------------------------------
# Contact route - single source of truth
# ---------------------------------------------------------------------------
# Everything about the published contact address lives in site.contact.json at
# the repository root. The build reads it here and regenerates website/config.js
# from the same values, so the HTML and the browser can never disagree.
#   python3 tools/set_contact.py --email you@example.com
#   (or run the "Change contact email" workflow from the GitHub UI)
import json as _json
from pathlib import Path as _Path

CONTACT_FILE = _Path(__file__).resolve().parents[2] / "site.contact.json"

_CONTACT_DEFAULTS = {
    "primary_email": "myself.atiff@gmail.com",
    "additional_emails": [],
    "form_endpoint": "",
}


def _load_contact() -> dict:
    data = dict(_CONTACT_DEFAULTS)
    try:
        raw = _json.loads(CONTACT_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return data
    if isinstance(raw.get("primary_email"), str) and raw["primary_email"].strip():
        data["primary_email"] = raw["primary_email"].strip()
    extra = raw.get("additional_emails")
    if isinstance(extra, list):
        data["additional_emails"] = [
            str(item).strip() for item in extra if str(item).strip()
        ]
    if isinstance(raw.get("form_endpoint"), str):
        data["form_endpoint"] = raw["form_endpoint"].strip()
    return data


CONTACT = _load_contact()

# Primary first, duplicates removed, order preserved.
CONTACT_EMAILS = tuple(
    dict.fromkeys([CONTACT["primary_email"], *CONTACT["additional_emails"]])
)
CONTACT_EMAIL = CONTACT_EMAILS[0]
FORM_ENDPOINT = CONTACT["form_endpoint"]

PRODUCT_VERSION = "5.2.0"
EDITION = "Public Sandbox Edition"
# Bumped when the privacy policy text changes. v2 (31 October 2026) records the
# removal of the third-party Google Fonts request: the site now serves every
# asset, including its typefaces, from its own origin.
POLICY_VERSION = "2026.10-sandbox-v2"
BUILD_VERSION = "2026.10"

# Recorded assessment metadata (genuine sandbox capture, see website/data).
RECORDED_DATE = "2026-10-28"
RECORDED_TIMESTAMP = "2026-10-28T17:25:30Z"
RECORDED_REPORT_ID = "SMB-SANDBOX-20261028-A91144E4"
RECORDED_CONSENT_ID = "CONSENT-20261028-A91144E4"
RECORDED_RECEIPT_SHA256 = (
    "b068e643725c90429199d458b31a0749b08b4af1caae57fe4ea8878f412820a6"
)

ALLOWED_DOMAINS = (
    "example.com",
    "example.org",
    "example.net",
    "scanme.nmap.org",
    "badssl.com",
)

# Primary navigation. `key` is used for aria-current and the active state.
NAV = (
    ("home", "Overview", "/"),
    ("capabilities", "Capabilities", "/capabilities/"),
    ("report", "Sample Report", "/sample-report/"),
    ("methodology", "Methodology", "/methodology/"),
    ("faq", "FAQ", "/faq/"),
    ("contact", "Contact", "/contact/"),
)

FOOTER_COLUMNS = (
    (
        "Product",
        (
            ("Overview", "/"),
            ("Capabilities", "/capabilities/"),
            ("Recorded Demo", "/demo/"),
            ("Sample Report", "/sample-report/"),
            ("Methodology", "/methodology/"),
        ),
    ),
    (
        "Resources",
        (
            ("Documentation", "/docs/"),
            ("Knowledge Base", "/resources/"),
            ("Technical Guides", "/resources/#guides"),
            ("Validation Record", "/validation/"),
            ("GitHub", REPO_URL),
        ),
    ),
    (
        "Legal",
        (
            ("Privacy Policy", "/privacy/"),
            ("Terms of Use", "/terms/"),
            ("Responsible Use", "/responsible-use/"),
            ("Assessment Limitations", "/limitations/"),
        ),
    ),
    (
        "Business",
        (
            ("Contact", "/contact/"),
            ("Request an Assessment", "/request-assessment/"),
            ("Project Acquisition", "/acquisition/"),
            ("About the Project", "/about/"),
        ),
    ),
)

# Pages that must appear in the sitemap: (path, changefreq, priority)
SITEMAP = (
    ("/", "weekly", "1.0"),
    ("/capabilities/", "monthly", "0.9"),
    ("/sample-report/", "monthly", "0.9"),
    ("/demo/", "monthly", "0.9"),
    ("/methodology/", "monthly", "0.8"),
    ("/validation/", "monthly", "0.8"),
    ("/request-assessment/", "monthly", "0.8"),
    ("/contact/", "yearly", "0.7"),
    ("/faq/", "monthly", "0.7"),
    ("/docs/", "monthly", "0.7"),
    ("/resources/", "weekly", "0.7"),
    ("/limitations/", "yearly", "0.6"),
    ("/responsible-use/", "yearly", "0.6"),
    ("/about/", "yearly", "0.6"),
    ("/acquisition/", "monthly", "0.5"),
    ("/privacy/", "yearly", "0.5"),
    ("/terms/", "yearly", "0.4"),
)
