/* SMB Scanner Lite Phase 4: private assessment portal.
   No dependencies, no third-party scripts, no credentials in URLs or localStorage.
   Tests import the network client without invoking the DOM. */
export class ScanAPIError extends Error {
  constructor(status, message) {
    super(message || "Assessment request failed");
    this.name = "ScanAPIError";
    this.status = status;
  }
}

export function checkedOrigin(value) {
  if (typeof value !== "string" || !value.trim()) throw new Error("API origin is not configured");
  const input = value.trim();
  let url;
  try { url = new URL(input); } catch { throw new Error("Invalid backend origin"); }
  if (url.protocol !== "https:" || !url.hostname || url.username || url.password ||
      url.port || url.pathname !== "/" || url.search || url.hash) {
    throw new Error("Backend must be an HTTPS origin without a path, port or credentials");
  }
  return url.origin;
}

function idValue(value) {
  if (typeof value !== "string" ||
      !/^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$/.test(value)) {
    throw new Error("Invalid assessment ID");
  }
  return value;
}
function tokenValue(value) {
  if (typeof value !== "string" || !/^[a-f0-9]{64}$/.test(value)) {
    throw new Error("Invalid private access token");
  }
  return value;
}
export function makeScanClient(apiBase, fetchImpl = fetch) {
  const origin = checkedOrigin(apiBase);
  async function call(method, path, token, payload) {
    const headers = { Accept: "application/json" };
    if (token !== undefined && token !== null) headers.Authorization = "Bearer " + tokenValue(token);
    if (payload !== undefined) headers["Content-Type"] = "application/json";
    let response;
    try {
      response = await fetchImpl(origin + path, {
        method, headers, ...(payload === undefined ? {} : { body: JSON.stringify(payload) }),
        credentials: "omit", redirect: "error", referrerPolicy: "no-referrer",
        cache: "no-store", signal: AbortSignal.timeout(12000),
      });
    } catch {
      // Network timeouts during dispatch are ambiguous. Never retry the POST.
      throw new ScanAPIError(0, "Connection interrupted. Check assessment status before trying anything again.");
    }
    let body;
    try { body = await response.json(); }
    catch { throw new ScanAPIError(response.status, "Server returned an unexpected response."); }
    if (!response.ok) {
      throw new ScanAPIError(response.status,
        typeof body.error === "string" ? body.error.slice(0, 180) : "Request was rejected.");
    }
    return body;
  }
  const path = id => "/api/v1/assessments/" + idValue(id);
  return Object.freeze({
    create: ({name,email,domain}) => call("POST", "/api/v1/assessments", null, {name,email,domain}),
    verify: (id,token) => call("POST", path(id) + "/verify", token),
    dispatch: (id,token) => call("POST", path(id) + "/scan", token),
    status: (id,token) => call("GET", path(id), token),
    preview: (id,token) => call("GET", path(id) + "/preview", token),
    checkout: (id,token) => call("POST", path(id) + "/checkout", token),
    report: (id,token) => call("GET", path(id) + "/report", token),
  });
}


/** Send only public contact metadata to Formspree. DNS ownership and scan
 * authorization are always checked separately by the private backend. */
export function checkedFormEndpoint(value) {
  if (typeof value !== "string" || !/^https:\/\/formspree\.io\/f\/[a-z0-9]{8,}$/i.test(value.trim())) {
    throw new Error("Form notification is not configured");
  }
  return value.trim();
}
export async function notifyRequest(endpoint, input, fetchImpl = fetch) {
  const tier = ["basic","regular","deep"].includes(input.tier) ? input.tier : "basic";
  const payload = {
    kind:"assessment-tier-enquiry",
    name:String(input.name || "").slice(0,100),
    email:String(input.email || "").slice(0,254),
    domain:String(input.domain || "").slice(0,253),
    tier,
    authorised:input.authorised===true ? "yes" : "no",
    page:"/scan/",
    note:tier==="basic" ? "Basic DNS/email enquiry; verified ownership required." :
      "Manually scoped assessment enquiry. No scan or payment initiated.",
  };
  const response=await fetchImpl(checkedFormEndpoint(endpoint),{
    method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},
    body:JSON.stringify(payload),credentials:"omit",redirect:"error",
    referrerPolicy:"no-referrer",cache:"no-store",signal:AbortSignal.timeout(9000),
  });
  if(!response.ok) throw new Error("Team notification could not be delivered");
  return true;
}
export const SCAN_STATUSES=Object.freeze({
  awaiting_verification:"Waiting for DNS TXT ownership proof",
  verified:"Ownership verified. Ready for one authorized scan",
  dispatching:"Securely contacting the remote worker",
  queued:"Request accepted. Waiting for an available worker",
  running:"Worker active. Reviewing public DNS and email policy",
  dispatch_unknown:"Dispatch uncertain. Operator review required",
  dispatch_failed:"The worker rejected the launch",
  failed:"Assessment could not finish",
  completed:"Assessment complete. Your score and findings are ready",
});
const BUSY_STATES=new Set(["dispatching","queued","running"]);
export function checkedCheckoutUrl(value) {
  let url;
  try { url=new URL(value); } catch { throw new Error("Invalid secure checkout destination"); }
  if(url.protocol!=="https:" || url.hostname!=="checkout.stripe.com" ||
     url.username || url.password || url.port || url.hash) {
    throw new Error("Unexpected checkout destination");
  }
  return url.href;
}

const STORE_KEY = "smbscanner.saas.session.v1";

export function parseSession(value) {
  try {
    const record = typeof value === "string" ? JSON.parse(value) : value;
    if (!record || typeof record !== "object") return null;
    return {
      id: idValue(record.id),
      token: tokenValue(record.token),
      domain: typeof record.domain === "string" ? record.domain.slice(0, 253) : "",
      recordName: typeof record.recordName === "string" ? record.recordName.slice(0, 300) : "",
      recordValue: typeof record.recordValue === "string" ? record.recordValue.slice(0, 300) : "",
      launchAuthorized: record.launchAuthorized === true,
    };
  } catch { return null; }
}

function startPortal() {
  const root = document.querySelector("[data-saas-portal]");
  if (!root) return;
  const $ = selector => root.querySelector(selector);
  const cfg = window.SMB_CONFIG?.saas || {};
  const active = cfg.enabled === true && Boolean(cfg.apiBaseUrl);
  const banner = $("#scan-message");
  const showMessage = (message,tone="info") => {
    banner.hidden = false;
    banner.dataset.tone = tone;
    banner.textContent = message;
  };
  const step = (id, visible = true) => { const x=$(id); if(x) x.hidden = !visible; };
  const text = (id,value) => {const x=$(id);if(x) x.textContent = String(value ?? "");};
  const busy = (button,value) => {
    button.disabled = value;
    button.setAttribute("aria-busy", String(value));
  };
  let client = null;
  if (active) {
    try { client = makeScanClient(cfg.apiBaseUrl); }
    catch { showMessage("Online configuration is incomplete. Enquiries remain available.","error"); }
  }
  if (!client) {
    step("#scan-create",true);step("#scan-closed",true);step("#scan-resume",false);
    showMessage("Live scans are not accepting public jobs yet. Choose a tier to send an enquiry. No scan or payment will start.");
  }
  let session = null, pollTimer = null, dispatchPending = false;
  let evidence = null, paymentPolls = 0;
  const checkoutResult = new URL(window.location.href).searchParams.get("checkout");
  const stopPolling = () => { if(pollTimer) clearTimeout(pollTimer); pollTimer=null; };
  const save = value => {
    session = value;
    try { window.sessionStorage.setItem(STORE_KEY,JSON.stringify(value)); } catch { /* private mode */ }
  };
  const discard = () => {
    stopPolling(); session = null; evidence=null; paymentPolls=0;
    try { window.sessionStorage.removeItem(STORE_KEY); } catch { /* private mode */ }
  };
  function showCreated() {
    if (!session) return;
    step("#scan-create",false);
    step("#scan-resume",false);
    step("#scan-closed",false);
    step("#scan-verify",true);
    step("#scan-status",true);
    text("#scan-domain",session.domain);
    text("#scan-record-name",session.recordName);
    text("#scan-record-value",session.recordValue);
    text("#scan-recovery-id",session.id);
    text("#scan-recovery-token",session.token);
    showMessage("Publish the TXT record at your DNS provider. Keep your private access token safe; it is needed to recover the assessment.", "info");
  }
  function drawPreview(data) {
    step("#scan-preview",true);
    text("#scan-preview-domain",data.domain);
    text("#scan-preview-grade",data.grade ?? "—");
    text("#scan-preview-score",Number.isFinite(data.score) ? data.score + "/100" : "Not available");
    text("#scan-preview-confidence",data.confidence ?? "Limited evidence");
    text("#scan-preview-controls",Number.isInteger(data.conclusive_controls)&&Number.isInteger(data.total_controls) ?
      data.conclusive_controls+" of "+data.total_controls+" controls conclusive" : "Public DNS/email profile only");
    const list = $("#scan-findings");
    list.replaceChildren();
    for (const entry of Array.isArray(data.top_findings) ? data.top_findings.slice(0,3) : []) {
      const item=document.createElement("li");
      item.className="scan-finding";
      const title=document.createElement("strong");
      title.textContent=String(entry.title || entry.control || "Finding");
      const detail=document.createElement("span");
      detail.textContent=String(entry.status || "WARNING") + " · " + String(entry.severity || "Unspecified");
      item.append(title,detail);
      list.appendChild(item);
    }
    text("#scan-report-notice","The preview is free. The complete DNS/email evidence report is available with one verified $19 payment.");
  }
  function renderPaywall(state) {
    step("#scan-paywall",!state.report_unlocked);
    const pay=$("#scan-pay-button");
    if(pay) pay.disabled=state.checkout_available!==true;
    text("#scan-pay-status",state.checkout_available===true
      ? "Pay $19 securely through Stripe. Your full evidence report unlocks only after the payment is verified."
      : "Secure checkout is not active yet. Your free preview remains available; no payment can be taken here.");
    root.querySelectorAll("[data-scan-stage]").forEach(el=>{
      const i=Number(el.dataset.scanStage);
      el.classList.toggle("is-active",i===4);
      el.classList.toggle("is-done",i<4);
    });
  }
  function drawFullReport(payload) {
    if(!payload || !payload.report || !Array.isArray(payload.report.results)) {
      throw new Error("The server returned an invalid evidence report");
    }
    evidence=payload.report;
    step("#scan-paywall",false);
    step("#scan-unlocked",true);
    text("#scan-full-domain",String(evidence.target || session?.domain || ""));
    text("#scan-full-id",String(evidence.report_id || "Not supplied"));
    const parent=$("#scan-full-findings");
    parent.replaceChildren();
    for(const entry of evidence.results) {
      const item=document.createElement("details");
      item.className="scan-evidence";
      const summary=document.createElement("summary");
      const heading=document.createElement("strong");
      heading.textContent=String(entry.title || entry.control || "Security control");
      const status=document.createElement("span");
      status.textContent=[entry.status || "UNSPECIFIED",entry.severity || ""].filter(Boolean).join(" · ");
      summary.append(heading,status);
      const body=document.createElement("div");
      body.className="scan-evidence-body";
      const desc=document.createElement("p");
      desc.textContent=String(entry.description || entry.explanation || entry.summary || "Recorded finding");
      const pre=document.createElement("pre");
      pre.textContent=typeof entry.evidence==="string" ? entry.evidence :
        JSON.stringify(entry.evidence ?? entry,null,2);
      body.append(desc,pre);item.append(summary,body);parent.appendChild(item);
    }
    if(!evidence.results.length) {
      const notice=document.createElement("p");
      notice.textContent="No individual control results were returned.";
      parent.appendChild(notice);
    }
    const dl=$("#scan-download-report");
    if(dl) dl.disabled=false;
    root.querySelectorAll("[data-scan-stage]").forEach(el=>{
      const i=Number(el.dataset.scanStage);
      el.classList.toggle("is-active",i===5);
      el.classList.toggle("is-done",i<5);
    });
  }
  async function receiveReport() {
    if(!session || !client || evidence) return;
    const payload=await client.report(session.id,session.token);
    drawFullReport(payload);
  }
  function statusView(status) {
    const message=SCAN_STATUSES[status] || "Waiting for a server status update";
    text("#scan-state",String(status || "unknown").replaceAll("_"," "));
    text("#scan-progress-label",message);
    text("#scan-activity",message);
    step("#scan-running",BUSY_STATES.has(status));
    const stage=status==="completed" ? 3 :
      BUSY_STATES.has(status) || ["failed","dispatch_failed","dispatch_unknown"].includes(status) ? 2 :
      status==="verified" ? 1 : 0;
    root.querySelectorAll("[data-scan-stage]").forEach(el=>{
      const pos=Number(el.dataset.scanStage);
      el.classList.toggle("is-active",pos===stage);
      el.classList.toggle("is-done",pos<stage);
    });
  }
  function schedulePoll() {
    stopPolling();
    if(!session) return;
    pollTimer=setTimeout(async()=>{
      try { await refresh(); }
      catch {
        stopPolling();
        showMessage("Status updates are temporarily unavailable. Use Refresh status; your scan was not restarted.","error");
      }
    },6000);
  }
  async function refresh() {
    if(!session || !client) return;
    const state=await client.status(session.id,session.token);
    step("#scan-status",true);
    statusView(state.status);
    if(state.status==="verified") {
      step("#scan-verify",false);
      step("#scan-dispatch",true);
      showMessage("Ownership verified. A single authorized DNS/email scan is ready.","success");
    } else if(BUSY_STATES.has(state.status)) {
      step("#scan-verify",false);step("#scan-dispatch",false);
      showMessage("Remote workflow active. Its actual status refreshes automatically.");
      schedulePoll();
    } else if(state.status==="dispatch_unknown") {
      stopPolling();step("#scan-verify",false);step("#scan-dispatch",false);
      showMessage("Dispatch outcome is unknown. Do not restart; contact support with your assessment ID.","error");
    } else if(state.status==="completed") {
      stopPolling();step("#scan-verify",false);step("#scan-dispatch",false);
      const data=await client.preview(session.id,session.token);
      drawPreview(data);
      if(state.report_unlocked===true) {
        step("#scan-paywall",false);
        try {
          await receiveReport();
          showMessage("Payment verified. The complete evidence report is unlocked below.","success");
        } catch {
          showMessage("Payment is recorded, but the report could not be loaded. Use Refresh status.","error");
        }
      } else {
        renderPaywall(state);
        if(checkoutResult==="success") {
          if(paymentPolls<10) {
            paymentPolls++;
            showMessage("Returned from checkout. Waiting for the payment provider to confirm your purchase; no report is unlocked yet.");
            schedulePoll();
          } else {
            showMessage("Payment has not yet been confirmed. Use Refresh status or contact support before paying again.");
          }
        } else if(checkoutResult==="cancelled") {
          showMessage("Checkout was cancelled. Your free preview is unchanged.");
        } else {
          showMessage("Assessment complete. View the free preview or unlock full evidence for $19.","success");
        }
      }
    } else if(["failed","dispatch_failed"].includes(state.status)) {
      stopPolling();step("#scan-verify",false);step("#scan-dispatch",false);
      showMessage("The assessment could not finish. No repeat scan was started.","error");
    } else {
      step("#scan-verify",true);
    }
  }
  async function startOneScan(button) {
    if(!session || !client || dispatchPending) return;
    dispatchPending=true;busy(button,true);
    try {
      showMessage("Ownership confirmed. Requesting a single remote DNS/email assessment…");
      const result=await client.dispatch(session.id,session.token);
      step("#scan-dispatch",false);
      statusView(result.status || "queued");
      showMessage("Remote assessment requested. Progress updates will appear automatically.","success");
      schedulePoll();
    } catch(e) {
      showMessage(e instanceof ScanAPIError ? e.message :
        "Launch could not be confirmed. Refresh status; never start twice.","error");
      try { await refresh(); } catch { /* status may be unavailable */ }
    } finally {dispatchPending=false;busy(button,false)}
  }
  function selectedTier() {
    return root.querySelector('input[name="tier"]:checked')?.value || "basic";
  }
  function updateTier() {
    const tier = selectedTier();
    root.querySelectorAll(".scan-tier").forEach(card =>
      card.classList.toggle("is-selected",card.querySelector("input")?.checked===true));
    text("#scan-submit-label",client && tier==="basic" ?
      "Create ownership verification" : "Send assessment enquiry");
    step("#scan-tier-disclosure",tier!=="basic");
  }
  root.querySelectorAll('input[name="tier"]').forEach(el=>el.addEventListener("change",updateTier));
  updateTier();
  $("#scan-request-form").addEventListener("submit",async event=>{
    event.preventDefault();
    const form=event.currentTarget;
    if(!$("#scan-consent").checked) {
      showMessage("Confirm domain ownership or explicit written authorization first.","error"); return;
    }
    const button=form.querySelector('button[type="submit"]');
    busy(button,true);
    const payload={
      name:form.elements.namedItem("name").value.trim(),
      email:form.elements.namedItem("email").value.trim(),
      domain:form.elements.namedItem("domain").value.trim(),
      tier:selectedTier(),authorised:true,
    };
    let notified=false;
    try {
      try { notified=await notifyRequest(window.SMB_CONFIG?.formEndpoint,payload); }
      catch { notified=false; }
      if(!client || payload.tier!=="basic") {
        if(notified) {
          form.reset(); updateTier();
          showMessage("Enquiry delivered. Scope, final pricing and authorization will be agreed before work. No scan has started.","success");
        } else {
          showMessage("Formspree could not deliver the enquiry. Use the Contact page. No scan has started.","error");
        }
        return;
      }
      const result=await client.create(payload);
      const next=parseSession({
        id:result.assessment_id,token:result.access_token,
        domain:result.domain,recordName:result.dns_record_name,
        recordValue:result.dns_record_value,launchAuthorized:true,
      });
      if(!next || !next.recordName || !next.recordValue) throw new Error("Invalid server response");
      save(next); showCreated();statusView("awaiting_verification");
      if(!notified) showMessage("Verification created, but team notification is unavailable. Keep the token private.");
    } catch(e) {
      showMessage(e instanceof ScanAPIError ? e.message :
        "Could not create verification. Please use the Contact page.","error");
    } finally {busy(button,false)}
  });
  $("#scan-verify-button").addEventListener("click",async event=>{
    if(!session || !client) return;
    const button=event.currentTarget;busy(button,true);
    try {
      await client.verify(session.id,session.token);
      statusView("verified");
      step("#scan-verify",false);
      if(session.launchAuthorized) {
        // Intake explicitly authorized one DNS/email scan after TXT proof.
        await startOneScan($("#scan-dispatch-button"));
      } else {
        // Resumed legacy sessions require a second explicit scan consent.
        await refresh();
      }
    } catch(e) {
      showMessage(e instanceof ScanAPIError ? e.message : "Could not verify DNS ownership.","error");
    } finally {busy(button,false)}
  });
  $("#scan-dispatch-button").addEventListener("click",async event=>{
    if(!$("#scan-dispatch-consent").checked) {
      showMessage("Confirm explicit authorization for this exact DNS/email assessment.","error");
      return;
    }
    await startOneScan(event.currentTarget);
  });
  $("#scan-refresh-button").addEventListener("click",async event=>{
    const button=event.currentTarget;busy(button,true);
    try {await refresh()}
    catch(e) {showMessage(e instanceof ScanAPIError ? e.message : "Could not load status.","error")}
    finally {busy(button,false)}
  });
  $("#scan-resume-form").addEventListener("submit",async event=>{
    event.preventDefault();
    const form=event.currentTarget;
    const next=parseSession({id:form.elements.namedItem("assessmentId").value.trim(),
      token:form.elements.namedItem("accessToken").value.trim()});
    if (!next) {showMessage("Enter a valid assessment ID and private access token.","error");return}
    save(next);
    step("#scan-create",false);
    step("#scan-resume",false);
    try {await refresh()}
    catch {
      discard();
      step("#scan-create",true);step("#scan-resume",true);
      showMessage("Could not resume. Check your assessment ID and private token.", "error");
    }
  });
  $("#scan-new-button").addEventListener("click",()=>{
    discard();step("#scan-create",true);step("#scan-verify",false);step("#scan-status",false);
    step("#scan-dispatch",false);step("#scan-preview",false);step("#scan-resume",true);
    step("#scan-running",false);step("#scan-closed",!client);step("#scan-resume",Boolean(client));
    step("#scan-paywall",false);step("#scan-unlocked",false);step("#scan-preview",false);
    showMessage("Session cleared from this tab. The server-side assessment was not deleted.");
  });
  $("#scan-copy-token").addEventListener("click",async()=>{
    if(!session) return;
    try {
      await navigator.clipboard.writeText(session.token);
      showMessage("Private token copied. Keep it secure and do not share it in chat.", "success");
    } catch { showMessage("Select and copy the private token manually.", "info"); }
  });
  $("#scan-pay-button")?.addEventListener("click",async event=>{
    if(!session || !client) return;
    const button=event.currentTarget;
    busy(button,true);
    try {
      const outcome=await client.checkout(session.id,session.token);
      if(outcome.unlocked===true) {
        await refresh();
      } else {
        const destination=checkedCheckoutUrl(outcome.checkout_url);
        // Never place assessment IDs, owner tokens, reports or PII into a URL.
        window.location.assign(destination);
      }
    } catch(e) {
      showMessage(e instanceof ScanAPIError ? e.message :
        "Secure checkout could not be opened. Please refresh status or contact support.","error");
    } finally { busy(button,false); }
  });
  $("#scan-download-report")?.addEventListener("click",()=>{
    if(!evidence) return;
    const blob=new Blob([JSON.stringify(evidence,null,2)],{type:"application/json"});
    const url=URL.createObjectURL(blob);
    const anchor=document.createElement("a");
    anchor.href=url;
    const safeDomain=String(evidence.target || "domain").replace(/[^a-z0-9.-]/gi,"-");
    anchor.download="smbscanner-evidence-"+safeDomain+".json";
    document.body.appendChild(anchor);anchor.click();anchor.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1500);
  });
  if(client) {
    try { session=parseSession(window.sessionStorage.getItem(STORE_KEY)); } catch { session=null; }
    if(session){
      showCreated();
      refresh().catch(()=>showMessage("Automatic refresh unavailable. Use Refresh status.","error"));
    } else {
      step("#scan-create",true);
      step("#scan-resume",true);
    }
  }
  window.addEventListener("pagehide",()=>{ if(pollTimer) clearTimeout(pollTimer); },{once:true});
}
if (typeof document !== "undefined") {
  // DOMContentLoaded follows all deferred site config scripts. A module in
  // <head> must not read SMB_CONFIG before the generated config.js is ready.
  if (document.readyState === "complete") startPortal();
  else document.addEventListener("DOMContentLoaded", startPortal, { once:true });
}
