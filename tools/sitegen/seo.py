"""Human-written search snippets for long-form site pages.

Controls the title and description actually emitted by the shared page shell,
rather than altering visible article headings or technical content.
Title target 15-65 characters; description target 60-165 characters.
"""
from __future__ import annotations

OVERRIDES = {
    "/acquisition/": (
        "Acquire SMB Scanner Lite — Software Project",
        "A documented cybersecurity assessment codebase, test suite, website and technical handover. A software project acquisition, not an established SaaS business.",
    ),
    "/contact/": (
        None,
        "Contact the developer about the scanner, a private assessment, technical methodology or project acquisition. No automated scan is triggered by an enquiry.",
    ),
    "/demo/": (
        None,
        "Explore a genuine, recorded example.com assessment from October 2026, with an evidence-backed score and findings. This is stored output, not a live scan.",
    ),
    "/docs/": (
        None,
        "Install the public sandbox, run authorized tests, understand outputs and manage consent receipts. The public edition uses five approved test domains.",
    ),
    "/faq/": (
        None,
        "Answers about scanner coverage, evidence, scoring, authorization, the public sandbox, private assessments and the limits of external testing.",
    ),
    "/limitations/": (
        "Limits of External Security Assessments | SMB Scanner Lite",
        "Understand what external assessments cannot show, from exploitability to internal controls, and why a high score cannot guarantee a secure system.",
    ),
    "/methodology/": (
        "Evidence-Based Assessment Method | SMB Scanner Lite",
        "How SMB Scanner Lite evaluates observable controls, determines findings, weights scores and reports inconclusive results and scope limitations.",
    ),
    "/privacy/": (
        None,
        "How SMB Scanner Lite handles public website visits, enquiries, local consent records and restricted assessment data. Read the project's privacy commitments.",
    ),
    "/request-assessment/": (
        None,
        "Request a manually reviewed security assessment for a domain you own. Scope, written authorization, timing and price are agreed before testing.",
    ),
    "/resources/": (
        "Security Knowledge Base | SMB Scanner Lite",
        "Technical guides to DNS, email authentication, public infrastructure, security misconfigurations and the interpretation of evidence-backed scores.",
    ),
    "/resources/assessment-methodology/": (
        "External Assessment: Scope and Evidence | SMB Scanner Lite",
        "Define scope, select the observation point, attach evidence and state the limits of an external security assessment without overstating its findings.",
    ),
    "/resources/dnssec-explained/": (
        "DNSSEC: What It Protects | SMB Scanner Lite",
        None,
    ),
    "/resources/external-security-posture-assessment/": (
        "External Security Posture Assessment | SMB Scanner Lite",
        None,
    ),
    "/resources/public-facing-infrastructure/": (
        "Mapping Public Infrastructure | SMB Scanner Lite",
        None,
    ),
    "/resources/security-misconfigurations/": (
        "Six Visible Security Misconfigurations | SMB Scanner Lite",
        None,
    ),
    "/resources/smb-cybersecurity-basics/": (
        "Small Business Cybersecurity Basics | SMB Scanner Lite",
        None,
    ),
    "/resources/spf-dkim-dmarc/": (
        "SPF, DKIM and DMARC Explained | SMB Scanner Lite",
        None,
    ),
    "/resources/understanding-posture-scores/": (
        "How to Read Security Posture Scores | SMB Scanner Lite",
        None,
    ),
    "/responsible-use/": (
        "Responsible Use and Authorization | SMB Scanner Lite",
        "Understand authorization, the five-domain public sandbox restriction, consent, responsible scanning, and the boundaries of legitimate defensive work.",
    ),
    "/sample-report/": (
        None,
        "Read an authentic recorded assessment with score, grade, scope, timestamp and detailed findings. Download example reports in HTML, JSON, CSV and TXT.",
    ),
    "/validation/": (
        "Validation and Reproducible Tests | SMB Scanner Lite",
        "Inspect five documented sandbox tests, consent controls and the published methodology. Reproduce the validation steps without trusting a marketing claim.",
    ),
}


def metadata(path: str, title: str, description: str) -> tuple[str, str]:
    override = OVERRIDES.get(path)
    if override:
        title = override[0] if override[0] is not None else title
        description = override[1] if override[1] is not None else description
    return title, description
