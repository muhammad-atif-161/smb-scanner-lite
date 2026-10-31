"""Validation, FAQ, limitations, responsible use and about pages."""

from __future__ import annotations

from . import config as C
from . import data as D
from . import schema as structured
from . import snippets as S
from .ui import btn, cta_band, e, icon, layout, section_head

TEST_RUN = {
    "command": "PYTHONPATH=src python3 -m unittest discover -s tests -v",
    "date": "30 October 2026, 14:01 UTC",
    "runtime": "CPython 3.11.2 on Linux",
    "summary": "Ran 5 tests in 0.031s — OK",
    "scope": "Public repository test suite (tests/test_sandbox.py)",
}


def validation() -> str:
    crumbs = [("Home", "/"), ("Validation & Trust", None)]

    test_rows = "".join(
        f"<tr><th scope='row'><span class='mono'>{t['id']}</span><br><span class='mono tiny'>{e(t['name'])}</span></th>"
        f"<td>{e(t['objective'])}</td><td>{e(t['expected'])}</td>"
        f"<td>{S.status_badge('pass')}</td><td class='tiny'>{e(t['notes'])}</td></tr>"
        for t in D.PUBLIC_TESTS
    )

    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Validation &amp; trust</p>
    <h1>Credibility from evidence, not from badges.</h1>
    <p class="lede">There are no customer logos, review scores or usage statistics on this page, because none are held with documented permission. What is published instead can be checked: a test record you can reproduce, a documented method, real sample evidence and an explicit list of limits.</p>
    <div class="hero-actions">{btn('/validation/#test-record', 'Jump to the test record', 'primary', 'check-circle')}{btn(C.REPO_URL, 'Run the tests yourself', 'ghost', 'external', external=True)}</div>
  </div>
</div>

<section class="section section--tight">
  <div class="wrap">
    <div class="notice notice--accent reveal">
      {icon('info', 18, 'notice-icon')}
      <div class="notice-body"><strong>What this page does not do</strong><p>It does not invent customer proof. It does not publish a test count that cannot be reproduced. A larger internal validation register is maintained in the private repository; its contents and results are not published here, and no figure from it is claimed on this site.</p></div>
    </div>
  </div>
</section>

<section class="section section--flush" id="test-record">
  <div class="wrap">
    {section_head("1 &middot; Test record", "The public sandbox suite, test by test.", "Five tests, all reproducible from the public repository, covering the boundaries that matter most: the five-domain allowlist, out-of-scope rejection, mandatory consent, hash-chain integrity and command-line enforcement.")}

    <div class="grid g2 mt-2" style="align-items:start">
      <div class="card reveal">
        <div class="row" style="justify-content:space-between"><span class="tag">last recorded run</span><span class="status-badge status-pass">all passing</span></div>
        <h3 class="mt-2" style="margin-bottom:0.2rem">{e(TEST_RUN['summary'])}</h3>
        <p class="small muted">Executed {e(TEST_RUN['date'])} &middot; {e(TEST_RUN['runtime'])}</p>
        <div class="evidence mt-1"><span class="val">{e(TEST_RUN['command'])}</span><button class="copy" type="button" data-copy="{e(TEST_RUN['command'])}">Copy</button></div>
        <p class="faint tiny mt-2">The log line below is the literal tail of that run. The blocked-target message is expected output from the negative test, not an error.</p>
        <div class="evidence"><span class="val">test_cli_enforces_sandbox_and_consent ... ERROR: TARGET BLOCKED ('unauthorized-domain.com') ... ok
test_consent_proof_hash_chain_and_sandbox_report ... ok
test_exactly_five_public_sandbox_domains_allowed ... ok
test_non_sandbox_domains_and_ips_are_blocked ... ok
test_scan_requires_explicit_user_consent ... ok

Ran 5 tests in 0.031s

OK</span></div>
      </div>
      <div class="reveal">
        <ul class="trust-list">
          <li><strong>Scope of the record</strong>The five tests in <span class="mono">tests/test_sandbox.py</span> plus the recorded assessment output. Nothing else is presented as validated.</li>
          <li><strong>What the tests protect</strong>The restriction is the product. These tests fail if the allowlist widens, if consent becomes optional, or if the hash chain stops chaining.</li>
          <li><strong>What they do not prove</strong>That every control in the private engine behaves correctly, or that any third-party infrastructure was tested. Those claims are not made.</li>
          <li><strong>Roadmap, stated as roadmap</strong>Expanding the published suite into a larger regression register is planned work, not completed work.</li>
        </ul>
        <div class="row mt-2">
          <a class="tlink" href="{C.REPO_URL}/blob/main/tests/test_sandbox.py" rel="noopener" target="_blank">Read the test source {icon('external', 16)}</a>
        </div>
      </div>
    </div>

    <div class="table-wrap mt-3 reveal">
      <table>
        <caption>Recorded run: {e(TEST_RUN['date'])}. Every row is a live unit test in the public repository, not a manual checklist item.</caption>
        <thead><tr><th scope="col">Test</th><th scope="col">Objective</th><th scope="col">Expected result</th><th scope="col">Status</th><th scope="col">Notes</th></tr></thead>
        <tbody>{test_rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("2 &middot; Technical methodology", "The method is documented, not implied.", "Measurement, statuses, scoring weights, grade bands, evidence handling and the boundary of the method are published in full on the methodology page.")}
    <div class="grid g3">
      <div class="card reveal">
        <div class="card-icon">{icon('eye', 20)}</div>
        <h3>What is observed</h3>
        <p>Public DNS records, mail authentication policy, TLS negotiation, HTTP response headers and protocol-level reachability of defined high-risk ports. Nothing authenticated.</p>
        <a class="tlink mt-1" href="/methodology/">Methodology {icon('arrow', 16)}</a>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('gauge', 20)}</div>
        <h3>How it is scored</h3>
        <p>Weighted over conclusive controls: pass full credit, warning partial, fail none, inconclusive excluded. Category weights and grade bands are published.</p>
        <a class="tlink mt-1" href="/methodology/#scoring">Scoring {icon('arrow', 16)}</a>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('list', 20)}</div>
        <h3>The control catalog</h3>
        <p>All 22 controls documented with what each evaluates, why it matters, an example of its evidence, and whether the public sandbox actually runs it.</p>
        <a class="tlink mt-1" href="/capabilities/">Catalog {icon('arrow', 16)}</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("3 &middot; Sample evidence", "A result you can inspect line by line.", "The recorded assessment of example.com is published in full: score, grade, eight findings, the evidence behind each one and the metadata of the run.")}
    <div class="grid g2" style="align-items:start">
      <div class="card reveal">
        <div class="recorded-banner" style="margin-bottom:0.6rem"><span class="dot"></span><span><b>Recorded</b> 28 Oct 2026</span></div>
        <div class="row" style="justify-content:space-between;align-items:flex-end">
          <div>
            <span class="mono faint tiny">POSTURE SCORE</span>
            <p style="font-family:var(--font-head);font-size:2.4rem;font-weight:600;margin:0;letter-spacing:-0.04em">86<span class="faint" style="font-size:1rem"> / 100</span></p>
          </div>
          <span class="grade-badge"><b>B</b><span>Grade</span></span>
        </div>
        {S.category_bars(D.RECORDED[D.RECORDED_DEFAULT])}
        <div class="row mt-2">{btn('/sample-report/', 'Open the report', 'ghost', 'arrow')}</div>
      </div>
      <div class="card reveal">
        <h3>Evidence, verbatim</h3>
        <p class="small muted">Three lines from the recorded run. Copy one and re-run the equivalent query from outside your network.</p>
        <div class="evidence"><span class="val">v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s</span><button class="copy" type="button" data-copy="v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s">Copy</button></div>
        <div class="evidence" style="margin-top:.4rem"><span class="val">v=spf1 -all (strict no-mail policy for reserved domain).</span><button class="copy" type="button" data-copy="v=spf1 -all (strict no-mail policy for reserved domain).">Copy</button></div>
        <div class="evidence" style="margin-top:.4rem"><span class="val">Zone signed with validated RRSIG and parent DS delegation.</span><button class="copy" type="button" data-copy="Zone signed with validated RRSIG and parent DS delegation.">Copy</button></div>
        <p class="faint tiny mt-2">The recorded run also showed two warnings: missing HSTS and missing Content-Security-Policy. They are published as warnings, not omitted.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("4 &middot; Privacy and safety", "What the site and the tool each do with data.", "This website is static. The sandbox runs on your machine. Neither sells data, and consent is recorded locally before any run.")}
    <div class="grid g2">
      <div class="card reveal">
        <div class="card-icon">{icon('shield', 20)}</div>
        <h3>The website</h3>
        <ul class="card-list">
          <li>No analytics, no advertising pixels, no tracking cookies</li>
          <li>No account, no login, no newsletter list</li>
          <li>Enquiry form fields are used to reply to that enquiry only</li>
          <li>The demo loads static stored data; it never contacts a target</li>
        </ul>
        <a class="tlink mt-1" href="/privacy/">Privacy policy {icon('arrow', 16)}</a>
      </div>
      <div class="card reveal">
        <div class="card-icon card-icon--cyan">{icon('lock', 20)}</div>
        <h3>The sandbox</h3>
        <ul class="card-list">
          <li>Five approved domains, enforced before any network request</li>
          <li>Consent receipt written locally, chained by SHA-256</li>
          <li>Read-only checks; no login, no payload, no exploitation</li>
          <li>Reports stay on the machine that produced them</li>
        </ul>
        <a class="tlink mt-1" href="/responsible-use/">Responsible use {icon('arrow', 16)}</a>
      </div>
    </div>
    <div class="callout mt-3 reveal">
      {icon('alert', 20)}
      <div><p><strong>Authorisation is not optional.</strong> The full engine is for domains you own or have written permission to assess. The MIT licence on the published code governs the software; it does not grant permission to test third-party infrastructure.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("5 &middot; Product limitations", "What it cannot establish, written down.", "A security product that only describes its strengths is not giving you a usable picture. The limitations page states the boundary of the evidence in plain language.")}
    <div class="grid g2">
      <div class="card reveal">
        <h3>Structural limits</h3>
        <ul class="card-list">
          <li>No visibility behind authentication or inside the network</li>
          <li>No proof that a weakness is exploitable</li>
          <li>No ability to detect compromise, past or present</li>
          <li>No coverage of people, process or physical security</li>
        </ul>
        <a class="tlink mt-1" href="/limitations/">Full limitations {icon('arrow', 16)}</a>
      </div>
      <div class="card reveal">
        <h3>Honest status of the project</h3>
        <ul class="card-list">
          <li>No published customer base, and none claimed</li>
          <li>No revenue claims, no usage statistics</li>
          <li>Public sandbox is a demonstration edition, not a service</li>
          <li>Assessment capacity is arranged directly and reviewed manually</li>
        </ul>
        <a class="tlink mt-1" href="/acquisition/">Project status and acquisition {icon('arrow', 16)}</a>
      </div>
    </div>
  </div>
</section>

{cta_band("Reproduce the record, then judge the product.", "The test suite and the recorded assessment are both public. That is the point.", ("/docs/", "Install the sandbox"), ("/contact/", "Ask a technical question"))}
"""
    return layout(
        "/validation/",
        "Validation & Trust — Reproducible Test Record | SMB Scanner Lite",
        "The published validation record for SMB Scanner Lite: five reproducible unit tests covering the allowlist, consent and hash chain, plus the recorded assessment, documented methodology and stated limits.",
        body,
        crumbs=crumbs,
    )


# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------

def faq() -> str:
    crumbs = [("Home", "/"), ("FAQ", None)]
    groups = []
    for key, label in D.FAQ_GROUPS:
        items = [q for q in D.FAQ if q[1] == key]
        if not items:
            continue
        rows = "".join(
            f'<details class="reveal"><summary>{q[0]}</summary><div><p>{q[2]}</p></div></details>'
            for q in items
        )
        groups.append(f"""
<div class="mt-4" id="faq-{key}">
  <h2 style="font-size:1.15rem">{e(label)}</h2>
  <div class="acc mt-2" style="max-width:52rem">{rows}</div>
</div>""")

    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">FAQ</p>
    <h1>Questions people actually ask.</h1>
    <p class="lede">Short answers, no upsell. Where a question needs the technical version, it links to the methodology page rather than repeating it in vague terms.</p>
    <div class="hero-actions">{btn('/methodology/', 'Read the methodology', 'primary', 'arrow')}{btn('/contact/', 'Ask something else', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    <div class="row" style="justify-content:space-between;align-items:flex-end">
      <div class="chips">
        {''.join(f'<a class="btn btn-subtle btn-sm" href="#faq-{k}">{e(v)}</a>' for k, v in D.FAQ_GROUPS if any(q[1] == k for q in D.FAQ))}
      </div>
      <div class="row" data-acc-controls="#faq-all">
        <button class="btn btn-subtle btn-sm" type="button" data-acc-open>Expand all</button>
        <button class="btn btn-subtle btn-sm" type="button" data-acc-close>Collapse all</button>
      </div>
    </div>
    <div id="faq-all">{''.join(groups)}</div>
  </div>
</section>

{cta_band("Still unsure whether this fits your situation?", "Ask a direct question. There is no sales sequence and no automatic scan.", ("/contact/", "Contact the maintainer"), ("/request-assessment/", "Request an assessment"))}
"""
    # FAQPage is still valid structured data for visible question/answer pairs,
    # but Google has limited FAQ rich results to authoritative government and
    # health sites. The markup is kept because it accurately describes content
    # that is on the page; no rich result is expected from it.
    faq_main_entity = structured.faq_entity(
        (
            q[0].replace("&ndash;", "-"),
            q[2].replace("&ndash;", "-").replace("<strong>", "").replace("</strong>", ""),
        )
        for q in D.FAQ
    )
    return layout(
        "/faq/",
        "FAQ — SMB Scanner Lite Security Posture Assessment",
        "Straight answers about SMB Scanner Lite: what it measures, how the 0-100 score and A-F grades work, why the public demo is restricted to five domains, what happens after an assessment request, and what the tool cannot do.",
        body,
        active="faq",
        crumbs=crumbs,
        page_type="FAQPage",
        page_extra={"mainEntity": faq_main_entity},
    )


# ---------------------------------------------------------------------------
# Limitations
# ---------------------------------------------------------------------------

def limitations() -> str:
    crumbs = [("Home", "/"), ("Assessment Limitations", None)]
    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Limitations</p>
    <h1>What an external assessment cannot tell you.</h1>
    <p class="lede">This page exists because a security product that only describes its strengths is not giving you a usable picture. These are the limits of the method, the tool and the evidence it produces &mdash; stated plainly, and reflected in how findings are worded.</p>
    <div class="hero-actions">{btn('/methodology/', 'Read the methodology', 'primary', 'arrow')}{btn('/sample-report/', 'See how findings are worded', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    <div class="prose">
      <h2 id="scope">1. Scope is external and unauthenticated</h2>
      <p>SMB Scanner Lite answers questions from the public internet, without credentials. It cannot see anything behind a login: applications, customer portals, admin interfaces that require a session, internal APIs, databases on a private network, directory services, endpoints or backups.</p>
      <p>A clean external result therefore means <em>the measured external controls looked correct at that moment</em>. It says nothing about what is happening behind the login screen.</p>

      <h2 id="exploitability">2. A failed control is not a proven vulnerability</h2>
      <p>When a control fails, it means the published expectation was not met &mdash; a DMARC policy set to <code>p=none</code>, an absent Content-Security-Policy, an SMB negotiate answered on port 445. None of these is an exploit. Proving exploitability requires attempting exploitation, which this tool never does, and which requires separate written authorisation.</p>

      <h2 id="compromise">3. It cannot detect compromise</h2>
      <p>External observation cannot establish whether a system has been breached, whether an account is compromised, or whether data has been exfiltrated. It can highlight exposure that often precedes those outcomes. That is a different claim, and the report keeps them separate.</p>

      <h2 id="vantage">4. Results depend on the vantage point</h2>
      <p>A DNS record can resolve differently for different resolvers. A firewall can answer one source address and drop another. A CDN can present different security headers on different routes. A finding is an observation made from one place at one time, which is why every finding quotes the observation rather than only the verdict.</p>

      <h2 id="time">5. A finding describes a moment</h2>
      <p>Configuration changes. A certificate valid at assessment time may expire next week; a header added yesterday may not appear in an older report. Always check the assessment timestamp before acting on a result, and re-assess after changes.</p>

      <h2 id="inconclusive">6. Silence is not evidence</h2>
      <p>Some controls will return no conclusive answer: rate limiting, geo-blocking, filtering or a slow endpoint. Those results are marked inconclusive and excluded from the score. They are not converted into failures, and they are not counted as passes.</p>

      <h2 id="coverage">7. The public edition runs a subset</h2>
      <p>The published sandbox executes eight controls across DNS, email authentication, transport and browser headers. The remaining controls belong to the private engine and are not executed publicly. A sandbox score is therefore not directly comparable to a full 22-control assessment, and the site says so wherever a sandbox score appears.</p>

      <h2 id="not-audit">8. It is not an audit, a certification or a guarantee</h2>
      <p>The output is not an ISO 27001 assessment, not a SOC 2 opinion, not a penetration-test report and not a compliance certificate. It does not certify that a business is secure, and no result from this tool should be presented as such to a customer, regulator or insurer.</p>

      <h2 id="not-commercial">9. A sandbox report is a demonstration</h2>
      <p>Reports produced by the public sandbox against its five reserved test domains are educational output. They are not commercial assessments of those domains, and they must not be represented as such.</p>

      <div class="callout">
        {icon('info', 20)}
        <div><p><strong>How to use a result responsibly.</strong> Treat every finding as a reason to look, not a verdict. Verify the observation from your own network, prioritise by the exposure it creates, and record what you changed. The report is a starting point for a conversation with someone who can act on it.</p></div>
      </div>
    </div>
  </div>
</section>

{cta_band("Want the full 22-control assessment instead of the sandbox?", "A private assessment covers your domain, with scope and written authorisation agreed first.", ("/request-assessment/", "Request an assessment"), ("/contact/", "Ask a question"))}
"""
    return layout(
        "/limitations/",
        "Assessment Limitations — What External Security Assessment Cannot Show",
        "The stated limits of SMB Scanner Lite: external-only scope, no exploitability proof, no compromise detection, vantage-point dependence, inconclusive results, and why a high score is not a guarantee.",
        body,
        crumbs=crumbs,
    )


# ---------------------------------------------------------------------------
# Responsible use
# ---------------------------------------------------------------------------

def responsible_use() -> str:
    crumbs = [("Home", "/"), ("Responsible Use", None)]
    commitments = [
        ("target", "Authorised targets only", "The full engine is for domains you own or are explicitly authorised in writing to assess. The public sandbox is limited to five reserved test domains, each published for that purpose."),
        ("lock", "The restriction is enforced, not requested", "The five-domain allowlist lives in the runtime. A look-alike subdomain, an alternate port, a raw IP address or a trailing dot is rejected before a network request is made."),
        ("file", "No claim without evidence", "A finding quotes the record, header or handshake behind it. Silence from the network is reported as inconclusive, never converted into an invented failure."),
        ("shield-alert", "No exploitation", "SMB is identified with a single unauthenticated negotiate that reads dialect and signing requirements. There is no login, no share listing, no fuzzing and no payload."),
        ("fingerprint", "Consent before action", "Each sandbox run records a hash-chained receipt on the operator's machine before any lookup. The receipt travels with the report."),
        ("scale", "Not a commercial audit", "A sandbox report is a lesson and a demonstration. It is not a certificate that a business is secure, and it must not be presented as one."),
    ]
    cards = "".join(f"""
<article class="card reveal">
  <div class="card-icon">{icon(i, 20)}</div>
  <h3>{e(title)}</h3>
  <p>{e(text)}</p>
</article>""" for i, title, text in commitments)

    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Responsible use</p>
    <h1>A scanner that is proud of what it refuses to do.</h1>
    <p class="lede">Six commitments the project is built around. Each one is enforced by the runtime or the reporting model, not just stated in a policy document.</p>
    <div class="hero-actions">{btn('/privacy/', 'Privacy policy', 'primary', 'shield')}{btn('/limitations/', 'Assessment limitations', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    <h2 class="sr-only">Responsible use commitments</h2>
    <div class="grid g2">{cards}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Authorisation</p>
        <h2>If you cannot answer "who said yes?", do not run it.</h2>
        <p class="section-lede">Assessing a system you do not own can breach computer-misuse law in most jurisdictions, regardless of intent. The five public domains exist precisely so that learning does not require that risk.</p>
        <ul class="trust-list mt-2">
          <li><strong>Ownership</strong>You own the domain and the infrastructure behind it.</li>
          <li><strong>Written permission</strong>Or the owner has given you documented authority to assess it, for a defined scope and period.</li>
          <li><strong>Scope clarity</strong>Hosting providers, CDNs and managed platforms may be separate parties &mdash; their terms apply too.</li>
        </ul>
        <div class="btn-row mt-3">{btn('/request-assessment/', 'Request an authorised assessment', 'primary', 'arrow')}</div>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('book', 20)}</div>
        <h3>Licence and acceptable use</h3>
        <p>The published code is MIT licensed. That licence governs the software itself &mdash; it does not grant permission to test third-party infrastructure, and it does not turn a sandbox report into a commercial audit.</p>
        <p class="small">The public edition is restricted to five testing domains. Attempting to bypass, modify or circumvent that allowlist, or to extract the protected runtime, is outside the acceptable use described in the privacy policy.</p>
        <div class="row mt-1"><a class="tlink" href="{C.REPO_URL}/blob/main/LICENSE" rel="noopener" target="_blank">Read the licence {icon('external', 16)}</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g3">
      <div class="card reveal">
        <div class="card-icon">{icon('user', 20)}</div>
        <h3>If you receive a report about your domain</h3>
        <p>Ask who ran it, under what authority, and at what time. A legitimate report names the target, the scanner version, the timestamp and the consent receipt used. Without those, treat it as unverified.</p>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('bell', 20)}</div>
        <h3>Reporting a concern</h3>
        <p>If you believe this project or its documentation has been used irresponsibly, contact the maintainer with the details. Concerns about misuse are treated as priority correspondence.</p>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('terminal', 20)}</div>
        <h3>Teaching with it</h3>
        <p>The sandbox edition exists for teaching and demonstration. The five reserved domains make it safe to run in a classroom without touching anyone else's infrastructure.</p>
      </div>
    </div>
  </div>
</section>

{cta_band("Use it where you have the right to use it.", "For anything outside the five public domains, request an assessment and start with authorisation.", ("/request-assessment/", "Request an assessment"), ("/contact/", "Report a concern"))}
"""
    return layout(
        "/responsible-use/",
        "Responsible Use — Authorisation and Acceptable Use | SMB Scanner Lite",
        "Authorisation requirements and acceptable use for SMB Scanner Lite: enforced allowlist, consent receipts, no exploitation, and clear guidance on when an assessment is legitimate.",
        body,
        crumbs=crumbs,
    )


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

def about() -> str:
    crumbs = [("Home", "/"), ("About", None)]
    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>A small-business tool, built by someone who wanted the honest version.</h1>
    <p class="lede">Large organisations pay teams to watch their domains every day. A clinic, a workshop or a family business usually does not. SMB Scanner Lite exists so that the outside view &mdash; forged mail, weak transport, an office file share facing the internet &mdash; can be explained without theatre.</p>
    <div class="hero-actions">{btn('/capabilities/', 'See the capabilities', 'primary', 'arrow')}{btn('/validation/', 'Check the evidence', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <h2>Purpose</h2>
        <div class="prose">
          <p>Show a domain's public security posture with proof attached to every line. Help an owner, or the person who looks after their IT, know what to fix first. Teach the difference between a real finding and a guess.</p>
          <p>The product is deliberately narrow. It assesses a defined catalog of externally observable controls, scores what it actually measured, and states the limits of the method in the same report that delivers the score.</p>
        </div>
        <h2 class="mt-4">Who it is for</h2>
        <div class="prose">
          <ul>
            <li>Small and medium businesses that need an outside view of their public exposure</li>
            <li>IT administrators and managed service providers who need a defensible baseline</li>
            <li>Cybersecurity consultants who want evidence rather than assertion</li>
            <li>Defensive learners and teachers who want a scanner that refuses to wander onto someone else's network</li>
          </ul>
        </div>
        <h2 class="mt-4">Who it is not for</h2>
        <div class="prose">
          <p>Anyone hoping to probe arbitrary companies, break in, or print a frightening report with nothing behind it. The public edition will not do that, and the private engine is distributed only for authorised assessments.</p>
        </div>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('user', 20)}</div>
        <h3>{e(C.AUTHOR)}</h3>
        <p class="small">Cybersecurity learner based in Rawalpindi, Punjab, Pakistan. Self-taught, building tools that can be explained to a non-specialist.</p>
        <p class="small">Fortinet NSE 2 and Cisco's Introduction to Cybersecurity sit alongside school study; this project is the practice.</p>
        <div class="row mt-1">
          <a class="tlink" href="{C.AUTHOR_URL}" rel="noopener" target="_blank">GitHub profile {icon('external', 16)}</a>
          <a class="tlink" href="mailto:{C.CONTACT_EMAIL}">Email {icon('mail', 16)}</a>
        </div>
        <hr>
        <h4>How it was built</h4>
        <p class="small">Python 3. Checks follow published standards: SPF (RFC 7208), DMARC (RFC 7489), DNSSEC (RFC 4034), TLS guidance, and an unauthenticated SMB2 negotiate that reads only dialect and signing.</p>
        <p class="small">Scores use an evidence model with four statuses &mdash; pass, warning, fail and inconclusive. The full source, catalog and tests live in a private repository; this public repository ships the website, the documentation and a sandbox whose allowlist is five domains long.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Project status", "Stated precisely, because vagueness would be misleading.")}
    <div class="grid g3">
      <div class="card reveal">
        <div class="card-icon">{icon('code', 20)}</div>
        <h3>What is public</h3>
        <p>This website, the documentation, the recorded assessment, the privacy policy and a sandbox runtime hard-locked to five test domains, with its test suite.</p>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('lock', 20)}</div>
        <h3>What stays private</h3>
        <p>The complete engine with all 22 controls, the scoring model, the internal test suite and the development history. A public scanner that can be pointed at any host becomes a weapon.</p>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('scale', 20)}</div>
        <h3>What is not claimed</h3>
        <p>No customer base, no recurring revenue, no usage statistics and no testimonials are asserted on this site. Assessment capacity is arranged directly and reviewed manually.</p>
      </div>
    </div>
    <div class="notice mt-3 reveal">
      {icon('info', 18, 'notice-icon')}
      <div class="notice-body"><strong>Project acquisition</strong><p>The complete project is available for acquisition as a documented software project. Terms, deliverables and the price are set out separately, so the product message on this site is not mixed with the sale message.</p></div>
    </div>
    <div class="row mt-2">{btn('/acquisition/', 'Acquisition details', 'ghost', 'arrow')}{btn('/contact/', 'Contact the maintainer', 'ghost')}</div>
  </div>
</section>

{cta_band("Read the claims, then check them.", "Everything asserted about this product is either reproducible from the public repository or stated as a limitation.", ("/validation/", "Validation record"), ("/methodology/", "Methodology"))}
"""
    return layout(
        "/about/",
        "About the Project — SMB Scanner Lite",
        "Why SMB Scanner Lite exists, who it is for, what is published and what stays private, and the honest status of the project.",
        body,
        crumbs=crumbs,
        page_type="AboutPage",
        page_extra={
            "mainEntity": {"@type": "Person", "name": C.AUTHOR, "url": C.AUTHOR_URL}
        },
    )
