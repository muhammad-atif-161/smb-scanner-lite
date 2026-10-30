"""Contact, private assessment request and project acquisition pages."""

from __future__ import annotations

from . import config as C
from . import data as D
from . import snippets as S
from .ui import btn, cta_band, e, icon, layout, notice, section_head


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

def contact() -> str:
    crumbs = [("Home", "/"), ("Contact", None)]
    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Ask a direct question.</h1>
    <p class="lede">Questions about the product, an assessment of your own domain, a technical detail in the methodology, or the project acquisition &mdash; all of it reaches the same person, and none of it is routed through a sales sequence.</p>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    <div class="grid g2" style="align-items:start;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr)">
      <div class="panel reveal">
        <div class="panel-head">
          <h2 style="font-size:1.2rem;margin:0">Send an enquiry</h2>
          <span class="tag">first-party form</span>
        </div>
        <p class="small muted">Choose the enquiry type that fits best &mdash; it only helps route the reply. Nothing here triggers a scan.</p>
        {S.form_core(kind="contact", include_company=True, include_domain=True, include_authorisation=True)}
      </div>
      {S.contact_card()}
    </div>

    <div class="grid g3 mt-4">
      <div class="card reveal">
        <div class="card-icon">{icon('target', 20)}</div>
        <h3>Assessment request</h3>
        <p>Ready to assess a domain you own? Use the dedicated form, which collects the domain and an authorisation confirmation up front.</p>
        <a class="tlink mt-1" href="/request-assessment/">Request an assessment {icon('arrow', 16)}</a>
      </div>
      <div class="card reveal">
        <div class="card-icon card-icon--cyan">{icon('scale', 20)}</div>
        <h3>Project acquisition</h3>
        <p>The complete project is offered separately as a documented software acquisition. Terms, deliverables and price are on that page.</p>
        <a class="tlink mt-1" href="/acquisition/">Acquisition details {icon('arrow', 16)}</a>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('code', 20)}</div>
        <h3>Technical questions</h3>
        <p>Installation, output formats, consent receipts or the scoring model: check the documentation first, then ask if something is unclear.</p>
        <a class="tlink mt-1" href="/docs/">Documentation {icon('arrow', 16)}</a>
      </div>
    </div>

    <div class="notice notice--accent mt-3 reveal">
      {icon('shield', 18, 'notice-icon')}
      <div class="notice-body"><strong>How delivery works on a static site</strong><p>This website has no backend. The form validates your message and then either delivers it to the maintainer's form endpoint or opens your mail client with the enquiry composed &mdash; whichever is configured. If your mail client does not open, write to <a href="mailto:{C.CONTACT_EMAIL}">{e(C.CONTACT_EMAIL)}</a> directly. Nothing is stored on this website.</p></div>
    </div>
  </div>
</section>
"""
    contact_schema = {
        "@type": "ContactPage",
        "name": "Contact SMB Scanner Lite",
        "description": "Contact the maintainer about the product, a private assessment, a technical enquiry or the project acquisition.",
    }
    return layout(
        "/contact/",
        "Contact — SMB Scanner Lite",
        "Contact the SMB Scanner Lite maintainer about a product question, a private assessment of your domain, a technical enquiry or the project acquisition. No automatic scanning, no data resale.",
        body,
        active="contact",
        crumbs=crumbs,
        schema=contact_schema,
    )


# ---------------------------------------------------------------------------
# Request an assessment
# ---------------------------------------------------------------------------

ASSESSMENT_NOTE = (
    "Reviewed manually. No scan is triggered by this form. Authorisation is verified before any "
    "assessment is agreed. Read the <a href=\"/privacy/\">privacy policy</a>."
)


def request_assessment() -> str:
    crumbs = [("Home", "/"), ("Request an Assessment", None)]
    steps = [
        ("You send the request", "Company, domain, contact email, a short description of what you want to understand, and a confirmation that you own the domain or are authorised to request an assessment of it."),
        ("It is reviewed by hand", "Nothing is scanned automatically. Requests are read, and domains are checked against the authorisation you describe before any work is agreed."),
        ("Scope and authorisation are agreed", "Written authorisation, the controls in scope, the window in which the assessment runs, and the report format are confirmed in writing."),
        ("The assessment runs and you receive a report", "Read-only external checks against the agreed scope, delivered as a report with the score, grade, findings, evidence and the consent record."),
    ]
    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Private assessment</p>
    <h1>Request an assessment of a domain you own.</h1>
    <p class="lede">The public edition is deliberately limited to five reserved test domains. For real infrastructure, an assessment is arranged directly: reviewed manually, authorised in writing, and reported with the same evidence standard you can inspect in the sample report.</p>
    <div class="hero-actions">{btn('/sample-report/', 'See what you would receive', 'primary', 'file')}{btn('/methodology/', 'Read the method first', 'ghost')}</div>
  </div>
</div>

<section class="section section--tight">
  <div class="wrap">
    <div class="notice notice--accent reveal">
      {icon('target', 18, 'notice-icon')}
      <div class="notice-body">
        <strong>Private assessment offer: from $149 USD</strong>
        <p>Most straightforward domain assessments are delivered within 3&ndash;5 business days after scope and written authorisation are confirmed. You receive an evidence-backed score and grade, prioritised findings, and the report in HTML, JSON, CSV and TXT formats.</p>
        <p class="small muted">The final price depends on scope. No payment is taken and no scan starts until the scope, authorisation, timing and price are agreed in writing.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush">
  <div class="wrap">
    <div class="grid g2" style="align-items:start;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr)">
      <div class="panel reveal">
        <div class="panel-head">
          <h2 style="font-size:1.2rem;margin:0">Assessment request</h2>
          <span class="tag">reviewed manually</span>
        </div>
        <p class="small muted">This form is a request, not a scan trigger. Submitting it does not cause any lookup, probe or assessment to run against the domain you enter.</p>
        {S.form_core(kind="assessment", include_company=True, include_domain=True, include_assessment=True, submit_label="Submit assessment request", note=ASSESSMENT_NOTE)}
      </div>

      <div class="form-aside">
        <div class="card reveal">
          <div class="card-icon">{icon('shield', 20)}</div>
          <h3>What happens next</h3>
          <ol class="card-list" style="counter-reset:none">
            <li>A person reads the request &mdash; there is no automated pipeline</li>
            <li>Ownership or authorisation is confirmed</li>
            <li>Scope, timing and format are agreed in writing</li>
            <li>Only then does an assessment run</li>
          </ol>
        </div>
        <div class="card reveal">
          <div class="card-icon card-icon--cyan">{icon('alert', 20)}</div>
          <h3>What not to send</h3>
          <p>No passwords, no private keys, no customer data. A domain name, a company name and a description of the concern are enough to start the conversation.</p>
        </div>
        <div class="card reveal">
          <div class="card-icon">{icon('mail', 20)}</div>
          <h3>Prefer email?</h3>
          <p>Write to <a href="mailto:{C.CONTACT_EMAIL}">{e(C.CONTACT_EMAIL)}</a> with the domain and your authorisation context.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("The process", "Four steps, and the first one is a human reading your request.", "The restriction that makes the public demo safe is also why a private assessment is arranged rather than self-served.")}
    <div class="steps reveal">
      {''.join(f'<div class="step"><span class="step-marker">{i:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(steps, start=1))}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g2" style="align-items:start">
      <div class="reveal">
        <h2>What an assessment covers</h2>
        <p class="muted">The full 22-control catalog: DNS integrity, email authentication, transport security, browser headers and network exposure. The public sandbox demonstrates eight of those controls on reserved domains; a private assessment covers the agreed scope for your infrastructure.</p>
        <ul class="trust-list mt-2">
          <li><strong>External and read-only</strong>No credentials, no exploitation, no payloads, no internal access.</li>
          <li><strong>Evidence per finding</strong>Every conclusive result quotes the observation that produced it.</li>
          <li><strong>Multiple formats</strong>HTML for reading, JSON for tooling, CSV for tracking, TXT for tickets.</li>
          <li><strong>Consent documented</strong>A hash-chained consent receipt is embedded in the report.</li>
        </ul>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('alert', 20)}</div>
        <h3>What it is not</h3>
        <p>An assessment is not a penetration test, not a compliance certification and not a guarantee that a business is secure. It reports what is observable from outside, with evidence, and states the limits of that view in the report itself.</p>
        <a class="tlink mt-1" href="/limitations/">Read the limitations {icon('arrow', 16)}</a>
      </div>
    </div>
  </div>
</section>

{cta_band("Questions before you request?", "The FAQ covers authorisation, scope, report formats and what happens to your data.", ("/faq/", "Read the FAQ"), ("/contact/", "Ask directly"))}
"""
    return layout(
        "/request-assessment/",
        "Request a Private Security Assessment — SMB Scanner Lite",
        "Request an authorised external security assessment of a domain you own. Reviewed manually, no automatic scanning, written authorisation agreed before any assessment runs.",
        body,
        crumbs=crumbs,
        schema={
            "@type": "ContactPage",
            "name": "Request an assessment",
            "description": "Request a private, authorised external security posture assessment from SMB Scanner Lite.",
        },
    )


# ---------------------------------------------------------------------------
# Acquisition
# ---------------------------------------------------------------------------

ACQUISITION_NOTE = (
    "Serious enquiries only. Details are used to respond to your enquiry and for nothing else. "
    "Read the <a href=\"/privacy/\">privacy policy</a>."
)


def acquisition() -> str:
    crumbs = [("Home", "/"), ("Project Acquisition", None)]
    controls = "".join(f"<li><span class='mono'>C{c['num']:02d}</span> &mdash; {e(c['name'])} <span class='faint tiny'>({e(D.category(c['cat'])['short'])})</span></li>" for c in D.CONTROLS)

    deliverables = [
        ("code", "The complete private engine", "All 22 controls, the scoring model, report renderers for HTML, JSON, CSV and TXT, the CLI and the desktop interface."),
        ("fingerprint", "Consent and sandbox system", "Hash-chained consent receipts, policy versioning, the five-domain allowlist and the public sandbox runtime."),
        ("layers", "Source history and documentation", "Full development history, development notes, methodology documentation and report templates."),
        ("globe", "Website and design assets", "This website's source, design system, logo, structured data and the static site generator that builds it."),
        ("check-circle", "Test suite and validation record", "The published sandbox test suite and the reproducible validation record described on this site."),
        ("scale", "Licensing and handover", "MIT-licensed published code, private repository transfer, and full copyright assignment on completion of the sale as set out in the marketplace listing."),
    ]
    deliverable_cards = "".join(f"""
<article class="card reveal">
  <div class="card-icon">{icon(i, 20)}</div>
  <h3>{e(t)}</h3>
  <p>{e(d)}</p>
</article>""" for i, t, d in deliverables)

    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Project acquisition</p>
    <h1>Acquire a documented cybersecurity assessment platform.</h1>
    <p class="lede">This is a software project acquisition, not a subscription and not an established revenue-generating SaaS business. You are acquiring a complete, documented technical asset: the engine, the evidence model, the website and the history behind them.</p>
    <div class="hero-actions">{btn('#enquiry', 'Make an acquisition enquiry', 'primary', 'mail')}{btn(C.LISTING_URL, 'View the marketplace listing', 'ghost', 'external', external=True)}</div>
  </div>
</div>

<section class="section section--tight">
  <div class="wrap">
    <div class="notice notice--warn reveal">
      {icon('info', 18, 'notice-icon')}
      <div class="notice-body"><strong>Read this first: what is being sold</strong><p>No customers, recurring revenue, traffic figures or commercial traction are claimed anywhere on this page. The project has been built as a documented product with a public website and a restricted public sandbox. The value on offer is the software, its documentation and its handover &mdash; not an income stream.</p></div>
    </div>
  </div>
</section>

<section class="section section--flush">
  <div class="wrap">
    <div class="grid g2" style="align-items:start">
      <div class="reveal">
        <h2>1 &middot; Project overview</h2>
        <div class="prose">
          <p>SMB Scanner Lite is an evidence-first external security posture assessment tool for small and medium businesses. It evaluates a catalog of 22 publicly observable security controls, produces a weighted 0&ndash;100 posture score and an A&ndash;F grade, and attaches the observation behind every conclusive finding.</p>
          <p>The project ships as two artefacts: a <strong>private full engine</strong> (controls, scoring, reporting) and a <strong>public sandbox edition</strong> locked to five reserved testing domains, with a public website, documentation and test suite.</p>
          <p>It was built by {e(C.AUTHOR)} as a defensive security product with an explicit "no claim without evidence" standard. That standard shapes the scoring model, the four-status evidence system and the deliberately conservative wording on this site.</p>
        </div>
      </div>
      <div class="panel reveal">
        <div class="eyebrow" style="margin-bottom:0.4rem">Asking price</div>
        <p style="font-family:var(--font-head);font-size:2.6rem;font-weight:600;letter-spacing:-0.04em;margin:0">$2,999 <span style="font-size:1rem;color:var(--text-muted);font-weight:500">USD</span></p>
        <p class="small muted mt-1">Negotiable &middot; serious enquiries only &middot; consistent with the current marketplace listing.</p>
        <hr>
        <dl class="meta-list">
          <div><dt>Asset type</dt><dd>Complete software project</dd></div>
          <div><dt>Revenue claimed</dt><dd>None</dd></div>
          <div><dt>Customers claimed</dt><dd>None</dd></div>
          <div><dt>Published code licence</dt><dd>MIT</dd></div>
          <div><dt>Private engine</dt><dd>Included on transfer</dd></div>
          <div><dt>Listing</dt><dd><a class="tlink" href="{C.LISTING_URL}" rel="noopener" target="_blank">SideProjectors {icon('external', 14)}</a></dd></div>
        </dl>
        <div class="row mt-2">{btn('#enquiry', 'Enquire about acquisition', 'primary', 'arrow')}</div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("2 &middot; Technical architecture", "A static public surface and a private assessment engine.", "Deliberately simple to operate and to hand over.")}
    <div class="grid g2">
      <div class="card reveal">
        <div class="card-icon">{icon('layers', 20)}</div>
        <h3>Public surface</h3>
        <p>A dependency-free static website (HTML, CSS and one JavaScript file) generated by a small Python build script and deployed to GitHub Pages. No framework, no runtime, no database, no third-party analytics.</p>
        <ul class="card-list">
          <li>Reusable design system and component layer</li>
          <li>Static site generator in <span class="mono">tools/</span> (Python standard library only)</li>
          <li>Structured data, sitemap, robots and per-page metadata</li>
          <li>Recorded assessment data served as static JSON</li>
        </ul>
      </div>
      <div class="card reveal">
        <div class="card-icon card-icon--cyan">{icon('code', 20)}</div>
        <h3>Assessment engine</h3>
        <p>Python 3.10+ with modules per control group and a scoring model grounded in published RFCs and vendor guidance. Reports render to HTML, JSON, CSV and TXT.</p>
        <ul class="card-list">
          <li>22 controls across five categories with severity weights</li>
          <li>Four-status evidence model including inconclusive</li>
          <li>Hash-chained consent receipts with policy digests</li>
          <li>Sandbox runtime with a hard five-domain allowlist</li>
          <li>CLI and desktop interface</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("3 &middot; Product capabilities", "What the platform does today.", "Documented in detail on the capability catalog, with coverage stated per control.")}
    <div class="grid g3">
      <div class="card reveal"><div class="card-icon">{icon('gauge', 20)}</div><h3>Scoring and grading</h3><p>Weighted 0&ndash;100 score, A&ndash;F grade bands, per-category scores and severity on every finding.</p></div>
      <div class="card reveal"><div class="card-icon">{icon('file', 20)}</div><h3>Reporting</h3><p>HTML, JSON, CSV and TXT. Executive summary, findings, technical evidence, recommendations and assessment metadata.</p></div>
      <div class="card reveal"><div class="card-icon">{icon('fingerprint', 20)}</div><h3>Consent evidence</h3><p>Pre-scan receipts, hash chaining, policy versioning and embedded consent proof in every report.</p></div>
      <div class="card reveal"><div class="card-icon">{icon('target', 20)}</div><h3>Scan comparison</h3><p>Compare two assessments of the same target to show what changed between runs.</p></div>
      <div class="card reveal"><div class="card-icon">{icon('lock', 20)}</div><h3>Restricted public demo</h3><p>A sandbox edition that cannot be aimed at arbitrary hosts, suitable for publishing and teaching.</p></div>
      <div class="card reveal"><div class="card-icon">{icon('book', 20)}</div><h3>Documentation</h3><p>Methodology, control catalog, installation guide and privacy position written for technical and non-technical readers.</p></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("4 &middot; The 22 controls", "The catalog is part of what you acquire.", "Each control is implemented, documented and weighted. The five categories carry published score weights of 20%, 25%, 20%, 15% and 20%.")}
    <div class="grid g2" style="align-items:start">
      <div class="card reveal">
        <h3>Control catalog</h3>
        <ul class="card-list" style="gap:0.3rem">{controls}</ul>
      </div>
      <div class="reveal">
        <div class="card">
          <div class="card-icon">{icon('scale-doc', 20)}</div>
          <h3>5 &middot; Testing documentation</h3>
          <p>The public repository contains a reproducible test suite covering the allowlist, consent enforcement, hash-chain integrity and CLI behaviour. Every test is named, and the validation page publishes the run metadata along with the objectives and expected results.</p>
          <p class="small">A larger internal validation register is maintained in the private repository. Its contents are not published, and no figures from it are claimed on this site &mdash; a buyer receives it as part of due diligence, not as marketing.</p>
          <a class="tlink mt-1" href="/validation/">Published validation record {icon('arrow', 16)}</a>
        </div>
        <div class="card mt-2">
          <div class="card-icon">{icon('terminal', 20)}</div>
          <h3>6 &middot; Installation and setup</h3>
          <p>Standard Python packaging with an editable install and a single console entry point. No services to provision, no database, no cloud dependencies. The website is a static bundle deployable to any static host.</p>
          <a class="tlink mt-1" href="/docs/">Installation documentation {icon('arrow', 16)}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("7 &middot; Included deliverables", "What transfers, concretely.")}
    <div class="grid g3">{deliverable_cards}</div>
    <div class="notice mt-3 reveal">
      {icon('info', 18, 'notice-icon')}
      <div class="notice-body"><strong>8 &middot; Source code and handover</strong><p>Handover covers the private repository transfer, the public repository, build instructions, a walkthrough of the scoring model and report pipeline, and a defined support window for questions after transfer. The exact window and transfer mechanics are agreed in writing before payment.</p></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="grid g2" style="align-items:start">
      <div class="reveal">
        <p class="eyebrow">9 &amp; 10</p>
        <h2>Licensing and intellectual property</h2>
        <p class="section-lede">Clear terms, stated before anyone pays anything.</p>
        <ul class="trust-list mt-2">
          <li><strong>Published code</strong>MIT licensed. That licence continues to apply to what has already been published.</li>
          <li><strong>Private engine</strong>Transfers with the acquisition; it is not published anywhere at present.</li>
          <li><strong>Copyright assignment</strong>Full assignment of the project's copyright on completion of the sale, as set out in the marketplace listing.</li>
          <li><strong>Third-party material</strong>The project relies on public standards (RFCs) and standard libraries. No third-party assets with incompatible licences are included.</li>
          <li><strong>Authorisation, not capability</strong>Nothing in the acquisition grants permission to assess third-party infrastructure. That remains a legal matter for the operator.</li>
        </ul>
      </div>
      <div class="reveal">
        <p class="eyebrow">11</p>
        <h2>Price and terms</h2>
        <div class="panel mt-1">
          <p style="font-family:var(--font-head);font-size:2rem;font-weight:600;letter-spacing:-0.03em;margin:0">$2,999 <span style="font-size:1rem;color:var(--text-muted);font-weight:500">USD</span></p>
          <p class="small muted mt-1">Negotiable. The price and terms here match the current official marketplace listing; if the two ever disagree, the listing governs.</p>
          <hr>
          <ul class="card-list">
            <li>No subscription, no revenue share, no ongoing obligation</li>
            <li>No claim of existing customers, revenue or traction</li>
            <li>Due diligence access to the private repository on request, under NDA where appropriate</li>
            <li>Handover support included for an agreed period</li>
          </ul>
          <div class="row mt-2">{btn('#enquiry', 'Start a conversation', 'primary', 'arrow')}</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="enquiry">
  <div class="wrap">
    <div class="grid g2" style="align-items:start;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr)">
      <div class="panel reveal">
        <div class="panel-head">
          <h2 style="font-size:1.2rem;margin:0">12 &middot; Acquisition enquiry</h2>
          <span class="tag">direct route</span>
        </div>
        <p class="small muted">Use this form for acquisition questions, due diligence requests or an offer. It reaches the maintainer directly and is not mixed into the product support queue.</p>
        {S.form_core(kind="acquisition", include_company=True,
                     types=["Project acquisition", "Technical due diligence", "Handover question", "Other acquisition question"],
                     submit_label="Send acquisition enquiry",
                     note=ACQUISITION_NOTE)}
      </div>
      <div class="form-aside">
        <div class="card reveal">
          <div class="card-icon">{icon('external', 20)}</div>
          <h3>Marketplace listing</h3>
          <p>The project is also listed on SideProjectors. The listing is an alternative route, not the only one.</p>
          <a class="tlink mt-1" href="{C.LISTING_URL}" rel="noopener" target="_blank">View the listing {icon('external', 16)}</a>
        </div>
        <div class="card reveal">
          <div class="card-icon card-icon--cyan">{icon('scale-doc', 20)}</div>
          <h3>Due diligence</h3>
          <p>Repository walkthrough, scoring model review, test suite and documentation are available to serious buyers before commitment. Ask for it in the form and say what you need to see.</p>
        </div>
        <div class="card reveal">
          <div class="card-icon">{icon('mail', 20)}</div>
          <h3>Direct email</h3>
          <p><a href="mailto:{C.CONTACT_EMAIL}">{e(C.CONTACT_EMAIL)}</a></p>
        </div>
      </div>
    </div>
  </div>
</section>

{cta_band("Product questions belong on the product side.", "If you want an assessment rather than the project itself, the assessment route is the right one.", ("/request-assessment/", "Request an assessment"), ("/contact/", "Contact the maintainer"))}
"""
    return layout(
        "/acquisition/",
        "Acquire the SMB Scanner Lite Project — Cybersecurity Assessment Platform",
        "Acquire a documented cybersecurity assessment platform: 22 controls, evidence-first reporting, consent system, website and full handover. $2,999 USD, negotiable. A software project acquisition, not a revenue-generating SaaS.",
        body,
        crumbs=crumbs,
        noindex=False,
        schema={
            "@type": "Product",
            "name": "SMB Scanner Lite — complete project acquisition",
            "description": "A documented external security posture assessment platform: 22 controls, scoring model, reporting, consent system, website and test suite, transferred as a complete software project.",
            "brand": {"@type": "Organization", "name": C.SITE_NAME},
            "offers": {
                "@type": "Offer",
                "price": "2999",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": C.SITE_URL + "/acquisition/",
                "description": "One-off acquisition of the complete project, negotiable. Not a subscription.",
            },
        },
    )
