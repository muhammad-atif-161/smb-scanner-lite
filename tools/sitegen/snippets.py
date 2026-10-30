"""Reusable page fragments built from the genuine recorded assessment data."""

from __future__ import annotations

from . import config as C
from . import data as D
from .ui import e, icon

STATUS_LABEL = {"pass": "Pass", "warning": "Warning", "fail": "Fail", "inconclusive": "Inconclusive"}
STATUS_DOT = {"pass": "pass", "warning": "warn", "fail": "fail", "inconclusive": "neutral"}


def recorded_banner(extra: str = "") -> str:
    extra_html = f"<span>{extra}</span>" if extra else ""
    return (
        '<div class="recorded-banner reveal"><span class="dot"></span>'
        f'<span><b>Recorded</b> &mdash; stored output from a real run on 28 October 2026. Not a live scan.</span>'
        f"{extra_html}</div>"
    )


def hero_window(record: dict | None = None) -> str:
    record = record or D.RECORDED[D.RECORDED_DEFAULT]
    categories = "".join(
        f'<div class="bar"><div class="bar-head"><span>{e(name)}</span><b>{value}</b></div>'
        f'<div class="bar-track"><span class="bar-fill{" bar-fill--warn" if value < 75 else ""}" style="width:{value}%"></span></div></div>'
        for name, value in record["categories"].items()
    )
    mini = "".join(
        f'<div class="mini-finding"><span class="dot dot-{STATUS_DOT[f["status"]]}"></span>'
        f'<div><span class="mf-title">{e(f["title"])}</span><p>{e(f["evidence"][:96])}{"…" if len(f["evidence"]) > 96 else ""}</p></div></div>'
        for f in record["findings"][:3]
    )
    return f"""
<div class="hero-visual hero-rise is-late">
  <div class="window">
    <div class="window-bar">
      <span class="window-dots"><i></i><i></i><i></i></span>
      <span>{e(record["report_id"])}</span>
      <span class="window-label">Recorded</span>
    </div>
    <div class="window-body">
      <dl class="report-meta">
        <div><dt>Target</dt><dd>{e(record["target"])}</dd></div>
        <div><dt>Assessed</dt><dd>{e(record["timestamp_display"])}</dd></div>
        <div><dt>Edition</dt><dd>v{e(record["version"])} &middot; Sandbox</dd></div>
        <div><dt>Controls</dt><dd>{record["counts"]["completed"]} completed &middot; {record["counts"]["inconclusive"]} inconclusive</dd></div>
      </dl>
      <div class="hero-score">
        <span class="hero-score-num">{record["score"]}<small> / 100</small></span>
        <span class="grade-badge"><b>{e(record["grade"])}</b><span>Grade</span></span>
        <span class="pill pill-info"><span class="dot dot-info"></span>{e(record["grade_label"])}</span>
      </div>
      <div class="bars">{categories}</div>
      <div class="mini-findings">{mini}</div>
    </div>
  </div>
  <p class="window-caption">Recorded assessment of {e(record["target"])} &middot; {e(record["timestamp_display"])} &middot; consent {e(record["consent_id"] or "n/a")}</p>
</div>"""


def status_badge(status: str) -> str:
    return f'<span class="status-badge status-{status}">{STATUS_LABEL.get(status, status)}</span>'


def finding_html(finding: dict, show_control: bool = True) -> str:
    control = D.CONTROL_BY_NUM.get(finding["control"])
    control_tag = ""
    if show_control and control:
        control_tag = f'<span class="component-tag mono">C{control["num"]:02d} &middot; {e(control["short"])}</span>'
    remediation = ""
    if finding.get("remediation"):
        remediation = f'<div class="remediation"><b>Recommended</b>{e(finding["remediation"])}</div>'
    return f"""
<article class="finding">
  <div class="finding-head">
    <span class="dot dot-{STATUS_DOT[finding["status"]]}"></span>
    <div class="finding-body">
      <div class="finding-title">
        <h4>{e(finding["title"])}</h4>
        {status_badge(finding["status"])}
        {control_tag}
      </div>
      <p>{e(finding["text"])}</p>
      <div class="evidence"><span class="val">{e(finding["evidence"])}</span><button class="copy" type="button" data-copy="{e(finding["evidence"])}">Copy</button></div>
      {remediation}
    </div>
  </div>
</article>"""


def findings_html(record: dict, limit: int | None = None) -> str:
    findings = record["findings"][:limit] if limit else record["findings"]
    return '<div class="findings">' + "".join(finding_html(f) for f in findings) + "</div>"


def category_bars(record: dict) -> str:
    return '<div class="bars">' + "".join(
        f'<div class="bar"><div class="bar-head"><span>{e(name)}</span><b>{value}</b></div>'
        f'<div class="bar-track"><span class="bar-fill{" bar-fill--warn" if value < 75 else ""}" style="width:{value}%"></span></div></div>'
        for name, value in record["categories"].items()
    ) + "</div>"


def score_panel(record: dict | None = None, heading: bool = True) -> str:
    record = record or D.RECORDED[D.RECORDED_DEFAULT]
    h = '<h3 class="mt-0">A recorded result, not a projection</h3>' if heading else ""
    return f"""
<div class="panel reveal" data-score-card data-score="{record["score"]}">
  <div class="score-panel">
    <div class="gauge" data-gauge style="--v:{record["score"]}">
      <div class="gauge-inner">
        <span class="gauge-value" data-score-value>{record["score"]}</span>
        <span class="gauge-label">Posture score</span>
        <span class="gauge-grade">Grade {e(record["grade"])} &middot; {e(record["grade_label"])}</span>
      </div>
    </div>
    <div style="flex:1 1 260px;min-width:0">
      {h}
      <p class="muted small">{e(record["summary"])}</p>
      {category_bars(record)}
    </div>
  </div>
  <p class="score-note">Recorded {e(record["timestamp_display"])} &middot; {e(record["report_id"])} &middot; {record["counts"]["completed"]} controls completed, {record["counts"]["inconclusive"]} inconclusive.</p>
</div>"""


def grade_scale(current: str = "B") -> str:
    rows = "".join(
        f'<div class="grade-row{" is-current" if letter == current else ""}">'
        f"<b>{letter}</b><span class=\"mono\">{band}</span><span class=\"mono\">{label}</span>"
        f'<span class="grade-desc muted">{desc}</span></div>'
        for letter, band, label, desc in D.GRADE_BANDS
    )
    return f'<div class="grade-scale reveal">{rows}</div>'


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------

ENQUIRY_TYPES = [
    "Product question",
    "Assessment request",
    "Technical enquiry",
    "Project acquisition",
    "Other enquiry",
]


def _field(name, label, *, kind="text", required=True, placeholder="", hint="", full=False, options=None, rows=None, autocomplete="", input_type=None) -> str:
    req = '<span class="req" aria-hidden="true">*</span>' if required else ""
    required_attr = f' data-required data-label="{e(label)}"' if required else ""
    full_cls = " field--full" if full else ""
    if kind == "select":
        opts = "".join(f'<option value="{e(o)}">{e(o)}</option>' for o in (options or []))
        control = f'<select class="select" id="{name}" name="{name}"{required_attr}>{opts}</select>'
    elif kind == "textarea":
        control = (
            f'<textarea class="textarea" id="{name}" name="{name}" rows="{rows or 5}" '
            f'placeholder="{e(placeholder)}"{required_attr}></textarea>'
        )
    else:
        control = (
            f'<input class="input" id="{name}" name="{name}" type="{input_type or "text"}" '
            f'placeholder="{e(placeholder)}" autocomplete="{e(autocomplete)}"{required_attr} />'
        )
    hint_html = f'<span class="field-hint">{hint}</span>' if hint else ""
    return (
        f'<div class="field{full_cls}"><label for="{name}">{label}{req}</label>{control}{hint_html}</div>'
    )


def form_core(*, kind: str, include_company=False, include_domain=False, include_assessment=False,
              include_authorisation=False, types=None, submit_label="Send enquiry", note=None) -> str:
    fields = [
        _field("name", "Your name", placeholder="First and last name", autocomplete="name"),
        _field("email", "Email address", kind="email", input_type="email", placeholder="name@company.com", autocomplete="email"),
    ]
    if include_company:
        fields.append(_field("company", "Company", placeholder="Business name", required=False, autocomplete="organization"))
    if include_domain:
        fields.append(_field("domain", "Business domain", placeholder="yourbusiness.com", required=include_assessment,
                             hint="The public domain you want assessed. No www. or path needed."))
    fields.append(_field("enquiryType", "Enquiry type", kind="select", options=types or ENQUIRY_TYPES, required=True))
    fields.append(_field("message", "Message", kind="textarea", required=False, full=True,
                         placeholder="What would you like to know, or what are you trying to assess?"))

    auth_block = ""
    if include_authorisation:
        auth_block = f"""
<div class="field field--full">
  <label for="{kind}-authorised">Are you authorised to request an assessment of this domain?</label>
  <select class="select" id="{kind}-authorised" name="authorised">
    <option value="no" selected>No &mdash; this is a question, not an assessment request</option>
    <option value="yes">Yes &mdash; I own the domain or am authorised to request an assessment</option>
  </select>
  <span class="field-hint">Answering &ldquo;no&rdquo; is fine. An assessment is only arranged after ownership or written authorisation is confirmed.</span>
</div>"""
    if include_assessment:
        auth_block = f"""
<div class="field field--full">
  <label class="check">
    <input type="checkbox" name="authorised" data-required data-label="Authorisation confirmation" />
    <span>I confirm that I own this domain, or that I am authorised by its owner to request an assessment of it. I understand that no assessment will run until authorisation has been verified.</span>
  </label>
</div>"""

    note_html = note or ('Reviewed manually. Your details are used only to reply to this enquiry &mdash; never sold, never added to a list. Read the <a href="/privacy/">privacy policy</a>.')
    return f"""
<form class="form" data-enquiry-form data-form-kind="{e(kind)}" novalidate>
  <div class="form-grid">
    {''.join(fields)}
    {auth_block}
  </div>
  <div class="hp" aria-hidden="true">
    <label for="{kind}-gotcha">Leave this field empty</label>
    <input id="{kind}-gotcha" type="text" name="_gotcha" tabindex="-1" autocomplete="off" />
  </div>
  <div class="form-status" data-form-status role="status" aria-live="polite" hidden></div>
  <div class="form-foot">
    <button class="btn btn-primary" type="submit">{icon('mail', 18, 'btn-icon')}<span>{e(submit_label)}</span></button>
    <p class="form-note">{note_html}</p>
  </div>
</form>"""


def contact_card() -> str:
    return f"""
<aside class="form-aside">
  <div class="card">
    <div class="card-icon">{icon('mail', 20)}</div>
    <h3>Direct email</h3>
    <p>Prefer your own mail client? Write to the address below and include the same details.</p>
    <p class="stack-tight">{''.join(f'<a class="tlink" href="mailto:{e(address)}">{e(address)}</a>' for address in C.CONTACT_EMAILS)}</p>
  </div>
  <div class="card">
    <div class="card-icon card-icon--cyan">{icon('clock', 20)}</div>
    <h3>What to expect</h3>
    <p>Enquiries are read by the maintainer. Assessment requests are reviewed manually &mdash; nothing is scanned automatically, and no assessment runs before written authorisation is agreed.</p>
  </div>
  <div class="card">
    <div class="card-icon">{icon('shield', 20)}</div>
    <h3>Do not send sensitive data</h3>
    <p>Never include passwords, private keys, customer records or anything you would not put in an ordinary email. A domain name and a description of the concern are enough to start.</p>
  </div>
</aside>"""
