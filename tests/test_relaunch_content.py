"""Relaunch product-positioning and content contract.

These tests run only on generated static files, never against a customer domain.
"""
from __future__ import annotations
import json
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from sitegen import blog as B, data as D  # noqa: E402

def page(path):
    return (ROOT/"website"/path).read_text(encoding="utf-8")

class SiteRelaunchTests(unittest.TestCase):
    def test_online_product_leads_and_is_safely_gated(self):
        home=page("index.html")
        self.assertIn("Understand what your domain", home)
        self.assertIn('href="/scan/"', home)
        self.assertIn("Online scans opening soon", home)
        self.assertNotIn("Try the Demo", home)
        settings=json.loads((ROOT/"site.saas.json").read_text())
        self.assertIs(settings["enabled"],False)
        self.assertEqual(settings["api_base_url"],
                         "https://smbscanner-edge.myself-atiff.workers.dev")
        portal=page("scan/index.html")
        self.assertIn('content="noindex, follow"', portal)
        self.assertIn('data-saas-portal',portal)

    def test_desktop_sandbox_is_separate_download(self):
        desktop=page("docs/index.html")
        self.assertIn("Public Sandbox Edition",desktop)
        self.assertIn("smb-scanner --help",desktop)
        self.assertIn("example.org",desktop)
        self.assertIn("github.com/muhammad-atif-161/smb-scanner-lite",desktop)
        scope=page("capabilities/index.html")
        self.assertIn("Not included in this online release",scope)
        self.assertIn("port scans",scope)
        self.assertIn("DKIM",scope)

    def test_all_ten_journal_posts_were_reauthored(self):
        self.assertEqual(len(B.POSTS),10)
        for post in B.POSTS:
            self.assertEqual(post["updated"],"2026-11-04",post["slug"])
            self.assertGreaterEqual(B.word_count(post),160,post["slug"])
            rendered=page(f"blogs/{post['slug']}/index.html")
            self.assertIn("The service boundary",rendered)
            self.assertIn(post["title"].replace("&","&amp;"),rendered)
            self.assertNotIn("The full catalog, a 0",rendered)

    def test_all_eight_reference_pages_explain_scope(self):
        self.assertEqual(len(D.RESOURCES),8)
        for record in D.RESOURCES:
            rendered=page(f"resources/{record['slug']}/index.html")
            self.assertIn("Service scope",rendered)
            self.assertIn("DNS/email",rendered)
            self.assertIn("Current scan coverage",rendered)

    def test_legal_and_support_do_not_claim_checkout(self):
        privacy=page("privacy/index.html")
        self.assertIn("Cloudflare D1",privacy)
        self.assertIn("payment",privacy.lower())
        terms=page("terms/index.html")
        self.assertIn("no active checkout",terms)
        faq=page("faq/index.html")
        self.assertIn("No.",faq)
        contact=page("contact/index.html")
        self.assertIn("data-enquiry-form",contact)
        self.assertIn('name="email"',contact)
        self.assertNotIn("from $149",page("request-assessment/index.html").lower())

    def test_no_private_tokens_in_web_assets(self):
        files=("website/config.js","website/scan-app.mjs","website/site.js",
               "website/index.html")
        for path in files:
            text=page(path)
            for key in ("WORKER_LEASE_SIGNING_KEY","GITHUB_DISPATCH_TOKEN",
                        "SMB_WORKER_API_TOKEN","IP_HASH_KEY"):
                self.assertNotIn(key,text,path)

if __name__=="__main__":
    unittest.main()
