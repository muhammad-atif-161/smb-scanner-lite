# SMB Scanner Lite — desktop sandbox

This public repository contains the restricted desktop learning tool and an older generated copy of the website. The production website and online assessment API are maintained in the private [smbscanner-full repository](https://github.com/muhammad-atif-161/smbscanner-full).

Start with [PROJECT_INDEX.md](PROJECT_INDEX.md) to find the right source file and understand which parts of this repository are legacy.

## Desktop sandbox

This local tool is restricted to five training domains: example.com, example.org, example.net, scanme.nmap.org, and badssl.com. It requires consent and records a local receipt. The allowlist is enforced by the program; it is not permission for intrusive testing.

Install with Python 3.10 or newer:

    git clone https://github.com/muhammad-atif-161/smb-scanner-lite.git
    cd smb-scanner-lite
    python -m pip install -e .
    smb-scanner --help

The private online assessment service uses a separate authorization model and private engine. This desktop sandbox cannot assess customer domains.

## Website files in this repository

The page builders in `tools/sitegen/` produce `website/`. The site is a legacy Pages copy; the production site is built and deployed from the private repository. Do not edit generated HTML directly.

- `tools/build_site.py`: rebuild and audit the static site.
- `tools/set_contact.py`: update this repository's legacy site contact.
- `site.contact.json`: contact source for this Pages copy.
- `.github/workflows/deploy-pages.yml`: GitHub Pages publishing for this copy.
- `.github/workflows/set-contact-email.yml`: changes this copy's contact and triggers its Pages deployment.
- `src/smb_scanner/`: sandbox application code, not the private online scan engine.

The production contact action is in the private repository under **Actions → Change production contact email**. The two repositories are separate sources, so this repository's legacy contact workflow does not change production.

## Safety and licensing

Never commit customer data, API tokens, reports, or credentials here. The full commercial engine and online customer database are private. Review [LICENSE](LICENSE) before reuse. For limitations and data handling, see [PRIVACY_POLICY.md](PRIVACY_POLICY.md).
