#!/usr/bin/env python3
"""Change the published contact email (and form endpoint) in one step.

`site.contact.json` at the repository root is the single source of truth for
the contact route. This helper edits it, rebuilds the site so every page,
footer, structured-data block and `website/config.js` agree, and verifies the
internal links.

Examples
--------
    # See the current settings
    python3 tools/set_contact.py --show

    # Change the primary address (rebuilds the site)
    python3 tools/set_contact.py --email hello@example.com

    # Add a second published address and keep the first as primary
    python3 tools/set_contact.py --add-email support@example.com

    # Remove an additional address
    python3 tools/set_contact.py --remove-email support@example.com

    # Point the forms at a form service (or clear it to fall back to mailto)
    python3 tools/set_contact.py --endpoint https://formspree.io/f/xxxxxxxx
    python3 tools/set_contact.py --clear-endpoint

    # Edit the JSON only, without rebuilding
    python3 tools/set_contact.py --email hello@example.com --no-build
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "site.contact.json"
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+'\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

DEFAULTS = {
    "primary_email": "",
    "additional_emails": [],
    "form_endpoint": "",
    "notes": (
        "Single source of truth for the website contact route. Edit this file, then run: "
        "python3 tools/build_site.py --check. tools/set_contact.py updates it for you, and the "
        "'Change contact email' GitHub Action does it from the browser."
    ),
}


def load() -> dict:
    data = dict(DEFAULTS)
    data["additional_emails"] = []
    if CONFIG_FILE.exists():
        try:
            raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except ValueError as exc:
            sys.exit(f"Cannot read {CONFIG_FILE}: {exc}")
        data.update({k: raw[k] for k in data if k in raw})
        data["additional_emails"] = [str(x).strip() for x in data.get("additional_emails", []) if str(x).strip()]
    return data


def save(data: dict) -> None:
    payload = {
        "primary_email": data["primary_email"],
        "additional_emails": data["additional_emails"],
        "form_endpoint": data["form_endpoint"],
        "notes": data.get("notes") or DEFAULTS["notes"],
    }
    CONFIG_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_email(value: str) -> str:
    value = value.strip()
    if not EMAIL_RE.match(value):
        sys.exit(f"'{value}' does not look like an email address. Nothing was changed.")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Change the contact email or form endpoint used across the website.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--email", help="New primary contact address")
    parser.add_argument("--add-email", action="append", default=[], metavar="EMAIL",
                        help="Additional published address (repeatable)")
    parser.add_argument("--remove-email", action="append", default=[], metavar="EMAIL",
                        help="Remove an additional address (repeatable)")
    parser.add_argument("--endpoint", help="Form POST endpoint (Formspree, Web3Forms, ...)")
    parser.add_argument("--clear-endpoint", action="store_true",
                        help="Remove the endpoint so forms use the visitor's mail client")
    parser.add_argument("--show", action="store_true", help="Print the current settings and exit")
    parser.add_argument("--no-build", action="store_true", help="Update the JSON without rebuilding")
    args = parser.parse_args()

    data = load()

    if args.show and not any([args.email, args.add_email, args.remove_email, args.endpoint, args.clear_endpoint]):
        print(f"Config file : {CONFIG_FILE}")
        print(f"Primary     : {data['primary_email'] or '(not set)'}")
        print(f"Additional  : {', '.join(data['additional_emails']) or '(none)'}")
        print(f"Endpoint    : {data['form_endpoint'] or '(none - forms use mailto)'}")
        return 0

    changed = False

    if args.email:
        data["primary_email"] = check_email(args.email)
        changed = True

    for address in args.add_email:
        address = check_email(address)
        if address != data["primary_email"] and address not in data["additional_emails"]:
            data["additional_emails"].append(address)
            changed = True

    for address in args.remove_email:
        address = address.strip()
        if address in data["additional_emails"]:
            data["additional_emails"].remove(address)
            changed = True
        elif address == data["primary_email"]:
            sys.exit("That address is the primary contact. Set a new primary with --email first.")

    if args.endpoint:
        data["form_endpoint"] = args.endpoint.strip()
        changed = True

    if args.clear_endpoint:
        data["form_endpoint"] = ""
        changed = True

    if not changed:
        parser.print_help()
        return 1

    if not data["primary_email"]:
        sys.exit("A primary email is required. Pass --email first.")

    save(data)
    print(f"Updated {CONFIG_FILE}")
    print(f"  primary    : {data['primary_email']}")
    print(f"  additional : {', '.join(data['additional_emails']) or '(none)'}")
    print(f"  endpoint   : {data['form_endpoint'] or '(none - forms use mailto)'}")

    if args.no_build:
        print("Skipped rebuild. Run: python3 tools/build_site.py --check")
        return 0

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_site  # noqa: E402  (imported after the JSON is written)

    build_site.build()
    print("Rebuilt the website, including website/config.js and every page.")
    return build_site.check_links()


if __name__ == "__main__":
    raise SystemExit(main())
