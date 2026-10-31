"""DNS and domain security cluster: the public switchboard and its failure modes."""

from __future__ import annotations

DATE = "2026-10-31"

POSTS = [
    {
        "slug": "dns-security-for-small-businesses",
        "cluster": "dns-security",
        "title": "What DNS security means for a small business",
        "seo_title": "What DNS security means for a small business",
        "desc": (
            "Your DNS records decide where mail goes, who may issue certificates for your domain, "
            "and whether a forged answer is detectable. Here is what to check, and how."
        ),
        "lede": (
            "DNS is the one part of your infrastructure that is both completely public and almost "
            "never reviewed. That combination is why it is the cheapest place to find a real "
            "problem and the easiest place to leave one."
        ),
        "date": DATE,
        "updated": DATE,
        "takeaways": [
            "Every DNS record is public. That is not a flaw, it is what makes an honest outside audit possible.",
            "The riskiest records are not the ones you added &mdash; they are the ones left pointing at a service you stopped paying for.",
            "DNSSEC does not encrypt anything; it makes a forged answer detectable. Broken DNSSEC is worse than none.",
            "Registrar account security matters more than any record: whoever controls the registrar controls every record at once.",
        ],
        "body": """
<p>When a customer types your domain into a browser, something has to answer the question "where
does this live?" and "where does mail for this go?" That something is DNS, a distributed
directory that has been answering those questions since the 1980s and has accumulated an
impressive collection of failure modes along the way.</p>
<p>For a small business, DNS security is not exotic. It is a short list of concrete mistakes:
a record pointing at a service you closed, a policy record nobody updated, a registrar account
with a reused password, a domain auto-renewing off a card that expired.</p>

<h2>Why it is worth looking at from outside</h2>
<p>Almost everything an outsider can learn about your infrastructure begins with a DNS query.
Address records tell them where you are hosted. MX records tell them who handles your mail. TXT
records announce whether your email is authenticated. CAA records say which certificate
authorities are allowed to issue for your name. None of that requires access, because all of it
is published on purpose.</p>
<p>This is the unusual advantage of the subject: a review does not need permission to read your
own public records, and it does not disturb anything. If you own the domain, you are auditing
yourself.</p>

<h2>The five failures that keep turning up</h2>

<h3>1. A record still pointing at a retired service</h3>
<p>Someone stood up a staging site at <code>staging.yourdomain.com</code> pointing at a Heroku
app, an S3 bucket or a Shopify store. The project ended, the subscription lapsed, the record
stayed. Whoever claims that service next inherits your subdomain &mdash; and with it, your
domain's reputation and any cookies scoped to it. This is subdomain takeover, and it is entirely
a hygiene problem rather than an attack.</p>
<pre><code># look for CNAMEs pointing outside your own zone
dig +short CNAME staging.yourdomain.com
dig +short CNAME blog.yourdomain.com</code></pre>
<p>If the answer points at a hostname you no longer control, load it in a browser. A generic
404, a "no such app" page or a provider's default landing page means the target is unclaimed,
which is the dangerous case. Delete the record if the service is gone.</p>

<h3>2. No DNSSEC, so answers can be altered in transit</h3>
<p>DNSSEC adds signatures to DNS answers so a validating resolver can tell a real answer from an
injected one. It does not encrypt queries &mdash; anyone on the path still sees which name you
looked up &mdash; but it does make silent substitution detectable.</p>
<pre><code># a DS record at the parent zone means the child zone is signed
dig +short DS yourdomain.com

# ask for signatures directly
dig +dnssec yourdomain.com A</code></pre>
<p>The trade-off is real: signing requires registrar support for DS records and a DNS host that
signs zones, and a botched key rollover takes the name offline for validating resolvers. Broken
DNSSEC is worse than absent DNSSEC. If you enable it, add an expiry check to whatever calendar
you actually look at.</p>

<h3>3. No CAA record, so any authority may issue for your domain</h3>
<p>CAA lets you name the certificate authorities allowed to issue for your domain. Without it,
a mis-issuance anywhere in the world is valid for your name. It is a five-minute record and one
of the least controversial hardening steps available.</p>
<pre><code>dig +short CAA yourdomain.com
# 0 issue "letsencrypt.org"
# 0 issuewild ";"            ; explicitly forbid wildcard issuance</code></pre>
<p>Add <code>iodef</code> if you want a mailbox that receives reports when someone requests a
certificate you did not authorise. Check your hosting and CDN providers first: some CAs need to
be listed or renewals start failing at the worst possible moment.</p>

<h3>4. Mail routing that nobody has read since setup</h3>
<p>MX mistakes are quiet. A null MX (<code>MX 0 .</code>) is the correct way to say "this domain
never receives mail" and is a sensible default for a domain used only for a website. A domain
that sends but cannot receive is a different story, and an MX pointing at a hostname that no
longer resolves is a third. All three are visible in one query.</p>
<pre><code>dig +short MX yourdomain.com
dig +short TXT yourdomain.com     # SPF lives here too</code></pre>

<h3>5. A registrar account that is the single point of failure</h3>
<p>Every record above can be replaced in a minute by someone with access to your registrar
account. That makes the account more important than any individual record: strong unique
password, two-factor authentication that is not SMS if you can avoid it, registrar lock enabled,
and a recovery address that reaches a person rather than a shared inbox someone left the company
from. Add a calendar reminder for domain expiry that does not depend on the auto-renew card
working.</p>

<h2>A quarterly DNS routine that takes twenty minutes</h2>
<div class="table-wrap">
<table>
<caption>Do this against your own domain only. Querying someone else's zone without permission is not an audit.</caption>
<thead><tr><th scope="col">Check</th><th scope="col">Command</th><th scope="col">What good looks like</th></tr></thead>
<tbody>
<tr><td>Zone delegation</td><td><code>dig NS yourdomain.com</code></td><td>Only nameservers you recognise and still use</td></tr>
<tr><td>Dangling records</td><td><code>dig CNAME</code> on every subdomain you know</td><td>No target you do not control</td></tr>
<tr><td>Zone transfer</td><td><code>dig AXFR @your-ns yourdomain.com</code></td><td>Refused unless you deliberately allow it</td></tr>
<tr><td>DNSSEC</td><td><code>dig DS yourdomain.com</code></td><td>Present, if your registrar and host support it</td></tr>
<tr><td>Certificate authority scope</td><td><code>dig CAA yourdomain.com</code></td><td>Only the CAs you actually use</td></tr>
<tr><td>Mail routing</td><td><code>dig MX</code>, <code>dig TXT</code></td><td>Deliberate, with SPF and DMARC present</td></tr>
</tbody>
</table>
</div>
<p>Keep the output. Last quarter's answers are the only reliable way to notice a record that
changed without anyone deciding to change it.</p>

<h2>What an external check can see</h2>
<p>SMB Scanner Lite evaluates five DNS controls from outside: address and record presence, the
DNSSEC chain, CAA authorisation, zone-transfer exposure and name-record hygiene. Each finding
quotes the answer it received, so you can re-run the query and compare &mdash; including when the
answer differs, which usually means a different resolver or a change made since the assessment.
For the mechanics of signing and validation, the reference article on
<a href="/resources/dnssec-explained/">DNSSEC in plain terms</a> goes deeper.</p>
<p>What this cannot see: records inside a private zone, anything behind split-horizon DNS, and
your registrar account itself. Those need a human with access, which is exactly why the routine
above is worth keeping.</p>
""",
        "related": [],
    },
]
