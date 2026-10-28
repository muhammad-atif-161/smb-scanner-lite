"""SMB Scanner Lite — Public Sandbox Edition (5-Domain Locked & Pre-Scan Consent Protected)."""

from __future__ import annotations

from ._core import render_sandbox_html, render_sandbox_text, run_sandbox_assessment
from .cli import build_parser, main, run_cli
from .consent import (
    ALLOWED_SANDBOX_DOMAINS,
    APP_NAME,
    CONSENT_STATEMENT,
    EDITION,
    POLICY_SHA256,
    POLICY_VERSION,
    SANDBOX_DOMAIN_DESCRIPTIONS,
    VERSION,
    ConsentReceipt,
    ConsentRequiredError,
    SandboxRestrictionError,
    normalize_sandbox_target,
    record_consent_proof,
    verify_consent_log,
)

__all__ = [
    "ALLOWED_SANDBOX_DOMAINS",
    "APP_NAME",
    "CONSENT_STATEMENT",
    "ConsentReceipt",
    "ConsentRequiredError",
    "EDITION",
    "POLICY_SHA256",
    "POLICY_VERSION",
    "SANDBOX_DOMAIN_DESCRIPTIONS",
    "SandboxRestrictionError",
    "VERSION",
    "build_parser",
    "main",
    "normalize_sandbox_target",
    "record_consent_proof",
    "render_sandbox_html",
    "render_sandbox_text",
    "run_cli",
    "run_sandbox_assessment",
    "verify_consent_log",
]
