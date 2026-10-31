/* ==========================================================================
   SMB Scanner Lite — site behaviour
   Dependency-free, progressive enhancement only. Every page is readable and
   every link works with JavaScript disabled; this file adds navigation,
   disclosure, tab and recorded-assessment behaviour on top.
   ========================================================================== */
(function () {
  "use strict";

  var CFG = window.SMB_CONFIG || {};
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  };
  var esc = function (value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  };

  /* ------------------------------------------------------------------------
     Toast
     ---------------------------------------------------------------------- */
  var toastRegion = $("#toastRegion");

  function toast(message, tone) {
    if (!toastRegion) return;
    var dotClass = tone === "success" ? "dot-pass" : tone === "error" ? "dot-fail" : "dot-info";
    var box = document.createElement("div");
    box.className = "toast";
    box.setAttribute("role", "status");
    box.innerHTML = '<span class="dot ' + dotClass + '"></span><span></span>';
    box.lastChild.textContent = message;
    toastRegion.appendChild(box);
    window.setTimeout(function () {
      box.classList.add("is-out");
      window.setTimeout(function () { box.remove(); }, 260);
    }, 3400);
  }

  /* ------------------------------------------------------------------------
     Clipboard
     ---------------------------------------------------------------------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.left = "-1000px";
      document.body.appendChild(area);
      area.select();
      try { document.execCommand("copy"); resolve(); }
      catch (err) { reject(err); }
      finally { area.remove(); }
    });
  }

  function bindCopy(root) {
    $$("[data-copy]", root).forEach(function (btn) {
      if (btn.dataset.bound === "1") return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", function () {
        var value = btn.getAttribute("data-copy") || "";
        copyText(value).then(function () {
          toast("Evidence copied to clipboard", "success");
        }).catch(function () {
          toast("Could not copy — select the text manually", "error");
        });
      });
    });
  }

  /* ------------------------------------------------------------------------
     Sticky navigation + mobile panel
     ------------------------------------------------------------------------
     The scrolled state used to be driven by a scroll listener that read
     window.scrollY on every event (Lighthouse attributed a forced reflow to
     that read). An 8px sentinel at the top of the document gives the same
     result from an IntersectionObserver, with no layout read in script and no
     work per scroll event. The scroll listener only remains as a fallback for
     browsers without IntersectionObserver, and it reads scroll position once
     per event and writes only when the state actually changes.
     ---------------------------------------------------------------------- */
  var nav = $(".nav");
  if (nav) {
    var navScrolled = false;
    var applyNavState = function (scrolled) {
      if (scrolled === navScrolled) return;
      navScrolled = scrolled;
      nav.classList.toggle("is-scrolled", scrolled);
    };

    if ("IntersectionObserver" in window) {
      var sentinel = document.createElement("div");
      sentinel.className = "scroll-sentinel";
      sentinel.setAttribute("aria-hidden", "true");
      document.body.insertBefore(sentinel, document.body.firstChild);
      new IntersectionObserver(function (entries) {
        applyNavState(!entries[entries.length - 1].isIntersecting);
      }, { threshold: 0 }).observe(sentinel);
    } else {
      var syncNav = function () {
        applyNavState(window.pageYOffset > 8);
      };
      syncNav();
      window.addEventListener("scroll", syncNav, { passive: true });
    }
  }

  var toggle = $("[data-nav-toggle]");
  var panel = $("[data-nav-panel]");
  var iconOpen = $("[data-nav-open]");
  var iconClose = $("[data-nav-close]");

  function setNav(open) {
    if (!toggle || !panel) return;
    panel.hidden = !open;
    panel.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("is-locked", open);
    if (iconOpen) iconOpen.hidden = open;
    if (iconClose) iconClose.hidden = !open;
    if (open) {
      var first = $("a, button", panel);
      if (first) first.focus();
    } else {
      toggle.focus();
    }
  }

  if (toggle && panel) {
    panel.hidden = true;
    toggle.addEventListener("click", function () {
      setNav(panel.hidden);
    });
    $$("a", panel).forEach(function (link) {
      link.addEventListener("click", function () { setNav(false); });
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !panel.hidden) setNav(false);
    });
    window.addEventListener("resize", function () {
      /* Test the cheap state first: when the panel is closed there is no need
         to read innerWidth (which can force a layout) at all. */
      if (!panel.hidden && window.innerWidth > 1080) setNav(false);
    });
  }

  /* ------------------------------------------------------------------------
     Scroll reveal
     ---------------------------------------------------------------------- */
  var reveals = $$(".reveal");
  if (!reveals.length) {
    /* nothing to do */
  } else if (reduced || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.1 });
    /* The stagger itself lives in CSS (`.reveal:nth-child(n)`); writing a
       custom property per element here meant hundreds of inline style writes
       before first paint. This loop now only registers observers. */
    reveals.forEach(function (el) { revealObserver.observe(el); });
  }

  /* ------------------------------------------------------------------------
     Tabs
     ---------------------------------------------------------------------- */
  $$("[data-tabs]").forEach(function (group) {
    var tabs = $$("[role='tab']", group);
    var panels = $$("[role='tabpanel']", group);
    if (!tabs.length) return;

    function activate(tab, moveFocus) {
      tabs.forEach(function (item) {
        var selected = item === tab;
        item.setAttribute("aria-selected", selected ? "true" : "false");
        item.tabIndex = selected ? 0 : -1;
      });
      panels.forEach(function (p) {
        var match = p.getAttribute("aria-labelledby") === tab.id;
        p.hidden = !match;
        p.classList.toggle("is-active", match);
      });
      if (moveFocus !== false) tab.focus();
    }

    tabs.forEach(function (tab, index) {
      tab.addEventListener("click", function () { activate(tab, false); });
      tab.addEventListener("keydown", function (event) {
        var next = null;
        if (event.key === "ArrowRight" || event.key === "ArrowDown") next = tabs[(index + 1) % tabs.length];
        if (event.key === "ArrowLeft" || event.key === "ArrowUp") next = tabs[(index - 1 + tabs.length) % tabs.length];
        if (event.key === "Home") next = tabs[0];
        if (event.key === "End") next = tabs[tabs.length - 1];
        if (next) {
          event.preventDefault();
          activate(next);
        }
      });
    });

    var initial = tabs.filter(function (t) { return t.getAttribute("aria-selected") === "true"; })[0] || tabs[0];
    activate(initial, false);
  });

  /* ------------------------------------------------------------------------
     Accordion groups: expand all / collapse all
     ---------------------------------------------------------------------- */
  $$("[data-acc-controls]").forEach(function (controls) {
    var target = $(controls.getAttribute("data-acc-controls"));
    if (!target) return;
    var details = $$("details", target);
    var openAll = $("[data-acc-open]", controls);
    var closeAll = $("[data-acc-close]", controls);
    if (openAll) openAll.addEventListener("click", function () {
      details.forEach(function (d) { d.open = true; });
    });
    if (closeAll) closeAll.addEventListener("click", function () {
      details.forEach(function (d) { d.open = false; });
    });
  });

  /* ------------------------------------------------------------------------
     Score, gauge and bar animation
     ---------------------------------------------------------------------- */
  function animateNumber(el, target, duration) {
    var start = null;
    function step(now) {
      if (start === null) start = now;
      var t = Math.min((now - start) / duration, 1);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = String(Math.round(target * eased));
      if (t < 1) window.requestAnimationFrame(step);
      else el.textContent = String(target);
    }
    window.requestAnimationFrame(step);
  }

  function paint(el) {
    var score = parseFloat(el.getAttribute("data-score")) || 0;
    var valueEl = $("[data-score-value]", el);
    var gauge = $("[data-gauge]", el);
    $$("[data-bar]", el).forEach(function (bar) {
      bar.style.width = (parseFloat(bar.getAttribute("data-bar")) || 0) + "%";
    });
    if (gauge) gauge.style.setProperty("--v", String(score));
    if (valueEl) {
      if (reduced) valueEl.textContent = String(Math.round(score));
      else animateNumber(valueEl, score, 900);
    }
  }

  $$("[data-score-card]").forEach(function (card) {
    if (reduced || !("IntersectionObserver" in window)) {
      paint(card);
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          paint(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.35 });
    observer.observe(card);
  });

  /* ------------------------------------------------------------------------
     Recorded assessment explorer
     ---------------------------------------------------------------------- */
  var demo = $("[data-demo]");

  if (demo) {
    var dataUrl = CFG.recordedDataUrl || "/data/recorded-assessment.json";
    var domainsBox = $("[data-demo-domains]", demo);
    var stageBox = $("[data-demo-stages]", demo);
    var progress = $("[data-demo-progress]", demo);
    var statusBox = $("[data-demo-status]", demo);
    var reportBox = $("[data-demo-report]", demo);
    var controlList = $("[data-demo-control-list]");
    var controlDetail = $("[data-demo-control-detail]");
    var allowlist = CFG.allowlist || [];
    var dataset = null;
    var currentTarget = null;
    var selectedControl = null;

    var STATUS_LABEL = { pass: "Pass", warning: "Warning", fail: "Fail", inconclusive: "Inconclusive" };

    function setStatus(html, tone) {
      if (!statusBox) return;
      statusBox.className = "form-status form-status--" + (tone || "warn");
      statusBox.innerHTML = html;
      statusBox.hidden = false;
    }

    function showStages(stageIndex) {
      if (!stageBox) return;
      var rows = $$("[data-stage]", stageBox);
      rows.forEach(function (row, index) {
        var complete = stageIndex >= rows.length;
        row.classList.toggle("is-active", index === stageIndex);
        row.classList.toggle("is-done", complete || index < stageIndex);
      });
      if (progress) {
        progress.style.width = Math.min(((stageIndex + 1) / 3) * 100, 100) + "%";
      }
    }

    function domainCard(record) {
      var label = record.source === "recorded" ? "Recorded capture" : "Reference profile";
      var when = record.source === "recorded" ? "28 Oct 2026" : "No dated capture";
      return (
        '<button class="domain-card" type="button" data-domain="' + esc(record.target) + '" aria-pressed="false">' +
        '<span class="dc-name">' + esc(record.target) + "</span>" +
        '<span class="dc-meta">' + esc(label) + " &middot; " + esc(when) + "</span>" +
        '<span class="dc-score">' + esc(record.score) + "/100 &middot; " + esc(record.grade) + "</span>" +
        "</button>"
      );
    }

    function renderMeta(record) {
      var rows = [
        ["Target", esc(record.target)],
        ["Source", esc(record.source_label)],
        ["Assessment timestamp", esc(record.timestamp_display)],
        ["Report ID", record.report_id ? '<span class="mono-inline">' + esc(record.report_id) + "</span>" : "Not issued for this profile"],
        ["Scanner version", "v" + esc(record.version) + " &middot; " + esc(record.edition)],
        ["Consent receipt", record.consent_id ? '<span class="mono-inline">' + esc(record.consent_id) + "</span>" : "Not recorded for this profile"]
      ];
      return '<dl class="meta-list">' + rows.map(function (row) {
        return "<div><dt>" + row[0] + "</dt><dd>" + row[1] + "</dd></div>";
      }).join("") + "</dl>";
    }

    function renderCategories(record) {
      return '<div class="bars">' + Object.keys(record.categories).map(function (name) {
        var value = record.categories[name];
        var cls = value >= 80 ? "" : value >= 65 ? " bar-fill--cyan" : " bar-fill--warn";
        return (
          '<div class="bar"><div class="bar-head"><span>' + esc(name) + "</span><b>" + value + '</b></div>' +
          '<div class="bar-track"><span class="bar-fill' + cls + '" style="width:' + value + '%"></span></div></div>'
        );
      }).join("") + "</div>";
    }

    function findingRow(finding) {
      var control = dataset.controls.filter(function (c) { return c.num === finding.control; })[0];
      var controlLabel = control ? "C" + (control.num < 10 ? "0" : "") + control.num + " &middot; " + esc(control.short) : "";
      var evidence = '<div class="evidence"><span class="val">' + esc(finding.evidence) + "</span>" +
        '<button class="copy" type="button" data-copy="' + esc(finding.evidence) + '">Copy</button></div>';
      var remediation = finding.remediation
        ? '<div class="remediation"><b>Recommended</b>' + esc(finding.remediation) + "</div>"
        : "";
      return (
        '<article class="finding" data-control="' + finding.control + '">' +
        '<div class="finding-head"><span class="dot dot-' +
        (finding.status === "pass" ? "pass" : finding.status === "fail" ? "fail" : finding.status === "warning" ? "warn" : "neutral") +
        '"></span><div class="finding-body">' +
        '<div class="finding-title"><h4>' + esc(finding.title) + "</h4>" +
        '<span class="status-badge status-' + esc(finding.status) + '">' + esc(STATUS_LABEL[finding.status] || finding.status) + "</span>" +
        (controlLabel ? '<span class="component-tag mono">' + controlLabel + "</span>" : "") +
        "</div><p>" + esc(finding.text) + "</p>" + evidence + remediation +
        "</div></div></article>"
      );
    }

    function renderReport(record) {
      if (!reportBox) return;
      reportBox.hidden = false;
      reportBox.innerHTML =
        '<div class="report-shell"><div class="window-bar"><span class="window-dots"><i></i><i></i><i></i></span>' +
        '<span class="mono">' + esc(record.source === "recorded" ? "recorded-assessment.json" : "reference-profile.json") + "</span>" +
        '<span class="window-label">' + esc(record.source_label) + "</span></div>" +
        '<div class="report-shell-body">' +
        '<div class="recorded-banner"><span class="dot"></span><span><b>Recorded</b> &mdash; stored output, not a live scan.</span>' +
        '<span>' + esc(record.timestamp_display) + "</span></div>" +
        '<div class="score-panel mt-3">' +
        '<div class="gauge" data-gauge style="--v:' + record.score + '"><div class="gauge-inner">' +
        '<span class="gauge-value" data-score-value>' + record.score + "</span>" +
        '<span class="gauge-label">Posture score</span>' +
        '<span class="gauge-grade">Grade ' + esc(record.grade) + " &middot; " + esc(record.grade_label) + "</span>" +
        "</div></div>" +
        '<div><h3 class="mt-0">' + esc(record.target) + "</h3>" +
        '<p class="muted small">' + esc(record.summary) + "</p>" + renderCategories(record) + "</div>" +
        "</div>" +
        '<div class="mt-3">' + renderMeta(record) + "</div>" +
        '<div class="mt-3"><h3 class="h-sm">Findings in this run</h3>' +
        '<p class="faint tiny">' + record.counts.completed + " controls completed &middot; " + record.counts.inconclusive + " inconclusive. The public sandbox evaluates a read-only subset of the 22-control catalog.</p>" +
        '<div class="findings mt-2" data-findings>' + record.findings.map(findingRow).join("") + "</div></div>" +
        "</div></div>";
      bindCopy(reportBox);
    }

    function renderControlDetail(num) {
      if (!controlDetail || !dataset) return;
      var control = dataset.controls.filter(function (c) { return c.num === num; })[0];
      if (!control) return;
      selectedControl = num;
      if (controlList) $$("[data-control-num]", controlList).forEach(function (btn) {
        btn.setAttribute("aria-pressed", Number(btn.getAttribute("data-control-num")) === num ? "true" : "false");
      });
      var record = dataset.domains[currentTarget];
      var finding = record.findings.filter(function (f) { return f.control === num; })[0];
      var runStatus = finding
        ? '<span class="status-badge status-' + esc(finding.status) + '">' + esc(STATUS_LABEL[finding.status]) + "</span>"
        : '<span class="status-badge status-inconclusive">Not in this run</span>';
      var evidenceBlock = finding
        ? '<div class="evidence"><span class="val">' + esc(finding.evidence) + "</span>" +
          '<button class="copy" type="button" data-copy="' + esc(finding.evidence) + '">Copy</button></div>'
        : '<p class="faint small">This control is part of the full 22-control engine. The public sandbox executes a read-only subset, and this control was not part of the ' +
          (record.source === "recorded" ? "recorded run" : "reference profile") + ".</p>";
      controlDetail.innerHTML =
        '<div class="row" style="justify-content:space-between">' +
        '<span class="mono faint">C' + (control.num < 10 ? "0" : "") + control.num + " &middot; " + esc(control.category_name) + "</span>" + runStatus + "</div>" +
        "<h4>" + esc(control.name) + "</h4>" +
        "<p class=\"muted small\">" + esc(control.summary) + "</p>" +
        "<dl><div><dt>What it evaluates</dt><dd>" + esc(control.evaluates) + "</dd></div>" +
        "<div><dt>Why it matters</dt><dd>" + esc(control.why) + "</dd></div>" +
        "<div><dt>Evidence in this " + (record.source === "recorded" ? "recorded run" : "reference profile") + "</dt><dd>" + evidenceBlock + "</dd></div></dl>";
      bindCopy(controlDetail);
    }

    function renderControls() {
      if (!controlList || !dataset) return;
      controlList.innerHTML = dataset.controls.map(function (control) {
        return (
          '<button type="button" data-control-num="' + control.num + '" aria-pressed="false">' +
          '<span class="cl-num">C' + (control.num < 10 ? "0" : "") + control.num + "</span>" +
          "<span>" + esc(control.name) + "</span></button>"
        );
      }).join("");
      $$("[data-control-num]", controlList).forEach(function (btn) {
        btn.addEventListener("click", function () {
          renderControlDetail(Number(btn.getAttribute("data-control-num")));
        });
      });
    }

    function selectDomain(target) {
      if (!dataset || !dataset.domains[target]) return;
      if (allowlist.length && allowlist.indexOf(target) === -1) {
        setStatus("<strong>Target not permitted.</strong><p>" + esc(target) + " is not one of the five approved demonstration domains. The public edition accepts example.com, example.org, example.net, scanme.nmap.org and badssl.com only.</p>", "err");
        return;
      }
      currentTarget = target;
      if (statusBox) statusBox.hidden = true;
      $$("[data-domain]", domainsBox).forEach(function (btn) {
        btn.setAttribute("aria-pressed", btn.getAttribute("data-domain") === target ? "true" : "false");
      });

      var steps = 3;
      var delay = reduced ? 0 : 320;
      var index = 0;

      function advance() {
        showStages(index);
        if (index < steps - 1) {
          index += 1;
          window.setTimeout(advance, delay);
        } else {
          window.setTimeout(function () {
            showStages(steps + 1);
            renderReport(dataset.domains[target]);
            renderControlDetail(dataset.domains[target].findings[0].control);
          }, delay);
        }
      }

      if (reportBox) reportBox.hidden = true;
      advance();
    }

    fetch(dataUrl, { cache: "no-cache" })
      .then(function (response) {
        if (!response.ok) throw new Error("HTTP " + response.status);
        return response.json();
      })
      .then(function (json) {
        dataset = json;
        if (domainsBox) {
          domainsBox.innerHTML = Object.keys(json.domains).map(function (key) {
            return domainCard(json.domains[key]);
          }).join("");
          $$("[data-domain]", domainsBox).forEach(function (btn) {
            btn.addEventListener("click", function () {
              selectDomain(btn.getAttribute("data-domain"));
            });
          });
        }
        renderControls();
        selectDomain(json.default || "example.com");
      })
      .catch(function () {
        setStatus(
          "<strong>The recorded data could not be loaded.</strong><p>This is usually a temporary network or hosting issue. The same assessment is published as a static page in the <a href=\"/sample-report/\">sample report</a>, and the raw data is available at <a href=\"/data/recorded-assessment.json\">/data/recorded-assessment.json</a>.</p>",
          "err"
        );
        if (progress) progress.style.width = "0%";
      });
  }

  /* ------------------------------------------------------------------------
     Enquiry forms
     ---------------------------------------------------------------------- */
  var REGISTRY_KEY = "smb-enquiry-last-sent";
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;

  function fieldWrap(el) {
    return el.closest(".field");
  }

  function setFieldError(el, message) {
    var wrap = fieldWrap(el);
    if (!wrap) return;
    wrap.classList.add("has-error");
    el.setAttribute("aria-invalid", "true");
    el.setAttribute("aria-describedby", "err-" + el.name);
    var err = wrap.querySelector(".field-error");
    if (!err) {
      err = document.createElement("p");
      err.className = "field-error";
      err.id = "err-" + el.name;
      err.innerHTML = '<svg viewBox="0 0 20 20" width="14" height="14" fill="none" aria-hidden="true" stroke="currentColor" stroke-width="1.5"><circle cx="10" cy="10" r="8.5"/><path d="M10 6v5"/><circle cx="10" cy="14" r="0.9" fill="currentColor" stroke="none"/></svg><span></span>';
      wrap.appendChild(err);
    }
    err.lastChild.textContent = message;
  }

  function clearFieldError(el) {
    var wrap = fieldWrap(el);
    if (!wrap) return;
    wrap.classList.remove("has-error");
    el.removeAttribute("aria-invalid");
    el.removeAttribute("aria-describedby");
    var err = wrap.querySelector(".field-error");
    if (err) err.remove();
  }

  function buildMailto(payload) {
    var email = CFG.contactEmail || "";
    var subject = "[" + payload.enquiryType + "] " + (payload.company || payload.name || "Website enquiry");
    var lines = [
      "Name: " + payload.name,
      "Email: " + payload.email
    ];
    if (payload.company) lines.push("Company: " + payload.company);
    if (payload.domain) lines.push("Domain: " + payload.domain);
    lines.push("Enquiry type: " + payload.enquiryType);
    lines.push("Submitted from: " + window.location.href);
    if (payload.authorised) lines.push("Authorisation: " + payload.authorised);
    lines.push("", "Message:", payload.message);
    var body = lines.join("\n").slice(0, 1800);
    return "mailto:" + encodeURIComponent(email) + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
  }

  function validateForm(form) {
    var problems = [];
    var required = $$("[data-required]", form);
    required.forEach(function (el) {
      var value = (el.type === "checkbox" ? (el.checked ? "yes" : "") : el.value).trim();
      if (!value) {
        var label = el.getAttribute("data-label") || el.name;
        setFieldError(el, label + " is required.");
        problems.push(el);
        return;
      }
      clearFieldError(el);
      if (el.type === "email" && !EMAIL_RE.test(value)) {
        setFieldError(el, "Enter a valid email address, for example name@company.com.");
        problems.push(el);
      }
    });
    var message = form.querySelector("[name='message']");
    if (message && message.value.trim().length > 0 && message.value.trim().length < 20) {
      setFieldError(message, "Please add a little more detail (at least 20 characters).");
      problems.push(message);
    }
    return problems;
  }

  $$("form[data-enquiry-form]").forEach(function (form) {
    var status = $("[data-form-status]", form);
    var submit = $("[type='submit']", form);
    var renderedAt = Date.now();

    $$("input, textarea, select", form).forEach(function (el) {
      el.addEventListener("input", function () { clearFieldError(el); });
      el.addEventListener("change", function () { clearFieldError(el); });
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (status) { status.hidden = true; status.innerHTML = ""; }

      var honeypot = form.querySelector("[name='_gotcha']");
      if (honeypot && honeypot.value) return; /* silently drop bots */

      var last = Number(window.localStorage.getItem(REGISTRY_KEY) || 0);
      if (Date.now() - last < 45000) {
        if (status) {
          status.hidden = false;
          status.className = "form-status form-status--warn";
          status.innerHTML = "<strong>Please wait a moment.</strong><p>An enquiry was already sent from this browser in the last minute. If it did not arrive, use the direct email address below.</p>";
        }
        return;
      }

      var problems = validateForm(form);
      if (problems.length) {
        problems[0].focus();
        if (status) {
          status.hidden = false;
          status.className = "form-status form-status--err";
          status.innerHTML = "<strong>Check the highlighted fields.</strong><p>" + problems.length + " field" + (problems.length > 1 ? "s need" : " needs") + " attention before this can be sent.</p>";
        }
        return;
      }

      if (Date.now() - renderedAt < 1500) {
        if (status) {
          status.hidden = false;
          status.className = "form-status form-status--warn";
          status.innerHTML = "<strong>Just a moment.</strong><p>Please take a second to review your message, then submit again.</p>";
        }
        return;
      }

      // "authorised" is a yes/no select on the contact form and a required
      // confirmation checkbox on the assessment form. Normalise both to yes/no
      // so the delivered enquiry always states the answer explicitly.
      var authEl = form.querySelector("[name='authorised']");
      var authorised = "not answered";
      if (authEl) {
        if (authEl.type === "checkbox") {
          authorised = authEl.checked ? "yes" : "no";
        } else {
          authorised = String(authEl.value || "no").toLowerCase() === "yes" ? "yes" : "no";
        }
      }

      function fieldValue(name) {
        var el = form.querySelector("[name='" + name + "']");
        return el ? String(el.value || "").trim() : "";
      }

      var payload = {
        kind: form.getAttribute("data-form-kind") || "enquiry",
        name: fieldValue("name"),
        email: fieldValue("email"),
        company: fieldValue("company"),
        domain: fieldValue("domain"),
        enquiryType: fieldValue("enquiryType") || "General enquiry",
        message: fieldValue("message"),
        authorised: authorised,
        page: window.location.pathname
      };

      function success(source) {
        window.localStorage.setItem(REGISTRY_KEY, String(Date.now()));
        if (submit) { submit.disabled = false; submit.removeAttribute("aria-busy"); }
        form.reset();
        if (status) {
          status.hidden = false;
          status.className = "form-status form-status--ok";
          status.innerHTML =
            "<strong>Thank you — your enquiry is ready to send.</strong>" +
            "<p>" + (source === "endpoint"
              ? "It has been delivered. You will receive a reply at " + esc(payload.email) + " once it has been reviewed."
              : "Your mail application should have opened with the enquiry filled in. Press send there to complete the handover — nothing is stored on this website.") +
            "</p><p class=\"tiny\">Prefer email? Write directly to <a href=\"mailto:" + esc(CFG.contactEmail) + "\">" + esc(CFG.contactEmail) + "</a>. Assessment requests are reviewed manually; nothing is scanned automatically.</p>";
          if (typeof status.scrollIntoView === "function") {
            status.scrollIntoView({ block: "nearest", behavior: reduced ? "auto" : "smooth" });
          }
        }
      }

      if (CFG.formEndpoint) {
        if (submit) { submit.disabled = true; submit.setAttribute("aria-busy", "true"); }
        if (status) {
          status.hidden = false;
          status.className = "form-status form-status--warn";
          status.innerHTML = "<strong>Sending…</strong><p>Please wait while the enquiry is delivered.</p>";
        }
        fetch(CFG.formEndpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(payload)
        })
          .then(function (response) {
            if (!response.ok) throw new Error("HTTP " + response.status);
            success("endpoint");
          })
          .catch(function () {
            if (submit) { submit.disabled = false; submit.removeAttribute("aria-busy"); }
            window.location.href = buildMailto(payload);
            success("mailto");
          });
      } else {
        window.location.href = buildMailto(payload);
        success("mailto");
      }
    });
  });

  /* ------------------------------------------------------------------------
     Page furniture
     ---------------------------------------------------------------------- */
  $$("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  bindCopy(document);
})();
