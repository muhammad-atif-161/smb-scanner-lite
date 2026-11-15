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
    <p class="eyebrow">Verified domain assessment / Online service</p>
    <h1>Start with proof of domain control.</h1>
    <p class="lede">The online service checks a defined set of public DNS and email controls. Ownership verification is required before any assessment can run. The result is an evidence report for this profile, not a complete security review.</p>
    <p class="scan-privacy"><strong>Current release:</strong> private beta. Basic is planned as a free, limited DNS and email assessment. Standard and In-Depth are not yet available for self-service; pricing and availability will be stated before release.</p>
  </div>
</div>
<section class="section section--tight">
  <div class="wrap scan-shell" data-saas-portal>
    <ol class="scan-steps" aria-label="Assessment process">
      <li class="scan-step" data-scan-stage="0"><b>01</b>Enter domain</li>
      <li class="scan-step" data-scan-stage="1"><b>02</b>Verify DNS TXT</li>
      <li class="scan-step" data-scan-stage="2"><b>03</b>Run scan</li>
      <li class="scan-step" data-scan-stage="3"><b>04</b>Preview results</li>
      <li class="scan-step" data-scan-stage="4"><b>05</b>Private report</li>
      <li class="scan-step" data-scan-stage="5"><b>06</b>JSON export</li>
    </ol>

    <p class="scan-message" id="scan-message" data-tone="info" aria-live="polite" role="status" hidden></p>

    <section class="scan-panel" id="scan-closed" hidden aria-label="Availability notice">
      <h2>Controlled onboarding</h2>
      <p>The online worker is not yet accepting public jobs. Select a tier and send an enquiry below. This will not initiate a scan or charge you.</p>
    </section>

    <section class="scan-panel" id="scan-create" hidden aria-labelledby="scan-create-title">
      <h2 id="scan-create-title">Choose a profile</h2>
      <p class="scan-privacy">Basic is the only profile planned for the public beta. Standard and In-Depth remain in private beta. No payment is collected here.</p>
      <form id="scan-request-form">
        <fieldset class="scan-tiers" aria-label="Select assessment level">
          <legend class="sr-only">Assessment level</legend>
          <label class="scan-tier is-selected">
            <input type="radio" name="tier" value="basic" checked>
            <span class="scan-tier-type">01 / Limited</span><strong>Basic</strong>
            <span class="scan-tier-price">Free <small>/ beta</small></span>
            <span class="scan-tier-note">Limited runs · ownership verification required</span>
            <span class="scan-tier-desc">Public DNS, SPF, DMARC and selected DKIM observations. Score and findings are limited to the controls that return usable evidence.</span>
            <em>Planned beta profile</em>
          </label>
          <label class="scan-tier">
            <input type="radio" name="tier" value="regular">
            <span class="scan-tier-type">02 / Expanded</span><strong>Standard</strong>
            <span class="scan-tier-price">Private beta</span>
            <span class="scan-tier-desc">A broader owner-verified assessment with a private evidence report and JSON download. Exact coverage will be published before release.</span>
            <em>Not available yet</em>
          </label>
          <label class="scan-tier">
            <input type="radio" name="tier" value="deep">
            <span class="scan-tier-type">03 / Extended scope</span><strong>In-Depth</strong>
            <span class="scan-tier-price">Private beta</span>
            <span class="scan-tier-desc">A separately scoped assessment with a private evidence report and JSON download. Coverage and terms will be agreed before any work begins.</span>
            <em>Not available yet</em>
          </label>
        </fieldset>
        <p class="scan-privacy" id="scan-tier-disclosure" hidden>Standard and In-Depth are not currently available and selecting them will not start a scan or payment.</p>
        <p class="scan-privacy">Enter your public domain and contact address. Never enter credentials, secrets, internal addresses or payment details.</p>
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
              <span>I own this domain or have written permission from its owner and agree to the
              <a href="/terms/">terms</a> and <a href="/privacy/">privacy policy</a>.
              For Basic, I authorize one low-impact DNS/email assessment after successful TXT verification.</span>
            </label>
          </div>
        </div>
        <div class="scan-actions">
          <button type="submit" class="btn btn-primary"><span id="scan-submit-label">Send assessment enquiry</span></button>
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
      <p class="scan-privacy">Server status: <strong id="scan-state" aria-live="polite">awaiting verification</strong></p>
      <p id="scan-progress-label" aria-live="polite">Waiting for ownership verification</p>
      <div class="scan-progress-track" id="scan-running" hidden aria-label="The remote scanner is busy"><span></span></div>
      <p class="scan-activity" id="scan-activity" role="status" aria-live="polite">Request created</p>
      <div class="scan-actions">
        <button class="btn btn-ghost" id="scan-refresh-button" type="button">Refresh status</button>
        <button class="btn btn-ghost" id="scan-new-button" type="button">Clear this tab</button>
      </div>
    </section>

    <section class="scan-panel" id="scan-dispatch" hidden aria-labelledby="scan-dispatch-title">
      <h2 id="scan-dispatch-title">Manual scan launch</h2>
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
      <p class="scan-privacy" id="scan-preview-controls"></p>
      <h3>Top findings</h3>
      <ul id="scan-findings" class="card-list"></ul>
      <div class="scan-lock"><p id="scan-report-notice">Detailed evidence stays private until payment is verified.</p></div>
    </section>

    <section class="scan-panel scan-paywall" id="scan-paywall" hidden aria-labelledby="scan-paywall-title">
      <p class="eyebrow">Private report access</p>
      <h2 id="scan-paywall-title">Unlock the evidence behind your score.</h2>
      <div class="scan-payment-row">
        <div><strong>Private</strong><span>Paid report access · release details pending</span></div>
        <p>Paid profiles are planned to include the complete evidence report and JSON download. Coverage and price will be shown before checkout is enabled.</p>
      </div>
      <div class="scan-actions">
        <button class="btn btn-primary" type="button" id="scan-pay-button" disabled>Checkout not available</button>
      </div>
      <p class="scan-privacy" id="scan-pay-status" role="status" aria-live="polite">Private beta. Checkout is not active, and no payment is collected.</p>
    </section>

    <section class="scan-panel scan-full-report" id="scan-unlocked" hidden aria-labelledby="scan-full-title">
      <p class="eyebrow">Payment confirmed / Private evidence</p>
      <h2 id="scan-full-title">Your full evidence report</h2>
      <p class="scan-privacy">This report covers public DNS and email authentication only. Its observations are time-specific; a good score does not guarantee security.</p>
      <dl class="scan-report-meta">
        <div><dt>Assessed domain</dt><dd id="scan-full-domain"></dd></div>
        <div><dt>Report ID</dt><dd id="scan-full-id"></dd></div>
        <div><dt>Assessment scope</dt><dd>DNS / email controls</dd></div>
      </dl>
      <h3>Detailed controls and evidence</h3>
      <div id="scan-full-findings" class="scan-full-findings"></div>
      <div class="scan-actions">
        <button class="btn btn-primary" id="scan-download-report" type="button" disabled>Download full JSON report</button>
      </div>
      <p class="scan-privacy">Private access requires your assessment ID and token. Store the downloaded report securely.</p>
    </section>
  </div>
</section>
"""
    return layout(
        "/scan/",
        "Online Domain Security Assessment | SMB Scanner Lite",
        "Owner-verified Basic DNS and email posture assessment. Standard and In-Depth remain in private beta; no checkout is available.",
        body, crumbs=[("Home", "/"), ("Security Scan", None)], noindex=True,
        extra_head=(
            f'<link rel="stylesheet" href="{asset("/scan.css")}" />'
            f'<script type="module" src="{asset("/scan-app.mjs")}"></script>'
        ),
    )
