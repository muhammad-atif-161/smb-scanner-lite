"""Structured data for the generated site.

Every page gets one JSON-LD block containing one ``@graph``. The graph is
assembled in ``ui.layout()`` and is composed of four parts, in this order:

1. ``Organization`` (``#organization``) and ``WebSite`` (``#website``) - the
   site-wide entities. Their ``@id`` values are identical on every page, so
   the site is described as one consistent set of things rather than 34
   unrelated documents.
2. A page node whose ``@type`` matches what the page actually is
   (``WebPage``, ``AboutPage``, ``ContactPage``, ``CollectionPage``,
   ``FAQPage``) and whose ``@id`` is ``<canonical-url>#webpage``.
3. Page-specific nodes: ``Article``, ``TechArticle``, ``Report``,
   ``SoftwareApplication`` or ``ItemList``, only on pages where that thing
   really exists.
4. ``BreadcrumbList`` - only on pages that render visible breadcrumbs.

Design decisions that must not be undone without checking the pages again
------------------------------------------------------------------------
* **No Product, Offer, AggregateRating or Review markup.** The site is not a
  retail storefront: there is no checkout, no cart, no shipping and no return
  process, and there are no customers who have left reviews. Merchant-listing
  markup on /acquisition/ previously described a project sale as a purchasable
  product, which is why Search Console asked for ``image``, ``shippingDetails``,
  ``hasMerchantReturnPolicy`` and a valid ``brand``. None of those can be
  answered truthfully, so the markup was removed rather than completed.
  The software itself is described with ``SoftwareApplication``, which is
  accurate and needs no price or rating. See ``docs/structured-data.md``.
* **No ``aggregateRating`` or ``review`` is ever generated.** There is no
  rating data on the site, and inventing it would be both dishonest and a
  structured-data policy violation.
* **``SoftwareApplication`` carries no ``offers`` node.** The public edition is
  free, but without genuine rating data the Software app rich result is not
  available; publishing an offer only put the node into product reporting with
  warnings that could not be fixed honestly. Price information stays in the
  visible page copy where it belongs.
* **``Article``/``TechArticle`` nodes are separate from the page node** and
  point back at it with ``mainEntityOfPage``, because Article is a
  ``CreativeWork``, not a ``WebPage`` subtype.
"""

from __future__ import annotations

from . import config as C

ORG_ID = C.SITE_URL + "/#organization"
SITE_ID = C.SITE_URL + "/#website"
SOFTWARE_ID = C.SITE_URL + "/#software"

BREADCRUMB_SUFFIX = "#breadcrumb"
PAGE_SUFFIX = "#webpage"


# ---------------------------------------------------------------------------
# Site-wide entities
# ---------------------------------------------------------------------------

def organization() -> dict:
    """The project/brand entity. Same ``@id`` and same facts on every page."""
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": C.SITE_NAME,
        "url": C.SITE_URL,
        # Google's logo guidance requires a raster image of at least 112x112,
        # so the SVG wordmark is not used here; logo-512.png is rendered from
        # the same artwork and is also the source of the touch icon.
        "logo": {
            "@type": "ImageObject",
            "url": C.SITE_URL + "/logo-512.png",
            "width": 512,
            "height": 512,
        },
        "email": C.CONTACT_EMAIL,
        "founder": {
            "@type": "Person",
            "name": C.AUTHOR,
            "url": C.AUTHOR_URL,
        },
        "description": (
            "An evidence-first external security posture assessment product for "
            "small and medium businesses, published as a restricted public "
            "sandbox edition."
        ),
        "sameAs": [C.REPO_URL, C.AUTHOR_URL],
    }


def website() -> dict:
    return {
        "@type": "WebSite",
        "@id": SITE_ID,
        "name": C.SITE_NAME,
        "url": C.SITE_URL,
        "description": (
            "Evidence-first external security posture assessment for small and "
            "medium businesses."
        ),
        "inLanguage": "en",
        "publisher": {"@id": ORG_ID},
    }


# ---------------------------------------------------------------------------
# Page node
# ---------------------------------------------------------------------------

def page_url(path: str) -> str:
    return C.SITE_URL + path


def page_node(path: str, name: str, description: str, kind: str = "WebPage",
              has_breadcrumb: bool = False, extra: dict | None = None) -> dict:
    node = {
        "@type": kind,
        "@id": page_url(path) + PAGE_SUFFIX,
        "url": page_url(path),
        "name": name,
        "description": description,
        "isPartOf": {"@id": SITE_ID},
        "inLanguage": "en",
    }
    if has_breadcrumb:
        node["breadcrumb"] = {"@id": page_url(path) + BREADCRUMB_SUFFIX}
    if extra:
        node.update(extra)
    return node


def graph(path: str, name: str, description: str, *, kind: str = "WebPage",
          extras=None, crumbs=None, page_extra: dict | None = None) -> dict:
    """Build the ``@graph`` published on one page."""
    nodes = [organization(), website(),
             page_node(path, name, description, kind, bool(crumbs), page_extra)]
    if extras:
        nodes.extend(extras if isinstance(extras, (list, tuple)) else [extras])
    if crumbs:
        nodes.append(breadcrumb(path, crumbs))
    return {"@context": "https://schema.org", "@graph": nodes}


def breadcrumb(path: str, items) -> dict:
    elements = []
    for position, (label, href) in enumerate(items, start=1):
        entry = {"@type": "ListItem", "position": position, "name": label}
        if href:
            entry["item"] = page_url(href)
        elements.append(entry)
    return {
        "@type": "BreadcrumbList",
        "@id": page_url(path) + BREADCRUMB_SUFFIX,
        "itemListElement": elements,
    }


# ---------------------------------------------------------------------------
# Page-specific nodes
# ---------------------------------------------------------------------------

def software_application() -> dict:
    """The product entity. Used where the software itself is the subject."""
    return {
        "@type": "SoftwareApplication",
        "@id": SOFTWARE_ID,
        "name": C.SITE_NAME,
        "applicationCategory": "SecurityApplication",
        "applicationSubCategory": "External security posture assessment",
        "operatingSystem": "Cross-platform (Python 3.10+), web demo in any modern browser",
        "softwareVersion": C.PRODUCT_VERSION,
        "url": C.SITE_URL,
        "author": {"@type": "Person", "name": C.AUTHOR, "url": C.AUTHOR_URL},
        "publisher": {"@id": ORG_ID},
        "description": (
            "Evaluates 22 publicly observable security controls, produces a 0-100 "
            "posture score and an A-F grade, and attaches the evidence behind every "
            "conclusive finding. The public edition is restricted to five approved "
            "test domains."
        ),
        "featureList": [
            "22 external security controls across DNS, email authentication, TLS, "
            "browser headers and service exposure",
            "0-100 weighted posture score with A-F grading",
            "Evidence string attached to every conclusive finding",
            "HTML, JSON, CSV and TXT report formats",
            "Hash-chained pre-scan consent receipts",
            "Restricted public sandbox edition with a five-domain allowlist",
        ],
    }


def software_ref() -> dict:
    """A short, self-contained reference to the product for pages that are
    *about* it (the demo, the acquisition page) without re-declaring the full
    application entity on every page."""
    return {"@type": "SoftwareApplication", "name": C.SITE_NAME, "url": C.SITE_URL}


def article(path: str, headline: str, description: str, published: str,
            modified: str = "", section: str = "", author_person: bool = True) -> dict:
    """An editorial page in the knowledge base."""
    node = {
        "@type": "Article",
        "@id": page_url(path) + "#article",
        "headline": headline,
        "description": description,
        "datePublished": published,
        "dateModified": modified or published,
        "author": (
            {"@type": "Person", "name": C.AUTHOR, "url": C.AUTHOR_URL}
            if author_person else {"@id": ORG_ID}
        ),
        "publisher": {"@id": ORG_ID},
        "mainEntityOfPage": {"@id": page_url(path) + PAGE_SUFFIX},
        "inLanguage": "en",
    }
    if section:
        node["articleSection"] = section
    return node


def tech_article(path: str, headline: str, description: str, published: str,
                 modified: str = "") -> dict:
    """Technical documentation: how the product works, how to run it."""
    return {
        "@type": "TechArticle",
        "@id": page_url(path) + "#article",
        "headline": headline,
        "description": description,
        "datePublished": published,
        "dateModified": modified or published,
        "author": {"@id": ORG_ID},
        "publisher": {"@id": ORG_ID},
        "mainEntityOfPage": {"@id": page_url(path) + PAGE_SUFFIX},
        "inLanguage": "en",
    }


def report(path: str, name: str, description: str, published: str) -> dict:
    """The published assessment report on /sample-report/."""
    return {
        "@type": "Report",
        "@id": page_url(path) + "#report",
        "name": name,
        "description": description,
        "about": "External security posture assessment",
        "datePublished": published,
        "author": {"@id": ORG_ID},
        "publisher": {"@id": ORG_ID},
        "mainEntityOfPage": {"@id": page_url(path) + PAGE_SUFFIX},
        "inLanguage": "en",
    }


def item_list(path: str, name: str, items) -> dict:
    """A catalogue of controls. ``items`` is an iterable of dicts with
    ``position``, ``name`` and ``description``."""
    return {
        "@type": "ItemList",
        "@id": page_url(path) + "#itemlist",
        "name": name,
        "numberOfItems": len(items),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": item["position"],
                "name": item["name"],
                "description": item["description"],
            }
            for item in items
        ],
    }


def faq_entity(questions) -> list:
    """``mainEntity`` value for the FAQ page. ``questions`` is a sequence of
    ``(question, answer_text)`` pairs taken from the same data the page renders."""
    return [
        {
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": answer},
        }
        for question, answer in questions
    ]
