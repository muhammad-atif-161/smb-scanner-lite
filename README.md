# SMB Scanner Lite v5.2.0 — Public Sandbox Edition

**Evidence-First External & SMB Security Assessment Demo · Created by Muhammad Atif**

<p align="center">
  <a href="https://smbscannerlite.me"><img src="https://img.shields.io/badge/Main%20Website-smbscannerlite.me-3ED6C5?style=for-the-badge" alt="Main Website" /></a>
  <a href="https://github.com/muhammad-atif-161/smb-scanner-lite"><img src="https://img.shields.io/badge/Public%20Repo-smb--scanner--lite-6C8CFF?style=for-the-badge&logo=github" alt="Public Repo" /></a>
  <a href="https://github.com/muhammad-atif-161"><img src="https://img.shields.io/badge/Creator-Muhammad%20Atif-3DDC97?style=for-the-badge&logo=github" alt="Creator" /></a>
</p>

---

## What Is This?

**SMB Scanner Lite (Public Sandbox Edition)** is the public face of an evidence-first external security posture assessment tool built for educational and defensive demonstration purposes.

It inspects a domain’s public-facing internet footprint (DNS, email authentication, TLS, security headers, and high-risk port exposure) and produces a clear 0–100 Posture Score.

**Important security constraints of this public repository:**

- Full scanning engine and internal modules remain **private**.
- The published package is hard-locked to **exactly 5 free-to-use testing domains**.
- Every scan requires explicit user consent and produces a tamper-evident SHA-256 consent proof receipt.
- No credentials, real customer data, or unrestricted scanning capability is published.

### Allowed Sandbox Domains (only these)

| Domain | Purpose |
|--------|--------|
| `example.com` | IANA RFC 2606 / RFC 6761 reserved test domain |
| `example.org` | IANA reserved organization test domain |
| `example.net` | IANA reserved network test domain |
| `scanme.nmap.org` | Official Nmap Project authorised test host |
| `badssl.com` | Public educational TLS & certificate test portal |

Any other target is rejected before any network request is made.

---

## Website (smbscannerlite.me)

The public site lives in `website/` and is deployed to GitHub Pages by
`.github/workflows/deploy-pages.yml` (static upload, no build step on the runner).
It is generated from a small, dependency-free Python builder so that navigation,
footer, metadata and the recorded assessment data stay consistent across pages.

```bash
# Rebuild every page, sitemap and downloadable report
python3 tools/build_site.py

# Rebuild and verify that every internal link resolves
python3 tools/build_site.py --check

# Rebuild, check links, and run the static SEO / accessibility / structured-data audit
python3 tools/build_site.py --check --audit
```

The audit fails the build on anything that would be wrong for a crawler or a
visitor: a `Product`/`Offer`/`AggregateRating` node appearing again, a relative
or dangling `@id`, a canonical that disagrees with the sitemap, a missing
`alt`, an unlabelled form field, a heading level skip, a third-party font
request. Title/description length is reported as a warning, not an error.

### Assets, fonts and caching

- The three typefaces (Inter, Space Grotesk, JetBrains Mono) are **self-hosted**
  from `website/fonts/` under the SIL OFL 1.1; there is no request to Google
  Fonts and no third-party preconnect. See `website/fonts/OFL.txt`.
- GitHub Pages serves everything with `cache-control: max-age=600` and cannot be
  configured, so the builder appends a content hash to the CSS/JS/config URLs
  (`/styles.css?v=c8f893d1`). Editing a file changes its URL immediately on the
  next build; old cached copies can never be served after a deploy.
- Nothing in `website/` is edited by hand. Change the template, then rebuild.

| Path | Purpose |
|------|---------|
| `tools/build_site.py` | Entry point: renders pages, sitemap, robots and report downloads |
| `tools/sitegen/config.py` | Site identity, navigation, footer, sitemap, contact address |
| `tools/sitegen/data.py` | 22-control catalog, recorded assessment data, FAQ, resources |
| `tools/sitegen/pages_*.py` | Page templates grouped by audience |
| `tools/sitegen/schema.py` | Structured data: site entities, page nodes, article/report builders (no merchant markup) |
| `tools/sitegen/audit.py` | Static audit run by `--audit`: structured data, head tags, headings, labels, links, sitemap |
| `website/styles.css` | Midnight Intelligence design system (single stylesheet, self-hosted `@font-face`) |
| `website/site.js` | Navigation, tabs, disclosures, recorded-demo explorer, forms |
| `website/fonts/` | Self-hosted latin WOFF2 faces + `OFL.txt` (SIL Open Font License 1.1) |
| `website/config.js` | **Generated** runtime config read by the browser (do not edit by hand) |
| `site.contact.json` | Single source of truth for the contact email and form endpoint |
| `tools/set_contact.py` | One-command helper that edits the JSON and rebuilds the site |
| `docs/structured-data.md` | Which schema types are published, which are refused, and why |
| `docs/technical-seo-remediation-2026-10.md` | Audit, plan and verification record for the 2026 SEO/performance work |

### Configuration you may need to change

- **Contact email** — one file only: `site.contact.json`. Do not edit
  `website/config.js` or any page; both are generated from it.

  ```bash
  python3 tools/set_contact.py --show                    # what is published now
  python3 tools/set_contact.py --email you@example.com   # change it + rebuild
  python3 tools/set_contact.py --add-email team@example.com
  python3 tools/set_contact.py --endpoint https://formspree.io/f/xxxxxxx
  python3 tools/set_contact.py --clear-endpoint          # fall back to the mail client
  ```

  It updates the footer, contact page, privacy policy, terms, about page,
  acquisition page, structured data and `website/config.js` in one pass, then runs
  the internal link check.

  You can also do it from the browser: **Actions → “Change contact email” → Run
  workflow**, enter the address, and the workflow commits the rebuild and triggers
  the Pages deployment. Nothing else needs to change.

- **Form delivery** — the site is static. When `form_endpoint` is set (currently a
  Formspree endpoint) the enquiry forms POST to it; when it is empty they compose
  the message in the visitor's mail client instead. Neither path stores data on the
  website. The endpoint lives in the same JSON, so it moves with the address.
- **Acquisition price and listing** — `tools/site/config.py` and the acquisition
  page template; keep them consistent with the marketplace listing.

### Content rules enforced by the site

- The recorded assessment shows genuine stored output with its real timestamp,
  report ID and scanner version. It is labelled "recorded", never "live".
- No testimonials, customer logos, review scores, revenue figures or usage
  statistics are published, because none are held with documented permission.
  The same rule applies to structured data: there is no `Review`,
  `AggregateRating` or `Offer` markup anywhere, and no `Product` markup on the
  acquisition page — a project sale is not a retail product with shipping and
  returns. See `docs/structured-data.md`.
- The five-domain allowlist is stated wherever the demo appears, and the public
  CLI/test suite remains unchanged.
- The 65-control "validation register" is not claimed. `validation/` publishes the
  five reproducible tests that actually exist in `tests/test_sandbox.py`.

### Legacy URLs

`/checks/`, `/how/`, `/ethics/` and the old `/blog/` entries are kept as static
redirect pages (meta refresh + canonical) so existing links and search results do
not break. GitHub Pages does not support server-side redirects.

---

## Quick Start (Public Sandbox)

```bash
# Clone
git clone https://github.com/muhammad-atif-161/smb-scanner-lite.git
cd smb-scanner-lite

# Install editable
pip install -e .

# List the only permitted domains
smb-scanner --list-domains

# Run a sandbox assessment (mandatory consent)
smb-scanner example.com --accept-privacy-policy --consent-user "Your Name" --html report.html

# Verify consent ledger integrity
smb-scanner --verify-consent-log
```

You can also launch the GUI:

```bash
smb-scanner --gui
```

---

## Privacy & Consent

Before any scan runs you must accept the [Privacy Policy](PRIVACY_POLICY.md).  
Each scan records a cryptographic consent proof (`CONSENT-YYYYMMDD-XXXXXXXX`) with a SHA-256 hash chain.

Consent logs are stored **locally** on your machine and are excluded from Git via `.gitignore`.

---

## Repository Layout (Public)

- `src/smb_scanner/` — Restricted sandbox runtime, CLI, GUI, and consent lock
- `tests/` — Safe public tests that verify the 5-domain restriction and consent proofs
- `PRIVACY_POLICY.md` — Mandatory user consent agreement
- `LICENSE` — MIT (does **not** authorise scanning systems you do not own)
- `website/` — the generated public site (GitHub Pages) and its builder in `tools/`

The full control catalog, scoring logic, private rules, internal tests, development notes, and complete source history remain in a **private** repository.

---

## Creator

**Muhammad Atif** — cybersecurity learner from Rawalpindi, Pakistan.  
Building practical defensive tools with an evidence-first philosophy.

- Website: [smbscannerlite.me](https://smbscannerlite.me)
- GitHub: [muhammad-atif-161](https://github.com/muhammad-atif-161)

---

## License & Acceptable Use

MIT License for the published code.  
**You may only use this tool against the five listed public testing domains or systems you own / are explicitly authorised to test.**
