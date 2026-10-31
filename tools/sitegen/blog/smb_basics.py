"""SMB basics cluster: the pillar guide for businesses without a security team."""

from __future__ import annotations

DATE = "2026-10-31"

POSTS = [
    {
        "slug": "small-business-cybersecurity-guide",
        "cluster": "smb-basics",
        "title": "Cybersecurity for small businesses: the 2026 field guide",
        "seo_title": "Small business cybersecurity: the 2026 field guide",
        "desc": (
            "The threats that actually reach a small business, the five controls that carry the "
            "most weight, a 30-day starting plan, and how to tell whether any of it is working."
        ),
        "lede": (
            "Most small business security advice is written for companies with a security team. "
            "This is the version for the person who also does the invoicing."
        ),
        "date": DATE,
        "updated": DATE,
        "takeaways": [
            "You are more likely to be impersonated than exploited: forged invoices, spoofed suppliers and hijacked mailboxes come before exploits.",
            "Five controls carry most of the weight: email authentication, multi-factor authentication, patching, a backup you have restored, and an inventory of what is exposed.",
            "Fix the free things first. Most of the exposure in a small business is configuration, not budget.",
            "Measure quarterly with something repeatable, or you cannot tell improvement from luck.",
        ],
        "body": """
<p>Ask a small business owner what cybersecurity means and you usually get one of two answers:
"we have antivirus" or "we are too small to be targeted". Both are reasonable, and both miss
what actually happens. Attacks on small businesses are rarely targeted in the cinematic sense.
They are opportunistic, automated, and shaped around the fact that a five-person company has no
one whose full-time job is noticing.</p>
<p>This guide is the condensed version: what reaches you, what to fix first, what to spend
money on once the free work is done, and how to check that it held. It is reviewed annually;
this revision is from October 2026.</p>

<h2>The threat model that actually applies</h2>
<p>Five patterns cover most of what a small business experiences. Knowing them changes what you
prioritise.</p>
<ol>
<li><strong>Invoice and payment fraud.</strong> Someone impersonates a supplier, or takes over a
real mailbox and replies inside an existing thread. The tell is rarely a bad email address these
days; it is a changed bank detail and a sense of urgency.</li>
<li><strong>Account takeover by password reuse.</strong> A password from an old breach is tried
against your email, your hosting, your accounting platform. If your email is compromised, every
password reset for everything else lands in the attacker's lap.</li>
<li><strong>Exposed remote access.</strong> A remote desktop port opened for a contractor, a NAS
admin panel, a database with a weak password &mdash; reachable from the internet and scanned
continuously by automated tools that do not care who you are.</li>
<li><strong>Phishing that leads to ransomware.</strong> A document, an attachment, a fake login
page, then encryption of the file share because the user had write access to all of it.</li>
<li><strong>A compromised supplier.</strong> Your data is fine; theirs is not. Their mailbox
sends you an invoice with new bank details, and the request is fluent because it was written by
someone who has read your correspondence.</li>
</ol>

<h2>Where a small business is actually exposed</h2>
<p>From the outside, the picture is narrower than the fear. The things that can be observed
about a typical small business are its DNS records, its mail authentication, its certificate and
headers, and which services answer the public internet. In practice, the same handful of gaps
appear again and again: no DMARC enforcement, so anyone can forge the domain; a remote desktop or
file-sharing port exposed because it was convenient once; a subdomain still pointed at a closed
hosting account; a certificate that renews automatically but a header set that nobody owns.</p>
<p>The reason to start here is not that these are the only risks. It is that they are the ones
you can find and fix this week without buying anything.</p>

<h2>The five controls that carry the most weight</h2>
<div class="table-wrap">
<table>
<caption>In rough order of value per hour spent. All five are achievable without a security hire.</caption>
<thead><tr><th scope="col">Control</th><th scope="col">What it stops</th><th scope="col">First step</th></tr></thead>
<tbody>
<tr><td>Email authentication (SPF, DKIM, DMARC)</td><td>Domain forgery in invoice fraud; your own mail being filtered</td><td>Inventory senders, then publish DMARC in monitoring mode</td></tr>
<tr><td>Multi-factor authentication</td><td>Account takeover from reused or leaked passwords</td><td>Email and finance systems first, then everything with a login</td></tr>
<tr><td>Patching and version hygiene</td><td>Exploitation of known vulnerabilities in anything internet-facing</td><td>A monthly calendar entry with someone's name on it</td></tr>
<tr><td>A backup you have actually restored</td><td>Ransomware extortion, accidental deletion, a bad migration</td><td>Restore one file and one folder to a clean machine this month</td></tr>
<tr><td>An inventory of what is exposed</td><td>Forgotten services: the old admin panel, the closed SaaS, the test environment</td><td>List every subdomain and every port you believe is open, then verify</td></tr>
</tbody>
</table>
</div>
<p>None of these is a project. Each is a decision plus an owner. The failure mode in a small
business is almost never ignorance of the control; it is that nobody was named as responsible
for it.</p>

<h2>A 30-day starting plan</h2>
<div class="table-wrap">
<table>
<caption>One thing per week. Do not start the next until the previous is finished.</caption>
<thead><tr><th scope="col">Week</th><th scope="col">Do this</th><th scope="col">Done when</th></tr></thead>
<tbody>
<tr><td>1</td><td>Turn on MFA for email, banking, accounting and hosting</td><td>Every account you would panic about losing has a second factor</td></tr>
<tr><td>2</td><td>Check email authentication and publish DMARC in monitoring mode</td><td>SPF and DKIM exist for every sender; DMARC reports arrive</td></tr>
<tr><td>3</td><td>List everything reachable from the internet, then close what should not be</td><td>Remote desktop and admin panels are behind a VPN or allowlist, not the open internet</td></tr>
<tr><td>4</td><td>Restore a backup on a machine that is not the original</td><td>You know how long it takes and who does it</td></tr>
</tbody>
</table>
</div>
<p>That is four weeks and no new software, apart from whatever MFA you already have. If it feels
slow, consider the alternative: a programme that starts with a tool purchase and ends with a
renewal invoice and no change in posture.</p>

<h2>What to spend money on, in order</h2>
<ol>
<li><strong>Free first.</strong> DNS records, MFA, closing exposed ports, deleting stale
subdomains. This is the majority of the improvement available to most small businesses.</li>
<li><strong>Backup that is off the main network.</strong> Immutable or offline copies, tested.
Worth paying for; worthless if untested.</li>
<li><strong>Endpoint protection with central visibility</strong>, if you have more than a handful
of machines. The visibility matters more than the brand.</li>
<li><strong>Someone to call.</strong> A retainer or an incident response agreement with a local
provider, so the first hour of a bad day is not spent looking for a phone number.</li>
<li><strong>Insurance</strong>, after the controls above. A policy cannot substitute for MFA, and
insurers increasingly ask about exactly these basics before quoting.</li>
</ol>

<h2>How to tell whether it is working</h2>
<p>Security work in a small business tends to be invisible until it fails, which makes it easy
to stop funding. Three habits keep it honest. Keep a written list of what you changed and when,
so a new person can inherit the reasoning. Re-check the external surface quarterly &mdash; the
same checks, compared against last quarter's answers. And run one restore and one "what if the
main mailbox is compromised" drill a year, because the recovery path is the part that is never
practised and always needed.</p>
<p>A posture score is a reasonable way to express the external part of that in one number,
provided you remember what it measures. Ours is a weighted summary of 22 publicly observable
controls, with the observation behind every conclusive finding; it says nothing about your
application code or your internal network. The
<a href="/blogs/what-is-a-security-posture-assessment/">assessment explainer</a> is explicit
about the boundary.</p>

<h2>Advice that does not survive contact with reality</h2>
<ul>
<li><em>"Use a password manager and you are fine."</em> Useful, insufficient. A password manager
does not stop a forged invoice or an exposed RDP port.</li>
<li><em>"Compliance means secure."</em> A questionnaire attests to a control existing on a date.
It does not measure whether it still works.</li>
<li><em>"Buy the enterprise stack."</em> Tools you do not operate are a subscription, not a
control. Fix the records first.</li>
<li><em>"We are too small to be a target."</em> You are probably not a target. You are a
population: automated scanning does not distinguish between you and a larger company.</li>
</ul>
<p>The useful question is not "are we a target" but "if someone tried the cheapest possible
attack against us today, would it work?" For a domain without DMARC and a remote desktop port
open to the world, the answer is often yes &mdash; and both are fixable before Friday.</p>
""",
        "related": ["business-email-marked-as-spam", "external-website-security-checks"],
    },
]
