"""Privacy, terms, 404 and legacy redirect pages."""

from __future__ import annotations

from . import config as C
from .ui import btn, e, icon, layout

EFFECTIVE = "30 October 2026"


def privacy() -> str:
    crumbs = [("Home", "/"), ("Privacy Policy", None)]
    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Privacy policy</p>
    <h1>What this site and this tool do with data.</h1>
    <p class="lede">Effective {EFFECTIVE} &middot; policy version <span class="mono">{e(C.POLICY_VERSION)}</span> &middot; maintainer {e(C.AUTHOR)}. Written to describe what the published edition actually does, not what a template says it might.</p>
    <div class="hero-actions">{btn('/responsible-use/', 'Responsible use', 'primary', 'shield')}{btn('/limitations/', 'Assessment limitations', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    <h2 class="sr-only">Privacy at a glance</h2>
    <div class="grid g3">
      <div class="card reveal"><div class="card-icon">{icon('eye', 20)}</div><h3>No tracking</h3><p>No analytics, no advertising pixels, no tracking cookies, no fingerprinting scripts.</p></div>
      <div class="card reveal"><div class="card-icon">{icon('user', 20)}</div><h3>No account</h3><p>Nothing on this site requires sign-up, and no profile is built from your visit.</p></div>
      <div class="card reveal"><div class="card-icon">{icon('lock', 20)}</div><h3>Local receipts</h3><p>Sandbox consent receipts are written on the machine that runs the assessment, never uploaded.</p></div>
    </div>

    <div class="prose mt-4">
      <h2 id="website">1. What this website collects</h2>
      <p>This website is a static publication served by GitHub Pages. It has no server-side application, no database and no login. Two things can involve your data:</p>
      <ul>
        <li><strong>Enquiry forms.</strong> If you submit the contact, assessment-request or acquisition form, the fields you type (name, email, optional company, optional domain, enquiry type and message) are used to read and reply to your enquiry. They are not sold, not shared for marketing, and not added to a mailing list.</li>
        <li><strong>Infrastructure logs.</strong> GitHub Pages, as the hosting provider, processes standard request logs (IP address, user agent, requested URL) under its own privacy terms. The project does not receive, aggregate or analyse those logs.</li>
      </ul>
      <p>There are no cookies set by this site, no localStorage keys beyond a single short-lived timestamp used to throttle duplicate form submissions, and no third-party analytics.</p>

      <h2 id="forms">2. How form submissions are delivered</h2>
      <p>The site has no backend, so the forms use one of two delivery routes, and the page tells you which happened when you submit:</p>
      <ul>
        <li><strong>Configured form endpoint.</strong> If a form endpoint is configured, the enquiry is posted directly from your browser to that provider. The provider processes it on the project's behalf and its own privacy terms apply. No database copy is kept on this website.</li>
        <li><strong>Your own mail client.</strong> If no endpoint is configured, the form prepares the enquiry and opens your mail application so you can review and send it yourself. In this case nothing leaves your browser until you press send in your own email client.</li>
      </ul>
      <p>Enquiries are retained in correspondence for as long as needed to answer them and to keep a record of any agreed assessment. You can ask for an enquiry to be deleted at any time by writing to <a href="mailto:{C.CONTACT_EMAIL}">{e(C.CONTACT_EMAIL)}</a>.</p>

      <h2 id="demo">3. The demo and recorded assessment</h2>
      <p>The demonstration page loads a static JSON file containing a genuine recorded assessment of <span class="mono">example.com</span> performed on 28 October 2026. It does not contact the target, and it cannot be made to contact anything else. There is no input field for a domain: the five approved domains are buttons, and the allowlist is checked again in the browser before any stored data is displayed.</p>

      <h2 id="sandbox">4. What the sandbox tool does</h2>
      <p>The published command-line sandbox is restricted to five approved public testing domains: <span class="mono">example.com</span>, <span class="mono">example.org</span>, <span class="mono">example.net</span>, <span class="mono">scanme.nmap.org</span> and <span class="mono">badssl.com</span>. Any other target &mdash; including a look-alike subdomain, an IP address or an alternate port &mdash; is rejected before any network request is made.</p>
      <p>Before a run, the operator must accept this policy and supply an identity. A consent receipt is then written <strong>locally</strong> to the machine that runs the assessment, by default at <span class="mono">~/.smb_scanner_lite/consent_proofs.jsonl</span>. Receipts are chained with SHA-256; each contains a consent ID, a UTC timestamp, the operator identity, the target, the policy version and its digest, the previous receipt hash and its own hash.</p>
      <p>During an approved run the tool performs read-only DNS queries, TLS handshakes, HTTP header reads and, where relevant, a single protocol-level reachability check against the selected approved domain. It does not authenticate, enumerate or exploit anything. Reports are written to the path you specify and are not uploaded anywhere.</p>

      <h2 id="not-collected">5. What is not collected</h2>
      <ul>
        <li>No passwords, credentials or private keys are requested or stored</li>
        <li>No scan results are transmitted to this website or to any third party</li>
        <li>No advertising identifiers, cross-site tracking or behavioural profiling</li>
        <li>No data is sold, rented or shared with data brokers</li>
      </ul>

      <h2 id="fonts">6. Third-party requests made by your browser</h2>
      <p>The website loads its three typefaces from Google Fonts. That request discloses your IP address and user agent to Google under its privacy terms. No other third-party assets are loaded: there are no CDN scripts, no embedded videos, no social widgets and no tracking beacons. If you prefer to avoid that request, block <span class="mono">fonts.googleapis.com</span> and <span class="mono">fonts.gstatic.com</span>; the site falls back to system fonts and remains fully usable.</p>

      <h2 id="authorisation">7. Authorisation requirements</h2>
      <p>You may only assess domains you own or have explicit written permission to assess. The MIT licence on the published code governs the software; it does not grant permission to test third-party infrastructure. Requests for a private assessment must include a confirmation of ownership or authority, which is verified before any work is agreed.</p>

      <h2 id="limitations">8. Assessment limitations</h2>
      <p>Results are external observations of a defined control set at a point in time. They do not establish that a system is secure, that a weakness is exploitable, or that a compromise has or has not occurred. The <a href="/limitations/">limitations page</a> states the boundary in full, and the report wording reflects it.</p>

      <h2 id="rights">9. Your choices</h2>
      <p>You can ask what enquiry data is held about you, request a correction, or request deletion by writing to <a href="mailto:{C.CONTACT_EMAIL}">{e(C.CONTACT_EMAIL)}</a>. Because the site collects so little, most requests resolve to confirming that a single email thread exists.</p>

      <h2 id="changes">10. Changes to this policy</h2>
      <p>When the implementation changes, this policy changes with it, and the policy version identifier is updated. Material changes are reflected on this page with a new effective date. Consent receipts record the policy version and digest that were accepted, so an older receipt always points to the exact policy it agreed to.</p>

      <h2 id="contact">11. Contact</h2>
      <p>Privacy questions: <a href="mailto:{C.CONTACT_EMAIL}">{e(C.CONTACT_EMAIL)}</a>, or use the <a href="/contact/">contact form</a>. The maintainer is {e(C.AUTHOR)}, Rawalpindi, Pakistan.</p>

      <div class="notice mt-4">{icon('info', 18, 'notice-icon')}<div class="notice-body"><strong>Plain-language summary</strong><p>This site does not track you. The forms are the only place you give it data, and that data is used to reply to you. The sandbox writes consent evidence on your own computer and scans nothing outside five reserved test domains.</p></div></div>
    </div>
  </div>
</section>

{_legal_footer_links()}
"""
    return layout(
        "/privacy/",
        "Privacy Policy — SMB Scanner Lite",
        "What the SMB Scanner Lite website and sandbox do with data: no tracking, no analytics, form fields used only to reply, locally stored hash-chained consent receipts, and the five-domain restriction.",
        body,
        crumbs=crumbs,
    )


def terms() -> str:
    crumbs = [("Home", "/"), ("Terms of Use", None)]
    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Terms of use</p>
    <h1>The terms that go with the software.</h1>
    <p class="lede">Effective {EFFECTIVE}. These terms cover this website and the published sandbox edition. They sit alongside the MIT licence on the source code and the privacy policy on data handling.</p>
    <div class="hero-actions">{btn('/privacy/', 'Privacy policy', 'primary', 'shield')}{btn('/responsible-use/', 'Responsible use', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    <div class="prose">
      <h2 id="acceptance">1. Acceptance</h2>
      <p>By using this website or the published sandbox edition, you agree to these terms. If you do not agree, do not use them.</p>

      <h2 id="licence">2. Licence scope</h2>
      <p>The source code published in the public repository is licensed under the MIT licence. That licence covers the software. It does not grant permission to assess infrastructure you do not own or have written permission to assess, and it does not make a sandbox report a commercial security audit.</p>

      <h2 id="acceptable-use">3. Acceptable use</h2>
      <ul>
        <li>Use the sandbox only against the five approved public testing domains, or against systems you are authorised to assess in the full-engine edition.</li>
        <li>Do not attempt to bypass, modify or circumvent the five-domain allowlist.</li>
        <li>Do not reverse-engineer, decompile or extract the protected runtime package.</li>
        <li>Do not represent sandbox output as a formal commercial audit or as certification that a business is secure.</li>
        <li>Do not use the software in breach of applicable law.</li>
      </ul>

      <h2 id="no-warranty">4. No warranty</h2>
      <p>The website, the sandbox edition and all generated reports are provided "as is", without warranty of any kind, express or implied, including fitness for a particular purpose. External assessment is inherently partial: results depend on the vantage point, the resolver and the moment of measurement.</p>

      <h2 id="liability">5. Limitation of liability</h2>
      <p>To the maximum extent permitted by law, the author is not liable for any loss or damage arising from use of, or reliance on, this website, the software or any report it produces &mdash; including decisions taken on the basis of a score, a grade or a finding.</p>

      <h2 id="accuracy">6. Accuracy and changes</h2>
      <p>The project aims to be accurate and to state its limits. It does not warrant that documentation, control definitions or sample data remain current. Content may change without notice; the recorded assessment is dated so that its age is always visible.</p>

      <h2 id="third-party">7. Third-party services and links</h2>
      <p>This site relies on GitHub Pages for hosting and Google Fonts for typefaces, and it links to external resources including the public repository and a marketplace listing. Those services are governed by their own terms and privacy policies.</p>

      <h2 id="ip">8. Intellectual property</h2>
      <p>The project name, website design, documentation and the private engine remain the property of the author, except where the MIT licence applies to published code. The acquisition page describes the terms under which the complete project may transfer.</p>

      <h2 id="law">9. Governing law</h2>
      <p>These terms are governed by the laws of Pakistan, without prejudice to mandatory protections available to consumers in their own jurisdiction.</p>

      <h2 id="contact">10. Contact</h2>
      <p>Questions about these terms: <a href="mailto:{C.CONTACT_EMAIL}">{e(C.CONTACT_EMAIL)}</a> or the <a href="/contact/">contact form</a>.</p>
    </div>
  </div>
</section>

{_legal_footer_links()}
"""
    return layout(
        "/terms/",
        "Terms of Use — SMB Scanner Lite",
        "Terms for the SMB Scanner Lite website and published sandbox edition: licence scope, acceptable use, no warranty, limitation of liability and governing law.",
        body,
        crumbs=crumbs,
    )


def _legal_footer_links() -> str:
    return f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="card reveal">
      <h3>Related documents</h3>
      <div class="row">
        <a class="tlink" href="/privacy/">Privacy policy {icon('arrow', 16)}</a>
        <a class="tlink" href="/terms/">Terms of use {icon('arrow', 16)}</a>
        <a class="tlink" href="/responsible-use/">Responsible use {icon('arrow', 16)}</a>
        <a class="tlink" href="/limitations/">Assessment limitations {icon('arrow', 16)}</a>
        <a class="tlink" href="{C.REPO_URL}/blob/main/LICENSE" rel="noopener" target="_blank">MIT licence {icon('external', 16)}</a>
      </div>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# 404
# ---------------------------------------------------------------------------

def not_found() -> str:
    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1>That page is not here.</h1>
    <p class="lede">The address may have changed when the site was reorganised. Everything below is a real destination.</p>
    <div class="hero-actions">{btn('/', 'Back to the overview', 'primary', 'arrow')}{btn('/contact/', 'Report a broken link', 'ghost')}</div>
  </div>
</div>
<section class="section section--flush">
  <div class="wrap">
    <h2 class="sr-only">Useful destinations</h2>
    <div class="grid g3">
      <div class="card"><div class="card-icon">{icon('list', 20)}</div><h3>Capabilities</h3><p>All 22 controls with definitions and evidence examples.</p><a class="tlink mt-1" href="/capabilities/">Open the catalog {icon('arrow', 16)}</a></div>
      <div class="card"><div class="card-icon">{icon('file', 20)}</div><h3>Sample report</h3><p>The complete recorded assessment, in five sections.</p><a class="tlink mt-1" href="/sample-report/">Open the report {icon('arrow', 16)}</a></div>
      <div class="card"><div class="card-icon">{icon('bolt', 20)}</div><h3>Recorded demo</h3><p>Explore the stored run against five approved domains.</p><a class="tlink mt-1" href="/demo/">Open the demo {icon('arrow', 16)}</a></div>
      <div class="card"><div class="card-icon">{icon('book', 20)}</div><h3>Knowledge base</h3><p>Technical articles on the controls this product measures.</p><a class="tlink mt-1" href="/resources/">Browse articles {icon('arrow', 16)}</a></div>
      <div class="card"><div class="card-icon">{icon('terminal', 20)}</div><h3>Documentation</h3><p>Installation and command reference for the sandbox.</p><a class="tlink mt-1" href="/docs/">Read the docs {icon('arrow', 16)}</a></div>
      <div class="card"><div class="card-icon">{icon('mail', 20)}</div><h3>Contact</h3><p>Ask a question or request an assessment.</p><a class="tlink mt-1" href="/contact/">Get in touch {icon('arrow', 16)}</a></div>
    </div>
  </div>
</section>
"""
    return layout(
        "/404.html",
        "Page not found — SMB Scanner Lite",
        "That page could not be found. Browse the capabilities, sample report, recorded demo, knowledge base or documentation instead.",
        body,
        noindex=True,
    )


# ---------------------------------------------------------------------------
# Legacy redirects
# ---------------------------------------------------------------------------

def redirect(target: str, title: str) -> str:
    """A static redirect page for GitHub Pages (no server-side rewrites)."""
    url = C.SITE_URL + target
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Moved — {e(title)} | {C.SITE_NAME}</title>
<meta name="robots" content="noindex, follow" />
<link rel="canonical" href="{url}" />
<meta http-equiv="refresh" content="0; url={target}" />
<link rel="stylesheet" href="/styles.css" />
</head>
<body>
<main id="main" class="wrap section">
  <p class="eyebrow">Moved</p>
  <h1>This page has a new address.</h1>
  <p class="lede">The site was reorganised. The current page is <a href="{target}">{e(url)}</a>.</p>
  <p class="mt-2"><a class="btn btn-primary" href="{target}">Continue <svg viewBox="0 0 24 24" width="18" height="18" fill="none" aria-hidden="true" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></a></p>
</main>
</body>
</html>
"""
