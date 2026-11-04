"""New journal articles for the online-first website (4 November 2026).

The original article slugs are retained as stable URLs. The published copy,
headlines, descriptions, summaries and conclusions are replaced below.
Unlike the old catalog-led journal, these articles do not imply TLS/port/web
checks are part of the current online DNS/email profile.
"""
from __future__ import annotations

def entry(title, desc, lede, takeaways, body):
    return {"title":title, "seo_title":title, "desc":desc, "lede":lede,
            "takeaways":takeaways, "body":body, "updated":"2026-11-04"}

ARTICLES = {
"spf-dkim-dmarc-explained": entry(
"SPF, DKIM and DMARC: three different jobs",
"Understand SPF, DKIM and DMARC, the role of domain alignment and what public DNS records can and cannot prove about email authentication.",
"The familiar three-letter acronyms are not three versions of one security control. Each answers a different question about a message.",
["SPF authorizes envelope senders, not every visible From address.",
 "DKIM signs a message using a selector-specific public key.",
 "DMARC connects authentication to the domain the reader sees."],
"""
<p>Someone receives an invoice that appears to be from your company. Their inbox displays your
domain, but display alone says little about who sent it. Email authentication addresses that
ambiguity with three separate mechanisms. Understanding how they connect is more useful than
memorizing a checklist of record names.</p>
<h2>SPF answers who may send</h2>
<p>Sender Policy Framework publishes which mail infrastructure is authorized to send using
a domain in the SMTP envelope. A receiving server evaluates the sending IP against the domain
used by that envelope identity. The critical distinction is that the envelope sender may differ
from the address the human reader sees in the From field.</p>
<p>An SPF record can also be malformed, duplicated, or too complicated to evaluate reliably.
Check the complete policy, not just whether a DNS query returns a string beginning with
<code>v=spf1</code>.</p>
<h2>DKIM answers whether a signature verifies</h2>
<p>DomainKeys Identified Mail adds a cryptographic signature to selected message headers and body
content. A receiver retrieves a public key at a selector-specific DNS name and verifies the
signature. A correctly published key is only part of the story: whether a particular outgoing
message is signed can only be learned by inspecting that message.</p>
<p>There is no universal list of DKIM selectors. A scanner that checks several common selectors
and finds none should report limited discovery, not assert that the organization never signs
mail.</p>
<h2>DMARC connects the pieces to the visible identity</h2>
<p>DMARC evaluates whether SPF or DKIM passes with a domain aligned to the visible From address.
It then communicates the publishing domain's policy, including monitoring
(<code>p=none</code>) or requested enforcement (<code>p=quarantine</code> or
<code>p=reject</code>). Receivers retain discretion, and real delivery also depends on
reputation, content and local filtering.</p>
<h2>A sensible first review</h2>
<ol>
<li>List every service allowed to send on behalf of the domain.</li>
<li>Query the domain's SPF and <code>_dmarc</code> TXT records.</li>
<li>Send test messages through each legitimate platform and inspect authentication results.</li>
<li>Correct missing signing or alignment before asking receivers to reject failed messages.</li>
<li>Monitor DMARC reports when possible and adjust policy deliberately.</li>
</ol>
<p>SMB Scanner Lite's online DNS/email profile can inspect published policy and a limited
set of discoverable keys. It cannot guarantee a mailbox is protected or that every
outgoing message authenticates successfully.</p>
"""),
"set-up-dmarc-without-breaking-email": entry(
"A careful path from DMARC monitoring to enforcement",
"A practical DMARC rollout: inventory senders, check alignment, analyze reports, move gradually to stronger policy and verify legitimate mail.",
"Rejecting mail is easy to write in DNS. Knowing what you would reject takes considerably more care.",
["Inventory all legitimate senders before enforcement.",
 "Look for aligned SPF or DKIM on messages, not only published records.",
 "Move policy deliberately and monitor legitimate delivery."],
"""
<p>The temptation is to copy a strong-looking DMARC record into DNS and call email security
finished. That is risky when invoices, payroll messages or customer confirmations come from
services nobody has inventoried. Enforcement can expose a configuration problem by rejecting
the messages your business relies on.</p>
<h2>Start with the sending map</h2>
<p>Write down every system that sends using your company domain: primary mailbox provider,
website forms, CRM, help desk, marketing provider and third-party billing software. Record
who owns each integration. A forgotten vendor is often more significant than a missing DNS tag.</p>
<h2>Observe before enforcing</h2>
<p>Publish a syntactically valid DMARC policy in monitoring mode with a reporting destination
you control or a trusted processor. Analyze aggregate reports for legitimate sources and
unexpected senders. Reports may contain sensitive operational detail, so treat them as
business records rather than unrestricted analytics data.</p>
<p>Send actual messages from each known system to a test mailbox and inspect
<code>Authentication-Results</code>. Look for a passing, aligned authentication method.
A DMARC policy cannot fix an improperly configured outgoing service by itself.</p>
<h2>Fix sender configuration one provider at a time</h2>
<p>For each authorized sender, confirm DKIM signing and/or aligned SPF behavior. Avoid adding
SPF includes blindly: a single record may have lookup limits, and broad authorization
increases attack surface. Verify that delegated domains and subdomains follow the intended
policy.</p>
<h2>Advance in measured stages</h2>
<p>When legitimate mail consistently authenticates, evaluate moving toward quarantine and
then reject. The precise schedule depends on the organization. Keep a rollback procedure,
monitor delivery failures, and coordinate with the people who receive billing and support
complaints before tightening enforcement.</p>
<p>A DNS-only scan can show the published DMARC state. It cannot know which of your providers
will be disrupted. The operational rollout remains your responsibility.</p>
"""),
"business-email-marked-as-spam": entry(
"When legitimate business email lands in spam",
"Diagnose email deliverability by separating SPF, DKIM and DMARC alignment from domain reputation, message content and provider-specific filtering.",
"A message can authenticate perfectly and still be classified as unwanted. That is a different failure.",
["Read the received message's authentication headers before changing DNS.",
 "Authentication and deliverability are related but not identical.",
 "Avoid changing multiple records at once without testing."],
"""
<p>A customer says your quote landed in spam. The first response is often to edit SPF or add
another DKIM record, but that can make diagnosis harder. Authentication establishes who sent
a message and whether it was altered. Inbox placement also responds to reputation,
recipient behavior and local provider policy.</p>
<h2>Get a sample that actually failed</h2>
<p>Ask for the original message headers or reproduce the issue in a mailbox you control.
Look for the sending IP, authentication outcomes and the provider's rejection or filtering
reason. If the message never arrived, investigate bounce notices and SMTP response codes
before guessing at spam-folder behavior.</p>
<h2>Separate alignment from simple passes</h2>
<p>An SPF pass for a marketing vendor's envelope domain does not automatically establish DMARC
alignment with your visible From domain. A DKIM pass for an unrelated signing domain can be
similarly insufficient. Read the complete authentication results, including the domains
involved.</p>
<h2>Then examine sending quality</h2>
<p>Confirm that the sending domain has coherent forward and reverse DNS where appropriate,
that the message platform is properly configured, and that the content does not mimic
phishing techniques. Unusual bursts, stale lists and high complaint rates can affect
reputation even with excellent DNS policy.</p>
<h2>Change one variable, then test</h2>
<p>Document the problem, make a targeted change and test mail through the affected system.
Ask the recipient provider for feedback when possible. A public DNS assessment helps rule in
certain configuration issues, but it does not read an organization's mail traffic or
promise inbox placement.</p>
"""),
"dns-security-for-small-businesses": entry(
"Your domain's DNS deserves an owner",
"Review public DNS records with an inventory, registrar protections, delegated services and a change process, without treating DNS visibility as an exploit.",
"DNS changes are small; the business effects can be enormous. The right first control is often knowing who can edit them.",
["Inventory active records and the teams responsible.",
 "Secure registrar and DNS-provider accounts before tuning optional records.",
 "Use consistent external queries to review changes over time."],
"""
<p>DNS directs visitors to websites, mail to providers and some trust decisions to public
policy. It rarely receives the same attention as the applications behind it. That is odd:
a record changed by mistake can interrupt an entire company before anyone notices.</p>
<h2>Know who controls the zone</h2>
<p>Document the registrar, authoritative DNS provider, account owners, recovery contacts and
who may edit records. Enable strong authentication on those accounts. The most carefully
written DNSSEC policy is not enough if an attacker can simply take over the control panel.</p>
<h2>Build a purposeful record inventory</h2>
<p>List the public records that support your domain: address records, mail routing, TXT policy,
CAA and delegations. Add a business owner to each service. A hostname pointed at a retired
platform is not inherently compromised, but it should be investigated and removed if unused.</p>
<h2>Measure externally, cautiously</h2>
<p>Compare answers from known resolvers and check authoritative data where possible. Resolver
caches, geographic routing and provider defaults can explain legitimate differences.
A timeout says the observation failed, not necessarily that the target misconfigured DNS.</p>
<h2>Understand DNSSEC's narrow benefit</h2>
<p>DNSSEC can help validating resolvers detect tampered DNS data through signatures and a chain
of trust. It does not hide records, encrypt DNS traffic or prevent registrar compromise.
An incorrectly maintained delegation may instead make valid names unreachable.</p>
<h2>Give DNS a change log</h2>
<p>For each edit, capture who approved it, what record changed, what result you expected and
how you verified it externally. Repeat the same queries afterward. A reliable before/after
record is more useful than a dashboard that only says 'healthy'.</p>
<p>The online scanner offers a narrow view of published DNS and email policy. It cannot inspect
your private zones or the provider accounts behind them.</p>
"""),
"external-website-security-checks": entry(
"Website security checks worth doing by hand",
"A measured checklist for HTTPS, certificates, redirects, browser headers and site exposure, with clear limits and no suggestion these tests are in the first online scan.",
"Not every useful check needs an exploit. Some of the first questions are visible from an ordinary browser request.",
["A browser padlock establishes connection properties, not application trust.",
 "Header and certificate checks are useful but incomplete.",
 "The current online DNS/email beta does not run these website tests."],
"""
<p>Before commissioning a deep application review, a site owner can check a few basic properties
that any visitor's browser encounters. These observations can reveal operational oversights.
They are not a substitute for vulnerability testing, authenticated access review or code audit.</p>
<h2>Start with the actual hostname</h2>
<p>Open the precise address customers use. Confirm it resolves, the TLS certificate covers
the hostname, the chain is trusted by your client and the certificate is valid. Remember that
a valid certificate proves a particular connection, not that the website behind it is safe.</p>
<h2>Inspect redirects rather than assuming them</h2>
<p>Test the public HTTP entry point and confirm that requests reach the intended HTTPS host.
Look at each hop for unexpected hosts or mixed-content resources. A redirect policy is
a deployment decision; it should not happen to work only on the home page.</p>
<h2>Review headers in context</h2>
<p>Security headers such as HSTS, CSP, X-Content-Type-Options and framing restrictions can
reduce specific browser-side risks. Their absence is not equally serious on every site,
and a policy that exists but is misconfigured may be worse than a carefully scoped exception.
A report should quote the exact header and response where it was observed.</p>
<h2>Check what is publicly reachable</h2>
<p>Review public services against your own inventory. Do not probe third-party systems or attempt
access to endpoints you are not authorized to test. Service reachability is an observation,
not proof of a remotely exploitable vulnerability.</p>
<h2>Know where these checks stop</h2>
<p>They cannot determine whether an application suffers authorization flaws, injection,
broken session handling or vulnerable dependencies. Those require different methods and
permissions. The first release of SMB Scanner Lite's hosted service checks DNS and email
policy only; the website checks in this article are educational steps for your own site.</p>
"""),
"small-business-cybersecurity-guide": entry(
"A modest security baseline for a small company",
"An achievable small-business security baseline covering accounts, recovery, mail policy, updates and documented ownership before new tools are purchased.",
"Security improves faster when someone knows which decisions are theirs than when another dashboard is added.",
["Protect critical accounts with MFA and reliable recovery.",
 "Know which services and domains are actually yours.",
 "Verify backups and public email policy separately."],
"""
<p>A small company rarely has a full-time person for security. That does not mean it needs
to begin with an expensive monitoring platform. Begin with ordinary operational controls
that can be assigned to real people and verified without a new subscription.</p>
<h2>First, protect the accounts that control everything else</h2>
<p>List the administrator accounts for domain registration, DNS, email, cloud hosting, banking
and backups. Require strong multi-factor authentication wherever supported, remove unused
administrators and document secure recovery procedures. A compromised registrar account
can undermine a perfectly configured domain.</p>
<h2>Second, understand what is connected</h2>
<p>Build a small inventory of employee devices, internet-facing services, third-party vendors,
domains and important information. An old service with no owner tends to persist until
something fails. You cannot patch or retire infrastructure nobody remembers.</p>
<h2>Third, practice restoring the business</h2>
<p>A backup that has never been restored is a hypothesis. Test recovery of a representative
file and a critical service, then record how long the process took and who can perform it.
Protect backup credentials independently from the primary environment.</p>
<h2>Fourth, check the public domain</h2>
<p>Review mail authentication policy and DNS service ownership. These are unusually visible
from outside and lend themselves to repeatable observations. They do not establish your
company's wider security posture, but they can identify manageable configuration work.</p>
<h2>A monthly review that fits in a calendar</h2>
<p>Check administrator access, overdue updates, backup recovery evidence and changes to key
public DNS records. Assign actions, not just 'risk levels'. The discipline of reviewing
what changed is more durable than a one-time score.</p>
"""),
"what-is-a-security-posture-assessment": entry(
"What an external security assessment can tell you",
"Define an external security assessment by its exact target, observation scope, evidence and limits rather than by a reassuring score.",
"The value of a security assessment lies in the questions it answers—and in the questions it refuses to guess at.",
["Define the target and scan profile before interpreting results.",
 "Demand observable evidence for every conclusive claim.",
 "Do not equate a public-domain grade with company-wide security."],
"""
<p>The phrase 'security assessment' can describe anything from a questionnaire to a full
penetration test. Before buying or relying on one, identify the method. What was observed?
From where? Against which exact systems? With what permission?</p>
<h2>Start with scope, not a score</h2>
<p>An external domain review might examine DNS records, sender authentication, TLS responses
or service reachability. An internal assessment might inspect accounts, devices and
configuration. A penetration test might safely attempt to demonstrate exploitability
under a specifically authorized rules-of-engagement agreement. These are not interchangeable.</p>
<h2>Ask what the result is based on</h2>
<p>A report that says 'weak mail authentication' should quote the relevant published policy
and explain why it fails a stated criterion. A timeout should say inconclusive.
A missing observation is not proof of a missing defense.</p>
<h2>Look at the timestamp and vantage point</h2>
<p>Public infrastructure changes. A record can be different next week; a resolver in another
location may see something else today. Good reports identify when and how observations
were made so a finding can be reproduced or challenged.</p>
<h2>Understand the difference between measurement and assurance</h2>
<p>Even a perfect score within the assessed controls does not cover staff behavior,
software defects, business processes or unknown systems. Treat the report as a prioritized
work list and a baseline for checking whether the next change actually improved something.</p>
<p>SMB Scanner Lite's initial online profile is deliberately limited to DNS and email records.
It should be judged on that narrow promise, not on unrelated controls in a historic sandbox
demonstration.</p>
"""),
"assessment-vs-penetration-test": entry(
"External assessment or penetration test?",
"A clear comparison of configuration assessment and authorized penetration testing, including evidence types, risk, permission and the questions each answers.",
"A configuration finding can be important without proving that an attacker could exploit it.",
["External observation describes published configuration.",
 "Penetration testing demonstrates possible attack paths under agreed rules.",
 "Neither method replaces the other or warrants absolute safety."],
"""
<p>A business owner might receive two proposals: one promises a security assessment, the other
a penetration test. They may be priced differently because they are designed to answer
different questions—not because one vendor has a better-looking dashboard.</p>
<h2>External assessment: what can be observed?</h2>
<p>An external assessment reads properties visible to an unauthenticated observer, such as
public DNS policy or a public TLS response. Findings describe the observed state and its
likely consequence. They can often be repeated cheaply and compared after remediation.</p>
<h2>Penetration test: can a weakness be demonstrated?</h2>
<p>In a scoped penetration test, an authorized specialist may attempt to exploit vulnerabilities
in a controlled manner to establish practical impact. This requires a detailed agreement on
targets, exclusions, methods, timing, safety controls and how sensitive findings are handled.</p>
<h2>Don't confuse reachability with exposure to compromise</h2>
<p>Seeing a service answer a request does not prove it is vulnerable. Conversely, a clean
DNS configuration does not imply the application is safe. A responsible report distinguishes
observations, hypotheses and demonstrated attack outcomes.</p>
<h2>Choosing between them</h2>
<p>For a small business with unclear public inventory, start by establishing ownership and
collecting a measured baseline. When the threat model includes sensitive applications,
customer data or high-impact operations, seek a properly scoped professional security
assessment and penetration testing as appropriate. Keep findings and retest evidence separate.</p>
<p>The online SMB Scanner Lite beta performs low-impact DNS/email record checks only. It is not
marketed or operated as a penetration testing service.</p>
"""),
"check-your-external-security-posture-free": entry(
"A free first look at your domain's public records",
"Check your own domain's DNS, SPF and DMARC configuration using ordinary public record queries, with important interpretation limits.",
"Before you run any scanner, you can learn a useful amount from the records your domain already publishes.",
["Start with your domain's public DNS responses and current provider list.",
 "Interpret SPF/DMARC records as policy, not evidence of actual mail delivery.",
 "Never expand testing beyond systems you control."],
"""
<p>Domain security can feel abstract because the relevant configuration is usually hidden
inside a hosting dashboard. Yet the DNS records themselves are public. With a domain you
control and a few carefully chosen queries, you can begin an inventory without installing
a security product.</p>
<h2>Identify the responsible providers</h2>
<p>Make a note of the registrar, authoritative name servers, email provider and website host.
Check the answers against what the business believes it owns. Unexpected records may be
deliberate delegation or stale configuration; investigate before removing them.</p>
<h2>Read the published mail policy</h2>
<p>Use a standard DNS lookup tool to inspect TXT records at the domain apex and at
<code>_dmarc</code>. Look for duplicate SPF records, contradictory policy and whether
DMARC requests monitoring or stronger treatment. A policy that exists is not necessarily
implemented correctly for outgoing messages.</p>
<h2>Ask whether the evidence supports the conclusion</h2>
<p>DNS responses can be cached and may differ by resolver. If you cannot retrieve a record,
verify at the authoritative source before declaring it absent. DKIM selectors are not
universally discoverable, so do not claim a signing failure from a short selector list.</p>
<h2>Keep a simple baseline</h2>
<p>Save the values, provider names and time of inspection. After changing any record, repeat
the same queries. The value lies in noticing differences you intended—and differences
you did not.</p>
<p>SMB Scanner Lite's verified online flow is built to organize these observations into
a limited report. While public access is closed, these careful manual checks remain useful.</p>
"""),
"how-to-read-your-security-report": entry(
"How to read a security report without being misled",
"Interpret the score, conclusive evidence, inconclusive controls, scope and remediation of a DNS/email security report without overstating its assurance.",
"The first page gives you a score. The rest should give you the reasons, boundaries and a plan.",
["Read scope and timestamp before reacting to a grade.",
 "Treat inconclusive as unknown, not as a pass or vulnerability.",
 "Assign a remediation owner and verify the exact evidence afterward."],
"""
<p>A security report is easy to skim badly: see a grade, search for the red labels and forward
the PDF to IT. That misses the most useful information. The score is a summary of selected
observations, not an answer to whether the business is generally secure.</p>
<h2>Find the boundary first</h2>
<p>Identify the exact domain, timestamp and tested profile. For SMB Scanner Lite's initial
online service, that profile is DNS/email authentication. Do not assume TLS, application
testing or internet-exposed ports were evaluated.</p>
<h2>Match each finding to its observation</h2>
<p>Look for the DNS value, response and criterion that produced the status. If a report says
DMARC requests monitoring only, read the actual <code>p=none</code> policy and consider
whether that matches the business's rollout plan. If the tool did not receive a reliable
answer, it should not claim the record is missing.</p>
<h2>Handle inconclusive results separately</h2>
<p>Unknown outcomes need investigation. A timeout could reflect provider behavior,
network conditions or a temporary outage. It should not enter a remediation queue as a
definite vulnerability without more evidence.</p>
<h2>Turn observations into accountable work</h2>
<p>For each issue, record an owner, intended change and verification step. Test legitimate
email flows before tightening DMARC. After changes propagate, repeat the observation from
a comparable vantage and keep the original result for comparison.</p>
<h2>Don't buy certainty the method cannot offer</h2>
<p>Even an excellent score within a narrow scan profile says nothing about passwords,
internal systems, backups or the safety of an application. Use the report to direct
attention, not to replace a broader risk program.</p>
"""),
}

CLUSTER_COPY = {
 "email-security":("Email authentication","The policies behind trustworthy mail",
   "Understand how published SPF, DKIM and DMARC controls interact, and how to change them without disrupting legitimate messages."),
 "dns-security":("Domain infrastructure","The records that direct your business",
   "A practical look at DNS ownership, delegation, integrity and the questions public records can actually answer."),
 "website-security":("Website security","Beyond the browser padlock",
   "Educational notes on HTTP and TLS configuration. These checks are not included in the first online DNS/email scan profile."),
 "smb-basics":("Business security","Small controls, substantial consequences",
   "A calmer approach to company security: accounts, recovery, ownership and a repeatable process."),
 "assessment":("Assessment literacy","Know what the report really says",
   "Understand scope, evidence, scores and the difference between observation and a deeper security test."),
}

def rewrite_registry(posts: list[dict], clusters: dict) -> None:
    for post in posts:
        original_slug=post["slug"]
        if original_slug not in ARTICLES:
            raise ValueError(f"Journal relaunch missing new content for {original_slug}")
        post.update(ARTICLES[original_slug])
        post.pop("read", None)
        post.pop("word_count", None)
    for slug, meta in clusters.items():
        label,title,desc=CLUSTER_COPY[slug]
        meta.update(label=label,title=title,seo_title=title+" | SMB Scanner Lite",
                    desc=desc,lede=desc,
                    intro=f"<p>{desc}</p><p>These guides explain mechanisms and decisions, not a promise that every control is part of a currently available scan.</p>")
