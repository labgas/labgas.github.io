---
layout: single
title: "Laboratory for Brain-Gut Axis Studies"
permalink: /
author_profile: false
classes:
  - wide
  - home-page
header:
  image: /assets/images/lab-group.jpg
  image_description: "The LaBGAS team"
  caption: "The LaBGAS team, KU Leuven"
# The lab mark goes in the theme's own left column, which the author profile
# would otherwise fill. Putting it there rather than in the content keeps the
# intro text aligned with every other block on the page, and the theme's
# breakpoints collapse it to a single column below 1024px for free.
sidebar:
  - image: /assets/images/labgas-logo.png
    image_alt: "LaBGAS — Laboratory for Brain-Gut Axis Studies"
---

{: .home-lede}
LaBGAS is a strongly interdisciplinary **human** research group at **KU Leuven**, embedded in
the [Translational Research Center for Gastrointestinal Disorders
(TARGID)](https://gbiomed.kuleuven.be/english/research/50000625/50000628) and a member of the
[Leuven Brain Institute](https://www.kuleuven.be/brain-institute). We study how signals
travelling between the gut and the brain shape what people feel — bodily symptoms, appetite,
mood and fear — combining functional brain imaging, PET, psychophysiology and controlled
nutritional and microbial interventions in humans.

We also build the analysis software behind that work, and release it openly.

## Research lines

<div class="line-grid">
  <div class="line-card">
    <h3><a href="{{ '/research/#gastrointestinal-symptom-pain-and-fatigue-perception' | relative_url }}">Gastrointestinal symptom, pain, and fatigue perception</a></h3>
    <p>Psychobiological mechanisms underlying symptom perception in disorders of gut-brain
    interaction, studied with functional brain imaging and psychophysiology.</p>
  </div>
  <div class="line-card">
    <h3><a href="{{ '/research/#appetite-food-intake--reward' | relative_url }}">Appetite, food intake &amp; reward</a></h3>
    <p>How gastrointestinal signals act on the homeostatic and hedonic brain circuits regulating
    appetite, feeding and body weight — including dopamine, opioid and endocannabinoid systems
    studied with PET-MR.</p>
  </div>
  <div class="line-card">
    <h3><a href="{{ '/research/#microbiota-gut-signals--the-mind' | relative_url }}">Microbiota, gut signals &amp; the mind</a></h3>
    <p>How nutrient- and microbiota-derived gut signals influence stress, fear learning, affect
    and cognition — the focus of our ERC-funded <strong>MoodBugs</strong> project.</p>
  </div>
</div>

[See all research lines and projects]({{ '/research/' | relative_url }}){: .btn .btn--primary}

## Open code and documentation

Our neuroimaging analyses run on an openly developed MATLAB codebase built on top of the
[CANlab](https://canlab.github.io/) toolset. Two repositories carry the reusable parts:

- **[LaBGAScore](https://github.com/labgas/LaBGAScore)** — core scripts and templates for our
  standard workflow: BIDS conversion, first-level modelling, second-level and multivariate
  pipelines, PET, MR spectroscopy and atlas tooling.
- **[CANlab_help_examples](https://github.com/labgas/CANlab_help_examples)** — our fork of the
  CANlab help repository, carrying the batch pipeline we use for second-level analysis and
  date-stamped HTML reporting.

<div class="canlab-note" markdown="1">
**Built on CANlab tools.** LaBGAScore is not a standalone toolbox. It depends on
[CanlabCore](https://github.com/canlab/CanlabCore) and
[Neuroimaging_Pattern_Masks](https://github.com/canlab/Neuroimaging_Pattern_Masks) from the
[Cognitive and Affective Neuroscience Lab](https://canlab.github.io/), plus
[SPM12](https://www.fil.ion.ucl.ac.uk/spm/). Start with the
[CANlab setup guide](https://canlab.github.io/setup/) before our
[pipeline documentation]({{ '/docs/' | relative_url }}).
</div>

[Tools overview]({{ '/tools/' | relative_url }}){: .btn .btn--primary}
[Pipeline documentation]({{ '/docs/' | relative_url }}){: .btn .btn--inverse}

{% assign recent = site.posts | slice: 0, 3 %}
{% if recent.size > 0 %}
## Latest news

{% for post in recent %}
- **[{{ post.title }}]({{ post.url | relative_url }})** — <span style="color:#5c6b7a">{{ post.date | date: "%-d %B %Y" }}</span>
{% endfor %}

[All news]({{ '/news/' | relative_url }}){: .btn .btn--inverse}
{% endif %}

## Take part

We regularly recruit healthy volunteers and patients for our studies, and we host master's
students, PhD candidates and post-docs. See [Join us]({{ '/join/' | relative_url }}), or write to
[Liene Bervoets](mailto:liene.bervoets@kuleuven.be) about taking part in a study and to
[Lukas Van Oudenhove](mailto:lukas.vanoudenhove@kuleuven.be) about research positions.

{: .funders}
Our work is supported by the European Research Council (ERC), Research Foundation – Flanders
(FWO), KU Leuven internal funds (BOF, including Methusalem), the Swiss National Science
Foundation (SNSF) and the European Commission's Horizon 2020 programme.
