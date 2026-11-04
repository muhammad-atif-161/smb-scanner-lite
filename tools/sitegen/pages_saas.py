"""Ownership-verified online DNS/email assessment portal.

This route is noindex; public requests are gated by the Cloudflare release switch.
Customer API requests and scans stay disabled until the operator completes deployment.
"""
from __future__ import annotations
from .ui import layout, icon, asset

def portal() -> str:
    body = f"""
<div class="page-head">
  <div class="wrap scan-shell">
    <p class="eyebrow">Online assessment / DNS and email</p>
    <h1>Your domain, verified. Your findings, explained.</h1>
    <p class="lede">Start with a domain you own. Verify control through a temporary DNS record, then authorize a limited review of public DNS and email-authentication policy. No login, vulnerability exploitation or intrusive probing.</p>
  </div>
</div>
<section class="section section--tight">
  <div class="wrap scan-shell" data-saas-portal>
    <ol class="scan-steps" aria-label="Assessment process">
      <li class="scan-step"><b>01</b>Request</li>
      <li class="scan-step"><b>02</b>Verify DNS</li>
      <li class="scan-step"><b>03</b>Run once</li>
      <li class="scan-step"><b>04</b>Preview</li>
    </ol>

    <p class="scan-message" id="scan-message" data-tone="info" aria-live="polite" role="status" hidden></p>

    <section class="scan-panel" id="scan-closed" hidden aria-label="Availability notice">
      <h2>Online scanning is opening soon</h2>
      <p>The assessment interface and private backend are being prepared for controlled customer access.
      Public scan requests are not enabled yet. Explore the example report or contact us about availability.</p>
      <a href="/request-assessment/" class="btn btn-primary">Ask about availability</a>
    </section>

    <section class="scan-panel" id="scan-create" hidden aria-labelledby="scan-create-title">
      <h2 id="scan-create-title">Set up your assessment</h2>
      <p class="scan-privacy">Enter your public domain and a contact address. Never enter passwords, API keys or internal network details.</p>
      <form id="scan-request-form">
        <div class="scan-form">
          <div class="field">
            <label for="scan-name">Your name</label>
            <input class="input" name="name" id="scan-name" type="text" autocomplete="name" maxlength="100" required>
          </div>
          <div class="field">
            <label for="scan-email">Email address</label>
            <input class="input" name="email" id="scan-email" type="email" autocomplete="email" maxlength="254" required>
          </div>
          <div class="field field--wide">
            <label for="scan-target">Public domain</label>
            <input class="input" name="domain" id="scan-target" type="text" maxlength="253" placeholder="yourcompany.com" required>
            <span class="field-hint">Hostname only. No https://, path, port or IP addresses.</span>
          </div>
          <div class="field field--wide">
            <label class="check"><input type="checkbox" id="scan-consent" required>
              <span>I own this domain or have explicit permission from its owner, agree to
              the <a href="/terms/">terms</a> and <a href="/privacy/">privacy policy</a>,
              and understand verification is required before scanning.</span>
            </label>
          </div>
        </div>
        <div class="scan-actions">
          <button type="submit" class="btn btn-primary">Create verification request</button>
          <a href="/demo/" class="btn btn-ghost">See a sample report instead</a>
        </div>
      </form>
    </section>

    <section class="scan-panel" id="scan-resume" hidden aria-labelledby="scan-resume-title">
      <h2 id="scan-resume-title">Return to your assessment</h2>
      <p class="scan-privacy">If you saved your assessment ID and private access token,
      use them here. Neither is ever placed in a URL.</p>
      <form id="scan-resume-form">
        <div class="scan-form">
          <div class="field field--wide">
            <label for="scan-existing-id">Assessment ID</label>
            <input class="input" id="scan-existing-id" name="assessmentId" autocomplete="off" required>
          </div>
          <div class="field field--wide">
            <label for="scan-existing-token">Private access token</label>
            <input class="input" id="scan-existing-token" name="accessToken" type="password" autocomplete="off" required>
          </div>
        </div>
        <div class="scan-actions"><button type="submit" class="btn btn-ghost">Resume securely</button></div>
      </form>
    </section>

    <section class="scan-panel" id="scan-verify" hidden aria-labelledby="scan-verify-title">
      <h2 id="scan-verify-title">Verify domain ownership</h2>
      <p class="scan-privacy">Add the following TXT record at the DNS provider that manages this domain.
      Only after its exact value is observed can the service authorize a scan.</p>
      <dl class="meta-list">
        <div><dt>Domain</dt><dd id="scan-domain"></dd></div>
        <div><dt>TXT record name</dt><dd class="scan-code" id="scan-record-name"></dd></div>
        <div><dt>TXT record value</dt><dd class="scan-code" id="scan-record-value"></dd></div>
      </dl>
      <p class="scan-privacy">The verification challenge expires after one hour. The token
      below gives access to the assessment; do not share it. It is shown for recovery.</p>
      <dl class="meta-list">
        <div><dt>Assessment ID</dt><dd class="scan-code" id="scan-recovery-id"></dd></div>
        <div><dt>Private access token</dt><dd class="scan-code" id="scan-recovery-token"></dd></div>
      </dl>
      <div class="scan-actions">
        <button class="btn btn-primary" id="scan-verify-button" type="button">Verify my TXT record</button>
        <button class="btn btn-ghost" id="scan-copy-token" type="button">Copy private token</button>
      </div>
    </section>

    <section class="scan-panel" id="scan-status" hidden aria-labelledby="scan-status-title">
      <h2 id="scan-status-title">Assessment status</h2>
      <p>Status: <strong id="scan-state">awaiting_verification</strong></p>
      <div class="scan-actions">
        <button class="btn btn-ghost" id="scan-refresh-button" type="button">Refresh status</button>
        <button class="btn btn-ghost" id="scan-new-button" type="button">Clear this tab</button>
      </div>
    </section>

    <section class="scan-panel" id="scan-dispatch" hidden aria-labelledby="scan-dispatch-title">
      <h2 id="scan-dispatch-title">Authorize a single DNS/email scan</h2>
      <p class="scan-privacy">The online worker reads public DNS and email-authentication records only. It does
      not test TLS, web applications or open ports. A scan is dispatched once; an uncertain result is not silently retried.</p>
      <label class="check"><input type="checkbox" id="scan-dispatch-consent">
        <span>I confirm I am authorised to assess this exact domain, and I want to start this single scan.</span>
      </label>
      <div class="scan-actions"><button class="btn btn-primary" id="scan-dispatch-button" type="button">Start authorised scan</button></div>
    </section>

    <section class="scan-panel scan-preview" id="scan-preview" hidden aria-labelledby="scan-preview-title">
      <h2 id="scan-preview-title">Assessment preview</h2>
      <p class="scan-privacy">This is a DNS/email-only posture assessment, not a full perimeter
      scan or a guarantee that the domain is secure.</p>
      <p>Domain: <strong id="scan-preview-domain"></strong></p>
      <div class="scan-grade"><b id="scan-preview-grade">—</b><span id="scan-preview-score">—</span></div>
      <p class="scan-privacy" id="scan-preview-confidence"></p>
      <h3>Top findings</h3>
      <ul id="scan-findings" class="card-list"></ul>
      <div class="scan-lock"><p id="scan-report-notice"></p>
        <p class="scan-privacy">The full evidence report is kept private. Payment and report unlocking are not yet active; this page does not collect any payment.</p>
      </div>
    </section>
  </div>
</section>
"""
    return layout(
        "/scan/",
        "Online Domain Security Assessment | SMB Scanner Lite",
        "A domain ownership verification and limited DNS/email security scan with an evidence-led preview. Online access is opening soon.",
        body, crumbs=[("Home", "/"), ("Security Scan", None)], noindex=True,
        extra_head=(
            f'<link rel="stylesheet" href="{asset("/scan.css")}" />'
            f'<script type="module" src="{asset("/scan-app.mjs")}"></script>'
        ),
    )
