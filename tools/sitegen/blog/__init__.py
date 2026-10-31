"""Blog registry: clusters, posts and the small amount of arithmetic the
templates need.

The blog is the practical, owner-facing layer of the site. The knowledge base
in ``/resources/`` stays as the technical reference: long-form mechanics, RFC
references and first-principles explanations. Every blog post links to the
matching reference article, and cluster hubs say which is which, so the two
sections describe different intentions instead of competing for the same query.

Layout of this package
----------------------
``__init__.py``            clusters, aggregation, helpers
``email_security.py``      three posts
``dns_security.py``        one post
``website_security.py``    one post
``smb_basics.py``          one post
``assessment.py``          four posts
``pages_blog.py`` (../)    index, cluster hubs, article template

Editorial rules the content follows, enforced socially rather than technically:
no invented statistics, no fabricated citations, no "studies show", no promise
of a rich result or a ranking, and an explicit authorisation note on anything
that touches scanning.
"""

from __future__ import annotations

import html
import re

from . import assessment, dns_security, email_security, smb_basics, website_security

# ---------------------------------------------------------------------------
# Clusters
# ---------------------------------------------------------------------------
# `checks` mirrors what SMB Scanner Lite actually evaluates in that area; it is
# the "what our tool looks at" block, and it must stay truthful to the control
# catalog in tools/sitegen/data.py.

CLUSTERS = {
    "email-security": {
        "label": "Email security",
        "icon": "mail",
        "title": "Email security, from the records up",
        "seo_title": "Email security guides for small businesses",
        "desc": (
            "Practical guides to SPF, DKIM and DMARC: what each record does, how to roll out "
            "enforcement without losing mail, and how to diagnose a spam folder problem."
        ),
        "lede": (
            "Email is where most small businesses are impersonated first, because forging a "
            "sender is cheap and the invoice that follows looks exactly like a real one. These "
            "guides are the fixes, in the order that does not break your mail."
        ),
        "intro": """
<p>There are three separate mechanisms in play, and they are routinely confused with each
other. SPF describes which servers may send mail for your domain. DKIM signs the message so a
receiver can tell whether it was altered in transit. DMARC is the policy that decides what to do
when either check fails &mdash; and, critically, whether the domain the receiver checks is the
domain your customer actually sees in their inbox.</p>
<p>It is common to find SPF published, less common to find a working DKIM signature on every
sender, and rarer still to find a DMARC policy that enforces anything &mdash; because enforcement
is the step that makes missing mail somebody's problem. The guides here take that sequence
seriously: inventory first, reporting second, enforcement last.</p>
""",
        "checks": [
            ("SPF policy strength", "Whether the record ends in a hard fail (<code>-all</code>), a soft fail, or nothing at all."),
            ("SPF record validity", "Whether the record stays inside the RFC 7208 ten-lookup limit, and whether more than one SPF record exists."),
            ("DMARC enforcement", "Whether <code>_dmarc</code> exists and which policy is published: none, quarantine or reject."),
            ("DKIM presence", "Whether discoverable selectors publish a usable key, and at what length."),
            ("MX and null-MX posture", "Whether mail routing is coherent, including deliberate null MX for domains that never send."),
        ],
        "reference": ("/resources/spf-dkim-dmarc/", "SPF, DKIM and DMARC: how email authentication actually works"),
    },
    "dns-security": {
        "label": "DNS security",
        "icon": "globe",
        "title": "DNS and domain security",
        "seo_title": "DNS and domain security guides for small businesses",
        "desc": (
            "Why DNS records decide whether your email and website can be trusted, the mistakes "
            "that expose a domain, and how to audit the records you already have."
        ),
        "lede": (
            "DNS is the part of your infrastructure everyone depends on and almost nobody reads. "
            "It is also completely observable from outside, which makes it the cheapest place to "
            "find real problems."
        ),
        "intro": """
<p>Every customer who types your domain name is trusting an answer they did not verify. DNS is
the system that answers them: where the website lives, where mail goes, which certificate
authority may issue for the name, and increasingly whether the answer itself was signed.</p>
<p>Because those answers are public by design, an outsider can audit them without touching
anything private. That is the unusual advantage of DNS security work: nearly all of it is
inspection, and almost none of it requires access.</p>
""",
        "checks": [
            ("DNSSEC chain validation", "Whether the zone is signed and the delegation from the parent zone validates end to end."),
            ("CAA authorisation", "Whether the domain restricts which certificate authorities may issue for it."),
            ("Zone transfer exposure", "Whether an unauthorised AXFR request is refused."),
            ("Name record hygiene", "Stale, dangling or surplus records that point at infrastructure you no longer control."),
            ("Address resolution", "Whether the apex and <code>www</code> records resolve coherently over IPv4 and IPv6."),
        ],
        "reference": ("/resources/dnssec-explained/", "DNSSEC in plain terms: what it protects and what it does not"),
    },
    "website-security": {
        "label": "Website and TLS",
        "icon": "lock",
        "title": "Website, TLS and browser security",
        "seo_title": "Website and TLS security guides for small businesses",
        "desc": (
            "What the padlock actually proves, which response headers are worth adding, and the "
            "external checks any business owner can run on their own website."
        ),
        "lede": (
            "A padlock means the connection is encrypted to somebody. It does not mean the site "
            "is trustworthy, patched or safe. These guides separate the reassurance from the "
            "things that are actually verifiable from outside."
        ),
        "intro": """
<p>Website security conversations tend to collapse two different questions: is the connection
private, and is the site well built? TLS answers the first. Response headers, redirect
behaviour and certificate hygiene start to answer the second, and all of them are visible in a
single unauthenticated request.</p>
<p>None of this replaces a code review or a penetration test. What it does is catch the
misconfigurations that were never a decision &mdash; the missing HSTS header, the certificate
covering the wrong hostname, the HTTP version of a page that quietly still works.</p>
""",
        "checks": [
            ("TLS protocol versions", "Whether obsolete protocols are still negotiable on the public endpoint."),
            ("Certificate validity", "Expiry, chain and whether the hostname is actually covered."),
            ("Cipher suites", "Whether forward secrecy is available and legacy suites are disabled."),
            ("HTTPS redirect path", "Whether plain HTTP redirects to HTTPS, and whether it leaks the path first."),
            ("Security headers", "HSTS, CSP, framing and MIME-sniffing protection, referrer and permissions policy."),
        ],
        "reference": ("/resources/security-misconfigurations/", "Six security misconfigurations that are visible from outside"),
    },
    "smb-basics": {
        "label": "SMB security basics",
        "icon": "shield",
        "title": "Cybersecurity basics for small businesses",
        "seo_title": "Small business cybersecurity basics",
        "desc": (
            "Straight answers about security posture for businesses without a security team: "
            "what to fix first, what it costs, and which questions to ask your IT provider."
        ),
        "lede": (
            "You do not need a security department to close the gaps that most small businesses "
            "actually have. You need a short list, someone with the authority to change a record, "
            "and a way to check that it stayed changed."
        ),
        "intro": """
<p>Small businesses are not usually breached by something clever. They are breached by
something ordinary that nobody owned: a mailbox that anyone could forge, a remote desktop port
that was opened for a contractor in 2021, a subdomain still pointed at a closed hosting
account.</p>
<p>The baseline guides here are written in that spirit. They assume one person wears five hats,
budgets are real, and the goal is a defensible minimum rather than a perfect one.</p>
""",
        "checks": [
            ("External exposure", "Which of your services answer the public internet, and whether that was a decision."),
            ("Email authenticity", "Whether a stranger could send mail as your domain today."),
            ("Transport and web hygiene", "Certificate and header configuration on your public endpoints."),
            ("DNS integrity", "Whether the records that direct mail and traffic can be silently altered."),
        ],
        "reference": ("/resources/smb-cybersecurity-basics/", "SMB cybersecurity: where small businesses are actually exposed"),
    },
    "assessment": {
        "label": "Assessment and scoring",
        "icon": "gauge",
        "title": "Assessment, scoring and reports",
        "seo_title": "Security assessment and scoring guides",
        "desc": (
            "How external security posture assessment works, how it differs from penetration "
            "testing, how the 0-100 score is calculated, and how to read a report properly."
        ),
        "lede": (
            "A score is only useful if you can explain where it came from. These guides cover the "
            "method behind the number, what the number cannot tell you, and what to do in the "
            "week after you receive one."
        ),
        "intro": """
<p>Assessment is a genre with a credibility problem: plenty of reports, very little that a
reader can check. The method here is deliberately narrow. It measures a fixed catalog of
publicly observable controls, records the observation behind every conclusive finding, and
states its limits in the same document as its findings.</p>
<p>That makes the output less impressive and considerably more useful. You can re-run a query,
reproduce a finding, and tell whether last quarter's fix actually held.</p>
""",
        "checks": [
            ("22 controls, five categories", "DNS, email authentication, TLS, browser headers and service exposure, each weighted 1-5."),
            ("Four statuses", "Pass, warning, fail and inconclusive, with inconclusive excluded from the score rather than counted as failure."),
            ("Evidence on every finding", "The record, header or handshake that produced the result, quoted so it can be re-checked."),
            ("Grade bands", "A 90-100, B 80-89, C 65-79, D 50-64, F below 50, applied to the weighted mean."),
        ],
        "reference": ("/resources/external-security-posture-assessment/", "External security posture assessment: what it measures"),
    },
}


# ---------------------------------------------------------------------------
# Posts
# ---------------------------------------------------------------------------

POSTS = (
    email_security.POSTS
    + dns_security.POSTS
    + website_security.POSTS
    + smb_basics.POSTS
    + assessment.POSTS
)

BY_SLUG = {post["slug"]: post for post in POSTS}
POSTS_BY_CLUSTER: dict[str, list[dict]] = {slug: [] for slug in CLUSTERS}
for _post in POSTS:
    POSTS_BY_CLUSTER[_post["cluster"]].append(_post)
for _posts in POSTS_BY_CLUSTER.values():
    _posts.sort(key=lambda p: p["date"], reverse=True)


# ---------------------------------------------------------------------------
# Helpers used by the templates
# ---------------------------------------------------------------------------

def plain(text: str) -> str:
    """Strip tags and entities so reading time is computed from real words."""
    without_tags = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(without_tags)


def word_count(post: dict) -> int:
    if "word_count" not in post:
        words = plain(post.get("lede", "") + " " + post.get("body", "")).split()
        post["word_count"] = len(words)
    return post["word_count"]


def read_minutes(post: dict) -> int:
    if "read" not in post:
        post["read"] = max(3, round(word_count(post) / 210))
    return post["read"]


def all_posts() -> list[dict]:
    """Newest first."""
    return sorted(POSTS, key=lambda p: p["date"], reverse=True)


def by_cluster(cluster_slug: str) -> list[dict]:
    return POSTS_BY_CLUSTER.get(cluster_slug, [])


def latest(count: int = 3, exclude: str = "") -> list[dict]:
    return [post for post in all_posts() if post["slug"] != exclude][:count]


def related(post: dict, count: int = 2) -> list[dict]:
    """Explicit related slugs first, then siblings from the same cluster."""
    picked = [BY_SLUG[slug] for slug in post.get("related", []) if slug in BY_SLUG]
    if len(picked) < count:
        for sibling in by_cluster(post["cluster"]):
            if sibling["slug"] != post["slug"] and sibling not in picked:
                picked.append(sibling)
            if len(picked) >= count:
                break
    return picked[:count]


def cluster_url(cluster_slug: str) -> str:
    return f"/blogs/{cluster_slug}/"


def post_url(post: dict) -> str:
    return f"/blogs/{post['slug']}/"


def cluster_sizes() -> list[tuple[str, dict, int]]:
    return [(slug, meta, len(POSTS_BY_CLUSTER[slug])) for slug, meta in CLUSTERS.items()]


# A tiny integrity check: it runs on every build, so a mistyped slug or cluster
# fails loudly instead of producing a dead link.
for _post in POSTS:
    assert _post["cluster"] in CLUSTERS, f"unknown cluster for {_post['slug']}"
    assert len({p["slug"] for p in POSTS}) == len(POSTS), "duplicate blog slug"
    for _slug in _post.get("related", []):
        assert _slug in BY_SLUG, f"{_post['slug']} links to unknown post {_slug}"
