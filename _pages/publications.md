---
layout: single
title: "Publications"
permalink: /publications/
author_profile: false
toc: true
toc_sticky: true
toc_label: "Research lines"
---

A selection of work, grouped by research line. This is a curated set — the complete record runs
to more than 300 items and lives on the profiles below, which are always current.

<div class="canlab-note" markdown="1">
**Complete and up-to-date lists**
[ORCID](https://orcid.org/0000-0002-6540-3113) ·
[PubMed](https://pubmed.ncbi.nlm.nih.gov/?term=Van+Oudenhove+L%5BAuthor%5D&sort=date) ·
[FRIS research portal](https://www.researchportal.be/nl/onderzoeker/lukas-van-oudenhove) ·
[KU Leuven Lirias](https://lirias.kuleuven.be/)

A caution for anyone searching by name: PubMed's `Van Oudenhove L` also returns work by an
unrelated researcher in entomology. The FRIS and ORCID profiles are identity-linked and do not
have this problem. Every entry below was checked against its PubMed author list.
</div>

{% assign pubs = site.data.publications %}
{% for line in pubs.lines %}
{% assign items = pubs.items | where: "line", line.id %}
{% if items.size > 0 %}

## {{ line.label }}

{% for p in items %}
<div class="pub" markdown="0">
  <p class="pub__title">{{ p.title }}</p>
  {% if p.authors and p.authors.size > 0 %}
  <p class="pub__authors">
    {%- for a in p.authors -%}
      {%- if a contains "Oudenhove" -%}<span class="pub__self">{{ a }}</span>{%- else -%}{{ a }}{%- endif -%}
      {%- unless forloop.last %}, {% endunless -%}
    {%- endfor -%}
  </p>
  {% endif %}
  <p class="pub__venue">
    <em>{{ p.journal }}</em>{% if p.year %} {{ p.year }}{% endif %}{% if p.volume %};{{ p.volume }}{% endif %}{% if p.issue %}({{ p.issue }}){% endif %}{% if p.pages %}:{{ p.pages }}{% endif %}.
  </p>
  <p class="pub__links">
    {% if p.doi %}<a href="https://doi.org/{{ p.doi }}">doi:{{ p.doi }}</a>{% endif %}
    {% if p.pmid %}<a href="https://pubmed.ncbi.nlm.nih.gov/{{ p.pmid }}/">PubMed {{ p.pmid }}</a>{% endif %}
  </p>
</div>
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
