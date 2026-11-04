"""SMB Scanner Lite product relaunch — human-edited service content.

This is the public website's primary content source. The online DNS/email
assessment is the product. The separately downloadable public sandbox is an
optional educational tool, not the commercial scanning service.

Never advertise an assessment as live unless the release gate is enabled.
"""
from __future__ import annotations

from . import config as C
from . import data as D
from . import snippets as S
from .ui import layout, btn, icon, e, section_head

def enabled() -> bool:
    return C.SAAS["enabled"] is True

def status() -> str:
    return ("Owner-verified online assessment" if enabled()
            else "Online assessment access / opening soon")

def main_button(label: str = "Check your domain") -> str:
    return btn("/scan/", label, "primary", "arrow")

def secondary(label: str = "See a sample report") -> str:
    return btn("/sample-report/", label, "ghost")

def head(label: str, title: str, lead: str, actions: str = "") -> str:
    return f"""<header class="page-head"><div class="wrap">
<p class="eyebrow">{label}</p><h1>{title}</h1>
<p class="lede">{lead}</p>
{f'<div class="hero-actions">{actions}</div>' if actions else ""}
</div></header>"""

def panel(number: str, title: str, text: str) -> str:
    return f"""<article class="relaunch-feature">
<small>{number}</small><h3>{title}</h3><p>{text}</p></article>"""

def article(text: str) -> str:
    return f'<section class="section"><div class="wrap"><div class="prose relaunch-legal">{text}</div></div></section>'

def frame(path: str, title: str, description: str, body: str, *,
          active: str = "", noindex: bool = False, page_type: str = "WebPage"):
    return layout(path, title, description, body, active=active,
                  noindex=noindex, crumbs=[("Home", "/"), (title, None)] if path != "/" else None,
                  page_type=page_type)

def home() -> str:
    sample = D.RECORDED[D.RECORDED_DEFAULT]
    waiting = ("""<span class="product-state"><i></i> Private beta &mdash; accepting verified domains</span>"""
               if enabled() else
               """<span class="product-state"><i></i> Online scans opening soon</span>""")
    work = [
        ("01", "Enter your domain", "Give the exact public hostname and a contact address. The request does not initiate a scan."),
        ("02", "Verify ownership", "Publish a temporary DNS TXT record. We check for the matching value before authorizing any work."),
        ("03", "Run the limited check", "An authorized, single-run worker reviews public DNS and email-authentication settings. No exploitation."),
        ("04", "Review the preview", "See the resulting score and selected findings. The detailed report stays private until payment access is available."),
    ]
    features = [
        ("01 / DNS", "Start with the records", "Resolve the public DNS posture of your domain. Results depend on what a resolver can actually observe."),
        ("02 / Email", "Understand impersonation defenses", "Check published SPF, DKIM selector coverage and DMARC policy without sending mail."),
        ("03 / Evidence", "Know why a finding exists", "Every conclusive result is tied to a specific response, rather than a generic red warning."),
    ]
    steps = "".join(f'<article><small>{a}</small><h3>{b}</h3><p>{c}</p></article>' for a,b,c in work)
    feat = "".join(panel(*f) for f in features)
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="home-dateline"><span class="home-mark"></span>External security, explained clearly</p>
      {waiting}
      <h1>Understand what your domain <span class="grad">reveals.</span></h1>
      <p class="lede">A practical security review for the public side of your business.
      Verify that the domain is yours, inspect DNS and email safeguards, and get
      a clear, evidence-led account of what needs attention.</p>
      <div class="hero-actions">{main_button("Explore online scanning")}
      {secondary("Inspect an example")}</div>
      <div class="hero-meta">
        <span class="meta-item">{icon("shield",16)} Ownership verification first</span>
        <span class="meta-item">{icon("file",16)} Evidence-led reporting</span>
        <span class="meta-item">{icon("lock",16)} No public customer reports</span>
      </div>
    </div>
    <div class="relaunch-hero-artifact" aria-label="Example recorded assessment">
      <div class="relaunch-artifact-top"><span>ASSESSMENT / RECORDED EXAMPLE</span>
      <span>{e(sample["target"])}</span></div>
      <div class="relaunch-artifact-body">
        <p class="eyebrow">An example of the reporting format</p>
        <div class="relaunch-artifact-score"><div><strong>{sample["score"]}<span> / 100</span></strong>
        <span>Historical sample · 28 October 2026</span></div>
        <div><span>GRADE</span><div class="relaunch-artifact-grade">{e(sample["grade"])}</div></div></div>
        <ul class="relaunch-artifact-list">
        <li><span>Measured results</span><b>{sample["counts"]["completed"]} complete</b></li>
        <li><span>Inconclusive results</span><b>{sample["counts"]["inconclusive"]}</b></li>
        <li><span>Underlying evidence</span><b>Included in sample</b></li>
        </ul>
      </div>
      <div class="relaunch-artifact-caption">
      Recorded sandbox data, not a real-time result or a forecast for your domain.
      <a href="/sample-report/">Read full example</a>.</div>
    </div>
  </div>
</section>

<section class="section section--tight"><div class="wrap">
<div class="home-proof-strip">
<div><b>Permission by design</b><span>A matching DNS challenge is required before a live job is eligible to run.</span></div>
<div><b>A focused first release</b><span>Public DNS and email policy only. Other security domains are not implied.</span></div>
<div><b>Understand the result</b><span>A result is attached to observed evidence and a stated assessment boundary.</span></div>
</div></div></section>

<section class="section"><div class="wrap">
{section_head("The service", "Start with what an outsider can measure.",
"A public-domain review will not uncover every security problem. It can reveal policy and configuration gaps that should be understood, owned and fixed.")}
<div class="relaunch-feature-grid">{feat}</div>
<div class="relaunch-links"><a class="tlink" href="/capabilities/">Explore current checks {icon("arrow",16)}</a>
<a class="tlink" href="/limitations/">What a scan cannot prove {icon("arrow",16)}</a></div>
</div></section>

<section class="section section--alt"><div class="wrap">
{section_head("How it works", "Four steps. No scan before proof of control.",
"From a temporary DNS record to a tightly scoped report preview, the process is designed to be understandable without a security team.")}
<div class="relaunch-inline-steps">{steps}</div>
<div class="relaunch-callout mt-3"><p><strong>Service availability:</strong>
{"The online flow is in a limited owner-verified beta." if enabled() else "The portal is prepared, but public scan creation remains disabled while the private deployment is finalized."}
You can explore the recorded example without registering or submitting a domain.</p></div>
<div class="hero-actions">{main_button("Open assessment portal")}{btn("/demo/","Explore sample findings","ghost")}</div>
</div></section>

<section class="section"><div class="wrap relaunch-split">
<div>{section_head("The report", "An answer you can examine, not just a number.",
"The assessment records what the public DNS and email policy indicated at a particular time. Observations, statuses and limitations are as important as the summary score.")}
<div class="relaunch-quote">The useful question is not “Is our domain secure?” It is “What did we observe, and what can we do next?”</div>
<div class="hero-actions">{secondary("Open the recorded report")}</div></div>
<div class="relaunch-list">
<article><small>01</small><div><h3>A readable summary</h3><p>Clear status, grade and prioritized findings for the assessed scope.</p></div></article>
<article><small>02</small><div><h3>Evidence you can challenge</h3><p>Each conclusive result is anchored to actual data, not inferred from a missing response.</p></div></article>
<article><small>03</small><div><h3>Precisely stated limits</h3><p>A DNS/email scan is not portrayed as a penetration test or complete infrastructure audit.</p></div></article>
</div>
</div></section>

<section class="section section--alt"><div class="wrap relaunch-split">
<div>{section_head("Prefer to learn locally?", "A separate desktop sandbox.",
"The downloadable public edition is for learning and demonstration. It accepts only five approved test domains and cannot scan arbitrary customer infrastructure.")}
<div class="hero-actions">{btn("/docs/","Download desktop sandbox","ghost","download")}</div></div>
<div class="relaunch-feature"><small>NOT THE ONLINE SERVICE</small>
<h3>Practice without a customer job.</h3>
<p>Install the standalone Python sandbox on your computer, inspect its documentation and run its restrictive, consent-led tests. Real-domain assessments use the separate verified online workflow.</p>
<a class="tlink mt-2" href="/docs/">Read desktop setup {icon("arrow",16)}</a></div>
</div></section>

<section class="home-closer"><div class="wrap">
<p class="eyebrow">A better starting point</p>
<h2>Make your next security decision with evidence.</h2>
<p class="section-lede">Explore the online assessment workflow or review a real recorded report while launch preparations are completed.</p>
<div class="hero-actions">{main_button("Check assessment availability")}
{btn("/sample-report/","View the sample","ghost")}</div>
</div></section>"""
    return frame("/", "SMB Scanner Lite | Online Domain Security Assessment",
                 "A careful, ownership-verified online assessment of your domain's public DNS and email safeguards, with evidence-led security reporting.",
                 body, active="home")


def capabilities() -> str:
    checks = [
      ("01", "DNS visibility", "Public resolution and selected integrity checks",
       "We retrieve observable DNS records for the verified hostname. DNS answers can differ by resolver and time; a missing or timed-out response is not automatically a vulnerability."),
      ("02", "SPF", "Sending policy", "Inspect the published SPF policy for syntactic issues, multiple records, lookup complexity and whether its stated enforcement is meaningful."),
      ("03", "DMARC", "Domain alignment policy", "Check whether a DMARC record exists, parses coherently and requests monitoring, quarantine or rejection. Published policy is not proof of how all receivers behave."),
      ("04", "DKIM", "Discoverable signing keys", "Look for keys at a limited list of common selectors. An undiscovered selector is inconclusive, not proof that DKIM is absent."),
    ]
    rows="".join(f"""<article class="relaunch-list-item">
      <div class="relaunch-feature"><small>{n} / ONLINE ASSESSMENT</small>
      <h3>{name}</h3><p><strong>{tag}</strong></p><p>{desc}</p></div></article>"""
      for n,name,tag,desc in checks)
    body=head("Service scope","A focused scan, with a clearly defined boundary.",
      "The online service is designed to inspect public DNS and email-authentication configuration for a domain that has passed ownership verification.",
      main_button("Open scanner")+btn("/methodology/","How findings are classified","ghost"))
    body+=f"""<section class="section"><div class="wrap">
    {section_head("What is checked","Four groups of observable signals.",
    "These are categories of checks, not promises of exhaustive coverage.")}
    <div class="relaunch-feature-grid">{rows}</div>
    <div class="relaunch-callout mt-3"><p><strong>Not included in this online release:</strong>
    port scans, TLS negotiation tests, website-header scans, application vulnerabilities,
    exploitation, login testing or internal network discovery. Broader controls belong to
    a separately scoped product, not this automated job.</p></div>
    </div></section>
    <section class="section section--alt"><div class="wrap relaunch-split">
    <div>{section_head("Reading a result","What each status means.","A finding reflects an observation at a specific time.")}</div>
    <div class="relaunch-list">
    <article><small>01</small><div><h3>Pass</h3><p>Observed behavior meets the control's stated criterion.</p></div></article>
    <article><small>02</small><div><h3>Warning</h3><p>Policy is ambiguous, limited or warrants review without proving a vulnerability.</p></div></article>
    <article><small>03</small><div><h3>Fail</h3><p>Measured evidence contradicts a defined security control.</p></div></article>
    <article><small>04</small><div><h3>Inconclusive</h3><p>The result could not be established with adequate confidence.</p></div></article>
    </div></div></section>"""
    return frame("/capabilities/","Online Scan Coverage | SMB Scanner Lite",
      "Exactly what the ownership-verified DNS and email assessment can observe, and which deeper security tests are excluded.",body,active="capabilities")


def methodology() -> str:
    body=head("The method","Every claim has a measurement behind it.",
      "An external assessment observes publicly available behavior. The method must distinguish what it measured from what it cannot know.",
      main_button("View assessment flow")+btn("/limitations/","Read the limitations","ghost"))
    body+=article("""
<h2>01. Permission comes first</h2>
<p>The requester receives a random DNS TXT challenge at <code>_smbscanner-verify</code> under the submitted domain.
An authorized owner adds the value through their DNS provider. A matching response verifies control of that DNS name for a limited period.
It is not identity verification, and it does not grant permission to probe a different domain.</p>
<h2>02. A limited observation profile</h2>
<p>The current GitHub Actions worker requests only the DNS/email profile. It does not launch
active TCP port probes, TLS testing, HTTP header checks or exploitation. Its job is to collect
a narrow, reproducible picture of published DNS and email records.</p>
<h2>03. A status that does not guess</h2>
<p>Checks are classified as pass, warning, fail, inconclusive or not tested, based on what was actually observed.
A timeout cannot be counted as proof that a record is missing. Limited DKIM selector discovery cannot establish
that a domain never signs mail.</p>
<h2>04. Scoring follows actual coverage</h2>
<p>The worker includes a score and grade for the assessed controls. That number does not represent
a full security audit. Unperformed checks and their absence from the tested profile must never be
interpreted as a clean result.</p>
<h2>05. Private results and access</h2>
<p>The backend records the assessment and stores the callback report in D1. A token bound to
the request authorizes status and preview access. The detailed report is not published by
the website. Payment and full-report delivery will be enabled only after a verified payment
integration has been implemented and tested.</p>
<h2>06. Reproduce and review</h2>
<p>The sample report documents a historical demonstration, not the state of any domain today.
For a current report, compare its timestamp, target, tested controls and observed DNS responses
before taking remedial action. Use <a href="/responsible-use/">only authorized targets</a>.</p>
""")
    return frame("/methodology/","Our Assessment Method | SMB Scanner Lite",
      "How domain ownership verification, DNS/email checks, evidence, limited-coverage scoring and private report delivery work.",body,active="methodology")


def docs() -> str:
    body=head("Desktop download","A sandbox you can run on your own computer.",
      "The desktop edition is a separate Python learning environment. It is deliberately restricted to five approved public testing domains and never gives unrestricted scanning access.",
      btn(C.REPO_URL, "Get public sandbox on GitHub","primary","download",True)
      +btn("/scan/","Use the online assessment instead","ghost"))
    body+=article(f"""
<h2>What you are downloading</h2>
<p>The publicly licensed <strong>SMB Scanner Lite v{e(C.PRODUCT_VERSION)} Public Sandbox Edition</strong> educational package,
not the private online worker. It supports the historical demo's restricted testing workflow
and stores consent receipts locally. It cannot scan arbitrary commercial domains.</p>
<h2>Requirements</h2>
<p>Python 3.10 or newer and a terminal. Read the public repository's README and usage policy before running any check.</p>
<h2>Install from source</h2>
<pre><code>git clone https://github.com/muhammad-atif-161/smb-scanner-lite.git
cd smb-scanner-lite
python -m pip install -e .
smb-scanner --help</code></pre>
<p>The package declares the <code>smb-scanner</code> command in its public <code>pyproject.toml</code>.
Its runtime rejects targets outside the hardcoded allowlist. Explicit consent is required.</p>
<h2>Approved training targets</h2>
<ul>
<li><code>example.com</code>, <code>example.org</code>, <code>example.net</code></li>
<li><code>scanme.nmap.org</code></li>
<li><code>badssl.com</code></li>
</ul>
<p>Being listed is not a blanket authorization to conduct intrusive testing. Follow each host's published test scope,
and do not try to disable the runtime allowlist. See <a href="/responsible-use/">responsible use</a>.</p>
<h2>Want to assess your own business domain?</h2>
<p>Use the <a href="/scan/">ownership-verified online flow</a> when available. It uses a separate private worker,
a different authorization model and a limited DNS/email scan profile. The desktop download cannot substitute for it.</p>
""")
    return frame("/docs/","Download the Public Desktop Sandbox | SMB Scanner Lite",
      "Install the restricted Python desktop sandbox for five approved test domains. Real business-domain assessments use the separate online service.",body)


def sample_report() -> str:
    sample=D.RECORDED[D.RECORDED_DEFAULT]
    files=[
     ("HTML","Readable example","/downloads/smb-scanner-lite-recorded-assessment-example-com.html"),
     ("JSON","Structured evidence","/downloads/smb-scanner-lite-recorded-assessment-example-com.json"),
     ("CSV","Spreadsheet-friendly","/downloads/smb-scanner-lite-recorded-assessment-example-com.csv"),
     ("TXT","Plain text","/downloads/smb-scanner-lite-recorded-assessment-example-com.txt")
    ]
    cards="".join(f'<a class="download-card" href="{u}" download><b class="dl-type">{t}</b><span class="dl-name">{label}</span></a>' for t,label,u in files)
    body=head("Recorded example","See how a security report reads.",
      "A genuine saved sandbox assessment of example.com from 28 October 2026. This is a demonstration of format and evidence, not a live finding about your own domain.",
      btn("/demo/","Explore the interactive sample","primary","arrow")+main_button("Start with your domain"))
    body+=f"""<section class="section"><div class="wrap relaunch-split">
    <div>{section_head("At a glance","A visible result with its limits.",
    "The example has a recorded timestamp and report identifier. A score summarizes tested observations, not the absence of all risk.")}
    <p class="small muted">Report: <code>{e(sample["report_id"])}</code></p>
    <p class="small muted">Target: <code>{e(sample["target"])}</code></p>
    <p class="small muted">Recorded: 28 October 2026</p>
    </div><div>{S.score_panel(sample)}</div></div></section>
    <section class="section section--alt"><div class="wrap">
    {section_head("Keep the evidence","Download the recorded report.","These files contain historical sample output only. They do not expose a real customer assessment.")}
    <div class="download-grid">{cards}</div>
    <div class="relaunch-callout mt-3"><p><strong>What changes in the online service?</strong> The live workflow
    performs the narrower DNS/email scan profile, not the full catalog represented in the historic example.
    The paid full-report access flow is still being built.</p></div>
    </div></section>"""
    return frame("/sample-report/","Example Security Report | SMB Scanner Lite",
      "Inspect a real historical security report with observed evidence, grade and downloadable examples in four formats.",body,active="report")


def demo() -> str:
    sample=D.RECORDED[D.RECORDED_DEFAULT]
    body=head("Interactive recorded demo","Explore the evidence without starting a scan.",
      "This saved report is a real historical example. It does not test your browser, device or domain and does not claim that the current online DNS/email profile runs every illustrated check.",
      main_button("Online scan availability")+secondary("Download the report"))
    body+=f"""<section class="section"><div class="wrap">
    {S.recorded_banner()}
    <div class="relaunch-split mt-3">
      <div><h2>The reference assessment</h2>
      <p>Recorded against <code>{e(sample["target"])}</code> on 28 October 2026.
      This specimen includes its timestamp, test context and recorded observations.</p>
      <p>Switch between the summary and findings to see how a result becomes an
      understandable recommendation. No action here sends a live request.</p></div>
      <div>{S.score_panel(sample)}</div>
    </div>
    <div class="panel mt-4" data-tabs="recorded-example">
      <div class="tabs" role="tablist" aria-label="Recorded report sections">
        <button type="button" class="tab" role="tab" id="recorded-tab-summary" aria-controls="recorded-panel-summary" aria-selected="true" tabindex="0">Report context</button>
        <button type="button" class="tab" role="tab" id="recorded-tab-findings" aria-controls="recorded-panel-findings" aria-selected="false" tabindex="-1">Observed findings</button>
      </div>
      <div class="tab-panel" role="tabpanel" id="recorded-panel-summary" aria-labelledby="recorded-tab-summary">
        <h3>What this specimen shows</h3>
        <p>A dated, scoped measurement with a score for its recorded controls.
        The report never substitutes for a current assessment or a certification.</p>
        <p>Report ID: <code>{e(sample["report_id"])}</code></p>
        <div class="hero-actions">{btn("/sample-report/","Download sample evidence","ghost","download")}</div>
      </div>
      <div class="tab-panel" role="tabpanel" id="recorded-panel-findings" aria-labelledby="recorded-tab-findings" hidden>
        <h3>Findings from the recorded run</h3>
        {S.findings_html(sample,limit=6)}
      </div>
    </div>
    </div></section>"""
    return frame("/demo/","Recorded Security Assessment Demo | SMB Scanner Lite",
      "Explore saved security-assessment evidence and findings through interactive tabs without launching a live scan.",body)

def validation() -> str:
    tests=D.PUBLIC_TESTS
    rows="".join(f"<tr><th scope='row'>{e(t['id'])}</th><td>{e(t['name'])}</td><td>{e(t['result']).upper()}</td></tr>" for t in tests)
    body=head("Engineering transparency","The checks have tests, not just claims.",
      "The public sandbox includes a reproducible consent and allowlist test record. The private SaaS worker has separate offline job/lease and callback tests.",
      btn("/methodology/","Read our method","primary","arrow"))
    body+=f"""<section class="section"><div class="wrap">
    {section_head("Published test record","What is publicly reproducible.","These are the five recorded tests of the desktop training edition, not independent audit certifications.")}
    <div class="table-wrap"><table class="relaunch-table"><thead><tr><th>Test</th><th>Purpose</th><th>Recorded</th></tr></thead>
    <tbody>{rows}</tbody></table></div>
    <p class="small muted mt-2">The online backend also has offline tests for claim exclusivity, authorization, callback digest validation and report locks.
    A passing unit test does not establish production reliability or GitHub Actions commercial-use approval.</p>
    <div class="relaunch-links"><a href="{e(C.REPO_URL)}" rel="noopener" target="_blank">Review desktop source</a>
    <a href="/limitations/">Review limitations</a></div>
    </div></section>"""
    return frame("/validation/","Validation & Test Evidence | SMB Scanner Lite",
      "Published sandbox tests and an explanation of the separate SaaS worker's offline test coverage, with important limitations.",body)
