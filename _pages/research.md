---
layout: single
title: "Research"
permalink: /research/
author_profile: false
toc: true
toc_sticky: true
toc_label: "On this page"
---

LaBGAS studies the two-way traffic between the gut and the brain in humans. Our common thread is
that bodily signals — mechanical, chemical, nutritional, immune and microbial — do not simply
report on the state of the body; they shape perception, appetite and affect, and they do so
through mechanisms we can measure and manipulate experimentally.

Three research lines organise that work. They overlap heavily in method and in people.

## Gastrointestinal/bodily symptom perception

Why do some people experience severe, disabling gastrointestinal symptoms with little or no
detectable organic abnormality, while others with clear pathology report almost nothing? This
line studies the psychobiological mechanisms underlying symptom perception in disorders of
gut-brain interaction (DGBI) — irritable bowel syndrome, functional dyspepsia, refractory
reflux — and in related functional somatic syndromes.

We combine controlled chemical and mechanical stimulation of the gut with functional brain
imaging, psychophysiology and experimental psychological manipulations such as emotion
induction, fear conditioning and attentional focus. Recurring themes include visceral
hypersensitivity, interoceptive fear learning, hypervigilance, and the relative contribution of
physiological versus psychological processes to symptom severity.

This line also covers fatigue — in ME/CFS and in inflammatory bowel disease — and the
sleep-pain relationship in chronic low back pain.

## Appetite, food intake & reward

This line investigates how gastrointestinal signals act on the homeostatic and hedonic brain
circuits that regulate appetite, feeding behaviour and ultimately body weight.

We deliver nutrients and tastants directly to the stomach or duodenum — often below the
threshold of conscious perception — and measure the consequences for gut hormone release, brain
responses, subjective appetite, emotion and food intake. Neurotransmitter systems including
dopamine, opioids and endocannabinoids are studied with PET and simultaneous PET-MR imaging.

Applied questions include whether non-caloric sweeteners such as erythritol can reproduce the
satiating and rewarding properties of sugar, what changes in food reward after bariatric
surgery, and how to select patients for GLP-1-based pharmacotherapy across the binge-eating
spectrum.

## Microbiota, gut signals & the mind

Our most recent line asks how nutrient- and microbiota-derived signals from the gut influence
psychological processes and their neural basis — particularly the response to psychosocial
stress, fear learning and extinction, executive function, and affect.

The flagship project is **MoodBugs**, funded by an ERC Consolidator Grant, which tests
short-chain fatty acids and inflammation as mediators of human microbiota-affect relationships.
Related work examines butyrate as an epigenetic modulator of fear memory, probiotic effects on
academic stress, and the role of microbial metabolites in anorexia nervosa.

---

## Projects

{% assign line_ids = "symptoms,appetite,microbiota" | split: "," %}
{% assign line_names = "Symptom perception projects|Appetite &amp; reward projects|Microbiota &amp; mind projects" | split: "|" %}

{% for lid in line_ids %}
{% assign idx = forloop.index0 %}
### {{ line_names[idx] }}

{% assign items = site.data.projects.projects | where: "line", lid %}
{% for p in items %}
<div class="project{% if p.featured %} is-featured{% endif %}">
  <h3 id="{{ p.name | slugify }}">{{ p.name }}</h3>
  {% if p.tagline %}<p class="project__tagline">{{ p.tagline }}</p>{% endif %}
  <p>{{ p.summary }}</p>
  {% if p.funder or p.period %}
  <p class="project__meta">
    {%- if p.funder %}{{ p.funder }}{% endif -%}
    {%- if p.funder and p.period %} · {% endif -%}
    {%- if p.period %}{{ p.period }}{% endif -%}
  </p>
  {% endif %}
</div>
{% endfor %}
{% endfor %}

---

## Methods

Our studies draw on a shared methodological toolkit:

- **Gut stimulation** — intragastric and intraduodenal infusion of nutrients, fatty acids,
  bitter tastants and sweeteners; gastric and rectal barostat distension; oesophageal acid
  perfusion.
- **Brain imaging** — task and resting-state fMRI, H₂¹⁵O and receptor PET
  (cannabinoid-1, opioid, dopamine), simultaneous PET-MR, and MR spectroscopy.
- **Psychophysiology** — autonomic nervous system measures, cortisol and neuroendocrine stress
  responses, interoceptive accuracy paradigms.
- **Interventions** — dietary challenges (FODMAP, gluten, sweeteners), probiotics and
  prebiotics, colonic short-chain fatty acid administration, pharmacological probes.
- **Analysis** — multivariate pattern analysis, predictive modelling and brain signature
  approaches, built on [CANlab tools](https://canlab.github.io/) and documented in our
  [pipeline docs]({{ '/docs/' | relative_url }}).

For the software behind the analyses, see [Tools]({{ '/tools/' | relative_url }}).
