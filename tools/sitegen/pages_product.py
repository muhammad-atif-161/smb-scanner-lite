"""Capabilities, sample report, methodology, recorded demo and documentation pages."""

from __future__ import annotations

from . import config as C
from . import data as D
from . import snippets as S
from .ui import btn, cta_band, e, icon, layout, notice, section_head


# ---------------------------------------------------------------------------
# Capabilities
# ---------------------------------------------------------------------------

def capabilities() -> str:
    crumbs = [("Home", "/"), ("Capabilities", None)]
    record = D.RECORDED[D.RECORDED_DEFAULT]

    cat_nav = "".join(
        f'<a class="btn btn-subtle btn-sm" href="#cat-{cat["key"]}">{icon(cat["icon"], 16, "btn-icon")}{e(cat["short"])}</a>'
        for cat in D.CATEGORIES
    )

    groups = []
    for cat in D.CATEGORIES:
        cards = []
        for control in D.controls_in(cat["key"]):
            coverage = (
                '<span class="status-badge status-pass">In recorded run</span>'
                if control["recorded"]
                else '<span class="status-badge status-inconclusive">Full engine</span>'
            )
            cards.append(f"""
<details class="control-card reveal">
  <summary>
    <span class="ctrl-num">C{control['num']:02d}</span>
    <span class="ctrl-title"><b>{e(control['name'])}</b><span>{e(control['short'])}</span></span>
    <span class="ctrl-chevron" aria-hidden="true"></span>
  </summary>
  <div class="ctrl-body">
    <div class="ctrl-meta">
      {coverage}
      <span class="chip">weight {control['weight']} / 5</span>
      <span class="chip">{e(cat['short'])}</span>
    </div>
    <div class="ctrl-facts">
      <div class="ctrl-fact"><span class="ctrl-fact-label">What it evaluates</span><p>{e(control['evaluates'])}</p></div>
      <div class="ctrl-fact"><span class="ctrl-fact-label">Why it matters</span><p>{e(control['why'])}</p></div>
      <div class="ctrl-fact"><span class="ctrl-fact-label">Example evidence</span>
        <div class="evidence"><span class="val">{e(control['example'])}</span><button class="copy" type="button" data-copy="{e(control['example'])}">Copy</button></div>
      </div>
    </div>
  </div>
</details>""")
        groups.append(f"""
<div class="mt-4" id="cat-{cat['key']}">
  <div class="row" style="justify-content:space-between;align-items:flex-end;gap:1rem">
    <div>
      <p class="eyebrow" style="margin-bottom:0.35rem">{cat['weight']}% of the score</p>
      <h2 style="margin:0">{e(cat['name'])}</h2>
    </div>
    <span class="pill pill-info"><span class="dot dot-info"></span>{len(D.controls_in(cat['key']))} controls</span>
  </div>
  <p class="section-lede" style="max-width:52rem">{e(cat['intro'])}</p>
  <div class="acc mt-2">{''.join(cards)}</div>
</div>""")

    coverage_rows = "".join(
        f"<tr><td><span class='mono'>C{c['num']:02d}</span></td><th scope='row'>{e(c['name'])}</th>"
        f"<td>{e(D.category(c['cat'])['short'])}</td>"
        f"<td>{'Recorded run' if c['recorded'] else 'Full engine'}</td></tr>"
        for c in D.CONTROLS
    )

    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Capabilities</p>
    <h1>Twenty-two controls, documented one by one.</h1>
    <p class="lede">What each control evaluates, why it matters to a small business, and an example of the evidence it produces. Nothing here is advertised unless the engine implements it &mdash; and the eight controls in the recorded public run are marked as such.</p>
    <div class="hero-actions">{btn('/sample-report/', 'See a real report', 'primary', 'arrow')}{btn('/methodology/', 'Read the methodology', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    <div class="kpi-row reveal">
      <div class="kpi"><b>22</b><span>controls in the catalog</span></div>
      <div class="kpi"><b>5</b><span>categories, each with a score weight</span></div>
      <div class="kpi"><b>8</b><span>controls covered by the recorded public run</span></div>
      <div class="kpi"><b>0</b><span>exploits, logins or payloads sent</span></div>
    </div>
    <div class="row mt-3" style="justify-content:space-between">
      <div class="chips">{cat_nav}</div>
      <div class="row" data-acc-controls="#catalog">
        <button class="btn btn-subtle btn-sm" type="button" data-acc-open>Expand all</button>
        <button class="btn btn-subtle btn-sm" type="button" data-acc-close>Collapse all</button>
      </div>
    </div>
    <div id="catalog">{''.join(groups)}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Coverage", "What the public edition actually runs.", "The recorded public assessment covers eight controls across DNS, email, transport and headers. The remaining fourteen belong to the full engine, and the public sandbox does not execute them. The catalog above is the product; the coverage column is the honesty.")}
    <div class="table-wrap reveal">
      <table>
        <caption>Coverage is stated per control. A control listed as “Full engine” is implemented in the private engine and is not executed by the published sandbox.</caption>
        <thead><tr><th scope="col">ID</th><th scope="col">Control</th><th scope="col">Category</th><th scope="col">Coverage</th></tr></thead>
        <tbody>{coverage_rows}</tbody>
      </table>
    </div>
    <div class="grid g3 mt-3">
      <div class="card reveal">
        <div class="card-icon">{icon('lock', 20)}</div>
        <h3>Read-only by design</h3>
        <p>DNS queries, TLS handshakes, HTTP header reads and, for exposure controls, a single protocol-level connection. There is no authentication attempt and no payload.</p>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('scale', 20)}</div>
        <h3>Inconclusive is a result</h3>
        <p>A control that returns no conclusive answer inside its timeout is reported as inconclusive and excluded from the score. Silence is never turned into a failure.</p>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('file', 20)}</div>
        <h3>Evidence is mandatory</h3>
        <p>Every conclusive finding carries the record, header or handshake that produced it, so a technical reader can reproduce the observation independently.</p>
      </div>
    </div>
  </div>
</section>

{cta_band("Check the catalog against a real report.", "The recorded example.com assessment shows eight of these controls with their actual evidence, score and grade.", ("/sample-report/", "Open the sample report"), ("/methodology/", "Read the methodology"))}
"""
    return layout(
        "/capabilities/",
        "22 Security Controls — SMB Scanner Lite Capability Catalog",
        "Every control in the SMB Scanner Lite catalog: what it evaluates, why it matters, the evidence it produces, and which controls the public sandbox actually runs.",
        body,
        active="capabilities",
        crumbs=crumbs,
        schema=[
            {
                "@type": "ItemList",
                "name": "SMB Scanner Lite security control catalog",
                "numberOfItems": len(D.CONTROLS),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": c["num"],
                        "name": c["name"],
                        "description": c["evaluates"],
                    }
                    for c in D.CONTROLS
                ],
            }
        ],
    )


# ---------------------------------------------------------------------------
# Sample report
# ---------------------------------------------------------------------------

def sample_report() -> str:
    crumbs = [("Home", "/"), ("Sample Report", None)]
    r = D.RECORDED[D.RECORDED_DEFAULT]

    findings = S.findings_html(r)
    evidence_lines = "".join(
        f'<div class="evidence" style="margin-bottom:.5rem"><span class="val">{e(f["evidence"])}</span>'
        f'<button class="copy" type="button" data-copy="{e(f["evidence"])}">Copy</button></div>'
        for f in r["findings"]
    )

    recommendations = []
    for f in r["findings"]:
        if f.get("remediation"):
            control = D.CONTROL_BY_NUM.get(f["control"])
            recommendations.append(f"""
<div class="card reveal">
  <div class="row" style="justify-content:space-between">
    <span class="component-tag mono">C{control['num']:02d} &middot; {e(control['name'])}</span>
    {S.status_badge(f['status'])}
  </div>
  <h3 style="font-size:1rem">{e(f['title'])}</h3>
  <p>{e(f['remediation'])}</p>
  <div class="evidence"><span class="val">{e(f['evidence'])}</span></div>
</div>""")

    tabs = [
        ("Executive Summary", 0),
        ("Security Findings", 1),
        ("Technical Evidence", 2),
        ("Recommendations", 3),
        ("Assessment Details", 4),
    ]
    tab_html = "".join(
        f'<button class="tab" type="button" role="tab" id="rep-tab-{i}" aria-controls="rep-panel-{i}" '
        f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(label)}</button>'
        for label, i in tabs
    )

    downloads = [
        ("html", "Readable report", "/downloads/smb-scanner-lite-recorded-assessment-example-com.html"),
        ("json", "Machine readable", "/downloads/smb-scanner-lite-recorded-assessment-example-com.json"),
        ("csv", "Spreadsheet ready", "/downloads/smb-scanner-lite-recorded-assessment-example-com.csv"),
        ("txt", "Plain text", "/downloads/smb-scanner-lite-recorded-assessment-example-com.txt"),
    ]
    download_cards = "".join(
        f'<a class="download-card" href="{href}" download><span class="dl-type">{kind}</span>'
        f'<span class="dl-name">{e(label)}</span><span class="tiny faint">{e(href.rsplit("/", 1)[-1])}</span></a>'
        for kind, label, href in downloads
    )

    grade_rows = "".join(
        f"<tr><td><b>{letter}</b></td><td class='mono'>{band}</td><td>{label}</td><td>{desc}</td></tr>"
        for letter, band, label, desc in D.GRADE_BANDS
    )

    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Sample report</p>
    <h1>A complete report, published in full.</h1>
    <p class="lede">This is the recorded SMB Scanner Lite assessment of <span class="mono">example.com</span> from 28 October 2026. Nothing is redacted for marketing and nothing is added: the score, findings, evidence, metadata and consent receipt are exactly what the run produced.</p>
    <div class="hero-actions">{btn('/demo/', 'Explore it interactively', 'primary', 'bolt')}{btn('/capabilities/', 'Match findings to controls', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    {S.recorded_banner("Report " + r["report_id"] + " · consent " + (r["consent_id"] or ""))}

    <div class="panel mt-3" data-tabs="report">
      <div class="panel-head">
        <div>
          <span class="tag">{e(r['edition'])}</span>
          <h2 class="mt-2 h-sm" style="margin:0">{e(r['target'])} &mdash; external posture assessment</h2>
        </div>
        <span class="pill pill-warn"><span class="dot dot-warn"></span>Recorded, not live</span>
      </div>

      <div class="tabs" role="tablist" aria-label="Report sections">{tab_html}</div>

      <div class="tab-panel" role="tabpanel" id="rep-panel-0" aria-labelledby="rep-tab-0">
        <div class="score-panel" data-score-card data-score="{r['score']}">
          <div class="gauge" data-gauge style="--v:{r['score']}">
            <div class="gauge-inner">
              <span class="gauge-value" data-score-value>{r['score']}</span>
              <span class="gauge-label">Posture score</span>
              <span class="gauge-grade">Grade {e(r['grade'])} &middot; {e(r['grade_label'])}</span>
            </div>
          </div>
          <div style="flex:1 1 260px;min-width:0">
            <h3 style="margin-top:0">Executive summary</h3>
            <p class="muted">{e(r['summary'])}</p>
            {S.category_bars(r)}
          </div>
        </div>
        <div class="grid g2 mt-3">
          <div class="card">
            <h3>What this result means</h3>
            <p>Eight controls completed and none returned an inconclusive answer, so the score covers every check that ran. DNS, email authentication and transport are strong. The two warnings are informational browser-header gaps typical of a minimal reference site.</p>
          </div>
          <div class="card">
            <h3>What it does not mean</h3>
            <p>A grade B is not a statement that the domain is secure. It means the controls that were measured met their expectations, subject to the limitations of external observation. No application, identity system or internal network was examined.</p>
          </div>
        </div>
        <div class="notice notice--accent mt-3">{icon('info', 18, 'notice-icon')}<div class="notice-body"><strong>Scope</strong><p>External and read-only. The assessment queried public DNS records, completed TLS handshakes, read HTTP response headers, and made no authentication attempt of any kind.</p></div></div>
      </div>

      <div class="tab-panel" role="tabpanel" id="rep-panel-1" aria-labelledby="rep-tab-1" hidden>
        <p class="small muted">Eight findings, ordered as recorded. Each carries a status, the control it maps to and the observation behind it.</p>
        {findings}
      </div>

      <div class="tab-panel" role="tabpanel" id="rep-panel-2" aria-labelledby="rep-tab-2" hidden>
        <p class="small muted">The literal observations recorded during the run. Copy any line and re-run the equivalent query from outside your own network; if the answer differs, the finding is stale or specific to the assessment vantage point.</p>
        <div class="mt-2">{evidence_lines}</div>
        <div class="table-wrap mt-3">
          <table>
            <caption>Grade bands applied by the scoring model. A 90&ndash;100, B 80&ndash;89, C 65&ndash;79, D 50&ndash;64, F below 50.</caption>
            <thead><tr><th scope="col">Grade</th><th scope="col">Score</th><th scope="col">Band</th><th scope="col">Interpretation</th></tr></thead>
            <tbody>{grade_rows}</tbody>
          </table>
        </div>
      </div>

      <div class="tab-panel" role="tabpanel" id="rep-panel-3" aria-labelledby="rep-tab-3" hidden>
        <p class="small muted">Recommendations are limited to the findings in this run. They are configuration changes with a published basis, not a remediation project plan.</p>
        <div class="grid g2 mt-2">{''.join(recommendations)}</div>
        <div class="callout mt-3">{icon('alert', 20)}<div><p><strong>A failed control is not a confirmed vulnerability.</strong> It means a published expectation was not met. Confirm the observation yourself before treating any finding as a defect, and prioritise by the exposure it creates rather than by the colour of a dot.</p></div></div>
      </div>

      <div class="tab-panel" role="tabpanel" id="rep-panel-4" aria-labelledby="rep-tab-4" hidden>
        <dl class="meta-list">
          <div><dt>Report ID</dt><dd class="mono">{e(r['report_id'])}</dd></div>
          <div><dt>Target</dt><dd>{e(r['target'])} &mdash; {e(r['description'])}</dd></div>
          <div><dt>Assessment timestamp</dt><dd>{e(r['timestamp_display'])}</dd></div>
          <div><dt>Scanner version</dt><dd>v{e(r['version'])}</dd></div>
          <div><dt>Edition</dt><dd>{e(r['edition'])}</dd></div>
          <div><dt>Controls completed</dt><dd>{r['counts']['completed']} completed &middot; {r['counts']['inconclusive']} inconclusive</dd></div>
          <div><dt>Consent receipt</dt><dd class="mono">{e(r['consent_id'])}</dd></div>
          <div><dt>Policy version</dt><dd class="mono">{e(r['policy_version'])}</dd></div>
          <div><dt>Receipt SHA-256</dt><dd class="mono" style="overflow-wrap:anywhere">{e(r['receipt_sha256'])}</dd></div>
          <div><dt>Source</dt><dd>Recorded sandbox run, stored as static output</dd></div>
        </dl>
        <div class="notice mt-3">{icon('shield', 18, 'notice-icon')}<div class="notice-body"><strong>Why a consent receipt is in a report</strong><p>Before any run, the operator accepts the privacy policy and signs a receipt that is hash-chained to the previous one. The receipt is embedded in the report so the authorisation behind the result travels with it. It is stored on the machine that ran the assessment, not on this website.</p></div></div>
      </div>
    </div>

    <div class="mt-4">
      <h2 style="font-size:1.3rem">Download this report</h2>
      <p class="small muted">The same recorded assessment in four formats. The data is sanitised: it contains no internal hostnames, no operator identity beyond the demo label, and no private infrastructure detail.</p>
      <div class="download-grid mt-2">{download_cards}</div>
    </div>

    <div class="grid g3 mt-4">
      <div class="card reveal">
        <div class="card-icon">{icon('terminal', 20)}</div>
        <h3>Reproduce it locally</h3>
        <p>Install the public sandbox and run the same reserved domain on your own machine. The documented commands and expected output are on the documentation page.</p>
        <a class="tlink mt-1" href="/docs/">Installation guide {icon('arrow', 16)}</a>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('gauge', 20)}</div>
        <h3>Understand the score</h3>
        <p>Weights, status credit and grade bands are documented. The score is a weighted summary of what completed &mdash; nothing else.</p>
        <a class="tlink mt-1" href="/methodology/">Scoring methodology {icon('arrow', 16)}</a>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('lock', 20)}</div>
        <h3>Check the limits</h3>
        <p>What an external assessment cannot establish is written down, because a credible tool states the boundary of its own evidence.</p>
        <a class="tlink mt-1" href="/limitations/">Assessment limitations {icon('arrow', 16)}</a>
      </div>
    </div>
  </div>
</section>

{cta_band("Want this report for a domain you own?", "Request an assessment and the same structure is produced for your infrastructure &mdash; after scope and written authorisation are agreed.", ("/request-assessment/", "Request an assessment"), ("/contact/", "Contact the maintainer"))}
"""
    return layout(
        "/sample-report/",
        "Sample Security Assessment Report — SMB Scanner Lite",
        "A complete, genuine SMB Scanner Lite report: 86/100, grade B, eight findings with evidence, recommendations and assessment metadata, downloadable as HTML, JSON, CSV and TXT.",
        body,
        active="report",
        crumbs=crumbs,
        schema={
            "@type": "Report",
            "name": "SMB Scanner Lite recorded assessment of example.com",
            "about": "External security posture assessment",
            "datePublished": C.RECORDED_DATE,
            "author": {"@type": "Organization", "name": C.SITE_NAME, "url": C.SITE_URL},
        },
    )


# ---------------------------------------------------------------------------
# Methodology
# ---------------------------------------------------------------------------

def methodology() -> str:
    crumbs = [("Home", "/"), ("Methodology", None)]

    weights = "".join(
        f"<tr><th scope='row'>{e(cat['name'])}</th><td class='mono'>{cat['weight']}%</td>"
        f"<td>{len(D.controls_in(cat['key']))}</td><td>{e(cat['intro'])}</td></tr>"
        for cat in D.CATEGORIES
    )
    statuses = [
        ("pass", "The observed control meets the published expectation."),
        ("warning", "The control exists but is weaker than intended, or partially configured."),
        ("fail", "The control is absent, or what was observed contradicts the expectation."),
        ("inconclusive", "No conclusive answer arrived before the timeout. This is not a failure."),
    ]
    status_rows = "".join(
        f"<tr><td>{S.status_badge(key)}</td><td>{desc}</td><td class='mono'>"
        f"{'100%' if key == 'pass' else 'partial' if key == 'warning' else '0%' if key == 'fail' else 'excluded'}</td></tr>"
        for key, desc in statuses
    )

    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Methodology</p>
    <h1>Built around evidence, not unexplained scores.</h1>
    <p class="lede">What is measured, how a status is assigned, how the score is weighted, how evidence is preserved, and where the method stops being able to tell you anything. Read this before you quote a number from the tool.</p>
    <div class="hero-actions">{btn('/capabilities/', 'See the 22 controls', 'primary', 'arrow')}{btn('/limitations/', 'Read the limitations', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    <div class="grid g2" style="align-items:start">
      <div>
        {section_head("Measurement", "Only what an outsider can observe.")}
        <div class="prose">
          <p>Every control in the catalog is answered from the public internet, without credentials and without privileged access. In practice that means five kinds of observation:</p>
          <ul>
            <li>DNS queries for records the domain publishes: addresses, mail routing, policy records and delegations.</li>
            <li>Mail authentication policy read from TXT records: SPF, DMARC and discoverable DKIM selectors.</li>
            <li>TLS handshakes against the public endpoint, including protocol version, cipher and certificate chain.</li>
            <li>HTTP response headers from a single unauthenticated request per control.</li>
            <li>Protocol-level reachability of specific high-risk ports, with at most a negotiation exchange &mdash; never a login, a listing or a payload.</li>
          </ul>
          <p>Nothing behind a login is examined. Nothing on a private network is reached. Nothing is enumerated, fuzzed, brute-forced or exploited.</p>
        </div>
      </div>
      <div class="card reveal">
        <div class="card-icon card-icon--cyan">{icon('fingerprint', 20)}</div>
        <h3>Vantage point and reproducibility</h3>
        <p>External observation depends on where it is made. A record can resolve differently for a different resolver, and a firewall can answer one network and drop another.</p>
        <p class="small">That is why every finding quotes the observation itself. A reader can repeat the query from a machine outside their own network and compare the answer. If the two disagree, the finding is stale or vantage-specific &mdash; and the report says that is a normal result, not a tool fault.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Statuses", "Four outcomes, and the difference between them matters.", "The distinction between a failure and an absence of an answer is the core of the evidence model.")}
    <div class="table-wrap reveal">
      <table>
        <caption>Score credit is shown per status. Inconclusive controls are excluded from both the numerator and the denominator of the score.</caption>
        <thead><tr><th scope="col">Status</th><th scope="col">Meaning</th><th scope="col">Score credit</th></tr></thead>
        <tbody>{status_rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("Scoring", "How the 0&ndash;100 score is calculated.", "The score is a weighted mean over the controls that reached a conclusive status. It is arithmetic, not judgement, and it is reproducible from the report.")}
    <div class="grid g2" style="align-items:start">
      <div class="prose">
        <ol>
          <li>Each control resolves to a status: pass, warning, fail or inconclusive.</li>
          <li>Each control carries a severity weight from 1 to 5, reflecting the consequence of the exposure it describes.</li>
          <li>Pass earns full credit, warning earns partial credit, fail earns none. Inconclusive controls are excluded from both sides of the fraction.</li>
          <li>Control results roll up into the five categories using the category weights below.</li>
          <li>The final score is rounded to the nearest integer and mapped to a grade band.</li>
        </ol>
        <p>If every control that ran passed, the score is 100. If none passed, it is 0. Partial configurations land in between, weighted by how much the individual control matters.</p>
        <blockquote>A high score means the measured controls met their expectations. It does not mean the business is secure.</blockquote>
      </div>
      <div class="table-wrap reveal">
        <table>
          <caption>Category weights. The public sandbox reports a read-only subset, so a sandbox score is derived from the subset that ran and is not directly comparable to a full 22-control assessment.</caption>
          <thead><tr><th scope="col">Category</th><th scope="col">Weight</th><th scope="col">Controls</th><th scope="col">What it covers</th></tr></thead>
          <tbody>{weights}</tbody>
        </table>
      </div>
    </div>
    <div class="mt-4">
      <h2 style="font-size:1.3rem">Grade bands</h2>
      <p class="small muted">The same bands apply to every target. The current recorded assessment is grade B.</p>
      {S.grade_scale("B")}
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Evidence", "No claim without evidence.", "Every conclusive finding quotes the record, header or handshake behind it. The report is designed so that a sceptical reader can check it without running the tool.")}
    <div class="grid g3">
      <div class="card reveal">
        <div class="card-icon">{icon('file', 20)}</div>
        <h3>Quoted observation</h3>
        <p>An evidence string is a literal fragment: a DNS answer, an SPF policy, a certificate subject, a header value, a negotiate response code.</p>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('copy', 20)}</div>
        <h3>Copy and re-check</h3>
        <p>Every evidence block in this site can be copied with one click. Re-run the equivalent query yourself and compare &mdash; that is the intended workflow.</p>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('lock', 20)}</div>
        <h3>Consent travelled with it</h3>
        <p>Each report embeds the hash-chained consent receipt recorded before the run, including the policy version and its digest.</p>
      </div>
    </div>
    <div class="callout mt-3 reveal">
      {icon('alert', 20)}
      <div><p><strong>A failed control is not a confirmed vulnerability.</strong> It means the published expectation was not met. It is not an exploit, it is not proof of compromise, and it is not a verdict on the business. Treat every finding as a reason to look, then verify.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("Boundaries", "Where this method stops.", "The limitations are part of the methodology, not a footnote to it.")}
    <div class="grid g2">
      <div class="card reveal">
        <h3>What the method cannot see</h3>
        <ul class="card-list">
          <li>Anything behind authentication: applications, admin panels, customer portals</li>
          <li>Internal networks, directory services and endpoint configuration</li>
          <li>People, process and physical security</li>
          <li>Whether a weakness is actually exploitable</li>
          <li>Compromise, past or present</li>
        </ul>
        <a class="tlink mt-1" href="/limitations/">Full limitations {icon('arrow', 16)}</a>
      </div>
      <div class="card reveal">
        <h3>Known sources of error</h3>
        <ul class="card-list">
          <li>Resolver and location differences producing different answers</li>
          <li>Rate limiting or filtering creating inconclusive results</li>
          <li>Configurations that are correct for the business but unusual for the standard</li>
          <li>Time: a finding describes one moment, not a permanent state</li>
        </ul>
        <p class="small mt-1">When an error is possible, the report states the observing condition instead of hiding it.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Reporting</p>
        <h2>Every report carries proof of authorisation.</h2>
        <p class="section-lede">Before a run, the operator accepts the privacy policy and records a receipt. Receipts are hash-chained, so a deleted or altered entry breaks the chain and verification fails.</p>
        <ul class="trust-list mt-2">
          <li><strong>Contents</strong>Consent ID, ISO-8601 UTC timestamp, operator, target, policy version and digest, previous receipt hash and this receipt's hash.</li>
          <li><strong>Storage</strong>Written to the machine that ran the assessment. Never uploaded to this website.</li>
          <li><strong>Verification</strong>One command re-walks the chain and reports whether it is intact.</li>
        </ul>
        <div class="btn-row mt-3">{btn('/privacy/', 'Privacy policy', 'ghost')}{btn('/validation/', 'See the test record', 'ghost', 'arrow')}</div>
      </div>
      <div class="card reveal">
        <div class="row" style="justify-content:space-between"><span class="tag">consent receipt</span><span class="status-badge status-pass">hash chain intact</span></div>
        <div class="evidence" style="margin-top:.6rem"><span class="val">{{
  "consent_id": "{e(C.RECORDED_CONSENT_ID)}",
  "timestamp_utc": "{e(C.RECORDED_TIMESTAMP)}",
  "operator": "public-demo",
  "target": "example.com",
  "policy_version": "{e(C.POLICY_VERSION)}",
  "statement": "authorised sandbox use",
  "receipt_sha256": "{e(C.RECORDED_RECEIPT_SHA256)}"
}}</span></div>
        <p class="faint tiny mt-2">Sanitised excerpt of the receipt embedded in the recorded report. The operator label is the demonstration identity used for the public run.</p>
      </div>
    </div>
  </div>
</section>

{cta_band("Read the method, then check the evidence.", "The catalog documents every control; the sample report shows what the output looks like when the method is applied.", ("/capabilities/", "Open the control catalog"), ("/sample-report/", "Inspect a real report"))}
"""
    return layout(
        "/methodology/",
        "Assessment Methodology — How SMB Scanner Lite Measures Security Posture",
        "The full method behind SMB Scanner Lite: what is observed, how pass, warning, fail and inconclusive are assigned, how the weighted 0-100 score and A-F grades are calculated, and the limits of external assessment.",
        body,
        active="methodology",
        crumbs=crumbs,
        schema={
            "@type": "TechArticle",
            "headline": "SMB Scanner Lite assessment methodology",
            "about": "External security posture assessment",
            "author": {"@type": "Organization", "name": C.SITE_NAME},
            "datePublished": "2026-10-28",
            "dateModified": "2026-10-30",
        },
    )


# ---------------------------------------------------------------------------
# Recorded demo
# ---------------------------------------------------------------------------

def demo() -> str:
    crumbs = [("Home", "/"), ("Recorded Demo", None)]
    r = D.RECORDED[D.RECORDED_DEFAULT]

    domain_buttons = "".join(
        f'<button class="domain-card" type="button" data-domain="{e(d)}" aria-pressed="false">'
        f'<span class="dc-name">{e(d)}</span>'
        f'<span class="dc-meta">{e(D.RECORDED[d]["source_label"])} &middot; '
        f'{"28 Oct 2026" if D.RECORDED[d]["source"] == "recorded" else "no dated capture"}</span>'
        f'<span class="dc-score">{D.RECORDED[d]["score"]}/100 &middot; {e(D.RECORDED[d]["grade"])}</span></button>'
        for d in C.ALLOWED_DOMAINS
    )

    stages = [
        ("target", "Target checked against the five-domain allowlist"),
        ("consent", "Consent receipt verified (SHA-256 hash chain)"),
        ("run", "Read-only checks recorded"),
        ("reported", "Report rendered from stored evidence"),
    ]
    stage_html = "".join(
        f'<div class="demo-stage-step" data-stage="{key}">{icon("check-circle", 18, "ds-icon")}'
        f"<span><b>{e(text)}</b></span></div>"
        for key, text in stages
    )

    downloads = [
        ("html", "Readable report", "/downloads/smb-scanner-lite-recorded-assessment-example-com.html"),
        ("json", "Machine readable", "/downloads/smb-scanner-lite-recorded-assessment-example-com.json"),
        ("csv", "Spreadsheet ready", "/downloads/smb-scanner-lite-recorded-assessment-example-com.csv"),
        ("txt", "Plain text", "/downloads/smb-scanner-lite-recorded-assessment-example-com.txt"),
    ]
    download_cards = "".join(
        f'<a class="download-card" href="{href}" download><span class="dl-type">{kind}</span>'
        f'<span class="dl-name">{e(label)}</span><span class="tiny faint">{e(href.rsplit("/", 1)[-1])}</span></a>'
        for kind, label, href in downloads
    )

    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Recorded assessment</p>
    <h1>The real thing, stored and labelled.</h1>
    <p class="lede">This page renders a genuine SMB Scanner Lite assessment that was run on 28 October 2026 against <span class="mono">example.com</span>. It is a recording, not a live scan: the timestamp, report ID, scanner version and consent receipt are all shown, and nothing you do here sends a network request to a target.</p>
    <div class="hero-actions">{btn('/sample-report/', 'Read the full report', 'primary', 'file')}{btn('/methodology/', 'How it was measured', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    {S.recorded_banner("Captured " + r["timestamp_display"] + " · report " + r["report_id"])}

    <div class="grid g2 mt-3" style="align-items:start">
      <div class="panel" data-demo>
        <div class="panel-head">
          <h2 style="font-size:1.15rem;margin:0">Choose an approved domain</h2>
          <span class="tag">5 permitted</span>
        </div>
        <p class="small muted">Selecting a domain loads its stored profile. The allowlist below is the same list enforced by the sandbox runtime &mdash; it is not possible to enter an arbitrary target here, because there is no field to type into.</p>
        <div class="domain-grid mt-2" data-demo-domains role="group" aria-label="Approved demonstration domains">{domain_buttons}</div>

        <div class="mt-3">
          <p class="mono faint tiny" style="letter-spacing:.08em;text-transform:uppercase">Loading a recorded profile</p>
          <div class="demo-stage" data-demo-stages>{stage_html}</div>
          <div class="progress-track"><i data-demo-progress></i></div>
        </div>

        <div class="form-status mt-3" data-demo-status role="status" aria-live="polite" hidden></div>
        <noscript>
          <div class="notice notice--warn mt-2">{icon('info', 18, 'notice-icon')}<div class="notice-body"><strong>JavaScript is off</strong><p>The interactive explorer needs JavaScript. The same recorded assessment is published as a complete static report on the <a href="/sample-report/">sample report page</a>.</p></div></div>
        </noscript>
        <div class="mt-3" data-demo-report hidden></div>
      </div>

      <div class="reveal">
        <div class="card">
          <div class="card-icon">{icon('fingerprint', 20)}</div>
          <h3>What "recorded" means here</h3>
          <p>An SMB Scanner Lite run was executed against a reserved test domain with the operator's consent. Its output was stored as static data. This page replays that output. It does not contact example.com, it does not scan your domain, and it cannot be made to scan anything else.</p>
          <ul class="card-list mt-1">
            <li>The score, grade, findings and evidence are the recorded values</li>
            <li>The timestamp is the moment the assessment ran</li>
            <li>Profiles without a dated capture are labelled as reference profiles</li>
            <li>Nothing is generated to look plausible</li>
          </ul>
        </div>
        <div class="table-wrap mt-2">
          <table>
            <caption>Metadata recorded with the public run.</caption>
            <tbody>
              <tr><th scope="row">Target</th><td class="mono">example.com</td></tr>
              <tr><th scope="row">Assessed</th><td>{e(r['timestamp_display'])}</td></tr>
              <tr><th scope="row">Report ID</th><td class="mono">{e(r['report_id'])}</td></tr>
              <tr><th scope="row">Scanner</th><td>v{e(r['version'])} &middot; {e(r['edition'])}</td></tr>
              <tr><th scope="row">Result</th><td>{r['score']}/100 &middot; grade {e(r['grade'])}</td></tr>
              <tr><th scope="row">Controls</th><td>{r['counts']['completed']} completed &middot; {r['counts']['inconclusive']} inconclusive</td></tr>
              <tr><th scope="row">Consent</th><td class="mono">{e(r['consent_id'])}</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Explore the controls", "Open any control to see what it evaluates and what this run recorded.", "All 22 controls are listed. The eight that ran are marked with their recorded status; the rest belong to the full engine and are labelled as not part of this run.")}
    <div class="panel" data-demo>
      <div class="control-explorer">
        <div class="control-list" data-demo-control-list role="group" aria-label="Security controls"></div>
        <div class="control-detail" data-demo-control-detail>
          <p class="muted small">Select a control to see its definition and, where available, the evidence recorded in this run.</p>
        </div>
      </div>
    </div>
    <p class="faint tiny mt-2">Loading the recorded data requires JavaScript. The full catalog is also published as static documentation on the <a href="/capabilities/">capabilities page</a>.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("Downloads", "Take the recorded assessment with you.", "Four formats, sanitised. They contain no internal hostnames, credentials or private infrastructure detail.")}
    <div class="download-grid">{download_cards}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Why the demo is restricted</p>
        <h2>A public scanner that can be aimed at anyone is a weapon.</h2>
        <p class="section-lede">The allowlist is enforced inside the runtime, not in this interface. A look-alike subdomain, a raw IP address, a trailing dot or a different port is rejected before a network request is made.</p>
        <ul class="trust-list mt-2">
          <li><strong>Five names, nothing else</strong>{', '.join(C.ALLOWED_DOMAINS)}</li>
          <li><strong>Rejection happens first</strong>Validation precedes any lookup, so an unapproved target never generates traffic.</li>
          <li><strong>No arbitrary input</strong>This page offers buttons, not a text field. Even the buttons are checked against the allowlist again before data is displayed.</li>
          <li><strong>Consent before action</strong>The actual command-line sandbox requires an accepted policy and a signed receipt before it runs.</li>
        </ul>
        <div class="btn-row mt-3">{btn('/responsible-use/', 'Responsible use policy', 'ghost')}{btn('/docs/', 'Install the sandbox locally', 'ghost', 'arrow')}</div>
      </div>
      <div class="card reveal">
        <div class="card-icon card-icon--cyan">{icon('target', 20)}</div>
        <h3>What you can learn from the demo</h3>
        <ul class="card-list">
          <li>How a posture score and grade are presented alongside the findings that produced them</li>
          <li>What an evidence string looks like, and how to verify one yourself</li>
          <li>How findings map to the 22-control catalog</li>
          <li>What a warning looks like next to a pass, and why inconclusive is separate</li>
          <li>What report metadata and consent proof look like in practice</li>
        </ul>
        <p class="small mt-1">What it cannot show you is your own domain. For that, request a private assessment &mdash; scope and authorisation are agreed first.</p>
        <div class="row mt-2">{btn('/request-assessment/', 'Request an assessment', 'primary', 'arrow')}</div>
      </div>
    </div>
  </div>
</section>

{cta_band("Seen enough? Request an assessment of your own domain.", "Reviewed manually, authorised in writing, and reported with the same evidence standard.", ("/request-assessment/", "Request an assessment"), ("/contact/", "Ask a question"))}
"""
    return layout(
        "/demo/",
        "Recorded Security Assessment Demo — SMB Scanner Lite",
        "Explore a genuine SMB Scanner Lite assessment of example.com recorded on 28 October 2026: score 86/100, grade B, eight findings with evidence, and five approved domains. Clearly labelled as recorded, not a live scan.",
        body,
        active="",
        crumbs=crumbs,
        schema={
            "@type": "SoftwareApplication",
            "name": C.SITE_NAME + " recorded assessment demo",
            "applicationCategory": "SecurityApplication",
            "operatingSystem": "Any modern browser",
            "description": "A recorded SMB Scanner Lite assessment published as static data, restricted to five approved test domains.",
        },
    )


# ---------------------------------------------------------------------------
# Documentation
# ---------------------------------------------------------------------------

def docs() -> str:
    crumbs = [("Home", "/"), ("Documentation", None)]
    flags = [
        ("--list-domains", "Print the five permitted testing domains. Makes no network request."),
        ("--accept-privacy-policy", "Record that the privacy policy was read and accepted. Required before any run."),
        ("--consent-user NAME", "Operator identity written into the consent receipt."),
        ("--consent-log PATH", "Optional path for the consent ledger (default: ~/.smb_scanner_lite/consent_proofs.jsonl)."),
        ("--verify-consent-log", "Re-walk the SHA-256 hash chain and report whether it is intact."),
        ("--html PATH", "Write an HTML report including the consent receipt."),
        ("--json PATH", "Write a JSON report for machine processing."),
        ("--txt PATH", "Write a plain-text report."),
        ("--gui", "Launch the desktop interface for the sandbox."),
        ("--version", "Print the application and edition version."),
    ]
    flag_rows = "".join(f"<tr><th scope='row'><code>{e(f)}</code></th><td>{e(d)}</td></tr>" for f, d in flags)

    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Documentation</p>
    <h1>Install the sandbox. It will not scan the open internet.</h1>
    <p class="lede">The published copy is the sandbox edition. Before any lookup it checks the target against five approved domains and requires a signed consent receipt. This page documents installation, the command-line surface, the outputs and the boundaries.</p>
    <div class="hero-actions">{btn('/demo/', 'See the recorded output first', 'primary', 'eye')}{btn(C.REPO_URL, 'View source', 'ghost', 'external', external=True)}</div>
  </div>
</div>

<section class="section section--flush">
  <div class="wrap">
    <div class="grid g2" style="align-items:start">
      <div class="reveal">
        <h2 style="font-size:1.3rem">1 &middot; Clone and install</h2>
        <p class="small muted">Python 3.10 or newer. The package is installed in editable mode so the console entry point becomes available.</p>
        <div class="evidence"><span class="val">git clone {C.REPO_URL}.git
cd smb-scanner-lite
pip install -e .</span></div>

        <h2 class="mt-4" style="font-size:1.3rem">2 &middot; List the permitted targets</h2>
        <p class="small muted">Read-only. Prints the five approved domains and makes no network request.</p>
        <div class="evidence"><span class="val">smb-scanner --list-domains</span></div>

        <h2 class="mt-4" style="font-size:1.3rem">3 &middot; Run an assessment</h2>
        <p class="small muted">Consent is mandatory. Without the policy flag and a name, the tool refuses.</p>
        <div class="evidence"><span class="val">smb-scanner example.com \\
  --accept-privacy-policy \\
  --consent-user "Your Name" \\
  --html report.html</span></div>

        <h2 class="mt-4" style="font-size:1.3rem">4 &middot; Verify the consent ledger</h2>
        <p class="small muted">Each receipt is chained to the previous one. Verification tells you whether the ledger on this machine is intact.</p>
        <div class="evidence"><span class="val">smb-scanner --verify-consent-log</span></div>
      </div>

      <div class="card reveal">
        <div class="card-icon">{icon('lock', 20)}</div>
        <h3>The allowlist is the product boundary</h3>
        <p>Any other name &mdash; including a look-alike subdomain, a raw IP address, an alternate port or a trailing dot &mdash; is rejected before a network request is made. The restriction lives in the runtime, so it cannot be disabled by editing a setting, passing a flag or modifying the interface.</p>
        <div class="chips mt-1">{''.join(f'<span class="chip">{e(d)}</span>' for d in C.ALLOWED_DOMAINS)}</div>
        <p class="small mt-2">Each name is a reserved documentation domain or a public testing resource published for this purpose:</p>
        <ul class="card-list">
          <li><span class="mono">example.com / .org / .net</span> &mdash; IANA reserved test domains</li>
          <li><span class="mono">scanme.nmap.org</span> &mdash; Nmap Project authorised test host</li>
          <li><span class="mono">badssl.com</span> &mdash; public TLS and certificate teaching site</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Command reference", "Every flag the sandbox accepts.", "The public CLI is deliberately small. Anything that would widen the target list is absent rather than hidden.")}
    <div class="table-wrap reveal">
      <table>
        <caption>Run <code>smb-scanner --help</code> for the authoritative list in your installed version.</caption>
        <thead><tr><th scope="col">Flag</th><th scope="col">Purpose</th></tr></thead>
        <tbody>{flag_rows}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g3">
      <div class="card reveal">
        <div class="card-icon">{icon('file', 20)}</div>
        <h3>What you get back</h3>
        <ul class="card-list">
          <li>Score, grade and completed-control count</li>
          <li>One evidence line per conclusive finding</li>
          <li>Inconclusive results listed separately</li>
          <li>Embedded consent receipt, hash-chained</li>
          <li>HTML, JSON or plain text output</li>
        </ul>
      </div>
      <div class="card reveal">
        <div class="card-icon card-icon--cyan">{icon('fingerprint', 20)}</div>
        <h3>Where the ledger lives</h3>
        <p>Consent receipts are written to the machine that ran the assessment, by default under your home directory. The path is configurable and the file is excluded from Git.</p>
        <div class="evidence mt-1"><span class="val">~/.smb_scanner_lite/consent_proofs.jsonl</span></div>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('terminal', 20)}</div>
        <h3>Desktop interface</h3>
        <p>The same sandbox runtime is available as a GUI for demonstration and teaching. It enforces the identical allowlist and consent requirements.</p>
        <div class="evidence mt-1"><span class="val">smb-scanner --gui</span></div>
      </div>
    </div>

    <div class="notice notice--warn mt-4">
      {icon('alert', 18, 'notice-icon')}
      <div class="notice-body"><strong>If a command fails</strong><p>A blocked target exits with code 2 and a message naming the five permitted domains. A missing policy acceptance or operator name exits with a consent error. Neither case produces a network request &mdash; that is the intended behaviour, not a bug to work around.</p></div>
    </div>
  </div>
</section>

{cta_band("Need a domain outside the sandbox?", "The public edition will not scan it. A private assessment can, after scope and written authorisation are agreed.", ("/request-assessment/", "Request an assessment"), ("/contact/", "Ask a technical question"))}
"""
    return layout(
        "/docs/",
        "Documentation — Install and Run the SMB Scanner Lite Sandbox",
        "Installation, command reference, output formats and consent-ledger handling for the restricted SMB Scanner Lite public sandbox edition. Five approved test domains, no arbitrary scanning.",
        body,
        crumbs=crumbs,
        schema={
            "@type": "TechArticle",
            "headline": "SMB Scanner Lite documentation",
            "about": "Installing and running the restricted sandbox edition",
            "author": {"@type": "Organization", "name": C.SITE_NAME},
            "dateModified": "2026-10-30",
        },
    )
