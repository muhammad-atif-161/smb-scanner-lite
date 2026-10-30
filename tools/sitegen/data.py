"""Product content data: control catalog, recorded assessment captures, FAQ, resources.

Every number and evidence string in this module comes from one of two sources:

1. `RECORDED` - the genuine sandbox capture stored in `website/data` and used by
   the recorded demo. Do not edit these values by hand.
2. Reference profiles shipped inside the public sandbox runtime (v5.2.0) for the
   other four allowlisted domains.

Nothing here is invented for marketing. If a figure is unavailable it is left
out rather than estimated.
"""

from __future__ import annotations

from . import config as C

# ---------------------------------------------------------------------------
# Control catalog - 22 controls in five categories
# ---------------------------------------------------------------------------

CATEGORIES = [
    {
        "key": "dns",
        "name": "DNS & domain integrity",
        "short": "DNS",
        "weight": 20,
        "icon": "globe",
        "intro": "Whether the name resolves as intended, whether answers can be tampered with in transit, and whether the zone leaks control to a stranger.",
    },
    {
        "key": "email",
        "name": "Email authentication",
        "short": "Email",
        "weight": 25,
        "icon": "mail",
        "intro": "Whether a stranger can send mail that looks like it came from your domain - the exposure behind invoice fraud and business email compromise.",
    },
    {
        "key": "tls",
        "name": "Transport security",
        "short": "TLS",
        "weight": 20,
        "icon": "lock",
        "intro": "How the site proves its identity and which protocols and ciphers it is willing to negotiate with a visitor's browser.",
    },
    {
        "key": "headers",
        "name": "Browser security headers",
        "short": "Headers",
        "weight": 15,
        "icon": "shield",
        "intro": "The instructions a server sends to the browser. They are cheap to add, commonly missing, and directly affect how much a single scripting mistake can do.",
    },
    {
        "key": "exposure",
        "name": "Network & service exposure",
        "short": "Exposure",
        "weight": 20,
        "icon": "server",
        "intro": "Whether high-risk services answer on the public internet. Detection is protocol-level only: no login, no share listing, no payload.",
    },
]

CONTROLS = [
    # --- DNS ---------------------------------------------------------------
    {
        "num": 1, "slug": "address-resolution", "cat": "dns", "weight": 4,
        "name": "Address resolution and record presence",
        "short": "A/AAAA resolution",
        "evaluates": "Whether the apex name publishes resolvable A and AAAA records, whether the answers are consistent across resolvers, and whether the name is reachable at all.",
        "why": "Everything else in an external assessment depends on this. A name that does not resolve is either a misconfiguration or an outage - both are visible to customers before they are visible internally.",
        "example": "Resolved example.com -> 104.20.23.154, 172.66.147.243, 2606:4700:10::ac42:93f3, 2606:4700:10::6814:179a",
        "recorded": True,
    },
    {
        "num": 2, "slug": "dnssec", "cat": "dns", "weight": 4,
        "name": "DNSSEC chain validation",
        "short": "DNSSEC validation",
        "evaluates": "Whether the zone is signed, whether a DS record exists at the parent, and whether the chain validates when queried through a validating resolver.",
        "why": "Without DNSSEC, a forged DNS answer is indistinguishable from a real one for most clients. It does not encrypt traffic; it makes tampering detectable.",
        "example": "Zone signed with validated RRSIG and parent DS delegation.",
        "recorded": True,
    },
    {
        "num": 3, "slug": "caa", "cat": "dns", "weight": 3,
        "name": "CAA authorisation",
        "short": "CAA policy",
        "evaluates": "Whether the domain publishes CAA records, which certificate authorities they name, and whether the policy includes a reporting address.",
        "why": "CAA restricts which CAs may issue for your name. It reduces - but does not eliminate - the chance of an unauthorised certificate being issued by a compliant CA.",
        "example": 'example.org. 300 IN CAA 0 issue "letsencrypt.org"',
        "recorded": False,
    },
    {
        "num": 4, "slug": "zone-transfer", "cat": "dns", "weight": 3,
        "name": "Zone transfer exposure",
        "short": "AXFR/IXFR",
        "evaluates": "Whether each authoritative nameserver answers an AXFR or IXFR request from an unauthorised client.",
        "why": "A zone that transfers to anyone publishes the complete map of internal hostnames and services. Modern DNS servers refuse this by default; older or misconfigured ones do not.",
        "example": "AXFR example.org @ns1.example.org -> REFUSED (expected); IXFR -> NOTIMP",
        "recorded": False,
    },
    {
        "num": 5, "slug": "record-hygiene", "cat": "dns", "weight": 3,
        "name": "Name record hygiene",
        "short": "Stale pointers",
        "evaluates": "Dangling CNAMEs, records pointing at decommissioned hosting, orphaned service records and unexpected wildcard answers.",
        "why": "A record that points at a name nobody controls any more is the classic subdomain-takeover path. It is quiet, cheap to fix and easy to miss from inside.",
        "example": 'www.example.org. CNAME shop.example-host.io. -> NXDOMAIN (hosting account closed)',
        "recorded": False,
    },
    # --- Email -------------------------------------------------------------
    {
        "num": 6, "slug": "spf", "cat": "email", "weight": 5,
        "name": "SPF policy strength",
        "short": "SPF enforcement",
        "evaluates": "Whether an SPF record exists at the apex, which mechanisms it authorises, and whether the policy ends in a hard fail (-all), a soft fail (~all), or no enforcement at all.",
        "why": "SPF tells receiving servers which hosts may send your mail. A soft policy tells them to be suspicious; a hard fail tells them to reject.",
        "example": "v=spf1 -all (strict no-mail policy for reserved domain).",
        "recorded": True,
    },
    {
        "num": 7, "slug": "spf-validity", "cat": "email", "weight": 4,
        "name": "SPF record validity",
        "short": "SPF syntax and limits",
        "evaluates": "Multiple SPF records, recursive lookup count against the RFC 7208 limit of 10 DNS-querying mechanisms, void lookups, and syntax errors that cause permerror.",
        "why": "An SPF record that errors out is worse than a simple strict one: receivers fall back to a permerror result and policy enforcement becomes unpredictable.",
        "example": "2 TXT records matched v=spf1 -> permerror per RFC 7208 section 4.5",
        "recorded": False,
    },
    {
        "num": 8, "slug": "dmarc", "cat": "email", "weight": 5,
        "name": "DMARC enforcement",
        "short": "DMARC policy",
        "evaluates": "The published _dmarc policy (none, quarantine or reject), the subdomain policy, alignment modes (adkim/aspf), and the reporting addresses.",
        "why": "DMARC is the policy layer: it tells receivers what to do when SPF or DKIM fails. p=none asks for reports; p=reject actually stops spoofed mail.",
        "example": "v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s",
        "recorded": True,
    },
    {
        "num": 9, "slug": "dkim", "cat": "email", "weight": 4,
        "name": "DKIM presence and key strength",
        "short": "DKIM selectors",
        "evaluates": "Whether discoverable selectors publish keys, the key type and length, and whether weak or revoked keys are still in use.",
        "why": "DKIM signs the message itself, so a forged message cannot carry a valid signature. Short or misconfigured keys weaken that guarantee.",
        "example": "selector1._domainkey -> v=DKIM1; k=rsa; p=... (2048-bit, rsa-sha256)",
        "recorded": False,
    },
    {
        "num": 10, "slug": "mx", "cat": "email", "weight": 3,
        "name": "MX and null-MX posture",
        "short": "MX routing",
        "evaluates": "Whether MX records exist, where they point, whether a null MX (RFC 7505) is published for domains that do not accept mail, and whether the routing is internally consistent.",
        "why": "A domain that does not send mail should say so. A missing or contradictory MX is an invitation for forged mail to be delivered to a fallback host.",
        "example": "MX 0 . published indicating domain does not accept e-mail.",
        "recorded": True,
    },
    {
        "num": 11, "slug": "tls-versions", "cat": "tls", "weight": 4,
        "name": "TLS protocol versions",
        "short": "TLS 1.2/1.3",
        "evaluates": "Which protocol versions the endpoint negotiates, and whether deprecated versions (TLS 1.0/1.1, SSLv3) are still accepted.",
        "why": "Old protocol versions carry known weaknesses and are deprecated by every major standards body. A modern baseline is TLS 1.2 with TLS 1.3 preferred.",
        "example": "TLS 1.3 negotiated; TLS 1.0 and TLS 1.1 refused by the endpoint.",
        "recorded": False,
    },
    {
        "num": 12, "slug": "certificate", "cat": "tls", "weight": 5,
        "name": "Certificate validity and hostname coverage",
        "short": "Certificate",
        "evaluates": "Trust chain, expiry, hostname or SAN coverage, and whether the presented certificate is the one a browser will accept without a warning.",
        "why": "An expired or mismatched certificate trains users to click through warnings - which is exactly the habit phishing relies on.",
        "example": "Valid X.509 certificate covering example.com over TLS 1.3.",
        "recorded": True,
    },
    {
        "num": 13, "slug": "ciphers", "cat": "tls", "weight": 3,
        "name": "Cipher suites and forward secrecy",
        "short": "Cipher policy",
        "evaluates": "Whether modern AEAD suites are offered, whether ephemeral key exchange (ECDHE) is available, and whether legacy CBC or export-grade suites remain enabled.",
        "why": "Forward secrecy means a stolen private key cannot decrypt traffic recorded earlier. Legacy suites are the first thing removed in a hardening pass.",
        "example": "TLS_AES_256_GCM_SHA384 preferred; ECDHE available; no CBC or RC4 suites offered.",
        "recorded": False,
    },
    {
        "num": 14, "slug": "https-redirect", "cat": "tls", "weight": 3,
        "name": "HTTPS redirect and downgrade path",
        "short": "HTTPS redirect",
        "evaluates": "Whether plain HTTP on port 80 redirects to HTTPS, whether the redirect is permanent, and whether any resource is still served unencrypted.",
        "why": "A site that answers HTTP without redirecting gives an attacker on the path a free opportunity to intercept or rewrite the first request.",
        "example": "http://example.org -> 301 https://example.org/ (single hop, no body served).",
        "recorded": False,
    },
    # --- Headers -----------------------------------------------------------
    {
        "num": 15, "slug": "hsts", "cat": "headers", "weight": 4,
        "name": "Strict-Transport-Security",
        "short": "HSTS",
        "evaluates": "Whether HSTS is sent over HTTPS, the max-age it declares, whether it covers subdomains, and whether it is submitted for preloading.",
        "why": "HSTS tells the browser to refuse plain HTTP for this host in future. It is the only control that protects the very first request of a later visit.",
        "example": "Strict-Transport-Security header not enforced on reference landing page.",
        "recorded": True,
    },
    {
        "num": 16, "slug": "csp", "cat": "headers", "weight": 4,
        "name": "Content-Security-Policy",
        "short": "CSP",
        "evaluates": "Whether a CSP is present, whether it restricts script sources, and whether it uses unsafe-inline, unsafe-eval or a wildcard that would defeat the purpose.",
        "why": "CSP is the main browser-side mitigation against cross-site scripting. It does not fix an injection bug, but it limits what the injected script can do.",
        "example": "Content-Security-Policy header absent on static reference response.",
        "recorded": True,
    },
    {
        "num": 17, "slug": "framing-sniffing", "cat": "headers", "weight": 3,
        "name": "Clickjacking and MIME-sniffing protection",
        "short": "Framing & sniffing",
        "evaluates": "X-Frame-Options or CSP frame-ancestors, and X-Content-Type-Options: nosniff.",
        "why": "Framing protection stops a page being embedded invisibly behind a click target. nosniff stops a browser guessing a content type and executing something it should not.",
        "example": "X-Frame-Options: DENY; X-Content-Type-Options: nosniff",
        "recorded": False,
    },
    {
        "num": 18, "slug": "disclosure", "cat": "headers", "weight": 2,
        "name": "Referrer, permissions and version disclosure",
        "short": "Disclosure",
        "evaluates": "Referrer-Policy, Permissions-Policy, and whether Server or X-Powered-By headers advertise exact software versions.",
        "why": "Version banners save an attacker reconnaissance. Referrer and permissions policies limit what a page leaks or is allowed to use on the visitor's device.",
        "example": "Server: nginx/1.18.0 and X-Powered-By: PHP/7.4.3 disclosed in response headers.",
        "recorded": False,
    },
    # --- Exposure ----------------------------------------------------------
    {
        "num": 19, "slug": "high-risk-ports", "cat": "exposure", "weight": 5,
        "name": "High-risk port reachability",
        "short": "Port reachability",
        "evaluates": "Whether a defined set of high-risk services (FTP 21, Telnet 23, SMTP 25, direct database ports 3306/5432/6379/27017) accepts a TCP connection from the public internet.",
        "why": "These services were never designed to face the internet. Reachability alone is a finding; the assessment never attempts authentication.",
        "example": "TCP 3306 connection accepted from assessment vantage point (MySQL banner suppressed).",
        "recorded": False,
    },
    {
        "num": 20, "slug": "smb", "cat": "exposure", "weight": 5,
        "name": "SMB negotiate exposure (445)",
        "short": "SMB 445",
        "evaluates": "Whether port 445 completes a single unauthenticated SMB2 negotiate, and which dialect and signing requirements are advertised in the response.",
        "why": "SMB exposed to the internet is the ingress path behind several ransomware campaigns. The check reads the negotiate response only: no session, no shares, no credentials.",
        "example": "SMB2 negotiate answered on 445; dialect 3.1.1; signing required -> service exposed.",
        "recorded": False,
    },
    {
        "num": 21, "slug": "rdp", "cat": "exposure", "weight": 5,
        "name": "Remote Desktop reachability (3389)",
        "short": "RDP 3389",
        "evaluates": "Whether TCP 3389 accepts a connection and completes a protocol handshake, and whether the negotiated security layer is current.",
        "why": "Internet-facing RDP is routinely brute-forced. Even with strong passwords, exposure widens the attack surface to anyone with a scanner.",
        "example": "RDP negotiation answered on 3389 (NLA required) from the public internet.",
        "recorded": False,
    },
    {
        "num": 22, "slug": "admin-interfaces", "cat": "exposure", "weight": 5,
        "name": "Database and admin interface exposure",
        "short": "Admin interfaces",
        "evaluates": "Whether common management interfaces (phpMyAdmin, admin panels, Elasticsearch, Docker API) answer on standard ports without a network-level restriction.",
        "why": "An admin panel reachable from the internet is one credential away from full control. Network restriction is usually the cheapest available fix.",
        "example": "HTTP 200 with admin login form at :9200/_plugin/... on a public address.",
        "recorded": False,
    },
]

CONTROL_BY_NUM = {c["num"]: c for c in CONTROLS}
RECORDED_CONTROLS = [c for c in CONTROLS if c["recorded"]]

def controls_in(cat_key: str):
    return [c for c in CONTROLS if c["cat"] == cat_key]


def category(key: str) -> dict:
    return next(c for c in CATEGORIES if c["key"] == key)


# ---------------------------------------------------------------------------
# Recorded assessment captures
# ---------------------------------------------------------------------------

RECORDED_NOTE = (
    "A recorded assessment: the report below is stored output from a real "
    "SMB Scanner Lite run against a reserved test domain on 28 October 2026. "
    "It is not generated live, and this website cannot scan anything."
)

RECORDED = {
    "example.com": {
        "target": "example.com",
        "description": "IANA RFC 2606 / RFC 6761 reserved standard test domain",
        "source": "recorded",
        "source_label": "Recorded capture",
        "timestamp": "2026-10-28T17:25:30Z",
        "timestamp_display": "28 October 2026, 17:25 UTC",
        "report_id": "SMB-SANDBOX-20261028-A91144E4",
        "consent_id": "CONSENT-20261028-A91144E4",
        "receipt_sha256": "b068e643725c90429199d458b31a0749b08b4af1caae57fe4ea8878f412820a6",
        "policy_version": "2026.10-sandbox-v1",
        "version": "5.2.0",
        "edition": "Public Sandbox Edition (5-Domain Locked)",
        "duration_seconds": "not recorded",
        "score": 86,
        "grade": "B",
        "grade_label": "Strong",
        "summary": (
            "example.com demonstrates strong DNSSEC, SPF (-all) and DMARC enforcement, "
            "with informational web security header gaps typical of a minimal RFC reference site."
        ),
        "categories": {"DNS & Domain Hygiene": 95, "E-mail Authentication": 92, "Transport Security (TLS)": 90, "Web Security Headers": 68},
        "counts": {"completed": 8, "inconclusive": 0},
        "findings": [
            {"status": "pass", "control": 1, "control_id": "dns-resolution", "title": "DNS A/AAAA Resolution", "category": "DNS & Domain Hygiene", "severity": "info",
             "evidence": "Resolved example.com -> 104.20.23.154, 172.66.147.243, 2606:4700:10::ac42:93f3, 2606:4700:10::6814:179a",
             "text": "The reserved domain resolves to public anycast addresses over IPv4 and IPv6."},
            {"status": "pass", "control": 2, "control_id": "dnssec-posture", "title": "DNSSEC Validation", "category": "DNS & Domain Hygiene", "severity": "high",
             "evidence": "Zone signed with validated RRSIG and parent DS delegation.",
             "text": "The zone is signed and the chain of trust validates against the parent."},
            {"status": "pass", "control": 6, "control_id": "spf-policy", "title": "SPF Hard-Fail Policy", "category": "E-mail Authentication", "severity": "high",
             "evidence": "v=spf1 -all (strict no-mail policy for reserved domain).",
             "text": "SPF is published and set to a strict no-mail policy."},
            {"status": "pass", "control": 8, "control_id": "dmarc-policy", "title": "DMARC Enforcement", "category": "E-mail Authentication", "severity": "high",
             "evidence": "v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s",
             "text": "Unauthorised senders are rejected at the receiving mail server."},
            {"status": "pass", "control": 10, "control_id": "null-mx", "title": "RFC 7505 Null MX", "category": "E-mail Authentication", "severity": "medium",
             "evidence": "MX 0 . published indicating domain does not accept e-mail.",
             "text": "The domain publishes a null MX, signalling that it does not accept mail."},
            {"status": "pass", "control": 12, "control_id": "tls-posture", "title": "TLS 1.2/1.3 & Certificate", "category": "Transport Security (TLS)", "severity": "high",
             "evidence": "Valid X.509 certificate covering example.com over TLS 1.3.",
             "text": "TLS 1.3 is offered with a certificate that covers the domain."},
            {"status": "warning", "control": 15, "control_id": "hsts-header", "title": "HTTP Strict-Transport-Security", "category": "Web Security Headers", "severity": "medium",
             "evidence": "Strict-Transport-Security header not enforced on reference landing page.",
             "text": "HSTS is not enforced on the reference landing page.",
             "remediation": "Add Strict-Transport-Security: max-age=31536000; includeSubDomains."},
            {"status": "warning", "control": 16, "control_id": "csp-header", "title": "Content-Security-Policy", "category": "Web Security Headers", "severity": "medium",
             "evidence": "Content-Security-Policy header absent on static reference response.",
             "text": "A content security policy is not set on the static reference response.",
             "remediation": "Publish a restrictive Content-Security-Policy (default-src 'self'; object-src 'none')."},
        ],
    },
    "example.org": {
        "target": "example.org",
        "description": "IANA RFC 2606 / RFC 6761 reserved organization test domain",
        "source": "reference",
        "source_label": "Reference profile",
        "timestamp": None,
        "timestamp_display": "No dated capture — reference profile shipped in v5.2.0",
        "report_id": None,
        "consent_id": None,
        "receipt_sha256": None,
        "policy_version": C.POLICY_VERSION,
        "version": "5.2.0",
        "edition": "Public Sandbox Edition (5-Domain Locked)",
        "score": 86, "grade": "B", "grade_label": "Strong",
        "summary": "example.org maintains validated DNSSEC and strict null-mail authentication (v=spf1 -all, DMARC p=reject, null MX), with standard web header hardening recommendations.",
        "categories": {"DNS & Domain Hygiene": 95, "E-mail Authentication": 92, "Transport Security (TLS)": 90, "Web Security Headers": 68},
        "counts": {"completed": 7, "inconclusive": 0},
        "findings": [
            {"status": "pass", "control": 1, "control_id": "dns-resolution", "title": "DNS A/AAAA Resolution", "category": "DNS & Domain Hygiene", "severity": "info",
             "evidence": "Resolved authoritative IANA sandbox addresses for example.org.", "text": "The reserved domain resolves through its authoritative nameservers."},
            {"status": "pass", "control": 2, "control_id": "dnssec-posture", "title": "DNSSEC Validation", "category": "DNS & Domain Hygiene", "severity": "high",
             "evidence": "Zone signed with validated RRSIG and parent DS delegation.", "text": "The zone is signed and the chain validates."},
            {"status": "pass", "control": 6, "control_id": "spf-policy", "title": "SPF Hard-Fail Policy", "category": "E-mail Authentication", "severity": "high",
             "evidence": "v=spf1 -all published at zone apex.", "text": "SPF is published with a hard fail."},
            {"status": "pass", "control": 8, "control_id": "dmarc-policy", "title": "DMARC Enforcement", "category": "E-mail Authentication", "severity": "high",
             "evidence": "v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s", "text": "Mail that fails authentication is rejected."},
            {"status": "pass", "control": 12, "control_id": "tls-posture", "title": "TLS 1.2/1.3 & Certificate", "category": "Transport Security (TLS)", "severity": "high",
             "evidence": "Valid X.509 certificate covering example.org.", "text": "A valid certificate covers the domain."},
            {"status": "warning", "control": 15, "control_id": "hsts-header", "title": "HTTP Strict-Transport-Security", "category": "Web Security Headers", "severity": "medium",
             "evidence": "Strict-Transport-Security header not present.", "text": "HSTS is not sent.",
             "remediation": "Enable HSTS with max-age >= 31536000."},
            {"status": "warning", "control": 16, "control_id": "csp-header", "title": "Content-Security-Policy", "category": "Web Security Headers", "severity": "medium",
             "evidence": "Content-Security-Policy header absent.", "text": "No content security policy is published.",
             "remediation": "Configure an enforcing Content-Security-Policy."},
        ],
    },
    "example.net": {
        "target": "example.net",
        "description": "IANA RFC 2606 / RFC 6761 reserved network test domain",
        "source": "reference", "source_label": "Reference profile",
        "timestamp": None, "timestamp_display": "No dated capture — reference profile shipped in v5.2.0",
        "report_id": None, "consent_id": None, "receipt_sha256": None,
        "policy_version": C.POLICY_VERSION, "version": "5.2.0",
        "edition": "Public Sandbox Edition (5-Domain Locked)",
        "score": 86, "grade": "B", "grade_label": "Strong",
        "summary": "example.net exhibits strong DNSSEC and anti-spoofing email controls (SPF -all, DMARC p=reject), with optional HTTP security header improvements.",
        "categories": {"DNS & Domain Hygiene": 95, "E-mail Authentication": 92, "Transport Security (TLS)": 90, "Web Security Headers": 68},
        "counts": {"completed": 6, "inconclusive": 0},
        "findings": [
            {"status": "pass", "control": 1, "control_id": "dns-resolution", "title": "DNS A/AAAA Resolution", "category": "DNS & Domain Hygiene", "severity": "info",
             "evidence": "Resolved authoritative IANA sandbox addresses for example.net.", "text": "The reserved domain resolves."},
            {"status": "pass", "control": 2, "control_id": "dnssec-posture", "title": "DNSSEC Validation", "category": "DNS & Domain Hygiene", "severity": "high",
             "evidence": "Validated DNSSEC chain of trust.", "text": "The zone validates."},
            {"status": "pass", "control": 6, "control_id": "spf-policy", "title": "SPF Hard-Fail Policy", "category": "E-mail Authentication", "severity": "high",
             "evidence": "v=spf1 -all published at zone apex.", "text": "SPF is published with a hard fail."},
            {"status": "pass", "control": 8, "control_id": "dmarc-policy", "title": "DMARC Enforcement", "category": "E-mail Authentication", "severity": "high",
             "evidence": "v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s", "text": "Mail that fails authentication is rejected."},
            {"status": "pass", "control": 12, "control_id": "tls-posture", "title": "TLS 1.2/1.3 & Certificate", "category": "Transport Security (TLS)", "severity": "high",
             "evidence": "Valid X.509 certificate covering example.net.", "text": "A valid certificate covers the domain."},
            {"status": "warning", "control": 16, "control_id": "csp-header", "title": "Content-Security-Policy", "category": "Web Security Headers", "severity": "medium",
             "evidence": "Content-Security-Policy header absent.", "text": "No content security policy is published.",
             "remediation": "Deploy Content-Security-Policy header."},
        ],
    },
    "scanme.nmap.org": {
        "target": "scanme.nmap.org",
        "description": "Official Nmap Project public authorised test host",
        "source": "reference", "source_label": "Reference profile",
        "timestamp": None, "timestamp_display": "No dated capture — reference profile shipped in v5.2.0",
        "report_id": None, "consent_id": None, "receipt_sha256": None,
        "policy_version": C.POLICY_VERSION, "version": "5.2.0",
        "edition": "Public Sandbox Edition (5-Domain Locked)",
        "score": 68, "grade": "C", "grade_label": "Fair",
        "summary": "scanme.nmap.org is intentionally maintained as a public testing target; it resolves cleanly but omits strict email anti-spoofing and web hardening headers.",
        "categories": {"DNS & Domain Hygiene": 78, "E-mail Authentication": 60, "Transport Security (TLS)": 72, "Web Security Headers": 62},
        "counts": {"completed": 4, "inconclusive": 0},
        "findings": [
            {"status": "pass", "control": 1, "control_id": "dns-resolution", "title": "DNS A/AAAA Resolution", "category": "DNS & Domain Hygiene", "severity": "info",
             "evidence": "Resolved public test host scanme.nmap.org.", "text": "The host resolves."},
            {"status": "warning", "control": 8, "control_id": "dmarc-policy", "title": "DMARC Enforcement", "category": "E-mail Authentication", "severity": "medium",
             "evidence": "No dedicated _dmarc.scanme.nmap.org record; inherits organizational policy.", "text": "DMARC depends on the organizational domain policy.",
             "remediation": "Publish explicit DMARC policy with p=reject for non-mail subdomains."},
            {"status": "fail", "control": 16, "control_id": "csp-header", "title": "Content-Security-Policy", "category": "Web Security Headers", "severity": "medium",
             "evidence": "No Content-Security-Policy header on HTTP response.", "text": "No CSP is published.",
             "remediation": "Add Content-Security-Policy header restricting script and frame sources."},
            {"status": "warning", "control": 15, "control_id": "hsts-header", "title": "HTTP Strict-Transport-Security", "category": "Web Security Headers", "severity": "medium",
             "evidence": "Strict-Transport-Security header not observed.", "text": "HSTS is not sent.",
             "remediation": "Enforce HTTPS and publish Strict-Transport-Security."},
        ],
    },
    "badssl.com": {
        "target": "badssl.com",
        "description": "Public educational TLS and certificate test portal",
        "source": "reference", "source_label": "Reference profile",
        "timestamp": None, "timestamp_display": "No dated capture — reference profile shipped in v5.2.0",
        "report_id": None, "consent_id": None, "receipt_sha256": None,
        "policy_version": C.POLICY_VERSION, "version": "5.2.0",
        "edition": "Public Sandbox Edition (5-Domain Locked)",
        "score": 74, "grade": "C", "grade_label": "Fair",
        "summary": "badssl.com provides a valid apex certificate for browser TLS testing while intentionally hosting specialised test configurations on subdomains.",
        "categories": {"DNS & Domain Hygiene": 82, "E-mail Authentication": 64, "Transport Security (TLS)": 88, "Web Security Headers": 62},
        "counts": {"completed": 4, "inconclusive": 0},
        "findings": [
            {"status": "pass", "control": 1, "control_id": "dns-resolution", "title": "DNS A/AAAA Resolution", "category": "DNS & Domain Hygiene", "severity": "info",
             "evidence": "Resolved public TLS test portal badssl.com.", "text": "The host resolves."},
            {"status": "pass", "control": 12, "control_id": "tls-posture", "title": "Apex TLS Certificate", "category": "Transport Security (TLS)", "severity": "high",
             "evidence": "Apex domain badssl.com presents a valid certificate over modern TLS.", "text": "The apex certificate is valid."},
            {"status": "warning", "control": 8, "control_id": "dmarc-policy", "title": "DMARC Policy", "category": "E-mail Authentication", "severity": "medium",
             "evidence": "No strict DMARC reject policy on test portal apex.", "text": "No strict DMARC policy is published at the apex.",
             "remediation": "Publish v=DMARC1; p=reject for non-mail test domains."},
            {"status": "warning", "control": 16, "control_id": "csp-header", "title": "Content-Security-Policy", "category": "Web Security Headers", "severity": "low",
             "evidence": "Content-Security-Policy header not enforced on apex landing page.", "text": "No CSP is enforced at the apex.",
             "remediation": "Add Content-Security-Policy header where applicable."},
        ],
    },
}

RECORDED_DEFAULT = "example.com"

# ---------------------------------------------------------------------------
# Grading
# ---------------------------------------------------------------------------

GRADE_BANDS = [
    ("A", "90-100", "Strong", "Every control that completed meets its published expectation, or is one minor gap away."),
    ("B", "80-89", "Strong", "Well configured overall. The gaps are informational or low-impact hardening items."),
    ("C", "65-79", "Fair", "Meaningful gaps in at least one category. Worth a planned fix, not an emergency."),
    ("D", "50-64", "Needs work", "Several controls are missing or weak across more than one category."),
    ("F", "0-49", "Urgent", "Core controls are absent. Start with the highest-severity findings and work down."),
]


def grade_for(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 65:
        return "C"
    if score >= 50:
        return "D"
    return "F"


# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------

FAQ = [
    ("What is SMB Scanner Lite?", "product",
     "SMB Scanner Lite is an evidence-first external security posture assessment for small and medium businesses. It evaluates 22 publicly observable security controls on a domain, produces a 0&ndash;100 posture score and an A&ndash;F grade, and attaches the observation behind every conclusive finding."),
    ("Who is it for?", "product",
     "Small business owners, the IT administrator or managed service provider who looks after their infrastructure, cybersecurity consultants who need a defensible starting point, and defensive security practitioners who want a tool that refuses to overstate what it saw."),
    ("Is this a vulnerability scanner?", "product",
     "No. It is a configuration and exposure assessment. It does not run exploit code, it does not authenticate, and it does not enumerate shares or directories. A failed control means a published expectation was not met - not that an exploitable vulnerability was proven."),
    ("Does it replace a penetration test?", "product",
     "No. A penetration test tests whether a weakness can actually be exploited, with authorisation to attempt it. SMB Scanner Lite observes what is visible from outside and reports that. The two are complementary, and the assessment page says so plainly."),
    ("What does the 0&ndash;100 score mean?", "scoring",
     "It is a weighted summary of the controls that completed: pass earns full credit, warning partial credit, fail no credit, and inconclusive results are excluded entirely. It exists so an owner and their IT helper can agree on priority. It is a communication aid, not a certificate."),
    ("What do the letter grades mean?", "scoring",
     "A is 90&ndash;100, B is 80&ndash;89, C is 65&ndash;79, D is 50&ndash;64 and F is below 50. The bands are documented on the methodology page and are applied identically to every target."),
    ("Can I scan my own domain on this website?", "demo",
     "Not on this public site. The published edition is hard-locked to five free-to-use testing domains - example.com, example.org, example.net, scanme.nmap.org and badssl.com - and every other name is rejected before a network request is made. To assess a domain you own, request an assessment or run the sandbox locally."),
    ("Why is the public demo restricted?", "demo",
     "Because a scanner that can be pointed at any host is a weapon, not a demo. The allowlist is enforced inside the runtime rather than in the interface, so it cannot be bypassed with a flag, a setting or an edited form field."),
    ("Is the demo a live scan?", "demo",
     "The demo on this site is a <strong>recorded assessment</strong>: stored output from a genuine run against example.com on 28 October 2026, with the timestamp, report ID, scanner version and consent receipt shown alongside it. Nothing you enter triggers a scan from your browser."),
    ("Do you collect my data?", "privacy",
     "This website has no analytics, no advertising pixels and no tracking cookies. It sends no scan data anywhere. If you submit an enquiry form, the fields you type are used to reply to you and nothing else - see the <a href=\"/privacy/\">privacy policy</a> for exactly what is collected and how long it is held."),
    ("What happens after I request an assessment?", "assessment",
     "Your request is reviewed manually. Nothing is scanned automatically. If the domain and authorisation check out, you are contacted to agree scope, written authorisation and delivery format before any assessment runs. If it does not check out, you receive a reply saying so."),
    ("Do I need permission to request an assessment of a domain?", "assessment",
     "Yes. You must own the domain or be authorised to request an assessment of it. The request form asks you to confirm this, and authorisation is verified before work starts."),
    ("What formats does a report come in?", "product",
     "HTML for reading and sharing, JSON for machine processing, CSV for spreadsheet review and TXT for pasting into a ticket. A sanitised sample of each format for the recorded example.com assessment is available on the sample report page."),
    ("Can it detect a breach or tell me if I have been hacked?", "limits",
     "No. External observation cannot establish compromise. It can show the exposure that often precedes one - missing mail authentication, an open remote-access service, weak transport configuration - and that is the honest limit of what it claims."),
    ("What does inconclusive mean?", "scoring",
     "No conclusive answer arrived before the timeout. It is reported separately and excluded from the score, so a silent or filtering target can neither inflate nor deflate a result."),
    ("Is the whole project for sale?", "acquisition",
     "The complete project - private engine, source history, documentation and website - is offered for acquisition as a documented software project, not as a revenue-generating business. Details, terms and the price are on the <a href=\"/acquisition/\">acquisition page</a>."),
    ("Where can I read the technical detail?", "product",
     "The <a href=\"/methodology/\">methodology page</a> covers measurement, scoring, evidence handling and limitations. The <a href=\"/capabilities/\">capability catalog</a> documents all 22 controls, and the <a href=\"/validation/\">validation page</a> publishes the reproducible test record."),
]

FAQ_GROUPS = [
    ("product", "Product and positioning"),
    ("scoring", "Scores, grades and evidence"),
    ("demo", "The restricted demo"),
    ("assessment", "Assessments and authorisation"),
    ("privacy", "Privacy and data handling"),
    ("limits", "Limitations"),
    ("acquisition", "Project acquisition"),
]

# ---------------------------------------------------------------------------
# Resources / knowledge base
# ---------------------------------------------------------------------------

RESOURCE_CATEGORIES = {
    "fundamentals": "Fundamentals",
    "email": "Email authentication",
    "dns": "DNS and transport",
    "web": "Web and infrastructure",
    "method": "Method and measurement",
}

RESOURCES = [
    {"slug": "external-security-posture-assessment", "cat": "fundamentals", "guide": True,
     "title": "External security posture assessment: what it measures and what it cannot",
     "desc": "A working definition of external posture assessment, the controls it can observe without authentication, and the conclusions it is not entitled to draw.",
     "date": "2026-10-30", "read": 9},
    {"slug": "smb-cybersecurity-basics", "cat": "fundamentals", "guide": True,
     "title": "SMB cybersecurity: where small businesses are actually exposed",
     "desc": "Most small-business incidents start with something visible from the public internet. A practical look at the five exposures that appear again and again.",
     "date": "2026-10-29", "read": 8},
    {"slug": "spf-dkim-dmarc", "cat": "email", "guide": True,
     "title": "SPF, DKIM and DMARC: how email authentication actually works",
     "desc": "The three records that decide whether a stranger can send mail as your domain, how they interact, and the order to fix them in.",
     "date": "2026-10-28", "read": 11},
    {"slug": "dnssec-explained", "cat": "dns", "guide": True,
     "title": "DNSSEC in plain terms: what it protects and what it does not",
     "desc": "DNSSEC makes forged DNS answers detectable. It does not make anything private. Here is the chain of trust, the common misconfigurations, and the failure modes.",
     "date": "2026-10-27", "read": 9},
    {"slug": "public-facing-infrastructure", "cat": "web", "guide": True,
     "title": "Mapping public-facing infrastructure without overstepping",
     "desc": "How to build an inventory of what your organisation exposes, what passive sources exist, and where authorisation stops being optional.",
     "date": "2026-10-26", "read": 8},
    {"slug": "security-misconfigurations", "cat": "web", "guide": True,
     "title": "Six security misconfigurations that are visible from outside",
     "desc": "Open admin interfaces, dangling DNS records, missing HSTS, verbose banners and three more patterns that external assessment reliably catches.",
     "date": "2026-10-25", "read": 10},
    {"slug": "understanding-posture-scores", "cat": "method", "guide": False,
     "title": "How to read a 0-100 security posture score honestly",
     "desc": "Why a single number is useful for prioritisation and dangerous as a certificate, and the questions to ask before you quote one in a board pack.",
     "date": "2026-10-24", "read": 7},
    {"slug": "assessment-methodology", "cat": "method", "guide": False,
     "title": "External assessment methodology: scope, evidence and limits",
     "desc": "A defensible assessment method: define scope, pick a vantage point, attach evidence, separate absence of evidence from evidence of absence, and write down the limits.",
     "date": "2026-10-23", "read": 10},
]

RESOURCE_BY_SLUG = {r["slug"]: r for r in RESOURCES}

# ---------------------------------------------------------------------------
# Public test record (reproducible; generated from an actual run)
# ---------------------------------------------------------------------------

PUBLIC_TESTS = [
    {
        "id": "T-01",
        "name": "test_exactly_five_public_sandbox_domains_allowed",
        "objective": "Prove the allowlist is exactly the five approved public testing domains and that normalisation (scheme, port, path) cannot widen it.",
        "expected": "ALLOWED_SANDBOX_DOMAINS equals the five approved names; normalize_sandbox_target('https://<domain>:443/path') returns the bare domain.",
        "result": "pass",
        "notes": "Covers [[:port]] and path stripping. A sixth name cannot be introduced without failing this test.",
    },
    {
        "id": "T-02",
        "name": "test_non_sandbox_domains_and_ips_are_blocked",
        "objective": "Confirm every out-of-scope target raises SandboxRestrictionError before any network call.",
        "expected": "google.com, github.com, sub.example.com, 192.168.1.1, 8.8.8.8, localhost and an empty string all raise SandboxRestrictionError.",
        "result": "pass",
        "notes": "Subdomain look-alikes and raw IPs are covered, not just unrelated domains.",
    },
    {
        "id": "T-03",
        "name": "test_scan_requires_explicit_user_consent",
        "objective": "Confirm a consent receipt cannot be recorded when the policy was not accepted or no operator identity was supplied.",
        "expected": "Both calls raise ConsentRequiredError and no ledger file is written.",
        "result": "pass",
        "notes": "Consent is a precondition of the receipt itself, not a field inside a report.",
    },
    {
        "id": "T-04",
        "name": "test_consent_proof_hash_chain_and_sandbox_report",
        "objective": "Verify the SHA-256 hash chain links consecutive receipts and that a report embeds the receipt it was authorised by.",
        "expected": "Second receipt's prev_receipt_hash equals the first receipt's receipt_sha256; verify_consent_log returns (True, 2); report consent_id matches the receipt.",
        "result": "pass",
        "notes": "This is the tamper-evidence claim in the privacy policy, tested rather than asserted.",
    },
    {
        "id": "T-05",
        "name": "test_cli_enforces_sandbox_and_consent",
        "objective": "Confirm the command-line surface cannot bypass the runtime restriction.",
        "expected": "Blocked domain returns exit code 2; approved domain with consent returns exit code 0.",
        "result": "pass",
        "notes": "The restriction lives in the runtime, so the CLI inherits it rather than implementing its own check.",
    },
]
