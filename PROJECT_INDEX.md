# Public repository index

This repository contains the restricted desktop sandbox and a legacy generated Pages site. It is not the production source for the online assessment service. Production source and deployment boundaries are documented in the private [smbscanner-full repository](https://github.com/muhammad-atif-161/smbscanner-full).

## Find the right file

| If you need to… | Edit or read |
| --- | --- |
| Change local sandbox behavior | `src/smb_scanner/` |
| Change sandbox consent or allowed targets | `src/smb_scanner/consent.py`, `src/smb_scanner/_core.py`, and corresponding tests |
| Change the legacy Pages copy | `tools/sitegen/`; rebuild into `website/` |
| Change the contact shown by this legacy Pages copy | **Actions → Change legacy Pages contact email**, or `tools/set_contact.py`; source is `site.contact.json` |
| Change the production website contact | In the private repository, **Actions → Change production contact email** |
| Change the online API or authorized scanner | Use the private `smbscanner-full` repository; its `src/` and `deploy/aws/` are not present here |
| Find online-service design records | `docs/`; check the private repository index for current production status |

## Repository map

- `src/smb_scanner/`: restricted desktop application.
- `tests/`: sandbox and legacy website tests.
- `tools/sitegen/`: page source for the older Pages copy.
- `tools/build_site.py`: static-site build and audit.
- `tools/set_contact.py` and `site.contact.json`: contact settings for the Pages copy.
- `website/`: generated output; do not edit pages by hand.
- `docs/`: design, search, and portal notes. These explain previous decisions and may not describe current production behavior.
- `.github/workflows/phase4-ci.yml`: offline portal/source checks; it does not run a scan.
- `.github/workflows/deploy-pages.yml`: Pages deployment for this legacy copy.
- `.github/workflows/set-contact-email.yml`: updates the legacy copy and requests a Pages deployment.

## Editing rules

Keep the sandbox, its public Pages copy, and the private online service separate. A site redesign belongs in the production repository. Do not copy private scanner modules, tokens, reports, or customer data here. For new external writing and assets, cite factual sources and record asset licenses. The locally served font license is at `website/fonts/OFL.txt`.
