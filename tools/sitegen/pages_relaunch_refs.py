"""Rewritten technical reference library — scope-first and online-service accurate.

Eight stable knowledge-base URLs; all visible guide text is newly authored.
The separate journal discusses decisions; this reference explains mechanisms.
"""
from __future__ import annotations
from . import config as C, data as D, schema as structured
from .ui import btn, e, layout, section_head
from . import pages_relaunch as P

GUIDES = {
"external-security-posture-assessment": (
"External assessment: the useful questions",
"What a public-domain assessment measures, how its findings are evidenced and why external visibility cannot establish complete security.",
"""
<h2>A defined outside view</h2>
<p>An external security assessment collects observations available from outside a particular
system. For a domain, these may include public records and services that deliberately respond
to unauthenticated internet clients. The word <em>external</em> defines the point of view,
not the size or quality of the security program.</p>
<h2>State precisely what was examined</h2>
<p>Before reading conclusions, identify the exact hostname, observation time, scanner
profile, tools and exclusions. A DNS/email profile can examine sender policy and selected
domain records. It cannot determine whether an employee's password was stolen or a
business-critical backup can be restored.</p>
<h2>Make each claim reproducible</h2>
<p>For a conclusive finding, retain the observed value and the rule used to classify it.
A transient DNS failure is inconclusive unless supported by further observations.
A public interface responding to a request does not alone establish exploitability.</p>
<h2>Keep the output proportional</h2>
<p>Scores are summaries within the tested profile. They should not be repurposed as
company-wide certifications. The important deliverable is a list of findings an owner
can understand, investigate and verify after making changes.</p>
"""),
"smb-cybersecurity-basics": (
"Practical small business security",
"A security baseline built around account ownership, recovery, updates, vendor relationships and public-domain policy rather than dashboard scores.",
"""
<h2>Identity first</h2>
<p>A business can have excellent public DNS and still lose an administrator account.
Protect registrar, email, hosting and financial accounts with strong authentication,
document who controls them and test recovery procedures. The people with access to these
accounts can change far more than the public records reveal.</p>
<h2>Make inventory ordinary</h2>
<p>Keep a current list of domains, services, important vendors and devices. Record
who is responsible for each one. Forgotten services create ambiguous ownership,
and ambiguous ownership is why routine updates and cancellations are missed.</p>
<h2>Recovery is a measured control</h2>
<p>Backups are valuable when someone can restore them under pressure. Practice a
limited recovery, protect backup credentials and document the steps. A scan from
the public internet cannot validate any of this.</p>
<h2>Use external observations as one workstream</h2>
<p>Published DNS and email policy can be checked repeatedly and cheaply.
Treat them as part of your security routine, not its entirety. An actionable baseline
connects outside findings to responsible people and recorded fixes.</p>
"""),
"spf-dkim-dmarc": (
"Email authentication: protocol reference",
"How SPF, DKIM and DMARC operate, what alignment means and what a DNS-only assessment can establish about published mail policy.",
"""
<h2>SPF</h2>
<p>SPF is evaluated using the domain in the SMTP envelope and the sending IP.
The domain owner publishes a policy in DNS indicating which sending infrastructure
is authorized. SPF processing has limits, including a maximum number of DNS-querying
mechanisms or modifiers in a single evaluation; repeated or contradictory records
can cause failures. SPF alone does not necessarily authenticate the visible From domain.</p>
<h2>DKIM</h2>
<p>A DKIM signer adds cryptographic information to a message. The signature references
a domain and selector, which direct receivers to a public key in DNS. A public key
is only evidence that a selector record exists. A message must be examined to determine
whether it carries a valid signature. There is no reliable enumeration of every possible selector.</p>
<h2>DMARC</h2>
<p>DMARC requires a passing SPF or DKIM result aligned with the visible From domain.
The policy may request monitoring, quarantine or rejection. Receiver-side
interpretation and delivery behavior can vary; enforcement should follow a deliberate
inventory and monitoring period, not a single copy-and-paste DNS edit.</p>
<h2>What the scanner can say</h2>
<p>It can read and evaluate published SPF/DMARC policy and test a limited set of
DKIM selectors. It cannot see every message flow or promise that a mail provider
delivers only authenticated mail.</p>
"""),
"dnssec-explained": (
"DNSSEC: integrity, not confidentiality",
"What DNSSEC signatures and delegation chains establish, how validation can fail and why DNSSEC does not encrypt DNS or protect registrar accounts.",
"""
<h2>The question DNSSEC answers</h2>
<p>DNSSEC enables validating resolvers to verify cryptographic signatures over
DNS data and a trust chain established through delegations. The aim is to distinguish
authentic signed answers from tampering; it is not designed to hide which records exist.</p>
<h2>The moving parts</h2>
<p>Signed zones publish DNSKEY and RRSIG material. Parent delegations can carry DS
records that connect the chain of trust. A mismatch between parent delegation
and child signing material may lead a validating resolver to reject otherwise
correct answers.</p>
<h2>What it does not solve</h2>
<p>DNSSEC does not encrypt DNS transport, secure the registrar password, prevent
a legitimate administrator from publishing a malicious record or guarantee the
website behind a name is trustworthy.</p>
<h2>How to review it</h2>
<p>Record whether a chain is present and validates from the chosen vantage point.
Distinguish unsigned, verified, invalid and inconclusive states. Treat validation
failure as an operational issue requiring investigation, not an automatic attack finding.</p>
"""),
"public-facing-infrastructure": (
"Mapping public infrastructure carefully",
"Build an accurate inventory of domains and publicly visible services, with a clear distinction between passive observation and active authorized testing.",
"""
<h2>Start with authoritative ownership records</h2>
<p>List registered domains, known subdomains, hosting providers and deliberate
delegations from the organization's internal inventory. This establishes what
should exist before comparing it with the public view.</p>
<h2>Record public observations cautiously</h2>
<p>External records may point to third-party infrastructure, content delivery
networks or abandoned services. A record alone does not prove that a resource
is vulnerable or even currently controlled by the business. Verify each
relationship with the service owner.</p>
<h2>Keep authorization explicit</h2>
<p>DNS lookups reveal public information, but probing services and applications
can create traffic, trigger alarms and affect availability. Obtain scope-specific
permission before active testing, especially where a domain resolves to shared
infrastructure.</p>
<h2>Maintain the inventory</h2>
<p>After a migration, inspect the old hostname and delegation records. Mark
services retired only after confirming traffic and dependencies are gone.
A periodic inventory prevents a one-time assessment from becoming obsolete.</p>
"""),
"security-misconfigurations": (
"Misconfiguration evidence: what it proves",
"Interpret common public security misconfigurations without equating missing headers, unusual ports or stale DNS records with confirmed compromise.",
"""
<h2>Observation is the first step</h2>
<p>A configuration assessment can reveal a published record that contradicts
a policy, a TLS certificate that does not cover the requested hostname,
or an HTTP response that lacks a relevant security header. Each case needs
the exact response and a defined rule; labels like 'unsafe' without evidence
are too broad to guide remediation.</p>
<h2>Severity depends on context</h2>
<p>A missing HSTS header on a production login page warrants different attention
from a test endpoint with no authentication. A public management port deserves
review, but reachability alone is not proof of an exploitable service.</p>
<h2>Do not infer an incident</h2>
<p>Misconfiguration is a state, not evidence that an adversary exploited it.
Confirm the owner, exposure, business consequence and any compensating controls
before describing the impact.</p>
<h2>Current online coverage</h2>
<p>The first SMB Scanner Lite hosted profile reads DNS and email policy.
TLS, HTTP header and port-testing examples here explain the broader domain
of configuration review; the current online worker does not run those tests.</p>
"""),
"understanding-posture-scores": (
"Reading a score without losing the details",
"A posture score is a summary within tested scope, not a security certificate. Learn how coverage, uncertainty and evidence should shape its interpretation.",
"""
<h2>The denominator is the story</h2>
<p>Two identical scores may represent different sets of measured controls.
Before comparing results, examine the profile, conclusive-control count,
weights, timing and unresolved checks. A narrow DNS/email score must not be
compared directly to a full perimeter assessment.</p>
<h2>Uncertainty does not disappear into a grade</h2>
<p>When a check could not run or a DNS response timed out, the result should
be recorded as inconclusive or not tested, not silently treated as a pass.
The report should make coverage visible enough for the reader to see what
was—and was not—examined.</p>
<h2>Use the number to prioritize work</h2>
<p>Read each finding's observation, the proposed change and whether the
conclusion follows from that evidence. Assign an owner, record the exact
configuration change and verify the result after propagation or deployment.</p>
<h2>Reject the false assurance trap</h2>
<p>A strong score is not evidence that accounts are protected, backups work,
application logic is safe or staff are trained. It is useful precisely
because it describes a smaller, repeatable set of questions.</p>
"""),
"assessment-methodology": (
"Assessment method: authorization to evidence",
"A reproducible workflow for scope, domain verification, observation, classification, report retention and interpretation of public DNS/email security findings.",
"""
<h2>Define a legitimate target</h2>
<p>Record the exact domain, the requested assessment profile and explicit
authority to test. A temporary DNS TXT challenge helps verify control of
the submitted name before a worker can claim its job. It does not replace
contractual authorization or verify the identity of the requester.</p>
<h2>Collect with bounded methods</h2>
<p>Read only the public records defined by the scan profile. The online
worker uses DNS/email checks, and must not silently follow into TCP port
scanning or browser vulnerability testing. Report where selector-based
discovery or DNS resolver behavior limits confidence.</p>
<h2>Classify observed outcomes</h2>
<p>Use pass, warning, fail, inconclusive or not tested according to the
method's rule. A failed network request is not evidence that a control
is absent. Do not manufacture confidence when data is incomplete.</p>
<h2>Keep a private evidence record</h2>
<p>Store the scan's target, profile, timestamp and findings. Report previews
should expose only agreed high-level details. Full evidence remains
protected until the authorized owner has the required access; payment
unlocks are not currently in operation.</p>
<h2>Re-evaluate after a change</h2>
<p>Repeat the same observations from a comparable vantage. Note DNS
propagation, different resolvers and policy changes rather than comparing
two scores without context.</p>
"""),
}

def _meta(slug: str) -> tuple[str,str,str]:
    title,desc,body=GUIDES[slug]
    return title,desc,body

def index() -> str:
    cards="".join(f"""<a class="resource-card" href="/resources/{e(r['slug'])}/">
    <span class="component-tag">{e(D.RESOURCE_CATEGORIES[r['cat']])} / REFERENCE</span>
    <h3>{e(_meta(r['slug'])[0])}</h3><p>{e(_meta(r['slug'])[1])}</p>
    <span class="resource-meta">Revised 4 November 2026</span></a>""" for r in D.RESOURCES)
    body=P.head("Reference library","The mechanics, without the marketing.",
      "Independent explanations of the records, protocols and limits behind security assessment. Start with the mechanism before reading any grade.",
      btn("/blogs/","Read practical field notes","ghost","book"))
    body+=f"""<section class="section"><div class="wrap">
    {section_head("Reference","Eight topics, one consistent standard.",
    "Each page distinguishes the observable technical fact from the security conclusion that might follow.")}
    <div class="resource-grid">{cards}</div></div></section>"""
    return layout("/resources/","Security Reference Library | SMB Scanner Lite",
      "Technical reference guides covering external assessments, DNSSEC, email authentication, scoring and responsible security observations.",
      body,crumbs=[("Home","/"),("Reference library",None)],page_type="CollectionPage")

def article(slug: str) -> str:
    title,desc,content=_meta(slug)
    r=D.RESOURCE_BY_SLUG[slug]
    label=D.RESOURCE_CATEGORIES[r["cat"]]
    body=P.head("Reference / "+e(label),e(title),e(desc),btn("/scan/","Online scan status","ghost","arrow"))
    body+=f"""<section class="section"><div class="wrap">
    <div class="article-layout">
    <div class="prose">{content}
    <div class="relaunch-callout mt-3"><p><strong>Service scope:</strong>
    The prepared online scanner observes public DNS/email policy only.
    This reference may discuss controls that are not in that live profile.</p></div>
    </div>
    <aside class="article-aside">
      <div class="relaunch-feature"><small>TECHNICAL REFERENCE</small>
      <h3>For your own domain?</h3><p>Review the actual scope and
      ownership-verification process before you request a scan.</p>
      {btn("/capabilities/","Current scan coverage","ghost","arrow")}</div>
      <div class="relaunch-feature"><small>READ NEXT</small><h3>Field notes</h3>
      <p>Find practical decisions and troubleshooting examples in the journal.</p>
      <a href="/blogs/">Browse field notes</a></div>
    </aside></div></div></section>"""
    return layout(f"/resources/{slug}/",title+" | SMB Scanner Lite",desc,body,
      og_type="article",crumbs=[("Home","/"),("Reference library","/resources/"),(title,None)],
      schema=structured.article(f"/resources/{slug}/",title,desc,"2026-11-04",section=label),
      page_extra={"mainEntity":{"@id":structured.page_url(f"/resources/{slug}/")+"#article"}})
