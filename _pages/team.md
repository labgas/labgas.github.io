---
layout: single
title: "Team"
permalink: /team/
author_profile: false
toc: true
toc_sticky: true
toc_label: "Groups"
header:
  image: /assets/images/lab-group.jpg
  image_description: "The LaBGAS team"
  caption: "The LaBGAS team, KU Leuven"
---

LaBGAS is a strongly interdisciplinary group — medicine, psychology, nutrition, neuroscience,
bioengineering and biostatistics all sit in the same lab meeting. We are embedded in
[TARGID](https://gbiomed.kuleuven.be/english/research/50000625/50000628/) at KU Leuven and work
closely with microbiology, nutrition, psychology and neuroscience groups in Leuven and beyond.

Each **KU Leuven profile** link opens that person's entry in the university's
[who's who](https://www.kuleuven.be/wieiswie/en/) directory, with their publications,
memberships and contact details.

{% for g in site.data.team.groups %}
{% assign people = site.data.team.members | where: "group", g.id %}
{% if people.size > 0 %}
<div class="team-group" markdown="0">
<h2 id="{{ g.label | slugify }}">{{ g.label }}</h2>
<div class="team-list">
{% for m in people %}
  {%- comment -%}
    Initials from the first two words, not first-and-last: Dutch surname
    particles mean the last word is often not the distinguishing one
    ("Maaike Van Den Houte" would otherwise render as MH, not MV).
  {%- endcomment -%}
  {% assign words = m.name | split: " " %}
  {% assign first_initial = words[0] | slice: 0 | upcase %}
  {% if words.size > 1 %}
    {% assign second_initial = words[1] | slice: 0 | upcase %}
  {% else %}
    {% assign second_initial = "" %}
  {% endif %}
  <div class="person">
    <div class="person__aside">
      {% if m.photo %}
      <img class="person__avatar" src="{{ '/assets/images/team/' | append: m.photo | relative_url }}" alt="{{ m.name }}" loading="lazy">
      {% else %}
      <div class="person__avatar" aria-hidden="true">{{ first_initial }}{{ second_initial }}</div>
      {% endif %}
    </div>
    <div class="person__body">
      <h3 class="person__name" id="{{ m.name | slugify }}">{{ m.name }}</h3>
      {% if m.title %}<p class="person__title">{{ m.title }}</p>{% endif %}

      {% if m.bio %}
        {% for para in m.bio %}<p class="person__bio">{{ para }}</p>{% endfor %}
      {% endif %}

      {% if m.projects_all %}
      <p class="person__projects">
        <span class="person__projects-label">Projects</span>
        {% if m.projects_link == false %}
        <span class="project-chip is-plain">All LaBGAS projects</span>
        {% else %}
        <a class="project-chip" href="{{ '/research/' | relative_url }}">All LaBGAS projects</a>
        {% endif %}
      </p>
      {% elsif m.projects %}
      <p class="person__projects">
        <span class="person__projects-label">Projects</span>
        {% for p in m.projects %}
          {% if p.ref %}
          <a class="project-chip" href="{{ '/research/#' | append: p.ref | relative_url }}">{{ p.title }}</a>
          {% else %}
          <a class="project-chip" href="{{ p.url }}">{{ p.title }}</a>
          {% endif %}
        {% endfor %}
      </p>
      {% endif %}

      {% if m.kuleuven_id or m.orcid or m.scholar or m.github or m.email %}
      <p class="person__links">
        {% if m.kuleuven_id %}<a href="https://www.kuleuven.be/wieiswie/en/person/{{ m.kuleuven_id }}">KU Leuven profile</a>{% endif %}
        {% if m.orcid %}<a href="https://orcid.org/{{ m.orcid }}">ORCID</a>{% endif %}
        {% if m.scholar %}<a href="{{ m.scholar }}">Scholar</a>{% endif %}
        {% if m.github %}<a href="https://github.com/{{ m.github }}">GitHub</a>{% endif %}
        {% if m.email %}<a href="mailto:{{ m.email }}">Email</a>{% endif %}
      </p>
      {% endif %}
    </div>
  </div>
{% endfor %}
</div>
</div>
{% endif %}
{% endfor %}

---

Interested in joining? See [Join us]({{ '/join/' | relative_url }}), or write to
[Lukas Van Oudenhove](mailto:lukas.vanoudenhove@kuleuven.be) about research positions and to
[Liene Bervoets](mailto:liene.bervoets@kuleuven.be) about taking part in a study.

Biographies are reproduced from the
[LaBGAS pages](https://gbiomed.kuleuven.be/english/research/50000625/50000628/labgas/staff-folder/labgasmembers)
on the KU Leuven site.
