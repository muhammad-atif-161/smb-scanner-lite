"""Knowledge base: index and eight original technical articles."""

from __future__ import annotations

from . import config as C
from . import data as D
from . import schema as structured
from . import pages_blog  # noqa: F401  (used by _practical)
from .ui import btn, cta_band, e, icon, layout, section_head

# ---------------------------------------------------------------------------
# Article content: (anchor, heading, [paragraph html, ...])
# ---------------------------------------------------------------------------

ARTICLES = {
    "external-security-posture-assessment": [
        ("definition", "A working definition", [
            "External security posture assessment is the practice of describing an organisation's security configuration and exposure using only what can be observed from the public internet, without credentials and without privileged access.",
            "The word <em>posture</em> is doing real work here. It describes a configuration state, not an attack outcome. A posture assessment can tell you that a domain publishes no DMARC policy. It cannot tell you that someone is currently spoofing that domain, or that anyone ever has.",
            "That distinction matters commercially as well as technically. Posture findings are usually cheap to fix and easy to verify, which makes them a sensible first pass before anyone commissions deeper work.",
        ]),
        ("observable", "What is actually observable", [
            "Almost everything an external assessment reads is published deliberately. DNS answers exist so that the internet can find you. SPF and DMARC records exist so that receivers can decide whether to trust a message. TLS certificates exist so that a browser can verify an identity. HTTP headers exist so that a browser knows how to behave.",
            "The assessment reads those artefacts and compares them with published expectations: RFC 7208 for SPF, RFC 7489 for DMARC, RFC 4034 for DNSSEC, the relevant TLS guidance for protocol and certificate configuration, and vendor documentation for header behaviour.",
            "Five observation types cover the catalog used by this project: DNS queries, mail authentication policy records, TLS handshakes, HTTP response headers, and protocol-level reachability of specific ports. Read the <a href=\"/capabilities/\">22-control catalog</a> for the specific checks.",
        ]),
        ("not-entitled", "What it is not entitled to conclude", [
            "An external assessment cannot establish that a system is secure, that a weakness is exploitable, or that a compromise has occurred. Each of those requires either access the assessment does not have, or actions it deliberately does not take.",
            "This is not a limitation to be buried in a footnote. It changes how a report should be read. A failed DMARC check is a fact about a DNS record. Whether that fact was exploited is a separate question with a separate evidence requirement.",
            "Similarly, a passing control is not a control that cannot be bypassed. It is a control that was configured as expected at the moment it was observed.",
        ]),
        ("evidence", "Why evidence changes the conversation", [
            "A finding that quotes its observation can be checked by someone who was not there. That is the difference between a report that starts an argument about trust and a report that starts a work item.",
            "In practice this looks unremarkable: a DMARC record, an SPF policy, a certificate subject, a header line. Unremarkable is the point. Anyone with a terminal can reproduce the query and compare the answer. If they differ, the finding is stale or vantage-specific &mdash; and saying so openly is more useful than defending a number.",
            "SMB Scanner Lite applies this as a rule it calls <strong>no claim without evidence</strong>, including a separate status for a check that returned no conclusive answer. See the <a href=\"/methodology/\">methodology</a> for how that is implemented.",
        ]),
        ("who", "Who should care, and when", [
            "Small and medium businesses are the clearest beneficiaries. They are visible enough to be impersonated by email, frequently run remote-access services that were intended to be internal, and rarely have anyone whose job is to look at the public footprint monthly.",
            "Consultants and managed service providers use external posture assessment as a defensible starting point: it produces a short list of verifiable observations before a deeper engagement is scoped or sold.",
            "The practical trigger points are familiar: a new customer questionnaire, a cyber-insurance renewal, an acquisition due-diligence request, a suspicious invoice email, or simply a change of hosting provider.",
        ]),
        ("limits", "The honest boundary", [
            "Everything an external assessment produces is partial. It depends on a vantage point, a resolver and a moment in time. It cannot see behind authentication. It says nothing about people, process or physical security.",
            "The correct posture towards that boundary is to state it in the same document that delivers the findings. Read the full list on the <a href=\"/limitations/\">assessment limitations</a> page, or inspect a real report in the <a href=\"/sample-report/\">recorded assessment</a>.",
        ]),
    ],
    "smb-cybersecurity-basics": [
        ("why", "Why small businesses are exposed in a specific way", [
            "A small business rarely loses data because an attacker developed a novel exploit for it. The usual path is more mundane: a spoofed invoice that arrives from the company's own domain, a remote desktop service reachable from the internet with a reused password, or a file share exposed by a router rule nobody remembers adding.",
            "These are configuration outcomes, not sophisticated attacks. They persist because nobody's job includes looking at the outside view, and because the systems involved were set up to work, not to be safe from the public internet.",
        ]),
        ("five", "Five exposures that appear again and again", [
            "<strong>1. Email that anyone can forge.</strong> Without SPF, DKIM and a DMARC policy that actually enforces, a supplier or customer has no reliable way to tell a real invoice from a fake one. This is the highest-value, lowest-cost gap in most small businesses. It is also the one most likely to be described as \"we have antivirus\" in conversation.",
            "<strong>2. Remote access facing the world.</strong> Remote Desktop on port 3389 and SMB on port 445 were designed for networks where everyone was already trusted. Exposing them to the internet exposes every credential-stuffing list in existence to the same login prompt.",
            "<strong>3. A DNS record pointing at something retired.</strong> A subdomain that points at a decommissioned hosting account is a takeover waiting to happen. It costs nothing to check and takes ten minutes to clean up.",
            "<strong>4. No DNSSEC, so answers can be forged.</strong> DNSSEC does not encrypt anything. It makes a forged answer detectable, which matters most for the records that direct mail and logins.",
            "<strong>5. Browser headers that were never added because nobody asked.</strong> HSTS, Content-Security-Policy and framing protection are cheap and commonly absent. On a simple brochure site the consequences are modest; on a site with a login form they are not.",
        ]),
        ("cheap", "Start with what is cheap to change", [
            "A pragmatic order is: publish a DMARC policy in monitoring mode, confirm SPF and DKIM pass for your real senders, then move DMARC to quarantine and eventually reject. In parallel, close remote-access ports that should never have been open, and clean up DNS records that point at retired infrastructure.",
            "None of that requires new products. It requires an inventory and someone with the authority to change records.",
            "Header hardening and DNSSEC come next. They are slightly more involved and considerably less urgent than email authentication, but they are still configuration work rather than projects.",
        ]),
        ("what-to-ask", "What to ask an IT provider", [
            "Ask for the current DMARC policy and who owns it. Ask which ports on the public IP addresses accept connections from the internet and which of those are deliberate. Ask what happens to DNS records when a hosting account is closed. Ask for a dated report rather than a verbal assurance.",
            "A provider who can answer those four questions is measurably ahead. A provider who cannot is not necessarily negligent &mdash; but the gap is now visible, which is the useful part.",
        ]),
        ("measure", "Measure it, then re-measure it", [
            "An external posture assessment gives you a baseline you can compare against next quarter. The comparison matters more than the absolute score: a finding that disappears after a change is proof the change worked, and a finding that reappears is a process that regressed.",
            "The <a href=\"/demo/\">recorded assessment</a> shows what the output looks like. If you want the equivalent for your own domain, <a href=\"/request-assessment/\">request an assessment</a> &mdash; scope and authorisation are agreed before anything runs.",
        ]),
    ],
    "spf-dkim-dmarc": [
        ("problem", "The problem in one sentence", [
            "By default, the email protocol lets anyone claim to be anyone. SPF, DKIM and DMARC are three separate mechanisms that together give a receiving mail server enough information to decide whether a message claiming to be from your domain is plausible.",
            "They are not interchangeable, and implementing one without the others is a common way to feel protected without being protected.",
        ]),
        ("spf", "SPF: which hosts may send", [
            "SPF is a TXT record at the domain apex that lists the hosts authorised to send mail for that domain. A receiving server checks the connecting IP against that list.",
            "The important detail is the qualifier at the end. <code>v=spf1 include:_spf.example.net -all</code> means \"reject anything not listed\". A trailing <code>~all</code> means \"mark it suspicious but accept it\", which is a soft policy that many receivers treat generously. No <code>all</code> mechanism at all means the record expresses no opinion.",
            "SPF also has operational limits. It breaks when mail is forwarded, because the forwarding server is not in your list. It breaks at scale: RFC 7208 caps DNS-querying mechanisms at ten, and exceeding that produces a permerror, which is worse than a simple strict record. Publishing two SPF records is also a permerror, not a merge.",
            "This is why the assessment checks SPF validity as a separate control from SPF strength. A weak-but-valid record and an invalid record fail differently in production.",
        ]),
        ("dkim", "DKIM: a signature on the message", [
            "DKIM signs selected headers and the body with a private key held by the sending system. The public key is published at a selector under <code>_domainkey</code> in DNS, and the receiver verifies the signature.",
            "Because the signature travels with the message, DKIM survives forwarding in many cases where SPF does not. Key length matters: 1024-bit RSA keys are still seen, 2048-bit is the sensible baseline, and shorter keys should be rotated out.",
            "A practical caveat: DKIM is only useful if you know your selectors. Selector names are not discoverable by design, so an external assessment can only check the selectors it is told about or can reasonably guess. That limitation is stated rather than hidden.",
        ]),
        ("dmarc", "DMARC: what to do when authentication fails", [
            "DMARC is the policy layer. It is published at <code>_dmarc.yourdomain.com</code> and tells receivers what to do when a message fails SPF and DKIM alignment: nothing (<code>p=none</code>), quarantine it (<code>p=quarantine</code>), or reject it (<code>p=reject</code>).",
            "It also introduces alignment, which is the subtle part. SPF can pass for a domain that is not the one in the From header. DMARC asks whether an authenticated identifier aligns with the visible From domain. <code>adkim=s</code> and <code>aspf=s</code> require strict alignment; relaxed mode allows organisational-domain matching.",
            "<code>sp=</code> sets the policy for subdomains, and it is routinely forgotten. A domain with <code>p=reject</code> and no <code>sp=</code> inherits the reject policy for subdomains, which can break legitimate mail from a subdomain you forgot about. Publishing <code>sp=reject</code> deliberately is the safer, more explicit choice for domains that do not send from subdomains.",
            "Reporting addresses (<code>rua=</code>) are how you find out what you are breaking. Turn reporting on before you turn enforcement on.",
        ]),
        ("order", "The order to fix it in", [
            "First, inventory every system that sends mail as your domain &mdash; including the website, the CRM, the invoicing tool and the printer that nobody admits to. Second, configure SPF and DKIM for each. Third, publish DMARC at <code>p=none</code> with reporting enabled and watch the reports for a few weeks. Fourth, move to quarantine, then to reject.",
            "A useful sign you are ready for enforcement: your reports show aligned SPF or DKIM passes for all legitimate traffic, and the failures are things you can name.",
        ]),
        ("check", "How to check it yourself", [
            "Query the records directly: <code>dig TXT yourdomain.com</code>, <code>dig TXT _dmarc.yourdomain.com</code>, and <code>dig TXT selector._domainkey.yourdomain.com</code>. Read the qualifiers and the policy values rather than trusting a green tick from a third-party checker.",
            "SMB Scanner Lite evaluates SPF strength, SPF validity, DMARC enforcement, DKIM presence and MX posture as five separate controls. The <a href=\"/sample-report/\">recorded assessment</a> shows the evidence strings for the ones it covered, and the <a href=\"/capabilities/\">catalog</a> documents the rest.",
        ]),
    ],
    "dnssec-explained": [
        ("what", "What DNSSEC actually does", [
            "DNSSEC adds cryptographic signatures to DNS records. A validating resolver can then tell whether an answer it received is the answer the zone owner published, or something injected along the way.",
            "It does not encrypt DNS queries. Anyone on the path can still see that you looked up a name. What they cannot do, with DNSSEC in place and validated, is quietly substitute a different answer.",
        ]),
        ("chain", "The chain of trust", [
            "Each zone signs its records with a private key and publishes the signatures (RRSIG). The parent zone publishes a delegation signer record (DS) containing a digest of the child's key. A resolver starts at the root trust anchor and walks down, verifying each link.",
            "If any link is missing, the zone is treated as unsigned. If a link is present but the signature does not validate, the answer is bogus and the resolver should return SERVFAIL rather than the forged data. That failure mode is the point: a broken DNSSEC deployment makes names unresolvable for validating resolvers, which is worse than no DNSSEC at all.",
            "The most common operational mistake is a key rollover where the DS record at the parent was never updated. The second most common is an expired signature because a signer stopped running.",
        ]),
        ("not", "What it does not protect", [
            "DNSSEC does not protect the web server, the TLS certificate, or the application behind the name. It does not prevent a domain owner from publishing malicious records, and it does not stop a registrar account takeover &mdash; the attacker simply publishes new, validly signed records.",
            "It also does not improve privacy. For that, a separate mechanism (DNS over TLS or HTTPS) is required, and it protects the transport rather than the content.",
        ]),
        ("why", "Why a small business might care", [
            "The records that matter most are the ones that direct where mail goes and where authentication happens. A forged MX or TXT answer can redirect or defeat mail authentication for a domain that otherwise looks well configured.",
            "DNSSEC is not free: it requires a registrar that supports DS records, a DNS host that signs zones, and a process for monitoring expiry. That cost is why it is often skipped &mdash; and why it is worth noting when it is present.",
        ]),
        ("assess", "How it is assessed externally", [
            "An external check looks at whether the zone publishes signed records, whether the parent publishes a DS record, and whether validation succeeds through a validating resolver. It cannot see private keys, and it does not attempt to.",
            "SMB Scanner Lite reports this as control C02, with the evidence line naming the validation path that succeeded. In the <a href=\"/sample-report/\">recorded assessment</a> the evidence reads <span class=\"mono\">Zone signed with validated RRSIG and parent DS delegation.</span>",
        ]),
        ("next", "If you are implementing it", [
            "Enable signing at your DNS host first, confirm the zone answers correctly, then add the DS record at the registrar. Monitor signature expiry. Decide in advance what you will do if validation breaks, because the answer cannot be \"disable DNSSEC quickly\" without accepting that resolvers will fail closed.",
            "Read the related controls in the <a href=\"/capabilities/\">capability catalog</a>, particularly CAA and zone transfer exposure, which address adjacent parts of the DNS trust story.",
        ]),
    ],
    "public-facing-infrastructure": [
        ("inventory", "You cannot assess what you have not inventoried", [
            "Most organisations know their primary domain and their website. Fewer can list every subdomain, every public IP address and every service listening on them. That inventory is the foundation of any external assessment, and it is usually the first output of one.",
            "Start with what is authoritative: the DNS zone file from your DNS provider, the public IP ranges from your hosting provider, and the certificate transparency logs for your domain, which reveal hostnames that were issued certificates even if you have forgotten them.",
        ]),
        ("sources", "Passive sources worth knowing", [
            "Certificate transparency logs are public by design: every publicly trusted certificate is recorded, so searching them for your domain surfaces historical hostnames. Search engine indexes reveal pages that were meant to be unlisted. Job postings reveal technology stacks. None of this requires touching the organisation's infrastructure.",
            "Passive sources are also useful for the reverse case: understanding what an attacker could learn about you without any active probing at all.",
        ]),
        ("authorisation", "Where authorisation stops being optional", [
            "Passive research is generally benign. Active probing is not: connecting to a host, requesting a URL or completing a protocol handshake is traffic to a system someone else may own.",
            "If the infrastructure is yours, you are the authorisation. If it belongs to a client, get it in writing, scoped to specific hosts and a specific window. If it belongs to your hosting provider, their acceptable-use policy applies on top of your own permission.",
            "SMB Scanner Lite's public edition avoids the question entirely by restricting itself to five reserved test domains. There is no legitimate reason for a public demo to connect to arbitrary hosts.",
        ]),
        ("shadow", "Shadow infrastructure is the hard part", [
            "A marketing landing page stood up by an agency, a staging environment with a default password, an old intranet still resolving &mdash; these are the systems that never appear in the inventory because nobody considered them part of it.",
            "External assessment is particularly good at surfacing them, because it observes what is reachable rather than what is documented. That is also why findings occasionally produce the response \"we did not know that existed\", which is the most valuable result an assessment can deliver.",
        ]),
        ("scope", "Scoping an assessment defensibly", [
            "Write down the domains and IP ranges in scope, the exclusions, the time window, the vantage points and the contact who can authorise stopping. Include what will happen if something in scope turns out to belong to a third party.",
            "For a small business that inventory may be five lines long. The discipline still matters: it is the difference between an assessment and unauthorised scanning.",
        ]),
        ("continue", "Where to go next", [
            "The <a href=\"/methodology/\">methodology</a> describes how SMB Scanner Lite turns observations into findings. The <a href=\"/capabilities/\">capability catalog</a> lists which controls address exposed services, and the <a href=\"/responsible-use/\">responsible use</a> page covers authorisation in more detail.",
        ]),
    ],
    "security-misconfigurations": [
        ("what", "The pattern behind most findings", [
            "Security misconfiguration is not a bug in someone's code. It is a system doing exactly what it was told, in a context nobody re-examined. Six of these patterns account for a large share of what an external assessment finds on small-business infrastructure.",
        ]),
        ("one", "1. Exposed administrative interfaces", [
            "A database console, a web hosting panel or an object-storage browser reachable from the public internet is one credential away from full compromise. The usual cause is a temporary exception that became permanent.",
            "The fix is network-level: restrict the interface to known addresses or put it behind a VPN. Authentication is not a substitute for an exposure boundary.",
        ]),
        ("two", "2. Remote access exposed by accident", [
            "RDP on 3389 and SMB on 445 exposed to the internet are the canonical examples. Attackers do not need a vulnerability when a login prompt is available to everyone, and credential stuffing lists are cheap.",
            "If remote access is required, put it behind a VPN or an identity-aware proxy, enforce multi-factor authentication, and verify from outside that the port no longer answers.",
        ]),
        ("three", "3. Dangling DNS records", [
            "A CNAME pointing at a hosting account that was closed is an invitation: whoever claims that name inherits your subdomain. The same applies to cloud storage buckets and marketing platforms referenced by DNS or JavaScript.",
            "The fix is a periodic review of records against active services. It is cheap and it is almost never done.",
        ]),
        ("four", "4. Missing transport hardening", [
            "TLS without HSTS still allows a downgrade on the first request of a later visit. HTTP without a redirect serves content unencrypted. A valid certificate is necessary but not sufficient.",
            "The combination worth aiming for: redirect all HTTP to HTTPS, send HSTS with a long max-age and includeSubDomains, and confirm the certificate covers every name you serve.",
        ]),
        ("five", "5. No content security policy", [
            "CSP is the browser-side mitigation for cross-site scripting. It does not fix an injection bug, but it constrains what an injected script can do. Its absence is a common finding even on sites that otherwise look carefully built.",
            "Start in report-only mode, collect violations, then enforce. A wildcard or <code>unsafe-inline</code> policy that defeats the purpose is worse than none, because it creates false confidence.",
        ]),
        ("six", "6. Verbose banners and directory lists", [
            "Server and framework version headers save an attacker reconnaissance. Directory listing turns a missing index file into a file inventory. Stack traces in error responses reveal paths and library versions.",
            "None of these is a compromise on its own. Together they shorten the path to one.",
        ]),
        ("conclusion", "Why external assessment finds these", [
            "Every one of the six is observable without authentication, which is exactly why an external assessment is a useful first pass. It cannot confirm exploitability, and it cannot see inside the network &mdash; but it can produce a verifiable shortlist.",
            "The <a href=\"/capabilities/\">capability catalog</a> maps each pattern to the controls that detect it. The <a href=\"/limitations/\">limitations page</a> explains what the finding does not mean.",
        ]),
    ],
    "understanding-posture-scores": [
        ("appeal", "Why a single number is appealing", [
            "A score compresses a complicated picture into something a non-specialist can hold in their head. That is genuinely useful: it lets an owner ask \"are we better or worse than last quarter\" without learning what a DMARC alignment mode is.",
            "It is also dangerous in the same breath, because compression loses the thing that matters most &mdash; which specific controls produced the result.",
        ]),
        ("arithmetic", "What a defensible score is made of", [
            "A posture score should be reproducible arithmetic over defined inputs. In SMB Scanner Lite, each control reaches one of four statuses, each control carries a severity weight, and the score is a weighted mean over the controls that completed. Inconclusive controls are excluded from both the numerator and the denominator.",
            "That last rule is the one most worth checking in any scoring model. If a scanner treats a timeout as a failure, a quiet network produces a bad score. If it treats silence as a pass, a filtering firewall produces a good one. Either way the number stops describing configuration and starts describing reachability.",
        ]),
        ("grades", "What a grade band adds", [
            "Letter grades are a second compression on top of the first. They are useful for conversation and useless for diagnosis: nobody fixes a B, they fix a missing header.",
            "The bands should be published and fixed, not adjusted per customer. Ours are A 90&ndash;100, B 80&ndash;89, C 65&ndash;79, D 50&ndash;64 and F below 50, and they are applied identically to every target.",
        ]),
        ("questions", "Questions to ask before quoting a score", [
            "What was measured, and what was excluded? How were inconclusive results handled? What weights were used, and who decided them? Is the score comparable between two different scopes? How old is it?",
            "If a vendor cannot answer those five questions, the number is decoration. If they can, the number is a useful index &mdash; still not a certificate, but an index with a methodology behind it.",
        ]),
        ("abuse", "The three ways scores get abused", [
            "<strong>Comparability.</strong> A sandbox score derived from eight controls is not comparable to a full 22-control assessment. Presenting them side by side without that context is misleading, which is why the sandbox report says so explicitly.",
            "<strong>Guarantees.</strong> \"Score 95, therefore secure\" is a non-sequitur. The score describes measured configuration only.",
            "<strong>Marketing.</strong> A high score on a marketing site is a claim about that site's configuration, not about the product or the business behind it.",
        ]),
        ("use", "Using one well", [
            "Treat the score as an index into the findings. Read the findings, act on the highest-severity ones, and re-assess after the change. The movement between two assessments of the same scope is more informative than either absolute value.",
            "The <a href=\"/methodology/\">methodology page</a> documents the weights and the arithmetic. The <a href=\"/sample-report/\">recorded report</a> shows a score next to the findings that produced it, which is the only responsible way to present one.",
        ]),
    ],
    "assessment-methodology": [
        ("scope", "Start with scope, not with tools", [
            "A methodology begins with what is in scope, who authorised it, and what the output is for. Tools are interchangeable; scope and authorisation are not.",
            "Write the scope down: domains, IP ranges, exclusions, vantage points, time window, and the person who can authorise stopping. An assessment without those is a scan.",
        ]),
        ("evidence-model", "Define how a finding is stated before you collect any", [
            "An evidence-first method defines its output vocabulary first. SMB Scanner Lite uses four statuses: pass, warning, fail and inconclusive. Each finding quotes the observation that produced it.",
            "The critical decision is the fourth status. Without it, every timeout becomes a judgement call, and judgement calls drift towards whichever conclusion is more convenient.",
        ]),
        ("vantage", "Record the vantage point", [
            "External observations depend on where they are made. A record can resolve differently for different resolvers; a firewall can answer one source and drop another.",
            "Recording the vantage point is what makes a finding reproducible. Without it, \"we observed X\" is an anecdote.",
        ]),
        ("scoring", "Score only what completed", [
            "If a score is produced, it should be arithmetic over completed controls with published weights, and inconclusive results should be excluded rather than counted as failures.",
            "Publish the weights and the grade bands. A scoring model that cannot be inspected cannot be trusted, and a model that changes per engagement cannot be compared over time.",
        ]),
        ("limitations", "Write the limitations in the report", [
            "Every method has a boundary: what it cannot see, what it cannot prove, how it can be wrong. Stating that boundary in the report is not weakness; it is what makes the rest of the report usable.",
            "A reader who understands the boundary can decide which findings to act on. A reader who does not will over-trust the rest.",
        ]),
        ("iterate", "Compare runs, not snapshots", [
            "A single assessment is a snapshot. Two assessments of the same scope, compared, are a measurement of change &mdash; and change is what an organisation can act on.",
            "Record the date, the version of the tool and the scope with every report, or you will find yourself comparing incomparable things six months later.",
        ]),
        ("apply", "How this project applies it", [
            "The full method is documented on the <a href=\"/methodology/\">methodology page</a>, with the control catalog on the <a href=\"/capabilities/\">capabilities page</a> and a genuine output in the <a href=\"/sample-report/\">recorded assessment</a>. The <a href=\"/validation/\">validation record</a> shows the reproducible tests behind the restrictions.",
        ]),
    ],
}


def _article_body(slug: str) -> tuple[str, str]:
    sections = ARTICLES[slug]
    prose = []
    toc = []
    for anchor, heading, paragraphs in sections:
        toc.append(f'<li><a href="#{anchor}">{e(heading)}</a></li>')
        prose.append(f'<h2 id="{anchor}">{e(heading)}</h2>')
        prose.extend(f"<p>{p}</p>" for p in paragraphs)
    return "".join(prose), "".join(toc)


def _related(slug: str) -> str:
    current = D.RESOURCE_BY_SLUG[slug]
    related = [r for r in D.RESOURCES if r["slug"] != slug][:3]
    cards = "".join(f"""
<a class="resource-card" href="/resources/{r['slug']}/">
  <span class="component-tag mono">{e(D.RESOURCE_CATEGORIES[r['cat']])}</span>
  <h3>{e(r['title'])}</h3>
  <span class="resource-meta"><span>{r['read']} min read</span></span>
</a>""" for r in related)
    return f"""
<section class="section section--alt">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Keep reading</p><h2>Related articles</h2></div>
    <div class="resource-grid">{cards}</div>
  </div>
</section>"""


def resources_index() -> str:
    crumbs = [("Home", "/"), ("Knowledge Base", None)]
    guides = [r for r in D.RESOURCES if r["guide"]]
    method = [r for r in D.RESOURCES if not r["guide"]]

    def cards(items):
        return "".join(f"""
<a class="resource-card reveal" href="/resources/{r['slug']}/">
  <span class="component-tag mono">{e(D.RESOURCE_CATEGORIES[r['cat']])}</span>
  <h3>{e(r['title'])}</h3>
  <p>{e(r['desc'])}</p>
  <span class="resource-meta"><span>{e(r['date'])}</span><span>{r['read']} min read</span></span>
</a>""" for r in items)

    body = f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Knowledge base</p>
    <h1>Technical writing for people who have to fix it.</h1>
    <p class="lede">Eight articles on the controls this product measures and the method behind it. Each one is written for a specific question, links to the authoritative standard, and avoids restating the same introduction in different words.</p>
    <div class="hero-actions">{btn('/capabilities/', 'See the control catalog', 'primary', 'arrow')}{btn('/methodology/', 'Read the methodology', 'ghost')}</div>
  </div>
</div>

<section class="section section--flush" id="guides">
  <div class="wrap">
    {section_head("Guides", "How the controls work in practice.", "Fundamentals, email authentication, DNS, infrastructure and web configuration &mdash; each explained from first principles rather than from a vendor checklist.")}
    <div class="resource-grid">{cards(guides)}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Method", "How measurement and reporting should work.", "What a defensible assessment looks like, and how to read the number it produces.")}
    <div class="resource-grid">{cards(method)}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Editorial standard</p>
        <h2>What this section will not do.</h2>
        <p class="section-lede">A knowledge base is only useful if it says something. These are the rules the articles follow.</p>
        <ul class="trust-list mt-2">
          <li><strong>No keyword filler</strong>Every article answers a question someone would actually ask, and links to the RFC or vendor documentation rather than paraphrasing it loosely.</li>
          <li><strong>No invented authority</strong>No fabricated citations, no made-up statistics, no claims of testing that did not happen.</li>
          <li><strong>No disguised product pitch</strong>Articles explain the topic first. Where the product is relevant, the link is explicit.</li>
          <li><strong>Corrections welcome</strong>If something here is wrong or out of date, the contact form reaches the maintainer directly.</li>
        </ul>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('book', 20)}</div>
        <h3>Where to start</h3>
        <p>If you are new to this: begin with the external posture assessment definition, then read the SMB exposure survey.</p>
        <p class="small">If you are fixing email: go straight to SPF, DKIM and DMARC &mdash; it is the highest-value gap in most small businesses.</p>
        <p class="small">If you are evaluating the product: read the posture score article, then compare it with the <a href="/methodology/">methodology</a>.</p>
        <div class="row mt-1">{btn('/resources/external-security-posture-assessment/', 'Start here', 'ghost', 'arrow')}</div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("Blog", "Prefer a sequence to follow?", "The knowledge base explains how a control works. The blog covers what to do about it: a rollout order for DMARC, a fifteen-check website routine, and a walkthrough of an assessment report.")}
    {pages_blog.post_cards(pages_blog.B.latest(3))}
    <div class="row mt-3">{btn('/blogs/', 'All blog guides', 'ghost', 'arrow')}</div>
  </div>
</section>

{cta_band("Want to see the method applied to a real domain?", "The recorded assessment shows every finding with its evidence, score and timestamp.", ("/demo/", "Open the recorded assessment"), ("/sample-report/", "Read the sample report"))}
"""
    return layout(
        "/resources/",
        "Knowledge Base — External Security, DNS, Email and Assessment Method",
        "Original technical guides on external security posture assessment, SMB exposure, SPF/DKIM/DMARC, DNSSEC, public-facing infrastructure, misconfigurations and how to read a posture score.",
        body,
        crumbs=crumbs,
        page_type="CollectionPage",
        page_extra={
            "hasPart": [
                {
                    "@type": "Article",
                    "headline": r["title"],
                    "url": C.SITE_URL + f"/resources/{r['slug']}/",
                    "datePublished": r["date"],
                }
                for r in D.RESOURCES
            ]
        },
    )


# Practical counterparts: the blog answers "what do I do, in what order", which
# is a different intention from "how does this work". Linking the two keeps the
# cluster honest instead of making the articles compete for the same query.
PRACTICAL = {
    "spf-dkim-dmarc": (
        "spf-dkim-dmarc-explained",
        "set-up-dmarc-without-breaking-email",
        "business-email-marked-as-spam",
    ),
    "dnssec-explained": ("dns-security-for-small-businesses",),
    "security-misconfigurations": ("external-website-security-checks",),
    "smb-cybersecurity-basics": ("small-business-cybersecurity-guide",),
    "external-security-posture-assessment": (
        "what-is-a-security-posture-assessment",
        "assessment-vs-penetration-test",
    ),
    "understanding-posture-scores": ("how-to-read-your-security-report",),
    "assessment-methodology": (
        "check-your-external-security-posture-free",
        "how-to-read-your-security-report",
    ),
    "public-facing-infrastructure": ("external-website-security-checks",),
}


def _practical(slug: str) -> str:
    picks = PRACTICAL.get(slug, ())
    if not picks:
        return ""
    links = "".join(
        f'<li><a href="{pages_blog.B.post_url(pages_blog.B.BY_SLUG[item])}">'
        f'{e(pages_blog.B.BY_SLUG[item]["title"])}</a></li>'
        for item in picks
    )
    return f"""
        <div class="card mt-4">
          <h2 class="card-title">The practical version</h2>
          <p class="small">This article explains the mechanism. The blog covers the sequence: what to check, in what order, and what to do with the answer.</p>
          <ul class="small mt-1">{links}</ul>
        </div>"""


def article(slug: str) -> str:
    meta = D.RESOURCE_BY_SLUG[slug]
    prose, toc = _article_body(slug)
    crumbs = [("Home", "/"), ("Knowledge Base", "/resources/"), (meta["title"], None)]
    body = f"""
<article>
  <header class="article-head">
    <div class="wrap">
      <p class="eyebrow">{e(D.RESOURCE_CATEGORIES[meta['cat']])}</p>
      <h1>{e(meta['title'])}</h1>
      <p class="lede">{e(meta['desc'])}</p>
      <div class="article-meta">
        <span>Published {e(meta['date'])}</span>
        <span>{meta['read']} min read</span>
        <span>SMB Scanner Lite knowledge base</span>
      </div>
    </div>
  </header>
  <div class="wrap">
    <div class="article-layout">
      <div class="prose">
        {prose}
        <div class="callout mt-4">
          {icon('shield', 20)}
          <div><p><strong>See how this is measured.</strong> SMB Scanner Lite evaluates these controls from outside and attaches the observation behind every conclusive finding. <a href="/capabilities/">Browse the 22-control catalog</a> or inspect the <a href="/sample-report/">recorded assessment</a>.</p></div>
        </div>
        {_practical(slug)}
      </div>
      <aside class="article-aside">
        <nav class="toc" aria-label="On this page">
          <h2>On this page</h2>
          <ol>{toc}</ol>
        </nav>
        <div class="card">
          <h3 style="font-size:0.95rem">Questions about your own domain?</h3>
          <p class="small">A private assessment covers the full catalog, after scope and written authorisation are agreed.</p>
          <a class="tlink mt-1" href="/request-assessment/">Request an assessment {icon('arrow', 16)}</a>
        </div>
      </aside>
    </div>
  </div>
</article>
{_related(slug)}
"""
    return layout(
        f"/resources/{slug}/",
        f"{meta['title']} — SMB Scanner Lite Knowledge Base",
        meta["desc"],
        body,
        og_type="article",
        crumbs=crumbs,
        schema=structured.article(
            f"/resources/{slug}/",
            meta["title"],
            meta["desc"],
            meta["date"],
            section=D.RESOURCE_CATEGORIES[meta["cat"]],
        ),
        page_extra={
            "mainEntity": {"@id": structured.page_url(f"/resources/{slug}/") + "#article"}
        },
    )
