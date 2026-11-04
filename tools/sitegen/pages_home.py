"""Evidence-first homepage — editorial product narrative.

The public site shows a genuine recorded sandbox result. The separate
owner-verified SaaS service is strictly scoped to DNS/email, and is never
marketed as the complete 22-control catalog.
"""
from __future__ import annotations

from . import config as C
from . import data as D
from . import schema as structured
from . import snippets as S
from .ui import btn, e, icon, layout, section_head


def _capabilities() -> str:
    panels = []
    for index, cat in enumerate(D.CATEGORIES, 1):
        count = len(D.controls_in(cat["key"]))
        panels.append(f"""
<article class="home-capability">
  <span class="index">0{index} / {count} controls</span>
  <h3>{e(cat["name"])}</h3>
  <p>{e(cat["intro"])}</p>
</article>""")
    return '<div class="home-capability-grid">' + "".join(panels) + "</div>"


def _principles() -> str:
    principles = (
        ("01", "Only what we can observe",
         "Public DNS records, mail policy, TLS handshakes and service responses can be measured. Internal security, staff behaviour and exploitability cannot be inferred from them."),
        ("02", "The status follows the evidence",
         "Pass, warning, fail and inconclusive are distinct outcomes. Failed requests and timeouts never turn into made-up findings."),
        ("03", "The result has a boundary",
         "Every assessment states its target, timestamp, coverage and limitations. A posture score is a prioritisation tool, not a certification."),
    )
    return '<div class="home-lines">' + "".join(f"""
<article class="home-line"><span>{number}</span>
  <div><h3>{heading}</h3><p>{body}</p></div>
</article>""" for number, heading, body in principles) + "</div>"


def _steps() -> str:
    steps = (
        ("01 / Authorise", "Confirm ownership",
         "Only request assessments of domains you control or are explicitly authorised to test. The self-service workflow uses a DNS TXT challenge before a scan is permitted."),
        ("02 / Measure", "Run the scoped checks",
         "Current automated jobs inspect public DNS and email-authentication policy only. The broader catalog and private assessments are separate, with scope agreed first."),
        ("03 / Review", "Read the findings",
         "Get a score, grade and a concise preview. Full evidence is private; it is not released by the website until a secure payment flow exists."),
    )
    return '<div class="home-process">' + "".join(f"""
<article><small>{index}</small><h3>{title}</h3><p>{body}</p></article>
""" for index, title, body in steps) + "</div>"


def _resources() -> str:
    cards = []
    for article in D.RESOURCES[:3]:
        cards.append(f"""
<a class="resource-card" href="/resources/{e(article["slug"])}/">
  <span class="component-tag mono">{e(D.RESOURCE_CATEGORIES[article["cat"]])} / GUIDE</span>
  <h3>{e(article["title"])}</h3><p>{e(article["desc"])}</p>
  <span class="resource-meta"><span>{e(article["date"])}</span><span>{article["read"]} min read</span></span>
</a>""")
    return '<div class="resource-grid">' + "".join(cards) + "</div>"


def build() -> str:
    record = D.RECORDED[D.RECORDED_DEFAULT]
    schema = [structured.software_application()]
    beta_active = C.SAAS["enabled"]
    primary_url = "/scan/" if beta_active else "/request-assessment/"
    primary_label = "Open verified assessment" if beta_active else "Request an assessment"
    beta_notice = (
        "A limited DNS/email self-service assessment is now available for "
        "verified domain owners; other controls require a separate agreed scope."
        if beta_active else
        "Automated DNS/email assessment is being prepared. The recorded demo "
        "is available now; private assessment enquiries are reviewed manually."
    )
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="home-dateline"><span class="home-mark"></span>Independent security assessment / evidence first</p>
      <h1>Security, <span class="grad">without the guesswork.</span></h1>
      <p class="lede">A clearer view of what your business publishes to the internet.
      Understand its public security posture, see the observation behind each
      finding, and focus on what can actually be improved.</p>
      <div class="hero-actions">
        {btn('/demo/', 'Explore a real report', 'primary', 'arrow')}
        {btn(primary_url, primary_label, 'ghost')}
      </div>
      <div class="hero-meta">
        <span class="meta-item">{icon('check-circle', 16)} Evidence before claims</span>
        <span class="meta-item">{icon('shield', 16)} Authorised targets only</span>
        <span class="meta-item">{icon('file', 16)} Exportable reports</span>
      </div>
    </div>
    {S.hero_window(record)}
  </div>
</section>

<section class="section section--tight" aria-label="Product facts">
  <div class="wrap">
    <div class="home-proof-strip">
      <div><b>01 / Transparent</b><span>Real, dated assessment output you can inspect before making an enquiry.</span></div>
      <div><b>02 / Bounded</b><span>22 documented catalog controls. Current SaaS automation: DNS and email only.</span></div>
      <div><b>03 / Authorised</b><span>Domain verification precedes automated checks; the public demo remains restricted.</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap home-editorial">
    <div class="section-head">
      <p class="eyebrow">01 / The standard</p>
      <h2>A finding should never outrun its evidence.</h2>
      <p class="section-lede">Every external assessment has blind spots.
      We show the boundary, distinguish measurement from assumption, and keep
      inconclusive results visible instead of hiding them inside a score.</p>
      <div class="row mt-3">{btn('/methodology/', 'Examine the methodology', 'ghost', 'arrow')}</div>
    </div>
    {_principles()}
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="home-sample">
      <div class="section-head">
        <p class="eyebrow">02 / Recorded evidence</p>
        <h2>Open the report. Inspect the details.</h2>
        <p class="section-lede">This is a genuine, stored assessment of
        <span class="mono">example.com</span> from 28 October 2026. It is
        deliberately labelled <strong>recorded</strong> and never represented
        as a live scan of your browser or domain.</p>
        <div class="home-ribbon">
          <span>{e(record["report_id"])}</span>
          <a class="tlink" href="/sample-report/">Full sample report {icon('arrow', 16)}</a>
        </div>
        <p class="home-editorial-note">A recorded example demonstrates the
        report format, not the state of somebody else's infrastructure today.
        Full assessment evidence is only shared with its authorised owner.</p>
      </div>
      <div>
        {S.score_panel(record)}
        <div class="row mt-2">{btn('/demo/', 'Explore recorded findings', 'primary', 'arrow')}
        {btn('/validation/', 'See reproducible tests', 'ghost')}</div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head('03 / What gets measured',
      'Five areas. An explicitly limited view.',
      'The full product catalog contains 22 defined controls. A control in the catalog is not a claim that every live plan or assessment executes it.')}
    {_capabilities()}
    <div class="home-ribbon">
      <span>Current automated service: DNS + mail authentication only</span>
      <a class="tlink" href="/capabilities/">View the full control catalog {icon('arrow', 16)}</a>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head('04 / How the service works',
      'A clear workflow, with permission first.',
      'The public sandbox, limited self-service beta, and manually arranged private assessments are distinct services. No tool is permission to assess a domain you do not control.')}
    {_steps()}
    <p class="home-editorial-note">{e(beta_notice)}</p>
    <div class="row mt-3">
      {btn(primary_url, primary_label, 'primary', 'arrow')}
      {btn('/responsible-use/', 'Read acceptable use', 'ghost')}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap home-method">
    <div class="section-head">
      <p class="eyebrow">05 / Scoring integrity</p>
      <h2>Useful numbers. No false certainty.</h2>
      <p class="section-lede">A posture score summarises the results of
      checks actually performed. It cannot substitute for an internal audit,
      penetration test, compliance review, or comprehensive risk assessment.</p>
      <div class="row mt-3">{btn('/limitations/', 'Where the method stops', 'ghost', 'arrow')}</div>
    </div>
    <ul class="trust-list">
      <li><strong>Pass / warning / fail / inconclusive</strong>Unknown outcomes remain unknown. DNS timeouts never become a missing-policy finding.</li>
      <li><strong>Scoped by the job</strong>A DNS/email score is not presented as a full-network security grade.</li>
      <li><strong>Evidence you can revisit</strong>Findings carry observations and supporting context, not unsupported claims of exploitability.</li>
      <li><strong>Privacy by default</strong>Detailed customer reports are not posted publicly or included in the free preview.</li>
    </ul>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head('06 / Reference library',
      'Better decisions begin with better explanations.',
      'Explore practical guidance on public security controls and why the observations matter.')}
    {_resources()}
    <div class="row mt-3">{btn('/blogs/', 'Browse technical writing', 'ghost', 'arrow')}
    {btn('/resources/', 'Open reference library', 'ghost')}</div>
  </div>
</section>

<section class="home-closer">
  <div class="wrap">
    <p class="eyebrow">A more useful outside view</p>
    <h2>Make the next security conversation more precise.</h2>
    <p class="section-lede">Start with a genuine example or request a carefully
    scoped assessment for infrastructure you are authorised to manage.</p>
    <div class="hero-actions">
      {btn(primary_url, primary_label, 'primary', 'arrow')}
      {btn('/demo/', 'View the recorded demo', 'ghost')}
    </div>
  </div>
</section>
"""
    return layout(
        "/",
        "SMB Scanner Lite — Security Evidence, Without the Guesswork",
        "Independent external security posture assessments with clearly scoped checks, reproducible observations, and honest reporting. Explore a recorded report.",
        body, active="home", schema=schema, body_class="home-page",
        page_extra={"mainEntity": {"@id": structured.SOFTWARE_ID}},
    )
