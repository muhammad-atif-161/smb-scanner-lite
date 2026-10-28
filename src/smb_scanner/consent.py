"""Mandatory Pre-Scan User Consent, Privacy Policy Verification & 5-Domain Sandbox Lock."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import urllib.parse
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional

APP_NAME = "SMB Scanner Lite"
EDITION = "Public Sandbox Edition"
VERSION = "5.2.0"
POLICY_VERSION = "2026.10-sandbox-v1"

ALLOWED_SANDBOX_DOMAINS: tuple[str, ...] = (
    "example.com",
    "example.org",
    "example.net",
    "scanme.nmap.org",
    "badssl.com",
)

SANDBOX_DOMAIN_DESCRIPTIONS: dict[str, str] = {
    "example.com": "IANA RFC 2606 / RFC 6761 Reserved Standard Test Domain",
    "example.org": "IANA RFC 2606 / RFC 6761 Reserved Organization Test Domain",
    "example.net": "IANA RFC 2606 / RFC 6761 Reserved Network Test Domain",
    "scanme.nmap.org": "Official Nmap Project Public Authorised Scan Test Host",
    "badssl.com": "Public Educational TLS & Certificate Test Portal",
}

CONSENT_STATEMENT = (
    "I have read and agree to the SMB Scanner Lite Privacy Policy & Acceptable Use "
    "Agreement (2026.10-sandbox-v1). I understand that this public tool is strictly "
    "limited to the 5 approved public testing domains (example.com, example.org, "
    "example.net, scanme.nmap.org, badssl.com) and I consent to having a cryptographic "
    "proof of this consent recorded prior to scanning."
)

POLICY_SHA256 = hashlib.sha256(
    f"{POLICY_VERSION}:{CONSENT_STATEMENT}:{','.join(ALLOWED_SANDBOX_DOMAINS)}".encode("utf-8")
).hexdigest()

DEFAULT_CONSENT_LOG = Path.home() / ".smb_scanner_lite" / "consent_proofs.jsonl"


class SandboxRestrictionError(PermissionError):
    """Raised when a user attempts to scan any target outside the 5 public sandbox domains."""


class ConsentRequiredError(PermissionError):
    """Raised when a scan is attempted without explicit user consent and privacy policy acceptance."""


def normalize_sandbox_target(raw: str) -> str:
    """Normalize input and strictly enforce the 5-domain public sandbox allowlist."""
    s = (raw or "").strip()
    if not s:
        raise SandboxRestrictionError(
            f"No target specified. Choose one of the 5 allowed public test domains: "
            f"{', '.join(ALLOWED_SANDBOX_DOMAINS)}"
        )
    if "://" in s:
        parsed = urllib.parse.urlsplit(s)
        s = parsed.hostname or ""
    else:
        s = s.split("/")[0].split("?")[0].split("#")[0]
        if ":" in s:
            s = s.split(":")[0]
    s = s.strip().strip(".").lower()
    if s not in ALLOWED_SANDBOX_DOMAINS:
        raise SandboxRestrictionError(
            f"TARGET BLOCKED ('{raw}'): {APP_NAME} ({EDITION}) only permits scanning "
            f"the 5 publicly free-to-use testing domains: {', '.join(ALLOWED_SANDBOX_DOMAINS)}."
        )
    return s


@dataclass(frozen=True)
class ConsentReceipt:
    consent_id: str
    timestamp_utc: str
    operator: str
    target: str
    interface: str
    policy_version: str
    policy_sha256: str
    statement: str
    prev_receipt_hash: str
    receipt_sha256: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _compute_receipt_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        {
            "consent_id": payload["consent_id"],
            "timestamp_utc": payload["timestamp_utc"],
            "operator": payload["operator"],
            "target": payload["target"],
            "interface": payload["interface"],
            "policy_version": payload["policy_version"],
            "policy_sha256": payload["policy_sha256"],
            "statement": payload["statement"],
            "prev_receipt_hash": payload["prev_receipt_hash"],
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def record_consent_proof(
    *,
    operator: str,
    target: str,
    accepted_policy: bool,
    interface: str = "cli",
    log_path: Optional[Path] = None,
) -> ConsentReceipt:
    """Validate explicit user consent and append a tamper-evident proof receipt to the ledger."""
    normalized_target = normalize_sandbox_target(target)
    clean_operator = (operator or "").strip()
    if not accepted_policy:
        raise ConsentRequiredError(
            "SCAN ABORTED: You must accept the Privacy Policy & User Consent Agreement "
            "before initiating any scan."
        )
    if len(clean_operator) < 2:
        raise ConsentRequiredError(
            "SCAN ABORTED: Please provide your name or handle (--consent-user) to sign "
            "the pre-scan user consent proof."
        )

    ledger = Path(log_path) if log_path else DEFAULT_CONSENT_LOG
    ledger.parent.mkdir(parents=True, exist_ok=True)

    prev_hash = "0" * 64
    if ledger.exists():
        try:
            lines = [ln.strip() for ln in ledger.read_text(encoding="utf-8").splitlines() if ln.strip()]
            if lines:
                last_entry = json.loads(lines[-1])
                prev_hash = str(last_entry.get("receipt_sha256", prev_hash))
        except Exception:
            prev_hash = "0" * 64

    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    day_tag = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d")
    nonce = hashlib.sha256(f"{now}:{clean_operator}:{normalized_target}:{os.urandom(8).hex()}".encode()).hexdigest()[:8].upper()
    consent_id = f"CONSENT-{day_tag}-{nonce}"

    unsigned = {
        "consent_id": consent_id,
        "timestamp_utc": now,
        "operator": clean_operator,
        "target": normalized_target,
        "interface": interface,
        "policy_version": POLICY_VERSION,
        "policy_sha256": POLICY_SHA256,
        "statement": CONSENT_STATEMENT,
        "prev_receipt_hash": prev_hash,
    }
    digest = _compute_receipt_hash(unsigned)
    receipt = ConsentReceipt(**unsigned, receipt_sha256=digest)

    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(receipt.to_dict(), sort_keys=True) + "\n")

    return receipt


def verify_consent_log(log_path: Optional[Path] = None) -> tuple[bool, int, str]:
    """Verify the SHA-256 hash chain integrity of all recorded consent proofs."""
    ledger = Path(log_path) if log_path else DEFAULT_CONSENT_LOG
    if not ledger.exists():
        return True, 0, f"No consent log entries found at {ledger} yet."

    lines = [ln.strip() for ln in ledger.read_text(encoding="utf-8").splitlines() if ln.strip()]
    prev_hash = "0" * 64
    for idx, line in enumerate(lines, start=1):
        try:
            entry = json.loads(line)
        except Exception as exc:
            return False, idx - 1, f"Entry #{idx} is not valid JSON: {exc}"
        if entry.get("prev_receipt_hash") != prev_hash:
            return False, idx - 1, f"Entry #{idx} ({entry.get('consent_id')}) failed chain link check."
        expected = _compute_receipt_hash(entry)
        if entry.get("receipt_sha256") != expected:
            return False, idx - 1, f"Entry #{idx} ({entry.get('consent_id')}) failed SHA-256 signature verification."
        if entry.get("target") not in ALLOWED_SANDBOX_DOMAINS:
            return False, idx - 1, f"Entry #{idx} contains non-sandbox target '{entry.get('target')}'."
        prev_hash = expected

    return True, len(lines), f"Verified {len(lines)} consent proof receipt(s) in {ledger}; hash chain intact."
