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

# Contact route published across the site. The value is mirrored in
# website/config.js (which the forms read at runtime) - change both together.
CONTACT_EMAIL = "contact@smbscannerlite.me"

PRODUCT_VERSION = "5.2.0"
EDITION = "Public Sandbox Edition"
POLICY_VERSION = "2026.10-sandbox-v1"
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
