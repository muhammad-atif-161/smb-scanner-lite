"""Blog pages: the index, one hub per cluster, and the article template.

The knowledge base under ``/resources/`` is the reference layer: long-form
mechanics, one article per topic. The blog is the practical layer: a guide with
a sequence, a checklist, a walkthrough. Every post links to its reference
article, and every cluster hub states the difference so the two sections are not
competing for the same search intent.
"""

from __future__ import annotations

import calendar
import html
import re
from datetime import date, datetime

from . import blog as B
from . import config as C
from . import schema as structured
from .ui import btn, cta_band, e, icon, layout, section_head

DEFAULT_DATE = "2026-10-31"


def _long_date(value: str) -> str:
    parsed = datetime.strptime(value, "%Y-%m-%d")
    return f"{parsed.day} {parsed.strftime('%B %Y')}"


def _next_review(post: dict) -> str:
    """Next scheduled review, from the last update and the post's cadence.

    Provider-specific guides (selector names, console paths) are on a six-month
    cycle; everything else is annual. The date is a plan, not a claim that the
    content has already been re-checked.
    """
    months = int(post.get("review_months", 12))
    start = datetime.strptime(post["updated"], "%Y-%m-%d").date()
    month_index = start.month - 1 + months
    year = start.year + month_index // 12
    month = month_index % 12 + 1
    day = min(start.day, calendar.monthrange(year, month)[1])
    return f"{date(year, month, day).day} {date(year, month, day).strftime('%B %Y')}"


def _slug(text: str) -> str:
    plain = html.unescape(re.sub(r"<[^>]+>", "", text)).lower()
    anchor = re.sub(r"[^a-z0-9]+", "-", plain).strip("-")
    # An id has to start with a letter, so "1. The metadata block" becomes
    # "the-metadata-block" rather than "1-the-metadata-block".
    return re.sub(r"^\d+-", "", anchor) or "section"


def _with_ids(body: str) -> tuple[str, list[tuple[str, str]]]:
    """Give every h2 an id and collect the table of contents from them."""
    toc: list[tuple[str, str]] = []
    used: set[str] = set()

    def replace(match: re.Match) -> str:
        label = match.group(1)
        anchor = _slug(label)
        if anchor in used:
            counter = 2
            while f"{anchor}-{counter}" in used:
                counter += 1
            anchor = f"{anchor}-{counter}"
        used.add(anchor)
        toc.append((anchor, html.unescape(re.sub(r"<[^>]+>", "", label))))
        return f'<h2 id="{anchor}">{label}</h2>'

    return re.sub(r"<h2>(.*?)</h2>", replace, body, flags=re.S), toc


# ---------------------------------------------------------------------------
# Shared pieces
# ---------------------------------------------------------------------------

def _post_card(post: dict, tag: str | None = None) -> str:
    """A post card. ``tag=None`` uses the cluster label, ``tag=False`` omits it."""
    label = B.CLUSTERS[post["cluster"]]["label"] if tag is None else tag
    tag_html = f'<span class="component-tag mono">{e(label)}</span>' if label else ""
    return f"""
<a class="resource-card reveal" href="{B.post_url(post)}">
  {tag_html}
  <h3>{e(post['title'])}</h3>
  <p>{e(post['desc'])}</p>
  <span class="resource-meta"><span>{_long_date(post['date'])}</span><span>{B.read_minutes(post)} min read</span></span>
</a>"""


def post_cards(posts, tag=None) -> str:
    """A resource-grid of post cards, for other sections that link here."""
    return f'<div class="resource-grid">{"".join(_post_card(post, tag) for post in posts)}</div>'


def _cluster_card(slug: str, meta: dict, count: int) -> str:
    word = "post" if count == 1 else "posts"
    return f"""
<a class="resource-card reveal" href="{B.cluster_url(slug)}">
  <span class="card-icon">{icon(meta['icon'], 20)}</span>
  <span class="component-tag mono">{e(meta['label'])}</span>
  <h3>{e(meta['title'])}</h3>
  <p>{e(meta['lede'])}</p>
  <span class="resource-meta"><span>{count} {word}</span><span>Read the cluster {icon('arrow', 14)}</span></span>
</a>"""


def _checks_table(meta: dict) -> str:
    rows = "".join(
        f"<tr><th scope=\"row\">{e(name)}</th><td>{text}</td></tr>"
        for name, text in meta["checks"]
    )
    return f"""
<div class="table-wrap">
  <table>
    <caption>Read-only checks from the 22-control catalog. Every conclusive result quotes the observation behind it.</caption>
    <thead><tr><th scope="col">Control</th><th scope="col">What is evaluated</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>"""


def _product_block(post: dict) -> str:
    meta = B.CLUSTERS[post["cluster"]]
    return f"""
<h2>What SMB Scanner Lite checks here</h2>
<p>These are the controls from this area that the assessment evaluates from outside, without
credentials and without touching anything private. Each one returns a status and, for every
conclusive result, the record, header or handshake that produced it.</p>
{_checks_table(meta)}
<p class="small">Only assess domains you own or are authorised to test &mdash; see
<a href="/responsible-use/">responsible use</a>. The published
<a href="/demo/">recorded assessment</a> shows how a result and its evidence appear in a report,
and the <a href="/capabilities/">control catalog</a> lists all 22 controls with their weights.
Reference detail for this topic lives in <a href="{meta['reference'][0]}">{e(meta['reference'][1])}</a>.</p>"""


def _aside(post: dict, toc: list[tuple[str, str]]) -> str:
    meta = B.CLUSTERS[post["cluster"]]
    toc_html = "".join(f'<li><a href="#{anchor}">{e(label)}</a></li>' for anchor, label in toc)
    return f"""
<aside class="article-aside">
  <nav class="toc" aria-label="On this page">
    <h2>On this page</h2>
    <ol>{toc_html}</ol>
  </nav>
  <div class="card">
    <div class="card-icon card-icon--cyan">{icon('target', 20)}</div>
    <h3 style="font-size:0.95rem">Check your own domain</h3>
    <p class="small">A private assessment covers the full catalog, after scope and written authorisation are agreed. The public sandbox is limited to five allowlisted test domains.</p>
    <a class="tlink mt-1" href="/request-assessment/">Request an assessment {icon('arrow', 16)}</a>
  </div>
  <div class="card">
    <div class="card-icon">{icon('book', 20)}</div>
    <h3 style="font-size:0.95rem">{e(meta['label'])} cluster</h3>
    <p class="small">All guides in this area, plus the technical reference article.</p>
    <a class="tlink" href="{B.cluster_url(post['cluster'])}">Browse the cluster {icon('arrow', 16)}</a>
    <a class="tlink mt-1" href="{meta['reference'][0]}">Reference: the mechanics {icon('arrow', 16)}</a>
  </div>
</aside>"""


def _related(post: dict) -> str:
    picks = B.related(post, 2)
    if not picks:
        return ""
    cards = "".join(_post_card(item) for item in picks)
    return f"""
<section class="section section--alt">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Keep reading</p><h2>Related guides</h2></div>
    <div class="resource-grid">{cards}</div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------

START_HERE = (
    "spf-dkim-dmarc-explained",
    "small-business-cybersecurity-guide",
    "what-is-a-security-posture-assessment",
)


def index() -> str:
    latest = B.all_posts()
    start = [B.BY_SLUG[slug] for slug in START_HERE]
    clusters = "".join(_cluster_card(slug, meta, count) for slug, meta, count in B.cluster_sizes())
    start_cards = "".join(_post_card(post) for post in start)
    all_cards = "".join(_post_card(post) for post in latest)
    body = f"""
<header class="page-head page-head--wide">
  <div class="wrap">
    <p class="eyebrow">Blog</p>
    <h1>Security writing for businesses without a security team</h1>
    <p class="lede">Practical guides to the parts of security you can actually change this week: email authentication, DNS records, TLS and browser headers, and how to judge an assessment report. Written for the person who also does the invoicing.</p>
    <div class="article-meta">
      <span>{len(latest)} posts</span>
      <span>{len(B.CLUSTERS)} clusters</span>
      <span>Updated {_long_date(latest[0]['updated'] if latest else DEFAULT_DATE)}</span>
    </div>
  </div>
</header>

<section class="section section--flush">
  <div class="wrap">
    <div class="split">
      <div class="prose">
        <p>Most security content is written either for engineers who already know the answer or
        for buyers who need to be frightened into one. This section is for the third reader: the
        owner or operations lead of a small business who has to decide what to fix, in what order,
        with no budget for a security team.</p>
        <p>Every guide follows the same discipline. It explains the mechanism, shows the check you
        can run yourself, states what a good result looks like, and says plainly where the advice
        stops working. No invented statistics, no fear marketing, no "10 signs you are being
        hacked" listicles.</p>
        <p>If you want the RFC-level version of a topic instead, the
        <a href="/resources/">knowledge base</a> holds the reference articles. The two sections
        link to each other on purpose, and neither repeats the other's job.</p>
      </div>
      <div class="card reveal">
        <div class="card-icon card-icon--cyan">{icon('layers', 20)}</div>
        <h2 class="card-title">Blog or knowledge base?</h2>
        <p class="small"><strong>Blog</strong> &mdash; a sequence to follow, with commands, checklists and a decision at the end.</p>
        <p class="small"><strong>Knowledge base</strong> &mdash; the reference: how a mechanism works, what it does not protect, and where the specification says so.</p>
        <p class="small">Both are written from the same method, and both link to the published <a href="/methodology/">methodology</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Start here", "Three guides that cover the most ground.", "Email authentication, a whole-business baseline, and the assessment method these pages keep referring to.")}
    <div class="resource-grid">{start_cards}</div>
  </div>
</section>

<section class="section section--flush">
  <div class="wrap">
    {section_head("Clusters", "Browse by area.", "Each cluster is a hub: the guides in that area, the controls an external assessment can measure, and the technical reference behind them.")}
    <div class="resource-grid">{clusters}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("All posts", "Everything published so far.", "Newest first. Each cluster hub collects its own guides, the controls they map to, and the reference article behind them.")}
    <div class="resource-grid">{all_cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Editorial standard</p>
        <h2>What these guides will not do.</h2>
        <ul class="trust-list mt-2">
          <li><strong>No invented evidence</strong>No fabricated breach statistics, customer stories or benchmark numbers. Where a figure comes from a published report, it is named.</li>
          <li><strong>No scanning by implication</strong>Nothing here encourages testing a domain you do not own. The instructions assume you are working on your own infrastructure.</li>
          <li><strong>No product-first answers</strong>The mechanism is explained before the tool is mentioned, and the limit of the tool is stated in the same paragraph.</li>
          <li><strong>Corrections welcome</strong>If something is wrong or has aged badly, the contact form reaches the maintainer directly.</li>
        </ul>
      </div>
      <div class="card reveal">
        <div class="card-icon">{icon('clock', 20)}</div>
        <h3>How often this is reviewed</h3>
        <p class="small">Guides are reviewed when a specification, provider default or browser behaviour changes, and on a rolling annual basis otherwise. Each post shows its publication and last-updated date.</p>
        <p class="small">Posts that describe a provider's interface or a policy change carry a shorter review window, because those are the parts that go stale first.</p>
      </div>
    </div>
  </div>
</section>

{cta_band("Want the method applied to your own domain?", "A private assessment runs the full 22-control catalog under a written scope, and returns the observation behind every conclusive finding.", ("/request-assessment/", "Request an assessment"), ("/demo/", "See a recorded one"))}
"""
    return layout(
        "/blogs/",
        "Security blog for small businesses",
        (
            "Practical guides to email authentication, DNS security, TLS and browser headers, "
            "and how to read a security assessment report. Written for small businesses."
        ),
        body,
        active="blog",
        crumbs=[("Home", "/"), ("Blog", None)],
        page_type="CollectionPage",
        schema=structured.blog_collection(
            "/blogs/",
            "SMB Scanner Lite blog",
            "Practical external security guides for small businesses.",
            [
                (post["title"], B.post_url(post), post["desc"], post["date"])
                for post in latest
            ],
        ),
        page_extra={"mainEntity": {"@id": structured.page_url("/blogs/") + "#blog"}},
    )


# ---------------------------------------------------------------------------
# Cluster hubs
# ---------------------------------------------------------------------------

def cluster(slug: str) -> str:
    meta = B.CLUSTERS[slug]
    posts = B.by_cluster(slug)
    others = [item for item in B.CLUSTERS if item != slug]
    other_links = "".join(
        f'<a class="btn btn-ghost btn-sm" href="{B.cluster_url(item)}">{e(B.CLUSTERS[item]["label"])}</a>'
        for item in others
    )
    cards = "".join(_post_card(post, False) for post in posts)
    updated = max((post["updated"] for post in posts), default=DEFAULT_DATE)
    word = "post" if len(posts) == 1 else "posts"
    body = f"""
<header class="page-head page-head--wide">
  <div class="wrap">
    <p class="eyebrow">Blog &middot; {e(meta['label'])}</p>
    <h1>{e(meta['title'])}</h1>
    <p class="lede">{e(meta['lede'])}</p>
    <div class="article-meta">
      <span>{len(posts)} {word}</span>
      <span>Updated {_long_date(updated)}</span>
      <span>Cluster guide</span>
    </div>
  </div>
</header>

<section class="section section--flush">
  <div class="wrap">
    <div class="split">
      <div class="prose">
        {meta['intro']}
        <p>Every post in this cluster ends with the same question: what would you do on Monday?
        Where a check can be run by hand, the command is in the post. Where it cannot, the post
        says so rather than implying a tool will handle it.</p>
      </div>
      <div class="card reveal">
        <div class="card-icon card-icon--cyan">{icon(meta['icon'], 20)}</div>
        <h2 class="card-title">Reference article</h2>
        <p class="small">For the specification-level detail behind these guides &mdash; mechanisms, edge cases and what the standard does not cover:</p>
        <a class="tlink mt-1" href="{meta['reference'][0]}">{e(meta['reference'][1])} {icon('arrow', 16)}</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {section_head("Guides", f"{len(posts)} {word} in this cluster.", "Newest first.")}
    <div class="resource-grid">{cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("What the tool checks", "The controls this cluster maps to.", "Pulled from the published 22-control catalog, with the weights that drive the posture score.")}
    {_checks_table(meta)}
    <div class="row mt-3">{btn('/capabilities/', 'Full control catalog', 'ghost', 'arrow')}{btn('/methodology/', 'How statuses are assigned', 'ghost', 'arrow')}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Other clusters</p><h2>Keep going elsewhere</h2></div>
    <div class="row">{other_links}</div>
  </div>
</section>

{cta_band("Check this area on your own domain.", "The assessment covers all five clusters, with the observation quoted behind every conclusive finding.", ("/request-assessment/", "Request an assessment"), ("/demo/", "See a recorded assessment"))}
"""
    return layout(
        B.cluster_url(slug),
        meta["seo_title"],
        meta["desc"],
        body,
        active="blog",
        crumbs=[("Home", "/"), ("Blog", "/blogs/"), (meta["label"], None)],
        page_type="CollectionPage",
        schema=structured.blog_collection(
            B.cluster_url(slug),
            f"{meta['label']} — SMB Scanner Lite blog",
            meta["desc"],
            [(post["title"], B.post_url(post), post["desc"], post["date"]) for post in posts],
        ),
        page_extra={"mainEntity": {"@id": structured.page_url(B.cluster_url(slug)) + "#blog"}},
    )


# ---------------------------------------------------------------------------
# Posts
# ---------------------------------------------------------------------------

def post(slug: str) -> str:
    item = B.BY_SLUG[slug]
    meta = B.CLUSTERS[item["cluster"]]
    body_html, toc = _with_ids(item["body"] + _product_block(item))
    takeaways = "".join(f"<li>{point}</li>" for point in item.get("takeaways", []))
    updated = item["updated"] != item["date"]
    updated_html = f"<span>Updated {_long_date(item['updated'])}</span>" if updated else ""
    crumbs = [
        ("Home", "/"),
        ("Blog", "/blogs/"),
        (meta["label"], B.cluster_url(item["cluster"])),
        (item["title"], None),
    ]
    words = B.word_count(item)
    body = f"""
<article>
  <header class="article-head">
    <div class="wrap">
      <p class="eyebrow">Blog &middot; {e(meta['label'])}</p>
      <h1>{e(item['title'])}</h1>
      <p class="lede">{e(item['lede'])}</p>
      <div class="article-meta">
        <span>By {e(C.AUTHOR)}</span>
        <span>Published {_long_date(item['date'])}</span>
        {updated_html}
        <span>{B.read_minutes(item)} min read</span>
      </div>
    </div>
  </header>
  <div class="wrap">
    <div class="article-layout">
      <div class="prose">
        <div class="callout">
          {icon('list', 20)}
          <div>
            <p><strong>The short version</strong></p>
            <ul>{takeaways}</ul>
          </div>
        </div>
        {body_html}
      </div>
      {_aside(item, toc)}
    </div>
  </div>
</article>
{_related(item)}

<section class="section">
  <div class="wrap">
    <p class="small muted">{words} words &middot; published {_long_date(item['date'])} &middot; part of the
    <a href="{B.cluster_url(item['cluster'])}">{e(meta['label'].lower())} cluster</a>. Next scheduled review: {_next_review(item)}.
    Spotted an error? <a href="/contact/">Tell the maintainer</a> &mdash; corrections are published rather than quietly applied.</p>
  </div>
</section>

{cta_band("Check your own domain's external posture.", "The full catalog, a 0&ndash;100 score and the evidence behind every conclusive finding. Scope and written authorisation first; see the responsible-use policy.", ("/request-assessment/", "Request an assessment"), ("/demo/", "Open the recorded assessment"))}
"""
    return layout(
        B.post_url(item),
        item["seo_title"],
        item["desc"],
        body,
        active="blog",
        og_type="article",
        crumbs=crumbs,
        schema=structured.blog_posting(
            B.post_url(item),
            item["title"],
            item["desc"],
            item["date"],
            item["updated"],
            meta["label"],
            words,
            B.cluster_url(item["cluster"]),
            meta["label"],
        ),
        page_extra={"mainEntity": {"@id": structured.page_url(B.post_url(item)) + "#article"}},
    )
