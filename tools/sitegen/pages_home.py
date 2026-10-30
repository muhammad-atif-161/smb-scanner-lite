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
<article class=\"card reveal\">
  <div class=\"card-icon\">{icon(cat['icon'], 20)}</div>
  <span class=\"card-num mono\">{len(controls):02d}</span>
  <h3>{e(cat['name'])}</h3>
  <p>{e(cat['intro'])}</p>
  <ul class=\"card-list\">{sample}</ul>
  <span class=\"component-tag mono\" style=\"margin-top:auto\">{recorded} in the recorded run</span>
</article>""")
    return f'<div class=\"grid g3 reveal-group\">{"".join(cards)}</div>'


def _overview() -> str:
    items = [
        ("eye", "What a stranger can see", "An outsider cannot read your policies, your firewall rules or your backups. They can see your DNS, your published mail policy, your TLS handshake, your response headers and whether certain services answer. That view is what this assessment measures."),
        ("list", "Findings with evidence attached", "Every conclusive finding quotes the record, header or handshake that produced it. There is no score without an observation behind it, and no observation is presented as an exploit."),
        ("scale", "A shared language for priority", "The 0&ndash;100 score and A&ndash;F grade exist so an owner, an IT administrator and a consultant can agree on what to fix first &mdash; not so anyone can claim a business is secure."),
    ]
    cards = "".join(f"""
<article class=\"card reveal\">
  <div class=\"card-icon\">{icon(i, 20)}</div>
  <h3>{title}</h3>
  <p>{text}</p>
</article>""" for i, title, text in items)
    return f'<div class=\"grid g3\">{cards}</div>'


def _owner_risks() -> str:
    """Plain-English mapping of check categories to owner-level worries."""
    rows = [
        ("mail", "Fraudulent email that looks like it came from you", "Email authentication checks (SPF, DKIM, DMARC) show whether a stranger can send invoices, password-reset messages or customer emails in your name."),
        ("server", "Remote access or file shares left open to the internet", "Network exposure checks look for high-risk services such as SMB file sharing and Remote Desktop that answer from the public internet."),
        ("shield", "Failing a customer or vendor security questionnaire", "The assessment produces a clear score, grade and evidence you can attach when a customer asks how you protect your public-facing systems."),
        ("alert", "An embarrassing public security surprise", "DNS, TLS and header checks surface the common configuration gaps that turn into public incidents or lost deals before anyone inside notices."),
    ]
    cards = "".join(f"""
<article class=\"card reveal\">
  <div class=\"card-icon\">{icon(i, 20)}</div>
  <h3>{title}</h3>
  <p>{text}</p>
</article>""" for i, title, text in rows)
    return f"""
<div class=\"callout reveal\" style=\"margin-bottom:1.5rem\">
  {icon('user', 20)}
  <div><p><strong>For non-technical owners.</strong> You do not need to know DNS, TLS or security headers to use this. The checks answer four practical questions most small-business owners actually care about.</p></div>
</div>
<div class=\"grid g2\">{cards}</div>"""


def _steps() -> str:
    steps = [
        ("Select an authorised target", "An assessment needs a domain you own or are permitted to assess. The public edition is limited to five reserved testing domains; a private assessment starts with written authorisation."),
        ("Run the read-only checks", "DNS, mail authentication records, TLS handshakes, HTTP headers and protocol-level service probes. No login, no payload, no exploitation."),
        ("Collect the evidence", "Each check stores what it observed and the status it reached &mdash; pass, warning, fail or inconclusive. A timeout is never converted into a failure."),
        ("Review score and report", "A weighted 0&ndash;100 score, an A&ndash;F grade, findings ordered by severity, and a report you can read as HTML, JSON, CSV or TXT."),
    ]
    return '<div class=\"steps reveal\">' + "".join(f"""
<div class=\"step\">
  <span class=\"step-marker\">{i:02d}</span>
  <h3>{title}</h3>
  <p>{text}</p>
</div>""" for i, (title, text) in enumerate(steps, start=1)) + "</div>"
