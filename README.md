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
```

| Path | Purpose |
|------|---------|
| `tools/build_site.py` | Entry point: renders pages, sitemap, robots and report downloads |
| `tools/sitegen/config.py` | Site identity, navigation, footer, sitemap, contact address |
| `tools/sitegen/data.py` | 22-control catalog, recorded assessment data, FAQ, resources |
| `tools/sitegen/pages_*.py` | Page templates grouped by audience |
| `website/styles.css` | Midnight Intelligence design system (single stylesheet) |
| `website/site.js` | Navigation, tabs, disclosures, recorded-demo explorer, forms |
| `website/config.js` | Runtime config read by the browser (contact email, form endpoint) |

### Configuration you may need to change

- **Contact email** — set in `tools/sitegen/config.py` (`CONTACT_EMAIL`) *and*
  `website/config.js` (`contactEmail`), then rebuild. Both must match.
- **Form delivery** — the site is static. Forms post to `formEndpoint` in
  `website/config.js` when it is set (any endpoint accepting a JSON POST, such as
  Formspree or Web3Forms). When it is empty, the form composes the enquiry in the
  visitor's mail client and opens it, addressed to the contact email. Neither path
  stores anything on the website.
- **Acquisition price and listing** — `tools/site/config.py` and the acquisition
  page template; keep them consistent with the marketplace listing.

### Content rules enforced by the site

- The recorded assessment shows genuine stored output with its real timestamp,
  report ID and scanner version. It is labelled "recorded", never "live".
- No testimonials, customer logos, review scores, revenue figures or usage
  statistics are published, because none are held with documented permission.
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
