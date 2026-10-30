"""Homepage."""

from __future__ import annotations

from . import config as C
from . import data as D
from . import snippets as S
from .ui import btn, cta_band, e, icon, layout, pill, section_head


def _capability_cards() -> str:
    cards = []
    for cat in D.CATEGORIES:
        controls = D.controls_in(cat["key"])
        recorded = len([c for c in controls if c["recorded"]])
        sample = "".join(f"<li>{e(c['name'])}</li>" for c in controls[:3])
        cards.append(f"""
<article class="card reveal">
  <div class="card-icon">{icon(cat['icon'], 20)}</div>
  <span class="card-num mono">{len(controls):02d}</span>
  <h3>{e(cat['name'])}</h3>
  <p>{e(cat['intro'])}</p>
  <ul class="card-list">{sample}</ul>
  <span class="component-tag mono" style="margin-top:auto">{recorded} in the recorded run</span>
</article>""")
    return f'<div class="grid g3 reveal-group">{"".join(cards)}</div>'


def _overview() -> str:
    items = [
        ("eye", "What a stranger can see", "An outsider cannot read your policies, your firewall rules or your backups. They can see your DNS, your published mail policy, your TLS handshake, your response headers and whether certain services answer. That view is what this assessment measures."),
        ("list", "Findings with evidence attached", "Every conclusive finding quotes the record, header or handshake that produced it. There is no score without an observation behind it, and no observation is presented as an exploit."),
        ("scale", "A shared language for priority", "The 0&ndash;100 score and A&ndash;F grade exist so an owner, an IT administrator and a consultant can agree on what to fix first &mdash; not so anyone can claim a business is secure."),
    ]
    cards = "".join(f"""
<article class="card reveal">
  <div class="card-icon">{icon(i, 20)}</div>
  <h3>{title}</h3>
  <p>{text}</p>
</article>""" for i, title, text in items)
    return f'<div class="grid g3">{cards}</div>'


def _steps() -> str:
    steps = [
        ("Select an authorised target", "An assessment needs a domain you own or are permitted to assess. The public edition is limited to five reserved testing domains; a private assessment starts with written authorisation."),
        ("Run the read-only checks", "DNS, mail authentication records, TLS handshakes, HTTP headers and protocol-level service probes. No login, no payload, no exploitation."),
        ("Collect the evidence", "Each check stores what it observed and the status it reached &mdash; pass, warning, fail or inconclusive. A timeout is never converted into a failure."),
        ("Review score and report", "A weighted 0&ndash;100 score, an A&ndash;F grade, findings ordered by severity, and a report you can read as HTML, JSON, CSV or TXT."),
    ]
    return '<div class="steps reveal">' + "".join(f"""
<div class="step">
  <span class="step-marker">{i:02d}</span>
  <h3>{title}</h3>
  <p>{text}</p>
</div>""" for i, (title, text) in enumerate(steps, start=1)) + "</div>"


def _sample_tabs() -> str:
    record = D.RECORDED[D.RECORDED_DEFAULT]
    tabs = [("Summary", "0"), ("Findings", "1"), ("Evidence", "2")]
    tab_html = "".join(
        f'<button class="tab" type="button" role="tab" id="home-tab-{i}" aria-controls="home-panel-{i}" '
        f'aria-selected="{"true" if i == "0" else "false"}" tabindex="{0 if i == "0" else -1}">{label}</button>'
        for label, i in tabs
    )
    evidence = "".join(
        f'<div class="evidence"><span class="val">{e(f["evidence"])}</span><button class="copy" type="button" data-copy="{e(f["evidence"])}">Copy</button></div>'
        for f in record["findings"]
    )
    return f"""
<div class="panel reveal" data-score-card data-score="{record["score"]}">
  <div class="panel-head">
    <h3>{e(record["report_id"])}</h3>
    <span class="tag">{e(record["target"])} &middot; recorded</span>
  </div>
  <div data-tabs="home">
    <div class="tabs" role="tablist" aria-label="Sample report sections">{tab_html}</div>
    <div class="tab-panel" role="tabpanel" id="home-panel-0" aria-labelledby="home-tab-0">
      <div class="score-panel">
        <div class="gauge" data-gauge style="--v:{record["score"]}">
          <div class="gauge-inner">
            <span class="gauge-value" data-score-value>{record["score"]}</span>
            <span class="gauge-label">Posture score</span>
            <span class="gauge-grade">Grade {e(record["grade"])} &middot; {e(record["grade_label"])}</span>
          </div>
        </div>
        <div style="flex:1 1 240px;min-width:0">
          <p class="muted small">{e(record["summary"])}</p>
          {S.category_bars(record)}
        </div>
      </div>
      <p class="mono-muted small mt-2">Grade B &mdash; strong. Eight controls completed and none returned an inconclusive answer. The two warnings are informational header gaps typical of a minimal reference site.</p>
    </div>
    <div class="tab-panel" role="tabpanel" id="home-panel-1" aria-labelledby="home-tab-1" hidden>
      {S.findings_html(record, limit=4)}
      <p class="small mt-2"><a class="tlink" href="/sample-report/">Open the full report <svg viewBox="0 0 24 24" width="16" height="16" fill="none" aria-hidden="true" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15"/><path d="M13 6l6 6-6 6"/></svg></a></p>
    </div>
    <div class="tab-panel" role="tabpanel" id="home-panel-2" aria-labelledby="home-tab-2" hidden>
      <p class="small muted">Every conclusive finding quotes the observation that produced it. Copy any line and re-run the equivalent query from outside your network.</p>
      <div class="mt-2">{evidence}</div>
    </div>
  </div>
</div>"""


def _trust_cards() -> str:
    cards = [
        ("scale-doc", "A reproducible test record", "The published sandbox suite is listed test by test, with objective, expected result, actual result and notes. Run it yourself with two commands.", "/validation/", "Read the validation record"),
        ("layers", "Documented methodology", "What is measured, how statuses are assigned, how the score is weighted, what the grade bands mean, and where the method stops being able to tell you anything.", "/methodology/", "Read the methodology"),
        ("file", "Sample evidence", "The recorded assessment is published as HTML, JSON, CSV and TXT, with sanitised metadata you can inspect before you talk to anyone.", "/sample-report/", "Open the sample report"),
        ("shield", "Privacy and limitations", "No analytics, no tracking cookies, no scan data sent anywhere. The limitations page explains what an external assessment cannot establish.", "/limitations/", "Read the limitations"),
    ]
    return '<div class="grid g2">' + "".join(f"""
<article class="card reveal">
  <div class="card-icon">{icon(i, 20)}</div>
  <h3>{title}</h3>
  <p>{text}</p>
  <div class="card-link"><a class="tlink" href="{href}">{link} {icon('arrow', 16)}</a></div>
</article>""" for i, title, text, href, link in cards) + "</div>"


def _faq_preview() -> str:
    picks = [0, 4, 6, 8, 13]
    items = "".join(
        f'<details><summary>{D.FAQ[i][0]}</summary><div><p>{D.FAQ[i][2]}</p></div></details>' for i in picks
    )
    return f'<div class="acc reveal" style="max-width:52rem">{items}</div>'


def _resource_preview() -> str:
    cards = []
    for res in D.RESOURCES[:3]:
        cards.append(f"""
<a class="resource-card reveal" href="/resources/{res['slug']}/">
  <span class="component-tag mono">{e(D.RESOURCE_CATEGORIES[res['cat']])}</span>
  <h3>{e(res['title'])}</h3>
  <p>{e(res['desc'])}</p>
  <span class="resource-meta"><span>{e(res['date'])}</span><span>{res['read']} min read</span></span>
</a>""")
    return f'<div class="resource-grid">{"".join(cards)}</div>'


def build() -> str:
    record = D.RECORDED[D.RECORDED_DEFAULT]
    description = (
        "SMB Scanner Lite is an evidence-first external security posture assessment for small "
        "and medium businesses: 22 controls, a 0-100 score and an A-F grade, with the observation "
        "behind every conclusive finding. Explore a recorded assessment."
    )

    schema = [
        {
            "@type": "WebSite",
            "@id": C.SITE_URL + "/#website",
            "name": C.SITE_NAME,
            "url": C.SITE_URL,
            "description": "Evidence-first external security posture assessment for small and medium businesses.",
            "inLanguage": "en",
            "publisher": {"@id": C.SITE_URL + "/#organization"},
        },
        {
            "@type": "Organization",
            "@id": C.SITE_URL + "/#organization",
            "name": C.SITE_NAME,
            "url": C.SITE_URL,
            "logo": C.SITE_URL + "/logo.svg",
            "email": C.CONTACT_EMAIL,
            "founder": {"@type": "Person", "name": C.AUTHOR, "url": C.AUTHOR_URL},
            "description": "An evidence-first external security posture assessment product for small and medium businesses, published as a restricted public sandbox edition.",
            "sameAs": [C.REPO_URL, C.AUTHOR_URL],
        },
        {
            "@type": "SoftwareApplication",
            "@id": C.SITE_URL + "/#software",
            "name": C.SITE_NAME,
            "applicationCategory": "SecurityApplication",
            "applicationSubCategory": "External security posture assessment",
            "operatingSystem": "Cross-platform (Python 3.10+), web demo in any modern browser",
            "softwareVersion": C.PRODUCT_VERSION,
            "url": C.SITE_URL,
            "author": {"@type": "Person", "name": C.AUTHOR, "url": C.AUTHOR_URL},
            "publisher": {"@id": C.SITE_URL + "/#organization"},
            "description": "Evaluates 22 publicly observable security controls, produces a 0-100 posture score and an A-F grade, and attaches the evidence behind every conclusive finding. The public edition is restricted to five approved test domains.",
            "featureList": [
                "22 external security controls across DNS, email authentication, TLS, browser headers and service exposure",
                "0-100 weighted posture score with A-F grading",
                "Evidence string attached to every conclusive finding",
                "HTML, JSON, CSV and TXT report formats",
                "Hash-chained pre-scan consent receipts",
                "Restricted public sandbox edition with a five-domain allowlist",
            ],
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Public sandbox edition, restricted to five approved test domains."},
        },
    ]

    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="hero-rise eyebrow">Evidence-first external security posture</p>
      <h1 class="hero-rise">Understand your external <span class="grad">security posture.</span></h1>
      <p class="lede hero-rise">An evidence-first security assessment platform that helps small and medium businesses understand their public-facing exposure through structured checks, actionable findings and clear reporting.</p>
      <div class="hero-actions hero-rise">
        {btn('/demo/', 'Explore the demo', 'primary', 'bolt')}
        {btn('/sample-report/', 'View sample report', 'ghost')}
      </div>
      <div class="hero-meta hero-rise">
        <span class="meta-item">{icon('gauge', 16)}22 controls &middot; 0&ndash;100 score &middot; A&ndash;F grade</span>
        <span class="meta-item">{icon('lock', 16)}5 approved test domains</span>
        <span class="meta-item">{icon('file', 16)}HTML &middot; JSON &middot; CSV &middot; TXT</span>
      </div>
    </div>
    {S.hero_window(record)}
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="kpi-row reveal">
      <div class="kpi"><b>22</b><span>security controls in the assessment catalog</span></div>
      <div class="kpi"><b>0&ndash;100</b><span>weighted posture score with an A&ndash;F grade</span></div>
      <div class="kpi"><b>5</b><span>approved test domains in the public edition</span></div>
      <div class="kpi"><b>4</b><span>finding statuses, including inconclusive</span></div>
    </div>
    <p class="faint small mt-2">Positioning: <strong>evidence-first external security posture assessment for small and medium businesses.</strong> This is a defensive configuration and exposure assessment &mdash; not a penetration test, and not a guarantee.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("Product overview", "An outside view, written so it can be acted on.", "Most businesses cannot see their own public footprint the way a stranger does. SMB Scanner Lite looks from the outside, at a defined set of controls, and reports what it observed &mdash; without inventing certainty it does not have.")}
    {_overview()}
    <div class="grid g2 mt-4">
      <div class="card reveal">
        <div class="card-icon card-icon--cyan">{icon('user', 20)}</div>
        <h3>Who it is for</h3>
        <ul class="card-list">
          <li>SMB owners who need to know what is exposed before a customer asks</li>
          <li>IT administrators and managed service providers who need a defensible starting point</li>
          <li>Cybersecurity consultants who want evidence, not a sales deck</li>
          <li>Defensive practitioners learning how external assessment actually works</li>
        </ul>
      </div>
      <div class="card reveal">
        <div class="card-icon card-icon--cyan">{icon('alert', 20)}</div>
        <h3>What it deliberately is not</h3>
        <ul class="card-list">
          <li>Not a vulnerability scanner: nothing is exploited or fuzzed</li>
          <li>Not a penetration test: it cannot prove a weakness is exploitable</li>
          <li>Not a certification: a high score is not a statement that you are secure</li>
          <li>Not unrestricted: the public edition cannot be pointed at arbitrary hosts</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Capabilities", "Twenty-two controls, organised into five categories.", "The catalog covers DNS integrity, email authentication, transport security, browser headers and network exposure. Expand the full catalog for what each control evaluates, why it matters, and an example of the evidence it produces.")}
    {_capability_cards()}
    <div class="row mt-3">{btn('/capabilities/', 'Open the full capability catalog', 'ghost', 'arrow')}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("Scoring", "A score that shows its working.", "Each control resolves to a status. Only conclusive controls contribute to the score, and each category carries a weight that reflects how much it matters to a small business.")}
    <div class="grid g2" style="align-items:start">
      {S.score_panel(record)}
      <div class="reveal">
        <ul class="trust-list">
          <li><strong>Measured only</strong>A control that timed out is excluded from the score and reported as inconclusive, so silence can neither inflate nor deflate the result.</li>
          <li><strong>Weighted by consequence</strong>Email authentication carries the largest weight (25%), followed by DNS, transport and exposure (20% each) and browser headers (15%).</li>
          <li><strong>Grade bands are fixed</strong>A 90&ndash;100, B 80&ndash;89, C 65&ndash;79, D 50&ndash;64, F below 50. The same bands apply to every target.</li>
          <li><strong>Not a certificate</strong>The score says nothing about your applications, your people, your processes or your physical security.</li>
        </ul>
        <div class="row mt-2">{btn('/methodology/', 'Read the scoring methodology', 'ghost', 'arrow')}</div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Sample report", "Inspect the report before you talk to anyone.", "This is the genuine recorded assessment of example.com from 28 October 2026: score, grade, findings, evidence and report metadata. The same structure is used for every assessment.")}
    {_sample_tabs()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("How it works", "Four steps, one of which is authorisation.", "The assessment is read-only end to end. What changes between a public demonstration and a private assessment is the target, the scope and the authorisation behind it.")}
    {_steps()}
  </div>
</section>

<section class="section section--alt" id="demo">
  <div class="wrap">
    {section_head("Recorded demo", "A real result you can explore, not a simulation.", "The demo renders stored output from a genuine sandbox run. It is labelled as recorded, it shows the assessment timestamp and report ID, and it never pretends your browser is scanning anything.")}
    {S.recorded_banner()}
    <div class="grid g2 mt-3" style="align-items:start">
      <div class="card reveal">
        <h3>Five approved domains, enforced in the runtime</h3>
        <p>The public edition accepts exactly these names. A look-alike subdomain, a raw IP address or a trailing dot is rejected before any network request is made.</p>
        <div class="chips mt-1">{''.join(f'<span class="chip">{e(d)}</span>' for d in C.ALLOWED_DOMAINS)}</div>
        <p class="faint small mt-2">Each domain has a recorded or reference profile you can inspect: score, grade, category breakdown, findings and evidence.</p>
        <div class="row mt-2">{btn('/demo/', 'Open the recorded assessment', 'primary', 'arrow')}</div>
      </div>
      <div class="card reveal">
        <div class="recorded-banner" style="margin-bottom:0.4rem"><span class="dot"></span><span><b>Recorded</b> example.com &middot; 28 Oct 2026</span></div>
        <div class="row" style="justify-content:space-between;align-items:flex-end">
          <div>
            <span class="mono faint tiny">POSTURE SCORE</span>
            <p style="font-family:var(--font-head);font-size:2.4rem;font-weight:600;margin:0;letter-spacing:-0.04em">{record["score"]}<span class="faint" style="font-size:1rem;font-weight:500"> / 100</span></p>
          </div>
          <span class="grade-badge"><b>{e(record["grade"])}</b><span>Grade</span></span>
        </div>
        {S.category_bars(record)}
        <p class="faint tiny mt-2">Report {e(record["report_id"])} &middot; consent {e(record["consent_id"])}</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("Validation & trust", "Credibility from evidence, not from badges.", "There are no customer logos on this page, because there are no customers whose permission has been obtained. What is published instead is testable: the test record, the method, the sample evidence and the limits.")}
    {_trust_cards()}
    <div class="callout mt-3 reveal">
      {icon('info', 20)}
      <div><p><strong>No fabricated proof.</strong> This site contains no invented testimonials, review scores, client names, usage statistics or success stories. Where independent proof does not exist, the page says so rather than filling the gap.</p></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Knowledge base", "Technical writing, not keyword filler.", "Explanations of the controls this product measures, written for the people who have to fix them. Each article is original, internally linked and reviewed against the underlying standards.")}
    {_resource_preview()}
    <div class="row mt-3">{btn('/resources/', 'Browse the knowledge base', 'ghost', 'arrow')}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("FAQ", "Questions people actually ask.", "Short answers, no upsell. The methodology page has the longer technical version of most of these.")}
    {_faq_preview()}
    <div class="row mt-3">{btn('/faq/', 'Read all questions', 'ghost', 'arrow')}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Next step</p>
        <h2>Need an assessment of a domain you own?</h2>
        <p class="section-lede">The public edition is deliberately limited to five test domains. For your own infrastructure, request a private assessment: scope and written authorisation are agreed before anything runs.</p>
        <ul class="trust-list mt-2">
          <li><strong>Reviewed by a person</strong>No request triggers an automatic scan of any kind.</li>
          <li><strong>Authorisation first</strong>You confirm ownership; it is verified before work starts.</li>
          <li><strong>Same evidence standard</strong>Every finding comes with the observation behind it.</li>
        </ul>
        <div class="btn-row mt-3">
          {btn('/request-assessment/', 'Request an assessment', 'primary', 'arrow')}
          {btn('/contact/', 'Contact the maintainer', 'ghost')}
        </div>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('shield', 20)}</div>
        <h3>About the project</h3>
        <p>SMB Scanner Lite is built and maintained by {C.AUTHOR} in Rawalpindi, Pakistan, as an evidence-first defensive assessment tool. The public repository ships the website, the documentation and a sandbox runtime locked to five testing domains.</p>
        <p class="small">The full engine &mdash; all 22 controls, the scoring model and the private test suite &mdash; stays in a private repository so that unrestricted scanning capability is not published.</p>
        <div class="row mt-1">
          <a class="tlink" href="/about/">About the project {icon('arrow', 16)}</a>
          <a class="tlink" href="{C.REPO_URL}" rel="noopener" target="_blank">Public repository {icon('external', 16)}</a>
        </div>
      </div>
    </div>
  </div>
</section>

{cta_band("Explore the recorded assessment, or request one for your own domain.", "Both routes show the same report structure, the same evidence standard and the same stated limits.", ("/demo/", "Open the recorded assessment"), ("/request-assessment/", "Request an assessment"))}
"""

    return layout(
        "/",
        f"{C.SITE_NAME} — Evidence-First External Security Posture Assessment",
        description,
        body,
        active="home",
        schema=schema,
    )
