"""Editorial journal renderer for the rewritten online-first articles."""
from __future__ import annotations
from . import blog as B
from . import config as C
from . import schema as structured
from .pages_blog import _with_ids, _long_date
from .ui import btn, e, icon, layout, section_head
from . import pages_relaunch as P

def _card(post) -> str:
    label=B.CLUSTERS[post["cluster"]]["label"]
    return f"""<a class="resource-card" href="{B.post_url(post)}">
    <span class="component-tag">{e(label)} / GUIDE</span><h3>{e(post['title'])}</h3>
    <p>{e(post['desc'])}</p><span class="resource-meta">
    <span>Updated {_long_date(post['updated'])}</span><span>{B.read_minutes(post)} min</span>
    </span></a>"""

def index() -> str:
    posts=B.all_posts()
    clusters="".join(f"""<a class="relaunch-feature" href="{B.cluster_url(slug)}">
    <small>{count:02d} ARTICLES</small><h3>{e(meta['title'])}</h3>
    <p>{e(meta['desc'])}</p></a>""" for slug,meta,count in B.cluster_sizes())
    cards="".join(_card(p) for p in posts)
    body=P.head("Field notes","A quieter kind of security writing.",
     "Clear explanations for the person responsible for a domain, a mailbox or a company. Mechanics first, actionable decisions second, and no inflated promises.",
     btn("/resources/","Technical reference library","ghost","book"))
    body+=f"""<section class="section"><div class="wrap">
    {section_head("Choose a subject","Five areas, each with a specific question.",
    "The journal is practical writing, not automated sales content.")}
    <div class="relaunch-feature-grid">{clusters}</div></div></section>
    <section class="section section--alt"><div class="wrap">
    {section_head("The articles","Guides worth keeping open.",
    "The latest edit dates reflect this editorial relaunch. Source references and the limits of each technique remain part of the discussion.")}
    <div class="resource-grid">{cards}</div></div></section>"""
    return layout("/blogs/","Security Journal | SMB Scanner Lite",
      "Thoughtful guides on DNS, email authentication, security-assessment interpretation and practical small-business security.",
      body, active="blog", crumbs=[("Home","/"),("Journal",None)],page_type="CollectionPage",
      schema=structured.blog_collection("/blogs/","SMB Scanner Lite journal",
      "Independent, practical security writing.",[(p["title"],B.post_url(p),p["desc"],p["date"]) for p in posts]))

def cluster(slug: str) -> str:
    meta=B.CLUSTERS[slug]
    posts=B.by_cluster(slug)
    cards="".join(_card(p) for p in posts)
    body=P.head("Journal / "+e(meta["label"]),e(meta["title"])+".",e(meta["desc"]),
      btn("/blogs/","All journal topics","ghost","arrow"))
    body+=f"""<section class="section"><div class="wrap relaunch-split">
    <div><p class="eyebrow">The subject</p><h2>Understand the mechanism before the product.</h2>
    <p>{e(meta['desc'])}</p>
    <div class="relaunch-callout"><p><strong>Scan scope:</strong>
    The first online scanner checks published DNS and email authentication only.
    Other technical material here is educational, not a description of a live test.</p></div>
    </div><div class="resource-grid" style="grid-template-columns:1fr">{cards}</div></div></section>"""
    return layout(B.cluster_url(slug),meta["seo_title"],meta["desc"],body,
      active="blog",crumbs=[("Home","/"),("Journal","/blogs/"),(meta["label"],None)],
      page_type="CollectionPage",schema=structured.blog_collection(B.cluster_url(slug),
       meta["title"],meta["desc"],[(p["title"],B.post_url(p),p["desc"],p["date"]) for p in posts]))

def post(slug: str) -> str:
    item=B.BY_SLUG[slug]
    meta=B.CLUSTERS[item["cluster"]]
    rendered,toc=_with_ids(item["body"])
    toc_items="".join(f'<li><a href="#{e(anchor)}">{e(label)}</a></li>' for anchor,label in toc)
    takeaways="".join(f'<li>{e(x)}</li>' for x in item["takeaways"])
    related="".join(_card(p) for p in B.related(item))
    words=B.word_count(item)
    body=f"""<article>
    <header class="article-head"><div class="wrap">
    <p class="eyebrow">{e(meta['label'])} / Journal</p>
    <h1>{e(item['title'])}</h1><p class="lede">{e(item['lede'])}</p>
    <div class="article-meta"><span>{e(C.AUTHOR)}</span>
    <span>Updated {_long_date(item['updated'])}</span>
    <span>{B.read_minutes(item)} min read</span></div>
    </div></header>
    <div class="wrap"><div class="article-layout">
    <div class="prose">
      <div class="relaunch-callout"><p><strong>Worth remembering</strong></p>
      <ul>{takeaways}</ul></div>
      {rendered}
      <hr><p><strong>The service boundary:</strong> The prepared online assessment
      verifies domain ownership and inspects public DNS/email policy. This
      article may discuss broader security practices; it is not a promise that
      the hosted worker performs those checks. <a href="/capabilities/">See the actual scan scope</a>.</p>
    </div>
    <aside class="article-aside">
      <nav class="toc" aria-label="Article sections"><h2>In this article</h2>
      <ol>{toc_items}</ol></nav>
      <div class="relaunch-feature"><small>ONLINE ASSESSMENT</small><h3>Review your own domain.</h3>
      <p>The verified scan workflow is being prepared for a controlled launch.</p>
      {btn("/scan/","Check availability","ghost","arrow")}</div>
      <div class="relaunch-feature"><small>RELATED SUBJECT</small>
      <h3>{e(meta['label'])}</h3><p>{e(meta['desc'])}</p>
      <a href="{B.cluster_url(item['cluster'])}">View this subject</a></div>
    </aside></div></div></article>
    <section class="section section--alt"><div class="wrap">
    {section_head("Keep reading","Two related perspectives.",
    "Independent guides from the same technical subject.")}
    <div class="resource-grid">{related}</div>
    <p class="small muted mt-3">Published {_long_date(item['date'])};
    substantially rewritten {_long_date(item['updated'])}. Found an error?
    <a href="/contact/">Send a correction</a>.</p>
    </div></section>"""
    return layout(B.post_url(item),item["seo_title"],item["desc"],body,active="blog",
      og_type="article",
      crumbs=[("Home","/"),("Journal","/blogs/"),(meta["label"],B.cluster_url(item["cluster"])),(item["title"],None)],
      schema=structured.blog_posting(B.post_url(item),item["title"],item["desc"],
         item["date"],item["updated"],meta["label"],words,
         B.cluster_url(item["cluster"]),meta["label"]),
      page_extra={"mainEntity":{"@id":structured.page_url(B.post_url(item))+"#article"}})
