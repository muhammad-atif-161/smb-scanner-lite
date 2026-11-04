# Editorial redesign and Cloudflare Phase 4 integration — 2026-11-04

## Design direction

The entire GitHub Pages website is now styled by two intentionally separate
layers:

- \`website/styles.css\` retains the original accessible component/interaction
  system and all detailed report controls, forms, tables, blog and docs layouts.
- \`website/studio.css\` is the **editorial redesign**: mineral ink palette,
  warm light text, one restrained acid-lime accent, sharply set Space Grotesk,
  tabular JetBrains Mono, thin rules, intentional section rhythm, squared
  instrument panels, no gradients/glow and no fabricated graphics.

The home page \`tools/sitegen/pages_home.py\` has been rewritten as a concise
editorial product narrative. It uses real recorded report output from the
project data; no mock customer stories, unverified usage metrics, security
certification claims or AI-generated "partner logos".

Shared \`tools/sitegen/ui.py\` updates navigation, calls to action, metadata
and footer across all 51 generated HTML documents. The original page
builders remain the source of truth; individual \`website/*.html\` build
outputs are **not edited by hand**.

## Integration status — no security shortcuts

The actual Cloudflare API origin is configured in \`site.saas.json\`:

    https://smbscanner-edge.myself-atiff.workers.dev

This URL is public and safe in the website repository. However:

- \`enabled: false\` means no public form submission, domain verification
  requests, or scan dispatch is currently possible from the browser portal.
- The private Cloudflare backend must first receive the four **encrypted**
  Worker secrets: \`IP_HASH_KEY\`, \`GITHUB_DISPATCH_TOKEN\`,
  \`SMB_WORKER_API_TOKEN\`, and \`WORKER_LEASE_SIGNING_KEY\`.
- In the private \`smbscanner-full\` repo, Actions must receive the exact same
  \`SMB_WORKER_API_TOKEN\` secret and \`SMB_WORKER_API_URL\` variable set to
  the HTTPS origin above (no trailing path).
- Backend gates \`ENABLE_ASSESSMENTS\` and \`ENABLE_DISPATCH\` remain off until
  operational consent, access control, abuse limits, and the GitHub Actions
  commercial-workload policy are reviewed. A real scan is not an appropriate
  test of the website redesign.
- **Never** commit tokens, Cloudflare private keys, D1 customer data, or
  report JSON to the public site repo or send secrets through chat.
- Phase 5 verified-payment webhook and full report download do not exist yet.
  The portal has no checkout and the full report remains locked.

## Release procedure when the private integration is truly ready

1. Confirm \`/health\` and \`/ready\` at the real Worker origin.
2. Provision encrypted secrets in Cloudflare and matching GitHub Actions
   variable/secret; verify only using harmless authenticated tests.
3. With \`ENABLE_DISPATCH=false\`, enable assessment creation only on the
   backend and perform one authorized **DNS TXT verification-only** flow.
4. After verifying commercial scanning permission and backend claim/callback
   reliability on an authorized test domain, explicitly enable dispatch in
   the backend for a controlled run; do not retry ambiguous dispatches.
5. Only when secure end-to-end checks pass, change \`site.saas.json\` to
   \`enabled: true\` and run the generator/audit/CI on a dedicated PR.
   It will activate the form and a navigational link to \`/scan/\`.
6. Until then, the homepage directs customers to the existing manually
   reviewed \`/request-assessment/\` route and the authentic recorded demo.

The SaaS beta is DNS/email-only. The 22-control catalog is the full
product's documented capability, not a claim about the limited beta.

## Validation

From the repository root:

    python3 tools/build_site.py --check --audit
    node --test tests/scan_frontend.test.mjs

CI executes both commands without network scanning. The Pages workflow
generates the complete website before uploading it, so source templates and
live generated HTML cannot drift. CSS and JS are content-hashed in the
generated pages; no CDN, font fetching or package bundler is needed.
The \`/scan/\` portal remains \`noindex\`, even while disabled.

### Design QA checklist

- Desktop, tablet, mobile: no horizontal overflow at 360, 720, 960 and 1440px.
- Keyboard navigation, visible focus and functional mobile menu.
- Hero and article text visible with JavaScript disabled.
- Reduced-motion preference respected.
- Proper contrast on lime-on-dark and muted body copy.
- Search and sitemap rules exclude the disabled scan portal.
- No public secret, customer report evidence, or active unverified scan path.
