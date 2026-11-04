"""Blog registry — rewritten journal only; stable article URLs."""
from __future__ import annotations
import re
import html
from .relaunch import rewrite_registry

SPECS = {
    "spf-dkim-dmarc-explained":"email-security",
    "set-up-dmarc-without-breaking-email":"email-security",
    "business-email-marked-as-spam":"email-security",
    "dns-security-for-small-businesses":"dns-security",
    "external-website-security-checks":"website-security",
    "small-business-cybersecurity-guide":"smb-basics",
    "what-is-a-security-posture-assessment":"assessment",
    "assessment-vs-penetration-test":"assessment",
    "check-your-external-security-posture-free":"assessment",
    "how-to-read-your-security-report":"assessment",
}
CLUSTERS = {key: {} for key in (
    "email-security", "dns-security", "website-security", "smb-basics", "assessment"
)}
POSTS = [{"slug":slug,"cluster":cluster,"date":"2026-10-31"}
         for slug,cluster in SPECS.items()]
rewrite_registry(POSTS, CLUSTERS)
BY_SLUG = {post["slug"]:post for post in POSTS}
POSTS_BY_CLUSTER = {slug:[] for slug in CLUSTERS}
for post in POSTS:
    POSTS_BY_CLUSTER[post["cluster"]].append(post)

def plain(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>"," ",value))

def word_count(post: dict) -> int:
    if "word_count" not in post:
        post["word_count"] = len(plain(post["lede"]+" "+post["body"]).split())
    return post["word_count"]

def read_minutes(post: dict) -> int:
    if "read" not in post:
        post["read"] = max(2,round(word_count(post)/210))
    return post["read"]

def all_posts() -> list[dict]:
    return sorted(POSTS,key=lambda p:p["updated"],reverse=True)

def by_cluster(slug: str) -> list[dict]:
    return POSTS_BY_CLUSTER.get(slug,[])

def latest(count: int=3,exclude: str="") -> list[dict]:
    return [p for p in all_posts() if p["slug"]!=exclude][:count]

def related(post: dict,count: int=2) -> list[dict]:
    siblings = [p for p in by_cluster(post["cluster"]) if p["slug"]!=post["slug"]]
    if len(siblings)<count:
        siblings.extend(p for p in POSTS if p["slug"]!=post["slug"] and p not in siblings)
    return siblings[:count]

def cluster_url(slug: str) -> str:
    return f"/blogs/{slug}/"

def post_url(post: dict) -> str:
    return f"/blogs/{post['slug']}/"

def cluster_sizes():
    return [(slug,meta,len(POSTS_BY_CLUSTER[slug])) for slug,meta in CLUSTERS.items()]
