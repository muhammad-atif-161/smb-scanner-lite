"""Command-line interface for SMB Scanner Lite (Public Sandbox Edition)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from ._core import render_sandbox_html, render_sandbox_text, run_sandbox_assessment
from .consent import (
    ALLOWED_SANDBOX_DOMAINS,
    APP_NAME,
    CONSENT_STATEMENT,
    DEFAULT_CONSENT_LOG,
    EDITION,
    POLICY_VERSION,
    SANDBOX_DOMAIN_DESCRIPTIONS,
    VERSION,
    ConsentRequiredError,
    SandboxRestrictionError,
    normalize_sandbox_target,
    record_consent_proof,
    verify_consent_log,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="smb-scanner",
        description=(
            f"{APP_NAME} v{VERSION} ({EDITION}) — Restricted to the 5 publicly "
            "free-to-use testing domains with mandatory pre-scan user consent."
        ),
    )
    p.add_argument(
        "target",
        nargs="?",
        help=f"Approved sandbox domain to assess ({', '.join(ALLOWED_SANDBOX_DOMAINS)})",
    )
    p.add_argument("--gui", action="store_true", help="Launch graphical sandbox interface")
    p.add_argument(
        "--list-domains",
        action="store_true",
        help="List the 5 publicly free-to-use testing domains permitted by this edition",
    )
    p.add_argument(
        "--accept-privacy-policy",
        action="store_true",
        help="Confirm you have read and accept PRIVACY_POLICY.md prior to scanning",
    )
    p.add_argument(
        "--consent-user",
        default="",
        metavar="NAME",
        help="Your name or handle for the cryptographic pre-scan consent proof receipt",
    )
    p.add_argument(
        "--consent-log",
        default="",
        metavar="PATH",
        help=f"Path to consent proof ledger (default: {DEFAULT_CONSENT_LOG})",
    )
    p.add_argument(
        "--verify-consent-log",
        action="store_true",
        help="Verify the SHA-256 hash chain integrity of recorded consent proofs",
    )
    p.add_argument("--json", metavar="PATH", help="Write JSON report (includes consent proof)")
    p.add_argument("--html", metavar="PATH", help="Write HTML report (includes consent proof)")
    p.add_argument("--txt", metavar="PATH", help="Write text report (includes consent proof)")
    p.add_argument("--version", action="version", version=f"{APP_NAME} {VERSION} ({EDITION})")
    return p


def _prompt_interactive_consent(target: str) -> tuple[bool, str]:
    if not sys.stdin or not sys.stdin.isatty():
        return False, ""
    print("=" * 72)
    print(f"  {APP_NAME} v{VERSION} — MANDATORY PRE-SCAN USER CONSENT")
    print("=" * 72)
    print(f"  Policy Version : {POLICY_VERSION}")
    print(f"  Target Domain  : {target}")
    print(f"  Statement      : {CONSENT_STATEMENT}")
    print("-" * 72)
    operator = input("  Enter your name or handle to sign consent: ").strip()
    confirm = input("  Type 'I AGREE' to accept the Privacy Policy & proceed: ").strip()
    return (confirm == "I AGREE"), operator


def run_cli(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    log_path = Path(args.consent_log) if args.consent_log else None

    if args.list_domains:
        print(f"{APP_NAME} v{VERSION} — Approved Public Sandbox Domains (5):")
        for dom in ALLOWED_SANDBOX_DOMAINS:
            print(f"  - {dom:18s} : {SANDBOX_DOMAIN_DESCRIPTIONS[dom]}")
        return 0

    if args.verify_consent_log:
        ok, count, msg = verify_consent_log(log_path)
        stream = sys.stdout if ok else sys.stderr
        print(msg, file=stream)
        return 0 if ok else 1

    if args.gui or not args.target:
        from .gui import run_gui

        return run_gui()

    try:
        normalized = normalize_sandbox_target(args.target)
    except SandboxRestrictionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    accepted = bool(args.accept_privacy_policy)
    operator = (args.consent_user or "").strip()
    if not accepted or not operator:
        accepted, operator = _prompt_interactive_consent(normalized)

    try:
        receipt = record_consent_proof(
            operator=operator,
            target=normalized,
            accepted_policy=accepted,
            interface="cli",
            log_path=log_path,
        )
        report = run_sandbox_assessment(normalized, receipt)
    except ConsentRequiredError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4
    except SandboxRestrictionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    txt_out = render_sandbox_text(report)
    print(txt_out, end="")

    if args.txt:
        Path(args.txt).write_text(txt_out, encoding="utf-8")
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.html:
        Path(args.html).write_text(render_sandbox_html(report), encoding="utf-8")

    return 0


def main() -> None:
    sys.exit(run_cli())
