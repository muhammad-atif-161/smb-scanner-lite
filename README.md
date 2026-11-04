# SMB Scanner Lite

An evidence-led, ownership-verified **online domain security assessment** for small businesses, with a separately downloadable **restricted desktop sandbox** for learning.

**Website:** https://smbscannerlite.me

## The online service

The product is a hosted review of public **DNS and email-authentication posture** for a domain the customer can prove they control. A Cloudflare Worker coordinates ownership verification and jobs, a D1 database stores private assessment records, and a separate private Python worker collects bounded DNS/email evidence.

The intended customer journey is to submit a domain, publish a temporary TXT verification record, authorize a single scan, then view a limited preview. Detailed paid reports are planned but **payment and full-report delivery are not enabled yet**.

**Release status:** public scan creation is currently **disabled** until encrypted credentials, operational safeguards and an authorized end-to-end test are completed. The site must never imply public scans or payment are operational prematurely.

The current automated profile covers public DNS, SPF, DMARC and limited DKIM selector discovery. It does **not** perform TCP port probing, TLS tests, HTTP checks, credential testing or vulnerability exploitation.

Visit [scan availability](https://smbscannerlite.me/scan/), [current scope](https://smbscannerlite.me/capabilities/) or [methodology](https://smbscannerlite.me/methodology/).

## The desktop sandbox — different product

The code in this public repository is **SMB Scanner Lite v5.2.0 Public Sandbox Edition**, a small local Python training tool. It is separate from the hosted job runner, and it cannot scan arbitrary customer domains.

It is deliberately restricted to five training targets: example.com, example.org, example.net, scanme.nmap.org and badssl.com. Consent is required, and locally stored receipts are hash-linked. Respect the hosts' published test rules; an allowlist is not blanket permission for intrusive testing.

**Install on Python 3.10+** using these commands:

    git clone https://github.com/muhammad-atif-161/smb-scanner-lite.git
    cd smb-scanner-lite
    python -m pip install -e .
    smb-scanner --help

The full commercial worker and customer report database are private, not present in the public download.

## Website source

The public website is a lightweight static application generated with Python and published through GitHub Pages. It has been rewritten around the owner-verified online service.

- tools/build_site.py — builds all pages, sitemap, redirects and recorded example downloads.
- tools/sitegen/pages_relaunch.py — hosted product, scope, methodology and desktop download.
- tools/sitegen/pages_relaunch_more.py — questions, contact, privacy, terms and responsible use.
- tools/sitegen/pages_relaunch_journal.py and blog/relaunch.py — ten newly authored journal articles at stable URLs.
- tools/sitegen/pages_relaunch_refs.py — eight newly written reference guides.
- website/styles.css and website/studio.css — locally served ivory-and-ink design and tested interface primitives.
- website/scan-app.mjs — customer ownership verification, status and preview interactions; disabled by default.
- site.saas.json — public Worker origin and protected release flag. Never store secrets here.
- site.contact.json — public contact details and optional contact delivery configuration.

**Validate before publishing:**

    python3 tools/build_site.py --check --audit
    node --test tests/scan_frontend.test.mjs
    python3 -m unittest discover -s tests

The Pages workflow rebuilds source templates and validates links, metadata, document structure, form labels, basic structured data and assets. These checks do not replace human desktop/mobile visual review.

## Private backend operations

The operator must set the encrypted Cloudflare secrets IP_HASH_KEY, GITHUB_DISPATCH_TOKEN, SMB_WORKER_API_TOKEN and WORKER_LEASE_SIGNING_KEY, and matching GitHub Actions credentials for the private worker. Public assessment and dispatch feature gates must stay off until controlled authorized testing and operating-policy review are complete.

**Never commit customer data, worker secrets, access tokens or full reports to this public repository.**

## Project and use

Built independently by [Muhammad Atif](https://github.com/muhammad-atif-161). There are no implied third-party certifications, customer testimonials or proven commercial revenue figures. This is a bounded external assessment, **not** a penetration test or guarantee of security.

[Website](https://smbscannerlite.me/) · [Recorded example](https://smbscannerlite.me/sample-report/) · [Privacy](https://smbscannerlite.me/privacy/) · [Responsible use](https://smbscannerlite.me/responsible-use/)

For licensing, see [LICENSE](LICENSE).
