/* ==========================================================================
   SMB Scanner Lite — site interactions
   No dependencies. Every control degrades to a working static state.
   ========================================================================== */
(function () {
  "use strict";

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* --------------------------------------------------------------------------
     Toast
     -------------------------------------------------------------------------- */
  var toastRegion = $("#toastRegion");

  function showToast(message, tone) {
    if (!toastRegion) return;
    var dotClass = tone === "success" ? "dot-pass" : tone === "error" ? "dot-fail" : "dot-info";
    var toast = document.createElement("div");
    toast.className = "toast";
    toast.setAttribute("role", "status");
    toast.innerHTML = '<span class="dot ' + dotClass + '"></span><span></span>';
    toast.lastChild.textContent = message;
    toastRegion.appendChild(toast);
    window.setTimeout(function () {
      toast.classList.add("is-out");
      window.setTimeout(function () { toast.remove(); }, 260);
    }, 3600);
  }
  window.showToast = showToast;

  /* --------------------------------------------------------------------------
     Copy to clipboard
     -------------------------------------------------------------------------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.left = "-1000px";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); resolve(); }
      catch (err) { reject(err); }
      finally { ta.remove(); }
    });
  }

  function bindCopy(btn) {
    var source = btn.closest("[data-copy-source]");
    var value = btn.getAttribute("data-copy") || (source ? source.getAttribute("data-copy-source") : "") || "";
    if (value && !btn.dataset.bound) {
      btn.dataset.bound = "1";
      btn.addEventListener("click", function () {
        copyText(value).then(function () {
          showToast("Evidence copied to clipboard", "success");
        }).catch(function () {
          showToast("Could not copy — select the text manually", "error");
        });
      });
    }
  }

  /* --------------------------------------------------------------------------
     Sticky navigation
     -------------------------------------------------------------------------- */
  var nav = $(".nav");
  if (nav) {
    var onScroll = function () {
      if (window.scrollY > 8) nav.classList.add("is-scrolled");
      else nav.classList.remove("is-scrolled");
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* --------------------------------------------------------------------------
     Mobile navigation panel
     -------------------------------------------------------------------------- */
  var navToggle = $("[data-nav-toggle]");
  var navPanel = $("[data-nav-panel]");

  function setNav(open) {
    if (!navToggle || !navPanel) return;
    navPanel.classList.toggle("is-open", open);
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("is-locked", open);
    var focusables = $$('a[href], button:not([disabled])', navPanel);
    if (open && focusables.length) focusables[0].focus();
    if (!open) {
      var trigger = navToggle.querySelector("[data-icon-open]") || navToggle;
      if (trigger) trigger.focus();
    }
  }

  if (navToggle && navPanel) {
    navToggle.addEventListener("click", function () {
      setNav(!navPanel.classList.contains("is-open"));
    });
    $$("#navPanelLinks a").forEach(function (link) {
      link.addEventListener("click", function () { setNav(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && navPanel.classList.contains("is-open")) setNav(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 980 && navPanel.classList.contains("is-open")) setNav(false);
    });
  }

  /* --------------------------------------------------------------------------
     Scroll reveal
     -------------------------------------------------------------------------- */
  var reveals = $$(".reveal");
  if (reducedMotion || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.12 });
    reveals.forEach(function (el) { revealObserver.observe(el); });
  }

  /* --------------------------------------------------------------------------
     Score animation
     -------------------------------------------------------------------------- */
  function animateScore(card) {
    var target = parseFloat(card.getAttribute("data-score")) || 0;
    var numEl = $("[data-score-num]", card);
    var fill = $("[data-score-fill]", card);
    var gradeEl = $("[data-score-grade]", card);

    function finish() {
      if (numEl) numEl.textContent = String(target);
      if (fill) fill.style.width = target + "%";
    }

    if (reducedMotion || !("IntersectionObserver" in window)) { finish(); return; }

    var duration = 800;
    var startTime = 0;
    function step(now) {
      if (!startTime) startTime = now;
      var t = Math.min((now - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - t, 3);
      if (numEl) numEl.textContent = String(Math.round(target * eased));
      if (fill) fill.style.width = (target * eased) + "%";
      if (t < 1) requestAnimationFrame(step);
      else if (gradeEl) gradeEl.classList.add("is-done");
    }
    requestAnimationFrame(step);
  }

  $$("[data-score-card]").forEach(function (card) {
    if (reducedMotion || !("IntersectionObserver" in window)) { animateScore(card); return; }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateScore(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    observer.observe(card);
  });

  /* --------------------------------------------------------------------------
     Tabs
     -------------------------------------------------------------------------- */
  $$("[data-tabs]").forEach(function (group) {
    var tabs = $$("[role='tab']", group);
    var panels = $$("[role='tabpanel']", group);

    function activate(tab, focus) {
      tabs.forEach(function (t) {
        var selected = t === tab;
        t.setAttribute("aria-selected", selected ? "true" : "false");
        t.tabIndex = selected ? 0 : -1;
      });
      panels.forEach(function (p) {
        p.classList.toggle("is-active", p.getAttribute("aria-labelledby") === tab.id);
        p.hidden = p.getAttribute("aria-labelledby") !== tab.id;
      });
      if (focus !== false) tab.focus();
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { activate(tab); });
      tab.addEventListener("keydown", function (e) {
        var next = null;
        if (e.key === "ArrowRight" || e.key === "ArrowDown") next = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowLeft" || e.key === "ArrowUp") next = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === "Home") next = tabs[0];
        if (e.key === "End") next = tabs[tabs.length - 1];
        if (next) { e.preventDefault(); activate(next); }
      });
    });

    // Make sure one panel is visible even if JS was loaded late.
    var current = tabs.filter(function (t) { return t.getAttribute("aria-selected") === "true"; })[0] || tabs[0];
    if (current) activate(current, false);
  });

  /* --------------------------------------------------------------------------
     Modal
     -------------------------------------------------------------------------- */
  var modal = $("[data-modal]");
  var lastFocused = null;

  function openModal(opener) {
    if (!modal) return;
    lastFocused = opener || document.activeElement;
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("is-locked");
    var closeBtn = $("[data-modal-close]", modal);
    if (closeBtn) closeBtn.focus();
    else {
      var focusables = $$('a[href], button:not([disabled])', modal);
      if (focusables.length) focusables[0].focus();
    }
  }

  function closeModal() {
    if (!modal || !modal.classList.contains("is-open")) return;
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("is-locked");
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  if (modal) {
    $$("[data-modal-open]").forEach(function (btn) {
      btn.addEventListener("click", function (e) { e.preventDefault(); openModal(btn); });
    });
    var closeBtn = $("[data-modal-close]", modal);
    if (closeBtn) closeBtn.addEventListener("click", closeModal);
    var backdrop = $(".modal-backdrop", modal) || modal;
    backdrop.addEventListener("click", function (e) {
      if (e.target === backdrop) closeModal();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modal.classList.contains("is-open")) closeModal();
      if (e.key === "Tab" && modal.classList.contains("is-open")) {
        var focusables = $$('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])', modal)
          .filter(function (el) { return el.offsetParent !== null; });
        if (!focusables.length) return;
        var first = focusables[0];
        var last = focusables[focusables.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }

  /* --------------------------------------------------------------------------
     Copy buttons
     -------------------------------------------------------------------------- */
  $$("[data-copy]").forEach(bindCopy);

  /* --------------------------------------------------------------------------
     Footer year
     -------------------------------------------------------------------------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* --------------------------------------------------------------------------
     Demonstration assessment (demo page)
     -------------------------------------------------------------------------- */
  var ALLOWED = ["example.com", "example.org", "example.net", "scanme.nmap.org", "badssl.com"];

  var demo = $("[data-demo]");
  if (demo) {
    var form = $("[data-demo-form]", demo);
    var input = $("[data-demo-input]", demo);
    var consent = $("[data-demo-consent]", demo);
    var operator = $("[data-demo-operator]", demo);
    var submitBtn = $("[data-demo-submit]", demo);
    var resetBtn = $("[data-demo-reset]", demo);
    var progress = $("[data-demo-progress]", demo);
    var stateBox = $("[data-demo-state]", demo);
    var resultBox = $("[data-demo-result]", demo);
    var errorBox = $("[data-demo-error]", demo);

    function normalize(value) {
      return String(value || "")
        .trim()
        .toLowerCase()
        .replace(/^[a-z]+:\/\//, "")
        .replace(/\/.*$/, "")
        .replace(/^www\./, "")
        .replace(/\.$/, "");
    }

    function setState(html, tone) {
      if (!stateBox) return;
      stateBox.className = "state " + (tone ? "state-" + tone : "state-info");
      stateBox.innerHTML = html;
      stateBox.hidden = false;
    }

    function validate() {
      var value = normalize(input.value);
      var problems = [];
      if (!value) problems.push("Enter one of the approved test domains.");
      else if (/^[0-9.]+$/.test(value)) problems.push("IP addresses are not accepted — this edition works with domain names only.");
      else if (value.indexOf(" ") !== -1) problems.push("Domains cannot contain spaces.");
      else if (ALLOWED.indexOf(value) === -1) {
        problems.push("“" + value + "” is not on the public allowlist.");
        problems.push("This edition can assess example.com, example.org, example.net, scanme.nmap.org and badssl.com only.");
      }
      if (!consent.checked) problems.push("Read and accept the authorisation notice before continuing.");
      if (!operator.value.trim()) problems.push("Enter the name or handle that will sign the consent receipt.");
      return problems;
    }

    function fieldError(inputEl, problems) {
      var wrap = inputEl.closest(".field");
      if (!wrap) return;
      var msg = problems.filter(function (p) {
        return p.indexOf("allowlist") !== -1 || p.indexOf("IP address") !== -1 || p.indexOf("spaces") !== -1 || p.indexOf("Enter one") !== -1;
      })[0];
      wrap.classList.toggle("has-error", Boolean(msg));
      var err = $(".field-error", wrap);
      if (msg) {
        if (!err) {
          err = document.createElement("p");
          err.className = "field-error";
          err.innerHTML = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="8.5" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="10" cy="14" r="0.9" fill="currentColor"/></svg>';
          wrap.appendChild(err);
        }
        err.lastChild.textContent = msg;
      } else if (err) {
        err.remove();
      }
    }

    function showError(message) {
      if (!errorBox) return;
      errorBox.hidden = false;
      errorBox.innerHTML = '<strong>The assessment could not start.</strong><p>' + message + '</p>';
    }

    function hideError() { if (errorBox) { errorBox.hidden = true; errorBox.innerHTML = ""; } }

    function sleep(ms) { return new Promise(function (r) { window.setTimeout(r, ms); }); }

    /* The demonstration result is a stored, real capture of the public sandbox
       run against example.com - a reserved test domain. It is not a scan of the
       domain the visitor typed, and this website cannot run one. */
    var DEMO_FIXTURE = {
      target: "example.com",
      targetDescription: "IANA RFC 2606 / RFC 6761 reserved standard test domain",
      score: 86,
      grade: "B",
      reportId: "SMB-SANDBOX-20261028-A91144E4",
      consentId: "CONSENT-20261028-A91144E4",
      receiptHash: "b068e643725c90429199d458b31a0749b08b4af1caae57fe4ea8878f412820a6",
      timestamp: "2026-10-28T17:25:30Z",
      edition: "Public Sandbox Edition (5-Domain Locked)",
      controls: "8 completed · 0 inconclusive",
      categories: [
        ["DNS & Domain Hygiene", 95],
        ["E-mail Authentication", 92],
        ["Transport Security (TLS)", 90],
        ["Web Security Headers", 68]
      ],
      findings: [
        ["pass", "info", "DNS A/AAAA Resolution",
          "The reserved domain resolves to public anycast addresses.",
          "Resolved example.com -> 104.20.23.154, 172.66.147.243, 2606:4700:10::ac42:93f3, 2606:4700:10::6814:179a"],
        ["pass", "high", "DNSSEC Validation",
          "The zone is signed and the chain of trust validates against the parent.",
          "Zone signed with validated RRSIG and parent DS delegation."],
        ["pass", "high", "SPF Hard-Fail Policy",
          "SPF is published and set to a strict no-mail policy.",
          "v=spf1 -all (strict no-mail policy for reserved domain)."],
        ["pass", "high", "DMARC Enforcement",
          "Unauthorised senders are rejected at the receiving mail server.",
          "v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s"],
        ["pass", "medium", "RFC 7505 Null MX",
          "The domain publishes a null MX, signalling that it does not accept mail.",
          "MX 0 . published indicating domain does not accept e-mail."],
        ["pass", "high", "TLS 1.2/1.3 & Certificate",
          "TLS 1.3 is offered with a certificate that covers the domain.",
          "Valid X.509 certificate covering example.com over TLS 1.3."],
        ["warn", "medium", "HTTP Strict-Transport-Security",
          "HSTS is not enforced on the reference landing page.",
          "Strict-Transport-Security header not enforced on reference landing page."],
        ["warn", "medium", "Content-Security-Policy",
          "A content security policy is not set on the static reference response.",
          "Content-Security-Policy header absent on static reference response."]
      ]
    };

    var DEMO_NOTE =
      "This is the stored demonstration result for <strong>example.com</strong>, a reserved test " +
      "domain, captured 28 October 2026. It is not a scan of the domain you entered - this website " +
      "cannot scan anything. The public sandbox performs the real read-only checks on your own machine.";

    function dotFor(kind) {
      if (kind === "warn") return "dot dot-warn";
      if (kind === "fail") return "dot dot-fail";
      return "dot dot-pass";
    }

    function esc(v) { return String(v).replace(/"/g, "&quot;").replace(/&/g, "&amp;"); }

    function renderDemoResult() {
      if (!resultBox) return;
      var f = DEMO_FIXTURE;
      var cats = f.categories.map(function (c) {
        return '<div class="kpi"><b>' + c[1] + '</b><span>' + c[0] + '</span></div>';
      }).join("");
      var rows = f.findings.map(function (x) {
        return '<div class="finding"><div class="finding-head"><span class="' + dotFor(x[0]) + '"></span>' +
          '<div class="finding-body"><h4>' + x[2] + '</h4><p>' + x[3] + '</p>' +
          '<div class="evidence"><span class="val">' + x[4] + '</span>' +
          '<button class="copy" data-copy="' + esc(x[4]) + '" type="button">copy</button></div>' +
          '</div></div></div>';
      }).join("");
      resultBox.hidden = false;
      resultBox.innerHTML =
        '<div class="report-bar"><span class="dots"><i></i><i></i><i></i></span>' +
        '<span>demonstration · stored capture · not a live scan</span></div>' +
        '<div class="report-body">' +
        '<dl class="report-meta">' +
        '<div><dt>Target</dt><dd>' + f.target + ' - ' + f.targetDescription + '</dd></div>' +
        '<div><dt>Report</dt><dd>' + f.reportId + ' · ' + f.edition + '</dd></div>' +
        '<div><dt>Timestamp</dt><dd>' + f.timestamp + '</dd></div>' +
        '<div><dt>Consent receipt</dt><dd>' + f.consentId + ' · sha256 ' + f.receiptHash + '</dd></div>' +
        '<div><dt>Posture score</dt><dd>' + f.score + ' / 100 · Grade ' + f.grade + '</dd></div>' +
        '<div><dt>Controls assessed</dt><dd>' + f.controls + '</dd></div>' +
        '</dl>' +
        '<div class="alert alert-info" style="margin:1rem 0">' + DEMO_NOTE + '</div>' +
        '<div class="score-track"><div class="score-fill" style="width:' + f.score + '%"></div></div>' +
        '<div class="kpi-row">' + cats + '</div>' +
        '<div class="findings">' + rows + '</div>' +
        '<p class="faint" style="font-size:.8125rem;margin-top:1rem">Every line above quotes the observation ' +
        'the sandbox recorded. Run the tool on your own machine to reproduce it against a domain you are ' +
        'authorised to assess.</p>' +
        '</div>';
      $$("[data-copy]", resultBox).forEach(bindCopy);
    }

    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        hideError();
        resultBox.hidden = true;

        var problems = validate();
        fieldError(input, problems);
        if (!consent.checked) {
          var cWrap = consent.closest(".field");
          if (cWrap) {
            cWrap.classList.add("has-error");
            var cErr = $(".field-error", cWrap);
            if (!cErr) {
              cErr = document.createElement("p");
              cErr.className = "field-error";
              cErr.innerHTML = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="8.5" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="10" cy="14" r="0.9" fill="currentColor"/></svg>';
              cWrap.appendChild(cErr);
            }
            cErr.lastChild.textContent = "Read and accept the authorisation notice before continuing.";
          }
        } else {
          var cWrap2 = consent.closest(".field");
          if (cWrap2) { cWrap2.classList.remove("has-error"); var e2 = $(".field-error", cWrap2); if (e2) e2.remove(); }
        }
        if (problems.length) { showError(problems[0]); return; }

        var target = normalize(input.value);
        submitBtn.disabled = true;
        setState('<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="8.5" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="10" cy="14" r="0.9" fill="currentColor"/></svg><div><strong>Validating target…</strong><p>Checking the allowlist before any network request is made.</p></div>', "info");

        window.setTimeout(function () {
          setState('<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="8.5" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="10" cy="14" r="0.9" fill="currentColor"/></svg><div><strong>Allowlist check passed</strong><p>' + target + ' is an approved public test domain. Consent receipt is being signed.</p></div>', "info");
        }, 700);

        window.setTimeout(function () {
          setState('<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="8.5" stroke="currentColor" stroke-width="1.5" opacity="0.5"/><path d="M10 5.5v9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><div><strong>Assessment running (demonstration)</strong><p>This is illustrative output. The runnable sandbox performs the real read-only checks on your own machine.</p></div>', "info");
          if (progress) progress.hidden = false;
        }, 1400);

        window.setTimeout(function () {
          if (progress) progress.hidden = true;
          renderDemoResult();
          setState('<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 10.5l4 4 8-9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><div><strong>Demonstration report ready</strong><p>Signed consent receipt ' + DEMO_FIXTURE.consentId + ' · recorded locally by the sandbox, never uploaded. The result shown is the stored capture for example.com.</p></div>', "success");
          submitBtn.disabled = false;
        }, 2400);
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        form.reset();
        hideError();
        if (resultBox) { resultBox.hidden = true; resultBox.innerHTML = ""; }
        if (stateBox) { stateBox.hidden = true; stateBox.innerHTML = ""; }
        if (progress) progress.hidden = true;
        var wrap = input.closest(".field");
        if (wrap) { wrap.classList.remove("has-error"); var err = $(".field-error", wrap); if (err) err.remove(); }
        input.focus();
      });
    }

    $$("[data-demo-domain]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        input.value = btn.getAttribute("data-demo-domain");
        var wrap = input.closest(".field");
        if (wrap) { wrap.classList.remove("has-error"); var err = $(".field-error", wrap); if (err) err.remove(); }
        hideError();
        input.focus();
      });
    });
  }

  /* --------------------------------------------------------------------------
     Inline expansion for capability groups (progressive enhancement)
     -------------------------------------------------------------------------- */
  $$(".group-card summary").forEach(function (summary) {
    summary.addEventListener("click", function (e) {
      // Native <details> handles this; we only manage focus for keyboard users.
      if (e.detail === 0) {
        var details = summary.closest("details");
        window.setTimeout(function () {
          var first = $("a[href], button:not([disabled])", details.querySelector(".group-body"));
          if (first) first.focus();
        }, 30);
      }
    });
  });
})();
