"""Public Sandbox Edition verification suite (5-domain restriction & consent proofs)."""

from __future__ import annotations

from pathlib import Path
import unittest

from smb_scanner import (
    ALLOWED_SANDBOX_DOMAINS,
    ConsentRequiredError,
    SandboxRestrictionError,
    normalize_sandbox_target,
    record_consent_proof,
    run_cli,
    run_sandbox_assessment,
    verify_consent_log,
)


class TestPublicSandboxEdition(unittest.TestCase):
    def test_exactly_five_public_sandbox_domains_allowed(self) -> None:
        self.assertEqual(
            ALLOWED_SANDBOX_DOMAINS,
            (
                "example.com",
                "example.org",
                "example.net",
                "scanme.nmap.org",
                "badssl.com",
            ),
        )
        for dom in ALLOWED_SANDBOX_DOMAINS:
            self.assertEqual(normalize_sandbox_target(f"https://{dom}:443/path"), dom)

    def test_non_sandbox_domains_and_ips_are_blocked(self) -> None:
        blocked = [
            "google.com",
            "github.com",
            "sub.example.com",
            "192.168.1.1",
            "8.8.8.8",
            "localhost",
            "",
        ]
        for target in blocked:
            with self.assertRaises(SandboxRestrictionError):
                normalize_sandbox_target(target)

    def test_scan_requires_explicit_user_consent(self) -> None:
        tmp_log = Path("/tmp/test_consent_required.jsonl")
        tmp_log.unlink(missing_ok=True)
        with self.assertRaises(ConsentRequiredError):
            record_consent_proof(
                operator="Alice",
                target="example.com",
                accepted_policy=False,
                log_path=tmp_log,
            )
        with self.assertRaises(ConsentRequiredError):
            record_consent_proof(
                operator="",
                target="example.com",
                accepted_policy=True,
                log_path=tmp_log,
            )

    def test_consent_proof_hash_chain_and_sandbox_report(self) -> None:
        tmp_log = Path("/tmp/test_consent_chain.jsonl")
        tmp_log.unlink(missing_ok=True)

        r1 = record_consent_proof(
            operator="Muhammad Atif",
            target="example.com",
            accepted_policy=True,
            log_path=tmp_log,
        )
        r2 = record_consent_proof(
            operator="Muhammad Atif",
            target="scanme.nmap.org",
            accepted_policy=True,
            log_path=tmp_log,
        )
        self.assertEqual(r2.prev_receipt_hash, r1.receipt_sha256)

        ok, count, _msg = verify_consent_log(tmp_log)
        self.assertTrue(ok)
        self.assertEqual(count, 2)

        report = run_sandbox_assessment("example.com", r1)
        self.assertEqual(report["target"], "example.com")
        self.assertEqual(report["consent_proof"]["consent_id"], r1.consent_id)
        tmp_log.unlink(missing_ok=True)

    def test_cli_enforces_sandbox_and_consent(self) -> None:
        tmp_log = Path("/tmp/test_cli_consent.jsonl")
        tmp_log.unlink(missing_ok=True)

        # Blocked domain returns exit code 2
        self.assertEqual(
            run_cli(["unauthorized-domain.com", "--accept-privacy-policy", "--consent-user", "Tester"]),
            2,
        )
        # Approved domain with valid consent returns 0
        self.assertEqual(
            run_cli(
                [
                    "example.com",
                    "--accept-privacy-policy",
                    "--consent-user",
                    "Tester",
                    "--consent-log",
                    str(tmp_log),
                ]
            ),
            0,
        )
        tmp_log.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
