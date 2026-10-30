---
layout: single
title: "Publications"
permalink: /publications/
author_profile: false
toc: true
toc_sticky: true
toc_label: "Research lines"
---

Everything from the last 12 months first, then a selection of work grouped by research line. The
research-line sections are a curated set — the complete record runs to more than 300 items and
lives on the profiles below, which are always current.

<div class="canlab-note" markdown="1">
**Complete and up-to-date lists**
[ORCID](https://orcid.org/0000-0002-6540-3113) ·
[Google Scholar](https://scholar.google.com/citations?user=xYPdgr8AAAAJ) ·
[PubMed](https://pubmed.ncbi.nlm.nih.gov/?term=Van+Oudenhove+L%5BAuthor%5D&sort=date) ·
[FRIS research portal](https://www.researchportal.be/nl/onderzoeker/lukas-van-oudenhove) ·
[KU Leuven Lirias](https://lirias.kuleuven.be/)

The FRIS portal holds the fullest record — over 300 items, identity-linked to KU Leuven.

A caution for anyone searching by name: PubMed's `Van Oudenhove L` also returns work by an
unrelated researcher in entomology. The FRIS and ORCID profiles do not have this problem, and
every entry below was checked against its PubMed author list.
</div>

{%- comment -%}
  Generated daily from PubMed by scripts/refresh_recent_publications.py. Papers
  that are also curated highlights appear here and under their research line.
{%- endcomment -%}
{% assign recent = site.data.recent_publications.items %}
{% if recent and recent.size > 0 %}

## Recent publications

The last 12 months, from PubMed, updated daily.

{% for p in recent %}
{% include publication.html pub=p %}
{% endfor %}
{% endif %}

{% assign pubs = site.data.publications %}
{% for line in pubs.lines %}
{% assign items = pubs.items | where: "line", line.id %}
{% if items.size > 0 %}

## {{ line.label }}

{% for p in items %}
{% include publication.html pub=p %}
{% endfor %}
{% endif %}
{% endfor %}

---

## Code and data behind the papers

Several studies have their analysis code — and in some cases data — released as their own
repository in the [labgas GitHub organisation](https://github.com/labgas). The
[Tools page]({{ '/tools/' | relative_url }}) indexes all of them, including
`proj-emosymp`, `proj-fodmap-fmri`, `proj_erythritol_*`, `proj_reflux_database_*` and
`proj_Rome_IV_network_analysis`.

Version control uses [DataLad](https://www.datalad.org/) on top of git and git-annex, with code
pushed to GitHub and data to [GIN](https://gin.g-node.org/).
