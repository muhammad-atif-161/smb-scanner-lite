# Phase 4 — SaaS web portal (safe, disabled first)

This is the customer-facing companion to the **private** Cloudflare Workers/D1
backend and GitHub Actions Python worker in \`muhammad-atif-161/smbscanner-full\`.

The public website is still built by \`python3 tools/build_site.py\`. The
separate route **/scan/** provides a narrow, owner-authenticated DNS/email
assessment flow. The original sandbox and manual assessment request are
unchanged.

## Status and enable gate

**Do not advertise the portal as live or switch it on until Phase 3 secrets,
GitHub policy permission, and one controlled test are complete.**

\`site.saas.json\` is the only **public** release setting:

    {
      "enabled": false,
      "api_base_url": "https://smbscanner-edge.myself-atiff.workers.dev"
    }

The false gate disables the entire API client even though the public Worker origin is configured. It hides the request form and shows
a manual enquiry link. The portal is \`noindex\` and unlinked; existing live
website content stays unchanged. The browser never contains a GitHub PAT or a
Cloudflare worker secret. The only API value exposed to the browser later is
the normal HTTPS Worker origin (which is not a secret).

After all security checks succeed, use the exact, tested Workers URL:

    {
      "enabled": true,
      "api_base_url": "https://smbscanner-edge.myself-atiff.workers.dev"
    }

**Do not enable this without the private credentials, worker-policy review and a controlled authorized integration test.** The builder refuses
non-HTTPS origins or URLs with a path, query, credentials, or unusual port.
When enabled, the manual assessment page links to /scan/ as a separate
DNS/email beta, not the full multi-control service.

## User flow

1. Name, email and domain + explicit ownership/authorization checkbox.
2. POST /api/v1/assessments creates a **private access token** and time-limited
   _smbscanner-verify TXT record.
3. User publishes TXT; clicking Verify calls POST /verify.
4. User explicitly confirms once more before POST /scan.
5. Status is fetched only when requested by clicking Refresh; no unbounded
   background polling, speculative dispatch retries, or second scans.
6. On completion, GET /preview renders the grade/score and three public
   findings with **textContent** (not unsafe HTML).
7. Full evidence stays locked; no payment button or charge is presented
   until Phase 5 is implemented and a trusted payment webhook exists.

Assessments and customer access tokens are kept in **sessionStorage**
(browser-tab session only), not URLs or persistent localStorage. The user
is also shown the recovery ID and token so they can resume later. They must
keep these secret. The browser may lose its token when a tab is closed;
there is currently no automated recovery email. If an API call fails during
dispatch, the browser **never retries POST /scan** automatically.

All actions depend on the Phase 3 backend feature gates and permissions.
A failed HTTP 503 means the backend is still disabled — not a frontend bug.

## Deployment and test

The Pages deployment workflow now runs the Python site generator and full
link/SEO/accessibility audit on the runner *before* publishing its
\`website/\` artifact. This prevents drift between source templates and
GitHub Pages HTML while retaining an ordinary static site. A lightweight
pull-request-only CI workflow also validates the new browser API client
using Node 24 and in-memory/mock network responses.

Locally:

    python3 tools/build_site.py --check --audit
    node --test tests/scan_frontend.test.mjs

Do not start an actual scan while testing this repository. The tests never
contact Cloudflare or GitHub and do not consume scanning minutes.

## Before turning this on

1. Cloudflare backend /health and /ready must return success (already done).
2. In the Cloudflare Worker, configure **private Worker secrets**:
   \`IP_HASH_KEY\`, \`GITHUB_DISPATCH_TOKEN\`,
   \`SMB_WORKER_API_TOKEN\`, \`WORKER_LEASE_SIGNING_KEY\`.
   Do not put them in GitHub Pages, public config, or chat.
3. In the private GitHub scanner repo, set repository variable
   \`SMB_WORKER_API_URL\` to the exact HTTPS Worker origin, and repository
   secret \`SMB_WORKER_API_TOKEN\` to the same private value as on Cloudflare.
4. Keep \`ENABLE_DISPATCH=false\` while doing DNS-only verification smoke
   checks. To turn on customer scans after confirming commercial workload
   permission and receiving explicit authorization, carefully change backend
   \`ENABLE_ASSESSMENTS\` and \`ENABLE_DISPATCH\` to true and redeploy.
5. Enable this website using \`site.saas.json\` in a *separate, reviewed*
   commit, not during initial code delivery.
6. First customer flow should be a controlled domain you actually own,
   never a third party without written authority. Do not enable port, HTTP,
   or TLS probes on the GitHub runner until separately approved and isolated.

## Safety and current limitations

- This is **DNS/email only**, not a full perimeter/TLS/port scan; the
  separate full private/manual request page still describes a different
  service. Do not market the beta as full coverage.
- The website has no payment integration. Full report retrieval is locked
  by the backend until Phase 5. There is no manual bypass.
- Cookies are not used for backend authentication. A scoped bearer token is
  presented in request headers, not URL query strings.
- Page is noindex even when enabled, so beta testing will not result in
  public search indexing.
- Frontend controls are for usability; all authorization, rate limiting,
  verification, lease enforcement, and payment locking must stay backend-side.
- Before public production: strengthen bot/abuse protection, define customer
  privacy/retention notices for D1, test token loss/recovery UX, and confirm
  GitHub Actions' acceptability for commercial scans.
