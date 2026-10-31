"""Assessment cluster: method, comparison with penetration testing, free checks and
how to read the report."""

from __future__ import annotations

DATE = "2026-10-31"

POSTS = [
    {
        "slug": "what-is-a-security-posture-assessment",
        "cluster": "assessment",
        "title": "What is a security posture assessment?",
        "seo_title": "What is a security posture assessment?",
        "desc": (
            "A working definition, the five categories an external assessment can actually "
            "measure, and eight questions to ask before you buy one from anybody."
        ),
        "lede": (
            "The phrase gets used for everything from a questionnaire to a full red-team "
            "engagement. Here is the narrow, defensible version: a fixed catalog of externally "
            "observable controls, each with a status and an observation behind it."
        ),
        "date": DATE,
        "updated": DATE,
        "takeaways": [
            "A posture assessment measures configuration that is visible from outside, on a repeatable catalog, and reports a status per control.",
            "It is not a penetration test, a code review or a compliance audit &mdash; and it should say so in the report.",
            "The value comes from comparison over time, which requires the same scope, the same vantage and a published method.",
            "Ask any provider what is excluded. A method with no stated limits is marketing.",
        ],
        "body": """
<p>In a meeting, "security posture assessment" usually means "someone looked at our security and
gave us a number". That is not a method, it is a deliverable. The useful definition is narrower:
a repeatable evaluation of a fixed set of controls, performed from a defined vantage point
against a defined scope, with a recorded observation supporting each result.</p>
<p>Each part of that sentence is doing work. <em>Repeatable</em> means next quarter's result can
be compared with this quarter's. <em>Fixed set of controls</em> means the score cannot be moved
by measuring different things. <em>Defined vantage</em> means "the firewall blocks us" is an
observation, not a mystery. <em>Recorded observation</em> means you can check the finding without
trusting the person who wrote it.</p>

<h2>What an external assessment can measure</h2>
<p>The catalog behind SMB Scanner Lite has 22 controls in five categories. This is what
"external" means concretely: DNS records, mail policy records, a TLS handshake, HTTP response
headers, and whether specific high-risk services answer.</p>
<div class="table-wrap">
<table>
<caption>The 22-control catalog, grouped. Weights reflect the consequence of the exposure, not the effort of fixing it.</caption>
<thead><tr><th scope="col">Category</th><th scope="col">Controls</th><th scope="col">Examples</th></tr></thead>
<tbody>
<tr><td>DNS and domain integrity</td><td>5</td><td>DNSSEC chain, CAA authorisation, zone transfer, name record hygiene, address resolution</td></tr>
<tr><td>Email authentication</td><td>5</td><td>SPF strength and validity, DMARC enforcement, DKIM presence and key strength, MX posture</td></tr>
<tr><td>Transport security</td><td>4</td><td>Protocol versions, certificate validity and coverage, cipher suites, HTTPS redirect path</td></tr>
<tr><td>Browser security headers</td><td>4</td><td>HSTS, CSP, framing and MIME-sniffing protection, referrer and permissions policy</td></tr>
<tr><td>Network and service exposure</td><td>4</td><td>High-risk ports, SMB, remote desktop, database and admin interfaces</td></tr>
</tbody>
</table>
</div>
<p>Two of those categories are the ones worth acting on first in most small businesses, and
neither requires a budget: a domain that anyone can forge, and a remote desktop port open to the
internet, are the two findings that most often turn out to matter.</p>

<h2>Four statuses, and why the fourth matters</h2>
<div class="table-wrap">
<table>
<caption>Score credit per status. Inconclusive results are excluded from both sides of the weighted mean.</caption>
<thead><tr><th scope="col">Status</th><th scope="col">Meaning</th><th scope="col">Credit</th></tr></thead>
<tbody>
<tr><td>Pass</td><td>The control met its expectation, and the observation is quoted</td><td>Full</td></tr>
<tr><td>Warning</td><td>Present but weaker than it should be &mdash; a soft SPF qualifier, a short HSTS max-age</td><td>Partial</td></tr>
<tr><td>Fail</td><td>Absent, invalid or actively unsafe</td><td>None</td></tr>
<tr><td>Inconclusive</td><td>The check could not reach a conclusion: timeout, blocked, or an ambiguous answer</td><td>Excluded</td></tr>
</tbody>
</table>
</div>
<p>That fourth status is where most assessment tools quietly cheat. Counting "could not tell" as
a failure punishes a firewall for doing its job; counting it as a pass rewards silence. Removing
it from the calculation and reporting the count separately is the honest option, provided the
report shows how many controls actually ran.</p>

<h2>Why evidence changes the conversation</h2>
<p>A finding without an observation is an opinion. With one, it is a task: here is the TXT record
we received, here is the header that was missing, here is the certificate chain and the hostname
it covers. Anyone can re-run the query from outside the network and compare. If the answers
disagree, the finding is stale or vantage-specific &mdash; and that is a legitimate result rather
than a broken tool.</p>
<p>It also changes what happens after the report. A developer can verify the problem without
asking permission, and a manager can verify the fix without commissioning a second assessment.</p>
<p>In the published recorded assessment, one finding reads like this:</p>
<pre><code>15  Strict-Transport-Security   warning   weight 4
    Evidence: Strict-Transport-Security header not enforced on reference landing page.
    Recommended: send HSTS with max-age of at least one year over HTTPS only.</code></pre>
<p>That is the whole argument: a status, the observation behind it, and the change that would
clear it. A reader who disagrees can fetch the headers and say why, which is a better
conversation than one about a score.</p>

<h2>What it is not</h2>
<ul>
<li><strong>Not a penetration test.</strong> Nothing is exploited, no application logic is
tested, and no credentials are used. <a href="/blogs/assessment-vs-penetration-test/">The
comparison</a> covers this properly.</li>
<li><strong>Not a code review or a vulnerability scan of your application.</strong> A missing
authorisation check on an invoice page is invisible from outside.</li>
<li><strong>Not a compliance audit.</strong> Frameworks ask whether a control exists and is
documented; they do not usually check whether your SPF record is valid today.</li>
<li><strong>Not a guarantee.</strong> A high score means the measured controls met their
expectations. It says nothing about the parts nobody measured.</li>
</ul>

<h2>Eight questions to ask before you buy one</h2>
<ol>
<li>What exactly is in the catalog, and how many controls does it contain?</li>
<li>How is each status assigned, and is the rule published?</li>
<li>What does the score weigh, and can I recompute it from the report?</li>
<li>Will I get the raw observation behind each finding, or only a severity label?</li>
<li>What is explicitly out of scope, in writing?</li>
<li>Does it need credentials or any access beyond a public request?</li>
<li>Can I re-run it on the same scope at a known interval, and compare results?</li>
<li>Who is allowed to be scanned, and how is authorisation recorded?</li>
</ol>
<p>The answers to those eight questions separate a method from a dashboard. Ours are answered on
the <a href="/methodology/">methodology page</a>, with the boundary written down on
<a href="/limitations/">limitations</a> &mdash; and the catalog itself is browsable under
<a href="/capabilities/">capabilities</a>.</p>
""",
        "related": ["assessment-vs-penetration-test", "check-your-external-security-posture-free"],
    },
    {
        "slug": "assessment-vs-penetration-test",
        "cluster": "assessment",
        "title": "External security assessment vs penetration testing",
        "seo_title": "Security assessment vs penetration test: the difference",
        "desc": (
            "Breadth against depth, configuration against exploitation. What each engagement "
            "actually tests, when you need which, and how the two fit together in a year."
        ),
        "lede": (
            "Both produce a document with findings in it, which is why they get confused in "
            "procurement conversations. The difference is what a tester is allowed to do, and "
            "what question the engagement is answering."
        ),
        "date": DATE,
        "updated": DATE,
        "takeaways": [
            "An external assessment checks whether the outside is configured correctly. A penetration test tries to break in.",
            "A penetration test needs written authorisation and a scope document before anything happens. Unauthorised testing is not testing.",
            "An assessment is repeatable and cheap enough to run quarterly; a pentest is an event, usually annual or change-triggered.",
            "Neither replaces the other, and one report should never be presented as the other.",
        ],
        "body": """
<p>The distinction is easiest to hold onto as a question. An external assessment asks: <em>is
this configured the way it should be, and can anyone see otherwise?</em> A penetration test asks:
<em>given a motivated person and permission to attack, can they get in?</em> The first is
breadth. The second is depth.</p>

<h2>Side by side</h2>
<div class="table-wrap">
<table>
<caption>The two engagements answer different questions and produce different artefacts.</caption>
<thead><tr><th scope="col"></th><th scope="col">External posture assessment</th><th scope="col">Penetration test</th></tr></thead>
<tbody>
<tr><th scope="row">Goal</th><td>Measure configuration against a fixed catalog</td><td>Demonstrate whether an attacker can achieve an objective</td></tr>
<tr><th scope="row">Access</th><td>Public requests only; no credentials</td><td>Whatever the rules of engagement allow, often including credentials</td></tr>
<tr><th scope="row">Technique</th><td>Read records, negotiate TLS, inspect headers, check reachability</td><td>Exploit, chain, escalate, pivot, sometimes deceive</td></tr>
<tr><th scope="row">Output</th><td>Status per control with the observation quoted</td><td>Narrative of what was achieved, with proof and impact</td></tr>
<tr><th scope="row">Authorisation</th><td>Still required, but limited to public observation</td><td>Written scope, rules of engagement, testing windows, emergency contacts</td></tr>
<tr><th scope="row">Cadence</th><td>Quarterly, or after infrastructure changes</td><td>Annually, before a launch, or after a significant change</td></tr>
<tr><th scope="row">Blind spots</th><td>Application logic, authentication, internal network</td><td>Coverage depends on scope and time; usually a snapshot</td></tr>
</tbody>
</table>
</div>

<h2>Why the confusion exists</h2>
<p>Three reasons. Both produce "findings". Both are sold by the same kinds of provider. And many
vendors describe automated configuration checks as "penetration testing" because the phrase
carries more weight with a buyer who has one line item for security.</p>
<p>That inflation is not harmless. A business that believes a header scan was a penetration test
skips the engagement that would have found the authorisation bug in its customer portal. A
business that believes a pentest covers its email spoofing exposure gets a clean report and no
DMARC record.</p>

<h2>What a penetration test finds that an assessment never will</h2>
<ul>
<li>Broken access control: one customer reading another's invoice by changing an ID.</li>
<li>Authentication weaknesses: password reset flows, session fixation, token handling.</li>
<li>Business logic abuse: refunds, discounts, workflow bypasses.</li>
<li>Chained exploits where each step is unremarkable and the combination is not.</li>
<li>Insider and social engineering paths, if that is in scope.</li>
</ul>
<p>None of that is visible to an anonymous request, which is exactly why an assessment cannot
claim to cover it.</p>

<h2>What an assessment does that a pentest will not</h2>
<ul>
<li>Cover every domain you own, not just the one in scope, for roughly the effort of one.</li>
<li>Detect drift: the DMARC record that was tightened and then quietly loosened six weeks later.</li>
<li>Produce a comparable number each quarter, so a trend exists at all.</li>
<li>Give a non-specialist a starting point that does not require reading an exploit write-up.</li>
</ul>
<p>Drift is the underrated half. Most small business exposure is not a clever attack; it is a
control that was correct in March and is not in September, because someone changed a DNS host or
renewed a certificate through a different provider.</p>

<h2>When you need which</h2>
<div class="table-wrap">
<table>
<caption>Common triggers, and the engagement that answers them.</caption>
<thead><tr><th scope="col">Situation</th><th scope="col">Start with</th></tr></thead>
<tbody>
<tr><td>No one has ever looked at your external configuration</td><td>Assessment &mdash; it is the cheapest place to find the boring, high-consequence gaps</td></tr>
<tr><td>Taking payments or handling customer accounts in a new application</td><td>Penetration test before launch, assessment on the domain</td></tr>
<tr><td>A customer or insurer asks for evidence of security testing</td><td>Depends on what they specified; read the requirement rather than guessing</td></tr>
<tr><td>You changed hosting, DNS provider or mail platform</td><td>Assessment, to confirm nothing regressed</td></tr>
<tr><td>You suspect a specific incident</td><td>Neither: incident response, in that order of urgency</td></tr>
</tbody>
</table>
</div>

<h2>What the two artefacts actually look like</h2>
<p>The formats differ as much as the methods. Illustrative shapes below, not real engagements:</p>
<div class="table-wrap">
<table>
<caption>A finding from each engagement, in the form a reader would receive it.</caption>
<thead><tr><th scope="col">Assessment finding</th><th scope="col">Penetration test finding</th></tr></thead>
<tbody>
<tr>
<td><code>16 Content-Security-Policy &mdash; warning</code><br>Evidence: header absent on the static response.<br>Action: publish a policy in report-only mode, then enforce.</td>
<td>&ldquo;Access control bypass in invoice view&rdquo;<br>Method: changed an object identifier in the request.<br>Impact: a second customer's invoice was readable. Screenshot and request attached.</td>
</tr>
</tbody>
</table>
</div>
<p>The first can be fixed in a deployment and re-checked with one command. The second cannot be
found by any amount of header inspection, and cannot be fixed without changing application
code. Both are useful; neither substitutes for the other.</p>

<h2>Authorisation is not a formality</h2>
<p>A penetration test without written authorisation is not a penetration test, it is an attack
with a report attached. Scope, testing windows, excluded systems, data handling and an emergency
contact belong in a document both sides sign before the first packet. It is also why "we ran a
pentest on a supplier's portal to see" is a bad idea regardless of intent &mdash; see
<a href="/responsible-use/">responsible use</a>.</p>
<p>An external assessment sits at the low end of that spectrum: it reads what you publish and
makes ordinary requests. Authorisation is still the right starting point, and this project
records consent before a scan of any kind. That is a design decision, not paperwork.</p>

<h2>How they fit together</h2>
<p>The pattern that works for a small business is a cadence, not a purchase: an external
assessment each quarter as a baseline and a drift check, and a penetration test when the
application changes materially, before a launch, or annually if a customer or insurer requires
it. Findings from either should end up in the same register, with an owner and a date, or neither
will be fixed.</p>
<p>If you want the method behind the assessment half, it is published in full:
<a href="/methodology/">methodology</a>, <a href="/capabilities/">the catalog</a>, and
<a href="/limitations/">what the method cannot establish</a>.</p>
""",
        "related": ["what-is-a-security-posture-assessment", "how-to-read-your-security-report"],
    },
    {
        "slug": "check-your-external-security-posture-free",
        "cluster": "assessment",
        "title": "How to check your company's external security posture for free",
        "seo_title": "How to check your external security posture for free",
        "desc": (
            "A twenty-five minute routine you can run yourself, what to write down, and the "
            "honest limits of a manual pass compared with a scored assessment."
        ),
        "lede": (
            "You can establish a real baseline on your own domain without spending anything. What "
            "you cannot do for free is compare this quarter with last quarter, consistently, "
            "across every domain you own."
        ),
        "date": DATE,
        "updated": DATE,
        "takeaways": [
            "Six commands and two browser checks cover the highest-consequence controls on your own domain.",
            "Record the observation, not just the verdict &mdash; the observation is what makes next quarter comparable.",
            "Do this only on domains you own or administer.",
            "Manual passes drift in method; a scored assessment exists to stop exactly that.",
        ],
        "body": """
<p>There are three free routes, and they are not equivalent. The first is a manual pass on your
own domain: fastest, most educational, no account required. The second is reading a published
example report to understand what a scored assessment contains &mdash; this project publishes a
recorded one for <code>example.com</code>. The third is a free tier of some commercial scanner,
which usually trades coverage or history for the price.</p>
<p>Start with the first. It takes about twenty-five minutes and it will change how you read
every other report you receive.</p>

<h2>The routine</h2>
<p>Run these against your own domain from a machine outside your office network. The difference
matters: a firewall rule that blocks the office does not block a customer.</p>
<pre><code># 1. mail authentication policy
dig +short TXT yourdomain.com
dig +short TXT _dmarc.yourdomain.com

# 2. DNS integrity
dig +short DS yourdomain.com
dig +short CAA yourdomain.com

# 3. mail routing
dig +short MX yourdomain.com

# 4. web transport and headers
curl -sSIL https://yourdomain.com | grep -iE 'strict-transport|content-security|x-frame|x-content-type|referrer-policy|permissions-policy|^server|^location'</code></pre>
<p>Then two things a terminal will not tell you: whether the certificate covers the hostname you
actually use (open the site in a browser and read the padlock details), and whether any
subdomain still points at a service you have closed (check each CNAME you know about, and see
<a href="/blogs/external-website-security-checks/">the fifteen-check list</a> for the detail).</p>

<h2>What to write down</h2>
<p>The observation is the deliverable. A verdict without one cannot be compared later, and
"DMARC was fine in March" is not a finding. Keep a table like this one, one row per control:</p>
<div class="table-wrap">
<table>
<caption>A manual baseline that survives contact with next quarter. The observation column is the important one.</caption>
<thead><tr><th scope="col">Control</th><th scope="col">Observation</th><th scope="col">Verdict</th><th scope="col">Owner</th><th scope="col">Checked</th></tr></thead>
<tbody>
<tr><td>SPF</td><td><code>v=spf1 include:_spf.google.com ~all</code></td><td>Warning &mdash; soft fail</td><td>IT</td><td>2026-10-31</td></tr>
<tr><td>DMARC</td><td>No record returned</td><td>Fail</td><td>IT</td><td>2026-10-31</td></tr>
<tr><td>DNSSEC</td><td><code>DS</code> returned, RRSIG present</td><td>Pass</td><td>IT</td><td>2026-10-31</td></tr>
<tr><td>HSTS</td><td>Header absent</td><td>Fail</td><td>Web</td><td>2026-10-31</td></tr>
<tr><td>Certificate</td><td>Valid, covers apex and www, expires in 61 days</td><td>Pass</td><td>Web</td><td>2026-10-31</td></tr>
</tbody>
</table>
</div>
<p>Five rows is a legitimate baseline. Ten is better. What matters is that the same rows are
checked the same way next time.</p>

<h2>What to fix first</h2>
<p>Order by consequence, not by the number of items. A domain that anyone can forge will be used
for invoice fraud against your customers; a missing <code>Permissions-Policy</code> header will
not. In practice the order is almost always: DMARC enforcement, exposed remote access, then
certificate and redirect hygiene, then headers.</p>
<p>Two of those are DNS edits and one is a firewall rule. That is the honest shape of external
posture work at this size &mdash; unglamorous, and done in an afternoon.</p>

<h2>What free cannot give you</h2>
<ul>
<li><strong>Consistency.</strong> Two people checking by hand will classify the same soft SPF
record differently. A score needs a fixed rule.</li>
<li><strong>Weighting.</strong> Deciding whether a missing CSP matters more than a weak DMARC
policy is a judgement call you will make differently every quarter.</li>
<li><strong>History.</strong> Without a stored, comparable result, drift is invisible.</li>
<li><strong>Coverage.</strong> Every subdomain, every domain, every time &mdash; repeatedly, and
without forgetting one.</li>
<li><strong>An artefact.</strong> If a customer or insurer asks for evidence, a spreadsheet you
maintain is weaker than a timestamped report with quoted observations.</li>
</ul>
<p>If your situation is one domain, checked quarterly, by one person, manual is genuinely enough.
The case for a tool starts when there are multiple domains, more than one person, or an external
party asking for proof.</p>

<h2>Try it on a domain that is not yours</h2>
<p>The public sandbox behind this site runs against five allowlisted domains:
<code>example.com</code>, <code>example.org</code>, <code>example.net</code>,
<code>scanme.nmap.org</code> and <code>badssl.com</code>. You cannot point it at your own domain
&mdash; that restriction is deliberate and documented on
<a href="/limitations/">limitations</a>, because a public scanner that will point anywhere is a
weapon with a form on the front. What it is good for is seeing the method: the
<a href="/demo/">recorded assessment</a> shows eight concluded controls with quoted evidence and
a score of 86/100, grade B, including two warnings you can read and verify yourself.</p>
<p>A private assessment of your own domain runs under a written scope and consent record. If you
want that, the <a href="/request-assessment/">request form</a> is the way in; if you would rather
do the twenty-five minutes yourself, the table above is the whole method.</p>
""",
        "related": ["what-is-a-security-posture-assessment", "how-to-read-your-security-report"],
    },
    {
        "slug": "how-to-read-your-security-report",
        "cluster": "assessment",
        "title": "How to read your SMB Scanner Lite report",
        "seo_title": "How to read an SMB Scanner Lite report",
        "desc": (
            "A guided tour of the report: metadata and consent record, the score and its arithmetic, "
            "evidence strings, inconclusive results, and the order to fix things in."
        ),
        "lede": (
            "A report is only useful if you can argue with it. This walkthrough uses the published "
            "recorded assessment of example.com, so every number below can be checked against the "
            "document itself."
        ),
        "date": DATE,
        "updated": DATE,
        "takeaways": [
            "Read the metadata block first: target, timestamp, vantage, scope and the consent record.",
            "Check how many controls completed before trusting the score &mdash; a high score over three controls is not a result.",
            "Every conclusive finding quotes its observation. Re-run it; if the answer differs, the finding is stale or vantage-specific.",
            "Inconclusive is not a pass, and a warning is not a pass with nicer language.",
        ],
        "body": """
<p>The published example is a recorded capture of <code>example.com</code>, a reserved IANA test
domain. Its report ID is <code>SMB-SANDBOX-20261028-A91144E4</code>, the capture is timestamped
28 October 2026 at 17:25 UTC, and the result is <strong>86/100, grade B</strong>. Everything
below refers to that document, which is available in full under
<a href="/sample-report/">sample report</a> and as HTML, JSON, CSV and TXT downloads.</p>

<h2>1. The metadata block</h2>
<p>Before the score, read the header. It answers the questions that decide whether the numbers
mean anything.</p>
<ul>
<li><strong>Target and scope.</strong> Exactly one hostname and the records published for it. Not
"the company".</li>
<li><strong>Timestamp.</strong> A DNS record has no history; a report is a photograph. The date is
part of the finding.</li>
<li><strong>Vantage.</strong> Where the observation was made. A record can resolve differently
for a different resolver, and a firewall can answer one network and drop another.</li>
<li><strong>Policy version and edition.</strong> This capture is from the Public Sandbox Edition,
which runs a read-only subset of the catalog against five allowlisted domains. That is why the
counts below say eight completed rather than twenty-two.</li>
<li><strong>Consent record.</strong> A receipt hash, consent ID and policy version. In this
capture it is <code>CONSENT-20261028-A91144E4</code>. It exists so that "who authorised this
scan" is answerable after the fact.</li>
</ul>

<h2>2. The score, and the arithmetic under it</h2>
<p>86/100 maps to grade B on the published bands: A is 90&ndash;100, B 80&ndash;89, C
65&ndash;79, D 50&ndash;64, F below 50. The score is a weighted mean over the controls that
reached a conclusive status, where each control carries a weight from 1 to 5 and pass earns full
credit, warning earns partial credit, fail earns none.</p>
<div class="table-wrap">
<table>
<caption>Category scores from the recorded capture. Four categories, eight concluded controls.</caption>
<thead><tr><th scope="col">Category</th><th scope="col">Score</th><th scope="col">What it reflects in this capture</th></tr></thead>
<tbody>
<tr><td>DNS and domain hygiene</td><td>95</td><td>Address resolution and a validated DNSSEC chain, both passing</td></tr>
<tr><td>Email authentication</td><td>92</td><td>Strict SPF, <code>p=reject</code> DMARC with strict alignment, deliberate null MX</td></tr>
<tr><td>Transport security</td><td>90</td><td>Valid certificate over TLS 1.3</td></tr>
<tr><td>Web security headers</td><td>68</td><td>HSTS not enforced, CSP absent &mdash; both warnings</td></tr>
</tbody>
</table>
</div>
<p>Notice what the category table does that the headline number cannot: it tells you where the
remaining points are. Here, 86 overall with headers at 68 names the work to be done, and it is
small.</p>

<h2>3. Status and counts</h2>
<p>Check the counts line before anything else: <strong>eight completed, zero
inconclusive</strong>. Zero inconclusive is what makes this score interpretable, because
inconclusive results are excluded from both the numerator and the denominator. A report that
says 100/100 over two completed controls is not a good result; it is a narrow one.</p>
<p>In this capture, six controls pass and two warn. The two warnings are worth reading in full
because they show how the report argues:</p>
<pre><code>15  Strict-Transport-Security   warning
    Strict-Transport-Security header not enforced on reference landing page.

16  Content-Security-Policy     warning
    Content-Security-Policy header absent on static reference response.</code></pre>
<p>Both are ordinary for a minimal reference site, both are fixable in a header configuration,
and neither is presented as a catastrophe. That proportionality is deliberate: a warning is not
a pass with nicer language, and it is not a breach.</p>

<h2>4. Reading evidence like a sceptic</h2>
<p>Each finding carries the observation that produced it, in a form you can re-run:</p>
<pre><code>$ dig +short TXT example.com
"v=spf1 -all"

$ dig +short TXT _dmarc.example.com
"v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s"</code></pre>
<p>The SPF record above is a strict no-mail policy, which is correct for a reserved documentation
domain. That is exactly the kind of judgement an evidence-first report has to make explicitly:
the same record on a business domain that sends invoices would be a finding, not a pass. Method
notes should say so, and ours does on
<a href="/methodology/">methodology</a>.</p>

<h2>5. A triage order that respects weight</h2>
<ol>
<li><strong>Fails on weighted controls.</strong> DMARC enforcement, certificate validity, remote
desktop and high-risk ports. Fix first, verify the same day.</li>
<li><strong>Warnings on weighted controls.</strong> A soft SPF qualifier, a short HSTS
<code>max-age</code>. Usually one configuration change.</li>
<li><strong>Fails on light controls.</strong> Referrer or permissions policy. Batch these into
the next deployment.</li>
<li><strong>Inconclusive.</strong> Not a task for you; check whether the vantage or a firewall
explains it before treating it as either.</li>
</ol>

<h2>6. What to do in the first week</h2>
<p>Give every finding an owner and a date, and paste the evidence into the ticket. Then re-run
the same query that produced the evidence and confirm the fix at the same vantage &mdash; a fix
verified from inside the network is not verified. Keep the JSON export; it is the artefact that
makes next quarter's comparison possible, and it is the one file in the pack that a script can
read.</p>

<h2>7. Red flags in any report, including this one's genre</h2>
<ul>
<li>A score with no method, no weights and no way to recompute it.</li>
<li>Findings without an observation: "weak TLS configuration" and nothing else.</li>
<li>No timestamp, no scope, no statement of vantage.</li>
<li>No limitations section. Every method has limits; a report that claims none is selling.</li>
<li>"100% secure" or a guarantee against breach. No external assessment can offer one, and the
<a href="/limitations/">limitations page</a> says where this one stops.</li>
</ul>
<p>If a report fails three of those, the number in it is decoration. If it passes them, you can
disagree with a finding and still use the document &mdash; which is the whole point of writing
down the observation instead of the conclusion.</p>
""",
        "related": ["what-is-a-security-posture-assessment", "check-your-external-security-posture-free"],
    },
]
