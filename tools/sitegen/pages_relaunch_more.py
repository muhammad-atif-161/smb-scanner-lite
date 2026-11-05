"""Additional product, trust, legal and contact pages for the relaunch."""
from __future__ import annotations
from . import config as C
from .ui import btn, e, layout, section_head
from . import pages_relaunch as P

def faq() -> str:
    qa = [
     ("Can I scan a domain I do not own?", "No. An online assessment requires explicit authorization and a matching DNS TXT challenge for the exact domain. Do not use the service for unsolicited scans."),
     ("Is online scanning available today?", "The backend and customer interface have been built. Public requests remain disabled until credentials, operational safeguards and one authorized end-to-end test are complete. The portal shows its current availability."),
     ("What does the online scan actually check?", "Public DNS and email-authentication controls: selected DNS observations, SPF, DMARC and limited DKIM selector discovery. No port scanning, exploitation, TLS probing or web vulnerability testing."),
     ("Does a passing score mean the business is secure?", "No. It summarizes a narrow set of observed controls. Staff accounts, applications, internal networks, devices and business processes are outside this profile."),
     ("How do I prove control of a domain?", "The service returns a time-limited TXT value to publish under _smbscanner-verify.yourdomain. It verifies an exact match before making the job eligible to run."),
     ("What if my DNS change takes time?", "DNS may take time to propagate. The challenge expires after one hour and verification attempts are limited. Avoid repeated attempts while the record has not propagated."),
     ("Why can't I access every detail of the report?", "The backend currently stores detailed evidence privately and exposes only an authorized preview. Payment handling and full report delivery have not been launched. No purchase is taken by the portal today."),
     ("Can I rerun a scan automatically?", "No. A submitted job is designed to dispatch once. If its status is uncertain, the service does not silently submit another run."),
     ("Is the desktop download the same product?", "No. The desktop public sandbox is an educational Python package with a hard-coded five-domain allowlist. Business-domain scans use the separate owner-verified online backend."),
     ("Does the site sell my scan data?", "No data sale is part of the product. The backend stores the contact details, domain, verification state and private report needed to serve assessments. See the privacy policy for the stated processing and limits."),
    ]
    items="".join(f'<details><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>' for q,a in qa)
    body=P.head("Questions answered","Before you scan, know the limits.",
      "Plain answers about authorization, coverage, release status and access to results.")
    body+=f'<section class="section"><div class="wrap"><h2 class="sr-only">Common questions</h2><div class="acc" style="max-width:860px">{items}</div></div></section>'
    return P.frame("/faq/","Questions & Answers | SMB Scanner Lite",
      "Common questions about the online DNS/email scanner, domain verification, availability, report privacy and the separate desktop sandbox.",body)

def limitations() -> str:
    body=P.head("Scope & limitations","A useful result is not the whole picture.",
       "This release addresses public DNS and email policy. It cannot observe what happens inside your company or establish whether an attacker can compromise you.",
       btn("/capabilities/","Review scan coverage","primary","arrow"))
    body+=P.article("""
<h2>The vantage point matters</h2>
<p>An external resolver can observe published DNS and some policy records. DNS caching,
geographic resolvers, split-horizon configurations and temporary failures can alter answers.
A finding is bounded by its observation time and vantage.</p>
<h2>DKIM discovery is incomplete by nature</h2>
<p>DKIM public keys live at selector-specific names. The current service tests a limited set
of selectors. Finding no key among those selectors is not proof that the domain never signs
its messages.</p>
<h2>Policy is not outcome</h2>
<p>Published SPF and DMARC policy describes intent and receiver-facing instructions. It does
not demonstrate that every outbound system is configured correctly or that all receiving
mail platforms will treat every message identically.</p>
<h2>The scoring boundary is narrow</h2>
<p>The score refers only to checks run for the DNS/email profile. It does not assess application
code, account access, patch status, password policy, backups, remote desktop exposure, TLS
configuration, browser headers, intrusion detection or real-world exploitability.</p>
<h2>No guarantee or certification</h2>
<p>No automated external review can certify that a company is secure, compliant or breach-proof.
A result is a starting point for focused remediation and follow-up review. It is not a substitute
for a scoped penetration test or comprehensive risk assessment.</p>
<h2>Availability and failures</h2>
<p>Network calls can time out or return inconsistent evidence. We preserve inconclusive states
rather than inventing a failure. Jobs may also fail or be delayed. There is no promise of
uninterrupted service or automatic retries.</p>
""")
    return P.frame("/limitations/","Scan Limitations | SMB Scanner Lite",
      "The exact limitations of a public DNS and email-authentication assessment, including uncertain findings, incomplete discovery and scoring boundaries.",body)

def responsible_use() -> str:
    body=P.head("Responsible use","Permission isn't optional.",
      "SMB Scanner Lite is intended for defensive review of domains you control or have explicit authority to assess.",
      btn("/scan/","Review the verified workflow","primary","arrow"))
    body+=P.article("""
<h2>Authorized domains only</h2>
<p>Submit a domain only if you own it or the owner has expressly authorized the assessment.
A DNS TXT challenge is required before the service permits the private scanner worker to
claim a job. A successful DNS check is a technical control, not a substitute for legal or
contractual permission.</p>
<h2>Respect the stated scan profile</h2>
<p>The online release uses limited DNS and email-record queries. You must not use the portal
to probe other people's hosts, infer permission from public visibility, bypass rate limits,
automate bulk submissions or exploit returned findings.</p>
<h2>Stay within the desktop sandbox</h2>
<p>The downloadable public Python package is intentionally restricted to five approved
training domains. It is not intended to be modified into an unrestricted scanner for
third-party systems.</p>
<h2>Disclosure and evidence</h2>
<p>If a finding concerns a system you do not own, do not publish customer records or attempt
to demonstrate exploitability. Report responsibly to the authorized owner or provider
through an appropriate channel.</p>
<h2>Service controls</h2>
<p>The backend can decline, rate-limit or suspend unauthorized or abusive requests. The
server-side authorization and report access controls remain authoritative regardless
of what the frontend displays.</p>
""")
    return P.frame("/responsible-use/","Responsible Use | SMB Scanner Lite",
      "Authorization rules, DNS ownership proof, the limited online scan profile, desktop sandbox boundaries and responsible handling of findings.",body)

def about() -> str:
    body=P.head("About the product","Built for decisions, not security theater.",
      "SMB Scanner Lite is an independent project by Muhammad Atif, focused on making observable domain security controls easier to understand.")
    body+=f"""<section class="section"><div class="wrap relaunch-split">
    <div><h2>Why this exists</h2><p>A domain carries more information than a business owner
    usually reviews: where traffic goes, who may send email for it and what recipients are
    asked to do with suspicious mail.</p>
    <p>The aim is to make that public evidence legible, not to sell uncertainty as fear.
    The service records observed controls with stated limits, so the reader can ask a better question and request a specific fix.</p></div>
    <div class="relaunch-list">
    <article><small>01</small><div><h3>Small initial scope</h3><p>The first hosted scan profile covers DNS and email policy, not the entire perimeter.</p></div></article>
    <article><small>02</small><div><h3>Careful authorization</h3><p>Ownership verification and job access controls are built into the backend, not merely the form.</p></div></article>
    <article><small>03</small><div><h3>Transparent status</h3><p>No fabricated customer list, revenue, testimonials, reviews or claims of third-party certification.</p></div></article>
    </div></div></section>
    <section class="section section--alt"><div class="wrap">
    {section_head("Independent software","Engineering notes and public learning resources.",
    "The hosted worker remains private. The separate public desktop sandbox exists for inspection and education.")}
    <div class="relaunch-links">{btn("/docs/","Desktop sandbox","ghost","download")}
    {btn("/methodology/","Method and limitations","ghost")}{btn("/contact/","Contact the developer","primary","arrow")}</div>
    </div></section>"""
    return P.frame("/about/","About SMB Scanner Lite",
      "About the independent, evidence-led online DNS/email security assessment and the separate educational desktop sandbox.",body)

def _form(kind: str = "contact") -> str:
    request = kind == "assessment"
    intro = ("Describe the domain you control and what you would like reviewed. No scan starts from this message."
             if request else "Use this form for a product question, responsible disclosure or a manually reviewed request.")
    return f"""
<div class="relaunch-feature">
<h2>{'Request a manual review' if request else 'Send a message'}</h2>
<p>{intro}</p>
<form data-enquiry-form data-form-kind="{kind}">
  <div class="form-grid">
    <div class="field"><label for="{kind}-name">Name</label><input class="input" id="{kind}-name" name="name" type="text" autocomplete="name" maxlength="100" data-required data-label="Name" required></div>
    <div class="field"><label for="{kind}-email">Email</label><input class="input" id="{kind}-email" name="email" type="email" autocomplete="email" maxlength="254" data-required data-label="Email" required></div>
    <div class="field"><label for="{kind}-company">Company (optional)</label><input class="input" id="{kind}-company" name="company" maxlength="120"></div>
    <div class="field"><label for="{kind}-domain">Domain (optional)</label><input class="input" id="{kind}-domain" name="domain" placeholder="example.com" maxlength="253"></div>
    <div class="field"><label for="{kind}-category">Reason for contact</label>
      <select class="select" id="{kind}-category" name="enquiryType">
      <option value="Manual assessment">Manual assessment</option>
      <option value="Product question">Product question</option>
      <option value="Security disclosure">Security disclosure</option>
      <option value="Other enquiry">Other enquiry</option></select></div>
    <div class="field"><label for="{kind}-authorized">Authorized to assess this domain?</label>
    <select class="select" id="{kind}-authorized" name="authorised">
      <option value="no">Not requesting a scan</option>
      <option value="yes">Yes, I have permission</option>
    </select></div>
    <div class="field field--wide"><label for="{kind}-message">Message</label>
    <textarea class="textarea" id="{kind}-message" name="message" rows="5" minlength="20" maxlength="2000" data-required data-label="Message" required></textarea></div>
    <div class="hp" aria-hidden="true"><label for="{kind}-website">Leave this blank</label><input id="{kind}-website" name="_gotcha" tabindex="-1" autocomplete="off"></div>
  </div>
  <div class="form-foot mt-2"><button type="submit" class="btn btn-primary">Compose enquiry</button>
  <p class="form-note">When no contact endpoint is configured, your email application opens with the enquiry. You must press Send there.</p></div>
  <div data-form-status hidden aria-live="polite"></div>
</form>
</div>"""

def contact() -> str:
    body=P.head("Get in touch","A real person, a specific question.",
      "Ask about the assessment method, product availability, or a responsible security finding.",
      btn("/scan/","Online assessment status","ghost"))
    body+=f"""<section class="section"><div class="wrap relaunch-split">
    <div>{_form()}</div>
    <aside><h2>Prefer a direct email?</h2>
    <p><a href="mailto:{e(C.CONTACT_EMAIL)}">{e(C.CONTACT_EMAIL)}</a></p>
    <p>There is no automated commercial scan or paid checkout attached to this contact form.
    Never email credentials, confidential reports or authentication tokens.</p>
    <div class="relaunch-callout"><p><strong>For a domain assessment:</strong>
    Start with the <a href="/scan/">ownership-verified portal</a>. If it is closed, describe
    the scope you need in a manual enquiry.</p></div></aside>
    </div></section>"""
    return P.frame("/contact/","Contact SMB Scanner Lite",
      "Contact the developer about DNS/email assessment availability, a technical question or responsible disclosure.",body,active="contact",page_type="ContactPage")

def request_assessment() -> str:
    body=P.head("Manual enquiry","Need a separately scoped review?",
      "The primary product is the ownership-verified online DNS/email assessment. For questions about other work, use this manual enquiry; it does not start a scan.",
      btn("/scan/","Open the online scan portal","primary","arrow"))
    body+=f"""<section class="section"><div class="wrap relaunch-split">
    <div>{_form("assessment")}</div>
    <aside>
    <h2>Before any testing</h2>
    <div class="relaunch-list">
    <article><small>01</small><div><h3>Define the target</h3><p>Give the exact domain and describe what you own.</p></div></article>
    <article><small>02</small><div><h3>Confirm authorization</h3><p>Scope and permission must be established before a private assessment.</p></div></article>
    <article><small>03</small><div><h3>Agree on delivery</h3><p>Capabilities, timing and pricing are not assumed from this form.</p></div></article></div>
    </aside></div></section>"""
    return P.frame("/request-assessment/","Request a Manual Review | SMB Scanner Lite",
      "A manually reviewed request for a separately scoped security assessment. Online DNS/email scanning is a different, verified workflow.",body)

def acquisition() -> str:
    body=P.head("Software enquiries","Product questions, licensing and partnerships.",
      "The focus of this website is the online assessment service. Software ownership, licensing or partnership proposals can be discussed privately without implying a customer base or revenue history.",
      btn("/contact/","Contact the developer","primary","arrow"))
    body+=P.article("""
<h2>What can be discussed</h2>
<p>Licensing, technical collaboration and possible project proposals. Any arrangement would
require its own written scope and due diligence. The hosted backend, website, historical demo
and downloadable sandbox are separate parts of the project.</p>
<h2>What is not being represented</h2>
<p>No public offer claims established recurring revenue, customer contracts, independent
certification or a proven commercial operating history. If you need a customer assessment,
use the <a href="/scan/">verified online portal</a> instead.</p>
""")
    return P.frame("/acquisition/","Software & Partnership Enquiries | SMB Scanner Lite",
      "Contact the independent developer about a software partnership or licensing question, separate from the online assessment service.",body)

def privacy() -> str:
    body=P.head("Privacy policy","Your report is not public content.",
       "This policy describes the current website, the prepared Cloudflare backend and the separate desktop sandbox. Last reviewed 4 November 2026.")
    body+=P.article(f"""
<h2>Who operates the service</h2>
<p>SMB Scanner Lite is independently developed by {e(C.AUTHOR)}. For privacy questions, write to
<a href="mailto:{e(C.CONTACT_EMAIL)}">{e(C.CONTACT_EMAIL)}</a>.</p>
<h2>Public website</h2>
<p>The website is served as static pages through GitHub Pages. It does not include advertising
pixels, third-party analytics SDKs or tracking cookies. Hosting and network providers may
process ordinary request information such as IP addresses and access logs for operations,
security and abuse prevention.</p>
<h2>Online assessment data</h2>
<p>Once enabled, the Cloudflare Worker collects the name and email submitted with a request,
the target public domain, DNS-verification state, timestamps, operational job status and
private assessment results. Cloudflare D1 stores assessment records and reports. A hashed
access token authorizes report preview and status; the token is given to the customer once.
IP addresses may be converted to keyed hashes for basic abuse limiting.</p>
<h2>How results are accessed</h2>
<p>The browser stores a private recovery token in session storage for the active tab. Only a
holder of that token can request the free preview or full report. The full report is protected
by a separate payment-verification check; returning from checkout never by itself unlocks it.</p>
<h2>Payment processing</h2>
<p>When paid report access is activated, a $19 one-time report purchase is processed by Stripe
on its own secure checkout site. Stripe receives the contact email and report reference needed
to process and match the payment. Card details are not submitted to or stored by this website.
The backend stores the payment session identifier, payment state and confirmation time.
Checkout remains disabled until the operator completes payment-provider setup.</p>
<h2>Enquiries</h2>
<p>The manual form uses your mail application unless a dedicated contact endpoint is configured.
A composed email is only delivered after you send it. Avoid including passwords or sensitive
business records in an enquiry.</p>
<h2>Desktop sandbox</h2>
<p>The downloadable public Python sandbox runs on your own device. Its local consent receipts
and output files are not automatically uploaded to the SaaS backend. The desktop runtime has
a separate five-domain testing restriction.</p>
<h2>Retention, access and deletion</h2>
<p>Operational report retention and deletion rules must be finalized before public online
assessment onboarding. No indefinite retention promise or automatic purge is claimed here.
Contact us about access or deletion of assessment records; requests are reviewed against
available records and applicable obligations.</p>
<h2>Changes</h2>
<p>The service is in an early release stage. Material changes to collection, payment processing
or report access should be reflected in a revised privacy notice before activation.</p>
""")
    return P.frame("/privacy/","Privacy & Data Handling | SMB Scanner Lite",
      "How the website, prepared Cloudflare D1 assessment backend, customer access tokens, reports, enquiries and desktop sandbox handle data.",body)

def terms() -> str:
    body=P.head("Terms of use","A service with clear boundaries.",
      "These terms describe use of the website, recorded demo, downloadable sandbox and prepared online scanning service. Last reviewed 4 November 2026.")
    body+=P.article("""
<h2>Permitted purpose</h2>
<p>Use the services only for legitimate defensive education and assessments of systems you
own or are expressly authorized to test. You must not use the site for targeting third
parties, bulk reconnaissance, exploitation or unauthorized access.</p>
<h2>Service availability</h2>
<p>Online assessments are not publicly available while the backend's operational controls
remain disabled. Availability, report access and future pricing are displayed by the
appropriate product page. The site must not be interpreted as a promise of an operating
paid service until launch is announced.</p>
<h2>Limits of assessment</h2>
<p>The first online profile checks public DNS and email policy, not internal security or
exploitability. Reports are informational, time-bound and affected by resolver and network
conditions. They do not replace a professional penetration test or compliance audit.</p>
<h2>Customer responsibility</h2>
<p>You are responsible for the accuracy of submitted domain information, your authority to
assess it, and the confidentiality of your access token. Do not share customer results
without the domain owner's permission.</p>
<h2>Desktop software</h2>
<p>The public sandbox is available under the license published in the public repository and
is restricted by its intended educational scope. Review its license before installation.</p>
<h2>Payments, report delivery and refunds</h2>
<p>The Basic scan offers a free restricted preview. When securely activated, a one-time
$19 USD purchase for a completed assessment unlocks the full DNS/email evidence report,
not an additional scan. Stripe processes the payment separately. A valid server-side payment
confirmation and the assessment's private access token are required for delivery.
Checkout is disabled until the provider account and operational conditions are ready.
Applicable taxes, refunds, disputes and support procedures must be displayed and agreed
before live charges are accepted. There is no active checkout while the payment release switch is disabled. No card payment is collected by the website while disabled.</p>
<h2>No guarantee</h2>
<p>We work to present accurately observed findings, but do not warrant that an assessment
detects every security risk or that a passing grade proves a system secure. The service
may be unavailable, interrupted or declined for operational or abuse-prevention reasons.</p>
<h2>Contact</h2>
<p>For questions about these terms, use the <a href="/contact/">contact page</a>.</p>
""")
    return P.frame("/terms/","Terms of Use | SMB Scanner Lite",
      "Website and assessment terms covering authorized use, scope, report confidentiality, desktop software and the not-yet-launched payment flow.",body)
