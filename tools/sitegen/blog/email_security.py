"""Email security cluster: SPF/DKIM/DMARC, DMARC rollout, and spam triage."""

from __future__ import annotations

DATE = "2026-10-31"

POSTS = [
    {
        "slug": "spf-dkim-dmarc-explained",
        "cluster": "email-security",
        "title": "SPF, DKIM and DMARC, explained without the acronym soup",
        "seo_title": "SPF, DKIM and DMARC explained for small businesses",
        "desc": (
            "What the three email records actually do, how they work together, and a ten-minute "
            "check you can run on your own domain without changing anything."
        ),
        "lede": (
            "Three records, three jobs, one outcome: whether a receiving mail server has any "
            "reason to believe a message came from you. Here is the mental model that makes the "
            "rest of the internet's email advice make sense."
        ),
        "date": DATE,
        "updated": DATE,
        "review_months": 6,
        "takeaways": [
            "SPF says which servers may send mail for your domain. DKIM proves a message was not altered after it was signed. DMARC decides what a receiver does when either check fails.",
            "SPF or DKIM on their own are plumbing. DMARC is the part that changes someone else's behaviour.",
            "Alignment is the detail most people miss: DMARC asks whether the domain that authenticated matches the domain in the visible From line.",
            "You can inspect all three on your own domain in about ten minutes, with three <code>dig</code> commands.",
        ],
        "body": """
<p>The original email protocol has no concept of a sender identity. Anyone who can reach a mail
server can claim to be anyone, and for most of the internet's history the receiving side had
nothing to check that claim against. SPF, DKIM and DMARC were added later, one problem at a
time, by different working groups, which is precisely why they look like three unrelated
things bolted onto the same system.</p>
<p>They are not unrelated. Think of them as three questions a receiving mail server asks:</p>
<ol>
<li><strong>Is this machine allowed to send for that domain?</strong> (SPF)</li>
<li><strong>Was this message tampered with after the sender signed it?</strong> (DKIM)</li>
<li><strong>If either answer is bad, what should I do &mdash; and does the domain that passed
even match the one the customer sees?</strong> (DMARC)</li>
</ol>

<h2>What each record actually does</h2>
<div class="table-wrap">
<table>
<caption>The three mechanisms, in the order a receiving server usually evaluates them.</caption>
<thead><tr><th scope="col">Record</th><th scope="col">Where it lives</th><th scope="col">What it answers</th><th scope="col">What it cannot do</th></tr></thead>
<tbody>
<tr><th scope="row">SPF</th><td>A TXT record on the domain itself</td><td>Which IP addresses or hosts are authorised to send mail using this domain as the envelope sender</td><td>Survive forwarding, or tell you anything about the visible From line</td></tr>
<tr><th scope="row">DKIM</th><td>TXT records under <code>&lt;selector&gt;._domainkey</code></td><td>Whether the message body and selected headers match what the sender signed</td><td>Prove the sender is trustworthy &mdash; only that the message was signed with a key that domain published</td></tr>
<tr><th scope="row">DMARC</th><td>A TXT record at <code>_dmarc.yourdomain.com</code></td><td>What to do on failure, where to send reports, and whether authentication has to align with the From domain</td><td>Work at all unless SPF or DKIM aligns for legitimate mail</td></tr>
</tbody>
</table>
</div>

<h2>The part that connects them: alignment</h2>
<p>Here is the subtle bit that trips up almost everyone. SPF authenticates the <em>envelope</em>
sender &mdash; a routing detail the recipient usually never sees. DKIM authenticates a
<em>domain</em> that signed the message. The From line in the customer's inbox is a third thing
entirely, and nothing forces them to agree.</p>
<p>So an attacker can send a message with your domain in the From line, use a domain they
control for the envelope sender, pass SPF on <em>their</em> domain, and land in an inbox looking
like you. DMARC closes that gap by asking for alignment: did the domain that passed SPF or DKIM
match the domain in From? That question &mdash; not the pass itself &mdash; is what turns
authentication into protection.</p>
<blockquote>SPF passing for your domain is not the same as SPF passing for your domain on a
message that claims to be from you.</blockquote>

<h2>What a healthy configuration looks like</h2>
<p>Concretely, for a business on Google Workspace or Microsoft 365 with a couple of extra
senders, a working setup looks like this. The exact mechanisms differ; the shape does not.</p>
<pre><code>; the domain itself
yourdomain.com.        TXT  "v=spf1 include:_spf.google.com include:spf.protection.outlook.com -all"

; the policy
_dmarc.yourdomain.com. TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@yourdomain.com; adkim=r; aspf=r"

; one signing key (Google Workspace uses the "google" selector)
google._domainkey.yourdomain.com. TXT "v=DKIM1; k=rsa; p=MIIBIjANBg... "</code></pre>
<p>Three things are worth noticing. The SPF record ends in <code>-all</code>, a hard fail, not
<code>~all</code>. The DMARC policy is <code>p=reject</code>, which means receivers are told to
refuse failing mail outright. And the DKIM selector is named &mdash; selectors are not
discoverable by design, so the only people who can check a selector are the ones who know what
it is called.</p>

<h2>A ten-minute check on your own domain</h2>
<p>You do not need a tool for the basics. On macOS or Linux, three queries cover the three
records. On Windows, the same questions work in any DNS lookup site or in PowerShell with
<code>Resolve-DnsName</code>.</p>
<pre><code># 1. SPF (look for a single record, and for -all at the end)
dig +short TXT yourdomain.com

# 2. DMARC (look for v=DMARC1 and the p= value)
dig +short TXT _dmarc.yourdomain.com

# 3. DKIM (use the selector your provider documents, e.g. "google" or "selector1")
dig +short TXT google._domainkey.yourdomain.com</code></pre>
<p>Read the answers for what they are, not for whether something replied. Two SPF records is a
failure, not a merge. An SPF record that ends in <code>?all</code> expresses no opinion at all.
A DMARC record with <code>p=none</code> asks for reports and promises nothing. And a DKIM query
that returns nothing may mean the selector name is wrong rather than the key being missing
&mdash; which is exactly why "DKIM not found" from a checklist site deserves a second look
before you panic.</p>

<h2>Why "we already have SPF" is not the end of the conversation</h2>
<p>SPF is the easiest of the three to publish and the least useful on its own. It breaks when
mail is forwarded, it fails silently when a third-party tool sends on your behalf from an
address you forgot to authorise, and it says nothing about whether the visible sender is you.
A domain with SPF but no DMARC policy is a domain where anyone can still forge the From
line without consequence.</p>
<p>The order that works is unglamorous: inventory every system that sends mail as your domain,
give each one SPF authorisation and its own DKIM signature, then publish DMARC in monitoring
mode, then enforce. Skipping to enforcement is how a business discovers, mid-quarter, that its
invoices have been going to spam for a week.</p>
<p>If you want the record-syntax level detail &mdash; mechanisms, qualifiers, the ten-lookup
limit, the subdomain policy flag &mdash; the reference article on
<a href="/resources/spf-dkim-dmarc/">how email authentication actually works</a> goes deeper
than this page needs to. The <a href="/blogs/set-up-dmarc-without-breaking-email/">DMARC
rollout guide</a> takes the next step: turning a monitoring policy into enforcement without
losing mail.</p>
""",
        "related": ["set-up-dmarc-without-breaking-email", "business-email-marked-as-spam"],
    },
    {
        "slug": "set-up-dmarc-without-breaking-email",
        "cluster": "email-security",
        "title": "How to roll out DMARC without breaking your email",
        "seo_title": "How to set up DMARC without breaking your email",
        "desc": (
            "A staged rollout that starts in monitoring mode, uses aggregate reports to find every "
            "sender you forgot about, and only then moves to enforcement."
        ),
        "lede": (
            "DMARC enforcement is the step where forgotten senders stop being an inconvenience "
            "and start being missing invoices. The way to avoid that is to make the records tell "
            "you what will break before you break it."
        ),
        "date": DATE,
        "updated": DATE,
        "review_months": 6,
        "takeaways": [
            "Publish <code>p=none</code> with a reporting address first. Enforcement before reporting is how legitimately delivered mail disappears.",
            "Inventory every system that sends as your domain before raising the policy: CRM, invoicing, ticketing, website forms, scanners, mailing lists.",
            "Move none &rarr; quarantine &rarr; reject over weeks, using <code>pct=</code> to keep each step small.",
            "Forwarding, mailing lists and subdomains are the three things that break. Each has a known fix.",
        ],
        "body": """
<p>DMARC has two settings that people confuse: what it reports, and what it does. Reporting is
free and safe. Enforcing is neither, until you know what you are sending. A rollout that
respects that order takes a few weeks and usually ends with <code>p=reject</code>; a rollout
that skips it takes an afternoon and ends with a support ticket about missing invoices.</p>

<h2>What "breaking email" actually looks like</h2>
<p>It is rarely dramatic. A customer says the invoice never arrived. A salesperson's follow-up
gets no reply because it went to junk at the recipient. A booking confirmation silently
disappears. Nothing bounces on your side, because the message left your infrastructure
perfectly &mdash; it was rejected or quarantined after it arrived, by a policy you published.</p>
<p>The mechanism is worth internalising: <code>p=quarantine</code> and <code>p=reject</code>
apply to messages that fail both SPF alignment and DKIM alignment. If any legitimate sender
sends as your domain without one of those aligning, enforcement kills it.</p>

<h2>Step 1 &mdash; inventory every sender</h2>
<p>Before touching DNS, write a list. Ask accounts payable, sales and whoever runs the website.
Every entry below is a real sender in a typical small business:</p>
<ul>
<li>Primary mailbox provider: Google Workspace, Microsoft 365, Zoho, or a hosted mail server.</li>
<li>CRM and sales-engagement tools that "send as you".</li>
<li>Invoicing and accounting platforms, including payment reminders.</li>
<li>Helpdesk and ticketing systems, plus any form-to-email on the website.</li>
<li>Scheduling tools, survey tools and newsletter platforms.</li>
<li>Monitoring and alerting that emails from an application.</li>
<li>The scanner that emails documents to accounts, and any device that sends mail.</li>
<li>Agencies, freelancers and virtual assistants with delegated access.</li>
</ul>
<p>If you cannot produce this list from memory, that is the finding. DMARC reports will
complete it for you, which is the point of the next two steps.</p>

<h2>Step 2 &mdash; make SPF and DKIM worth aligning to</h2>
<p>For each sender, two questions: is it authorised in SPF, and does it sign with DKIM for your
domain? Authorising in SPF alone is fragile, because SPF authenticates the envelope sender and
breaks under forwarding. A DKIM signature made with a key published on your domain survives
forwarding in many cases and is the more durable signal.</p>
<p>Most platforms will publish a DKIM key for your domain if you ask them to &mdash; look for a
"domain authentication", "DKIM" or "sender authentication" setting. That is materially better
than sending with the platform's own domain in the envelope while your domain sits in From,
because that arrangement passes SPF for the platform and aligns for nobody.</p>

<h2>Step 3 &mdash; publish monitoring first</h2>
<p>Start with a policy that does nothing except collect reports:</p>
<pre><code>_dmarc.yourdomain.com. TXT "v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com; fo=1; adkim=r; aspf=r"</code></pre>
<p>Two practical notes. Use a dedicated mailbox or a forwarding alias for <code>rua=</code>, not
a person's inbox: aggregate reports arrive daily as XML attachments, one per reporting domain.
And leave <code>adkim</code> and <code>aspf</code> relaxed (<code>r</code>) at this stage, which
allows organisational-domain matching and avoids failing on legitimate subdomain senders you
have not catalogued yet.</p>
<p>If you would rather not read XML, plenty of free and paid services will parse aggregate
reports and present them as a table of source IPs and pass/fail counts. That is the one place
in this process where a third-party service earns its keep &mdash; just check where the reports
are being sent.</p>

<h2>Step 4 &mdash; read the reports until they are boring</h2>
<p>An aggregate report answers four useful questions per sending source: how many messages,
whether SPF aligned, whether DKIM aligned, and what the receiver did with them. You are looking
for two things: sources you did not know about, and volume from sources that fail both checks.</p>
<p>Two weeks of quiet reports &mdash; every legitimate source showing an aligned pass, and the
failures being sources you can name &mdash; is your green light. If a failing source turns out
to be real mail, fix the sender before continuing. If it is a marketing platform sending as
your domain without DKIM, either configure its DKIM or move it to a subdomain you control.</p>

<h2>Step 5 &mdash; enforce in small increments</h2>
<div class="table-wrap">
<table>
<caption>Each step should run for at least a week, longer if the business sends seasonal mail.</caption>
<thead><tr><th scope="col">Step</th><th scope="col">Record change</th><th scope="col">What to watch</th></tr></thead>
<tbody>
<tr><td>1</td><td><code>p=none</code></td><td>New sources appearing in reports; anything failing both checks</td></tr>
<tr><td>2</td><td><code>p=quarantine; pct=25</code></td><td>A quarter of failing mail is quarantined; look for reports of missing mail</td></tr>
<tr><td>3</td><td><code>p=quarantine; pct=100</code></td><td>Full quarantine; confirm no legitimate sender is affected</td></tr>
<tr><td>4</td><td><code>p=reject</code></td><td>Failing mail is refused outright; monitor reports for a fortnight</td></tr>
</tbody>
</table>
</div>
<p><code>pct=</code> asks receivers to apply the policy to a percentage of failing messages, which
is the closest thing DMARC has to a dial. It is imperfect &mdash; not every receiver honours it
exactly &mdash; but it turns a cliff into a ramp. Once you are stable at
<code>p=reject</code>, consider adding <code>sp=reject</code> so subdomains inherit the same
treatment deliberately rather than by accident.</p>

<h2>The three things that break, and their fixes</h2>
<ol>
<li><strong>Forwarding.</strong> A university, a supplier or an old colleague forwards mail from
your domain; the forwarding hop breaks SPF. DKIM alignment is the fix, because the signature
survives if the message is not modified. This is the single strongest argument for real DKIM
everywhere.</li>
<li><strong>Mailing lists.</strong> Lists often rewrite the From address to the list's own
domain, which removes your domain from the equation entirely &mdash; or leave it in place and
modify the body, breaking DKIM. Ask list operators how they handle DMARC; most have a
documented policy by now.</li>
<li><strong>Subdomains.</strong> Without <code>sp=</code>, subdomains inherit the parent policy.
If marketing sends from <code>news.yourdomain.com</code> through a platform you never
configured, <code>p=reject</code> will start refusing it. Either configure that subdomain or
publish an explicit <code>sp=</code> value.</li>
</ol>

<h2>If something breaks anyway</h2>
<p>Get the original message headers from whoever reported the problem &mdash; the
<code>Authentication-Results</code> line names which check failed and for which domain. Usually the answer is "DKIM did not align because the sender is a third party that was
not in the inventory". Fix the sender, then re-run that reporting window.</p>
<p>Rolling back is one DNS edit: lower the policy to <code>p=none</code> and the refusals stop
once the record propagates. That is worth knowing before you start, because it makes the
rollout a reversible decision &mdash; and reversible decisions are the ones that actually get
made in a small business.</p>

<h2>What an external check can and cannot tell you</h2>
<p>Anyone can read your published policy and see whether it is <code>none</code>,
<code>quarantine</code> or <code>reject</code>. What an outsider cannot see is your aggregate
reports &mdash; those are private, and should stay that way. They also cannot enumerate your
DKIM selectors; they can only check the selector names they are given or can reasonably guess.
Both limits are stated rather than hidden in the <a href="/resources/spf-dkim-dmarc/">reference
article</a>, and the <a href="/capabilities/">control catalog</a> shows exactly which email
checks this project performs.</p>
""",
        "related": ["spf-dkim-dmarc-explained", "business-email-marked-as-spam"],
    },
    {
        "slug": "business-email-marked-as-spam",
        "cluster": "email-security",
        "title": "Why your business email keeps landing in spam",
        "seo_title": "Why your business email lands in spam (and how to fix it)",
        "desc": (
            "Authentication failures, mismatched sending domains, new-domain reputation and "
            "list breakage all look the same from the inbox. Here is how to tell them apart."
        ),
        "lede": (
            "When your own email goes to junk, the temptation is to rewrite the message. Most of "
            "the time the words are not the problem &mdash; the domain is. Start with the headers "
            "and work backwards."
        ),
        "date": DATE,
        "updated": DATE,
        "review_months": 6,
        "takeaways": [
            "Read <code>Authentication-Results</code> in the received headers before changing a single word of the message.",
            "A third-party platform sending with your domain in From and its own domain in the envelope passes SPF and aligns for nobody.",
            "Your DMARC policy protects others from being fooled by your domain. It does not by itself improve your own deliverability.",
            "Fix DNS and sender configuration first; treat content and blocklists as the second and third suspects.",
        ],
        "body": """
<p>Deliverability problems feel personal, and that is the trap. You rewrite the subject line, add
a plain-text part, remove the word "free", and nothing changes &mdash; because the receiving
server was never judging your prose. It was judging your domain.</p>

<h2>Start with the headers</h2>
<p>Every delivered message carries the receiving server's verdict in its headers. In Gmail, open
the message, use the three-dot menu and choose <em>Show original</em>; in Outlook, open the
message properties and look at the internet headers. You are looking for a block like this:</p>
<pre><code>Authentication-Results: mx.google.com;
       spf=pass (google.com: domain of bounce@crm.example designates 203.0.113.10)
         smtp.mailfrom=bounce@crm.example;
       dkim=pass header.i=@yourdomain.com header.s=selector1;
       dmarc=fail (p=NONE sp=NONE) header.from=yourdomain.com</code></pre>
<p>That example is the single most common failure in a small business: SPF passed for somebody
else's domain, DKIM passed for the sending platform, and DMARC failed because neither aligned
with <code>yourdomain.com</code>, which is what the recipient sees. The mail was authentic.
It just was not authentic <em>for your domain</em>, and receivers treat that combination with
suspicion.</p>

<h2>The six usual causes</h2>
<div class="table-wrap">
<table>
<caption>Work down this list in order. The first two account for most cases.</caption>
<thead><tr><th scope="col">What you see</th><th scope="col">Likely cause</th><th scope="col">Where the fix lives</th></tr></thead>
<tbody>
<tr><td><code>dmarc=fail</code>, SPF/DKIM pass on another domain</td><td>A platform is sending as your domain without a DKIM key for it</td><td>The platform's domain-authentication settings</td></tr>
<tr><td><code>spf=softfail</code> or <code>spf=fail</code></td><td>Sender not authorised in SPF, or too many lookups (permerror), or two SPF records</td><td>DNS TXT record, at the domain apex</td></tr>
<tr><td><code>dkim=none</code> for your domain</td><td>No DKIM configured, or the provider's key was never added to DNS</td><td>Provider console plus a DNS TXT record</td></tr>
<tr><td>Passes everywhere, still junked</td><td>Domain or IP reputation, a new domain, or a listing on a blocklist</td><td>Reputation data, your sending IP's reverse DNS</td></tr>
<tr><td>Only forwarded mail fails</td><td>The forwarding hop breaks SPF; the message is modified, breaking DKIM</td><td>Cannot be fixed at your end &mdash; relevant to how you judge the failure</td></tr>
<tr><td>Only some recipients junk you</td><td>Receiver-specific scoring, or a user marked you as spam previously</td><td>Honest answer: partly outside your control</td></tr>
</tbody>
</table>
</div>

<h2>Sending "as" your domain from a platform</h2>
<p>Almost every CRM, newsletter tool and helpdesk will offer two options: send with the
platform's domain in the From line, or send as your own domain. The second looks far more
professional and is where the alignment problem starts.</p>
<p>If you choose it, you must authenticate the domain <em>inside that platform</em>. Most provide
a DKIM key and a set of CNAME or TXT records for exactly this. Configure them, wait for the
platform to verify, and only then switch the From address. If the platform cannot sign for your
domain, do not put your domain in From &mdash; use a subdomain you control for that channel, and
keep your main domain for mail that genuinely comes from you.</p>

<h2>Reputation and reverse DNS</h2>
<p>If the message authenticates cleanly and still lands in junk, the question moves from
identity to reputation. Two things are worth checking. First, whether the sending IP has a
reverse DNS entry that matches what the server claims to be &mdash; relevant if you run your own
mail server, irrelevant if you use a hosted provider. Second, whether your domain or IP appears
on a public blocklist; Spamhaus and the major providers publish their own lookup tools, and each
listing has its own removal process. Do not pay a "delisting service" to do something the
blocklist does for free.</p>
<p>A new domain or a newly assigned IP starts with no history, and some receivers are cautious
about it for a few weeks. That is not a bug to be worked around; it is a reason to start sending
small volumes of genuinely wanted mail first.</p>

<h2>What you cannot fix from your side</h2>
<p>Receiver-side scoring is not published, and individual users marking your mail as junk is
invisible to you. Nor does a DMARC policy improve your own deliverability: <code>p=reject</code>
tells receivers what to do with mail that fails <em>for your domain</em>, which protects your
customers from being fooled, not you from being filtered. Those are different problems that get
sold together constantly.</p>

<h2>A triage order that saves time</h2>
<ol>
<li>Get headers from a message that failed, and read <code>Authentication-Results</code>.</li>
<li>If DMARC failed on alignment, fix the sending platform's authentication. That is the whole
job, and no copywriting will help until it is done.</li>
<li>If SPF failed, check for a second SPF record, the ten-lookup limit, and the sender's
authorisation.</li>
<li>If everything passed, look at reputation, blocklists and reverse DNS.</li>
<li>Only then look at content: link shorteners, image-only messages, mismatched link and sender
domains, and attachments that receivers dislike.</li>
</ol>
<p>The first three steps are DNS and configuration work, which is also the part an external
assessment can see. The <a href="/blogs/spf-dkim-dmarc-explained/">explainer on the three
records</a> covers the mechanics, and the <a href="/capabilities/">control catalog</a> lists the
five email controls this project evaluates &mdash; SPF strength, SPF validity, DMARC
enforcement, DKIM presence and MX posture.</p>
""",
        "related": ["spf-dkim-dmarc-explained", "set-up-dmarc-without-breaking-email"],
    },
]
