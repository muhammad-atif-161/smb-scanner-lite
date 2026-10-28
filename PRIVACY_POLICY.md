# Privacy Policy & User Consent Agreement — SMB Scanner Lite

**Effective Date:** October 24, 2026  
**Policy Version:** `2026.10-sandbox-v1`  
**Author & Maintainer:** Muhammad Atif ([github.com/muhammad-atif-161](https://github.com/muhammad-atif-161))

---

## 1. Purpose & Public Sandbox Restriction

**SMB Scanner Lite (Public Sandbox Edition)** is an educational defensive security posture demonstration tool created to illustrate external DNS, e-mail authentication, TLS, and HTTP header hygiene concepts safely and responsibly.

To prevent misuse or unauthorised scanning of third-party infrastructure:

1. **The full internal source code of the scanner is kept private** and is not distributed in the public repository.
2. **All public executions (CLI, GUI, and Web Portal) are strictly hard-locked to five (5) publicly free-to-use testing domains:**
   - `example.com` *(IANA RFC 2606 / RFC 6761 reserved testing domain)*
   - `example.org` *(IANA RFC 2606 / RFC 6761 reserved testing domain)*
   - `example.net` *(IANA RFC 2606 / RFC 6761 reserved testing domain)*
   - `scanme.nmap.org` *(Official Nmap Project public authorised test host)*
   - `badssl.com` *(Public educational TLS/certificate test portal)*
3. Any attempt to scan any domain, hostname, or IP address outside these five approved public testing domains is automatically rejected before any network request is made.

---

## 2. Mandatory Pre-Scan User Consent

Before **any** scan can be initiated in SMB Scanner Lite (whether via the command line, the graphical desktop interface, or the interactive website), the user must explicitly review and accept this Privacy Policy & Acceptable Use Agreement.

When you grant consent prior to a scan, SMB Scanner Lite generates a tamper-evident **Consent Proof Receipt** containing:
- **`consent_id`**: Unique receipt identifier (`CONSENT-YYYYMMDD-XXXXXXXX`)
- **`timestamp_utc`**: Exact ISO-8601 UTC timestamp of consent
- **`operator`**: The name or identifier provided by the user giving consent
- **`target`**: The approved public sandbox domain selected for testing
- **`policy_version` & `policy_sha256`**: Cryptographic digest of the accepted Privacy Policy version
- **`statement`**: Explicit attestation of educational, authorised sandbox use
- **`prev_receipt_hash` & `receipt_sha256`**: Tamper-evident SHA-256 hash chain linking each consent receipt to the previous record

Every scan report embeds the corresponding `consent_receipt` as verifiable proof that explicit user consent was obtained prior to execution.

---

## 3. Data Handling & Privacy

1. **No Personal Data Sale or Third-Party Tracking:** SMB Scanner Lite does not sell, rent, or transmit your personal information to any advertising or analytics network.
2. **Local Consent Ledger:** When running the CLI or GUI tool, consent proof receipts are stored locally on your machine (`~/.smb_scanner_lite/consent_proofs.jsonl`, or a custom path specified via `--consent-log`) and are excluded from public Git commits via `.gitignore`.
3. **Network Queries:** During an approved sandbox run, the tool performs standard read-only DNS and HTTPS header lookups strictly against the selected domain from the five approved public test targets.

---

## 4. Acceptable Use & Prohibited Conduct

By using SMB Scanner Lite, you agree that you will **not**:
- Attempt to bypass, modify, or circumvent the 5-domain public sandbox allowlist;
- Reverse-engineer, decompile, or extract the protected runtime package;
- Misrepresent educational sandbox reports as formal commercial security audits; or
- Use this software in violation of any applicable local, national, or international law.

---

## 5. Disclaimer of Warranty

SMB Scanner Lite is provided **"AS IS"** for educational and defensive learning purposes only, without warranty of any kind. The author assumes no liability for any misuse of the software.
