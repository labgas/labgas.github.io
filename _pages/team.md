---
layout: single
title: "Team"
permalink: /team/
author_profile: false
toc: true
toc_sticky: true
toc_label: "Groups"
---

LaBGAS is a strongly interdisciplinary group — medicine, psychology, nutrition, neuroscience,
bioengineering and biostatistics all sit in the same lab meeting. We are embedded in
[TARGID](https://gbiomed.kuleuven.be/english/research/50000625/50000628/) at KU Leuven and work
closely with microbiology, nutrition, psychology and neuroscience groups in Leuven and beyond.

{% for g in site.data.team.groups %}
{% assign people = site.data.team.members | where: "group", g.id %}
{% if people.size > 0 %}
<div class="team-group" markdown="0">
<h2 id="{{ g.label | slugify }}">{{ g.label }}</h2>
<div class="team-grid">
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
    {% if m.photo %}
    <img class="person__avatar" src="{{ '/assets/images/team/' | append: m.photo | relative_url }}" alt="{{ m.name }}">
    {% else %}
    <div class="person__avatar" aria-hidden="true">{{ first_initial }}{{ second_initial }}</div>
    {% endif %}
    <div class="person__body">
      <span class="person__name">{{ m.name }}</span>
      {% if m.title %}<span class="person__title">{{ m.title }}</span>{% endif %}
      {% if m.focus %}<p class="person__focus">{{ m.focus }}</p>{% endif %}
      {% if m.kuleuven or m.orcid or m.github or m.email %}
      <div class="person__links">
        {% if m.kuleuven %}<a href="{{ m.kuleuven }}">Profile</a>{% endif %}
        {% if m.orcid %}<a href="https://orcid.org/{{ m.orcid }}">ORCID</a>{% endif %}
        {% if m.github %}<a href="https://github.com/{{ m.github }}">GitHub</a>{% endif %}
        {% if m.email %}<a href="mailto:{{ m.email }}">Email</a>{% endif %}
      </div>
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
[labgas@kuleuven.be](mailto:labgas@kuleuven.be).
