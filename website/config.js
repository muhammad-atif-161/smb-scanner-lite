/* ==========================================================================
   SMB Scanner Lite — runtime configuration
   --------------------------------------------------------------------------
   Everything a maintainer may need to change lives here. This file is served
   as a static asset; it contains no secrets and no credentials.

   formEndpoint
     Optional POST endpoint for the enquiry forms, for example a Formspree or
     Web3Forms URL ("https://formspree.io/f/XXXXXXXX"). It must accept a JSON
     POST body and answer with a 2xx status. When it is empty the forms fall
     back to composing the enquiry in the visitor's own mail client, addressed
     to contactEmail. Both paths are real delivery routes; neither stores data
     on this website, which has no backend.

   contactEmail
     The published contact address. Also appears in the footer and privacy
     policy, generated from tools/site/config.py — change both when it changes.
   ========================================================================== */
window.SMB_CONFIG = {
  siteName: "SMB Scanner Lite",
  siteUrl: "https://smbscannerlite.me",
  contactEmail: "myself.atiff@gmail.com",
  formEndpoint: "https://formspree.io/f/xbggayev",
  githubUrl: "https://github.com/muhammad-atif-161/smb-scanner-lite",
  listingUrl: "https://www.sideprojectors.com/project/104650/smb-scanner",
  allowlist: ["example.com", "example.org", "example.net", "scanme.nmap.org", "badssl.com"],
  recordedDataUrl: "/data/recorded-assessment.json"
};
