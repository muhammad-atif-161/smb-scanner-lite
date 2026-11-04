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
  });
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
  if (!active) {
    step("#scan-create",false);
    step("#scan-closed",true);
    showMessage("Online assessments are not open yet. The recorded demo and manual enquiry remain available.");
    return;
  }
  let client;
  try { client = makeScanClient(cfg.apiBaseUrl); }
  catch {
    step("#scan-create",false);
    step("#scan-closed",true);
    showMessage("Online assessment configuration is incomplete. Please use the manual request form.", "error");
    return;
  }
  let session = null;
  const save = value => {
    session = value;
    try { window.sessionStorage.setItem(STORE_KEY,JSON.stringify(value)); } catch { /* private mode */ }
  };
  const discard = () => {
    session = null;
    try { window.sessionStorage.removeItem(STORE_KEY); } catch { /* private mode */ }
  };
  function showCreated() {
    if (!session) return;
    step("#scan-create",false);
    step("#scan-resume",false);
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
    text("#scan-report-notice","The detailed evidence is locked until secure payment is available. There is no checkout or charge in this preview.");
  }
  async function refresh() {
    if (!session) return;
    const state = await client.status(session.id,session.token);
    step("#scan-status",true);
    text("#scan-state",state.status || "unknown");
    if (state.status === "verified") {
      step("#scan-verify",false);
      step("#scan-dispatch",true);
      showMessage("Ownership verified. A scan will start only if you explicitly confirm below.", "success");
    } else if (["queued","dispatching","dispatch_unknown","running"].includes(state.status)) {
      step("#scan-verify",false);
      step("#scan-dispatch",false);
      showMessage(state.status === "dispatch_unknown"
        ? "GitHub dispatch outcome is unknown. Do not click Start again; contact support with your assessment ID."
        : "Your assessment has been submitted. Use Refresh status to check progress.");
    } else if (state.status === "completed") {
      step("#scan-verify",false);
      step("#scan-dispatch",false);
      const data = await client.preview(session.id,session.token);
      drawPreview(data);
      showMessage("Assessment complete. A limited preview is available below.", "success");
    } else if (["failed","dispatch_failed"].includes(state.status)) {
      step("#scan-verify",false);
      step("#scan-dispatch",false);
      showMessage("The assessment could not complete. No second scan will start automatically. Contact support with your assessment ID.", "error");
    } else {
      step("#scan-verify",true);
    }
  }
  $("#scan-request-form").addEventListener("submit",async event=>{
    event.preventDefault();
    const form=event.currentTarget;
    const accept=$("#scan-consent");
    if (!accept.checked) { showMessage("Confirm that you own or are expressly authorized to assess this domain.", "error"); return; }
    const button=form.querySelector('button[type="submit"]');
    busy(button,true);
    try {
      const payload={name:form.elements.namedItem("name").value.trim(),
                     email:form.elements.namedItem("email").value.trim(),
                     domain:form.elements.namedItem("domain").value.trim()};
      const result=await client.create(payload);
      const next=parseSession({id:result.assessment_id,token:result.access_token,
        domain:result.domain,recordName:result.dns_record_name,recordValue:result.dns_record_value});
      if (!next || !next.recordName || !next.recordValue) throw new Error("Invalid server response");
      save(next);
      showCreated();
    } catch(e) {
      showMessage(e instanceof ScanAPIError ? e.message : "Could not create an assessment. Please use the manual request form.", "error");
    } finally {busy(button,false)}
  });
  $("#scan-verify-button").addEventListener("click",async event=>{
    const button=event.currentTarget; busy(button,true);
    try {
      await client.verify(session.id,session.token);
      await refresh();
    } catch(e) {showMessage(e instanceof ScanAPIError ? e.message : "Could not verify DNS ownership.", "error")}
    finally {busy(button,false)}
  });
  $("#scan-dispatch-button").addEventListener("click",async event=>{
    if (!$("#scan-dispatch-consent").checked) {
      showMessage("Confirm explicit authorization before starting the DNS/email assessment.","error"); return;
    }
    const button=event.currentTarget;busy(button,true);
    try {
      const result=await client.dispatch(session.id,session.token);
      showMessage("Assessment dispatch requested. The scanner cannot be started again for this assessment.","success");
      text("#scan-state",result.status);
      step("#scan-dispatch",false);
    } catch(e) {
      showMessage(e instanceof ScanAPIError ? e.message :
        "Dispatch status uncertain. Use Refresh status; do not submit again.","error");
    } finally {busy(button,false)}
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
    showMessage("Previous assessment cleared from this browser tab. Its stored report was not deleted.");
  });
  $("#scan-copy-token").addEventListener("click",async()=>{
    if(!session) return;
    try {
      await navigator.clipboard.writeText(session.token);
      showMessage("Private token copied. Keep it secure and do not share it in chat.", "success");
    } catch { showMessage("Select and copy the private token manually.", "info"); }
  });
  try {session=parseSession(window.sessionStorage.getItem(STORE_KEY));}catch{session=null}
  if(session){
    showCreated();
    refresh().catch(()=>showMessage("Couldn't refresh automatically. Use Refresh status to try again.", "error"));
  } else {
    step("#scan-create",true);
    step("#scan-resume",true);
  }
}
if (typeof document !== "undefined") {
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded",startPortal,{once:true});
  else startPortal();
}
