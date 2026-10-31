"""Website and TLS cluster: an externally verifiable checklist."""

from __future__ import annotations

DATE = "2026-10-31"

POSTS = [
    {
        "slug": "external-website-security-checks",
        "cluster": "website-security",
        "title": "15 external website checks any business can run today",
        "seo_title": "15 external website security checks you can run today",
        "desc": (
            "Fifteen things you can verify about your own website from outside, with the command "
            "or browser panel that shows each one and what a good result looks like."
        ),
        "lede": (
            "You do not need a penetration test to find out whether your certificate covers your "
            "own hostname or whether plain HTTP still works. You need fifteen minutes and a "
            "terminal."
        ),
        "date": DATE,
        "updated": DATE,
        "takeaways": [
            "These checks cover the connection and the response, not the application. A pass here is not a security guarantee.",
            "Most findings are configuration, which means most fixes are one deploy and one DNS edit.",
            "Run them quarterly. The value is in the diff, not the first report.",
            "Only run them against domains you own or are authorised to test &mdash; a scan is still a scan.",
        ],
        "body": """
<p>There is a useful dividing line in website security work. On one side: what an anonymous
visitor's browser can observe in a single request. On the other: everything that requires an
account, a payload or a code review. This page stays strictly on the first side, because that
side is free, safe to repeat, and catches the mistakes that were never a decision.</p>
<p>Every check below works against your own site only. If you are checking on behalf of a client,
get it in writing first &mdash; see <a href="/responsible-use/">responsible use</a>.</p>

<h2>Connection and certificate: checks 1 to 4</h2>
<p>Start with one command, which fetches the response headers and follows redirects:</p>
<pre><code>curl -sSIL https://www.yourdomain.com | head -40</code></pre>
<div class="table-wrap">
<table>
<caption>Checks 1-4. All four are visible without any special tooling.</caption>
<thead><tr><th scope="col">#</th><th scope="col">Check</th><th scope="col">How to verify</th><th scope="col">What good looks like</th></tr></thead>
<tbody>
<tr><td>1</td><td>HTTP redirects to HTTPS</td><td><code>curl -sI http://yourdomain.com</code></td><td>A 301 or 308 directly to the HTTPS URL, keeping the path</td></tr>
<tr><td>2</td><td>Certificate is valid and current</td><td>Click the padlock, or <code>openssl s_client -connect yourdomain.com:443 -servername yourdomain.com</code></td><td>Trusted chain, expiry well in the future, no hostname mismatch</td></tr>
<tr><td>3</td><td>Both hostnames are covered</td><td>Open the bare domain and the <code>www</code> version</td><td>Both work, both serve the certificate, neither throws a warning</td></tr>
<tr><td>4</td><td>Only modern TLS</td><td><code>openssl s_client -tls1_1 -connect yourdomain.com:443</code></td><td>The handshake fails; TLS 1.2 and 1.3 succeed</td></tr>
</tbody>
</table>
</div>
<p>Check 1 has a subtlety worth knowing: a redirect that goes to the homepage instead of the
requested path is technically working and practically broken, because it silently rewrites every
deep link. Check 4 fails loudly and harmlessly &mdash; an old protocol being refused is the
expected result, not an error worth investigating.</p>

<h2>Response headers: checks 5 to 11</h2>
<p>These come from the same <code>curl -sI</code> output. Headers are cheap to add and easy to
forget, and their absence is one of the most common findings in any external assessment.</p>
<div class="table-wrap">
<table>
<caption>Checks 5-11. Presence is the minimum; the value matters too.</caption>
<thead><tr><th scope="col">#</th><th scope="col">Header</th><th scope="col">What to look for</th><th scope="col">Why it matters</th></tr></thead>
<tbody>
<tr><td>5</td><td><code>Strict-Transport-Security</code></td><td><code>max-age=31536000; includeSubDomains</code></td><td>Tells browsers to refuse plain HTTP for your domain after the first visit</td></tr>
<tr><td>6</td><td><code>Content-Security-Policy</code></td><td>At minimum <code>default-src 'self'; object-src 'none'</code></td><td>Limits where scripts and embeds can load from, which is what turns an injected string into an executed one</td></tr>
<tr><td>7</td><td><code>X-Content-Type-Options</code></td><td><code>nosniff</code></td><td>Stops browsers guessing a file's type and executing an upload as script</td></tr>
<tr><td>8</td><td>Framing protection</td><td><code>frame-ancestors 'none'</code> in CSP, or <code>X-Frame-Options: DENY</code></td><td>Prevents your pages being embedded in a clickjacking overlay</td></tr>
<tr><td>9</td><td><code>Referrer-Policy</code></td><td><code>strict-origin-when-cross-origin</code> or stricter</td><td>Stops full URLs leaking to third parties through the Referer header</td></tr>
<tr><td>10</td><td><code>Permissions-Policy</code></td><td>Camera, microphone and geolocation denied unless needed</td><td>Limits what an embedded or injected script can request</td></tr>
<tr><td>11</td><td>Version disclosure</td><td>No <code>Server: Apache/2.4.x</code> or <code>X-Powered-By: PHP/8.x</code></td><td>Removes a free hint about which vulnerabilities to try</td></tr>
</tbody>
</table>
</div>
<p>Two honest caveats. A strict CSP will break a site that loads third-party widgets, so add it
in report-only mode first and read the violations. And HSTS with a long <code>max-age</code> is
effectively permanent for returning visitors &mdash; if any subdomain still only serves HTTP,
add <code>includeSubDomains</code> only after fixing it.</p>

<h2>Content and exposure: checks 12 to 15</h2>
<p>These need a browser rather than a single request, and they are the ones most likely to find
something real.</p>
<ol>
<li><strong>Mixed content.</strong> Open DevTools, load the console, and look for warnings about
insecure resources. A page served over HTTPS that pulls in a script over HTTP is only
half-protected, and the browser will often block it outright.</li>
<li><strong>Files that should not be public.</strong> Try a handful of paths that are common
deployment accidents: <code>/.git/config</code>, <code>/.env</code>, <code>/backup.sql</code>,
<code>/.DS_Store</code>. You are looking for a 404. Anything else deserves a conversation with
whoever deploys your site.</li>
<li><strong>Directory listing.</strong> Visit an image or upload directory without a filename.
If you get an index of files, the web server is configured to list them, and every file in it is
now public.</li>
<li><strong>Dangling subdomains.</strong> Enumerate the subdomains you know about &mdash;
<code>mail</code>, <code>blog</code>, <code>shop</code>, <code>staging</code>,
<code>dev</code> &mdash; and check each resolves. Then check where. A CNAME pointing at a
service you closed is the one finding here that can fully compromise your domain's reputation
without touching your server.</li>
</ol>
<p>One more that costs nothing while you are in DevTools: look at the cookies on your login
page. <code>Secure</code>, <code>HttpOnly</code> and <code>SameSite</code> should all be set.
A session cookie without them is a real weakness, not a style preference.</p>

<h2>What these fifteen cannot tell you</h2>
<p>Everything here is a property of the connection and the response. None of it tests whether
your login form can be bypassed, whether an old plugin has a known vulnerability, whether one
customer can read another's invoice by changing a number in the URL, or whether your admin panel
is protected by anything other than obscurity.</p>
<p>That is not a flaw in the list; it is the boundary between configuration review and
application testing. A clean sheet here means "the outside looks properly wired", which is worth
knowing and considerably less than "we are secure". The reference article on
<a href="/resources/security-misconfigurations/">misconfigurations visible from outside</a>
covers the same ground with more detail on each header, and the
<a href="/limitations/">limitations page</a> states the boundary in the same terms.</p>
<p>The fifteen checks map closely onto the controls SMB Scanner Lite automates &mdash; TLS
version, certificate validity, cipher suites, redirect path and the five header checks. Running
them by hand is a good way to understand what an automated result is actually reporting.</p>
""",
        "related": [],
    },
]
