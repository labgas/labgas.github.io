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

## Gastrointestinal symptom, pain, and fatigue perception

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

### Fatigue

Fatigue has grown into a substantial strand of this line in its own right, led by
[Maaike Van Den Houte]({{ '/team/#maaike-van-den-houte' | relative_url }}).

Two research traditions have approached fatigue separately and largely without talking to each
other. One documents dysfunction in (psycho)physiological systems — the stress response system,
including the hypothalamic-pituitary-adrenal axis and the autonomic nervous system; the immune
system and systemic inflammation; and the central nervous system, including neuroinflammation
and altered functional connectivity. The other, from health psychology, documents distortions in
how bodily sensations are perceived and interpreted. Our work integrates the two, on the premise
that neither alone accounts for why fatigue is experienced as severely as it is.

In **myalgic encephalomyelitis/chronic fatigue syndrome**, which affects roughly 20,000 people
in Belgium, we test an integrative psychophysiological model and use it to identify
[subgroups]({{ '/research/#biopsychosocial-mechanisms-of-chronic-fatigue-syndrome' | relative_url }})
defined by combinations of these parameters — subgroups intended to be clinically useful as
predictors of who responds to which rehabilitation approach.

In **inflammatory bowel disease**, fatigue is a common and disabling comorbidity that current
anti-inflammatory treatment does not resolve: around half of patients in clinical remission
remain fatigued. That dissociation between inflammation and symptom is the starting point for
our work on the
[gut-immune-brain axis]({{ '/research/#gut-immune-brain-axis-in-ibd-fatigue' | relative_url }}),
which asks what maintains fatigue once the gut has healed, and treats the immune-brain axis as a
moderator of fatigue perception rather than simply its cause.

Related work in this line examines the bidirectional
[sleep-pain relationship]({{ '/research/#sy-naps' | relative_url }}) in chronic low back pain,
and the role of neuroinflammation and microglia within it.

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
{%- comment -%}
  Harvested detail wins over the hand-written funder/period: the project pages
  name the actual funding body where our summary line only had the category.
{%- endcomment -%}
{% assign period = p.detail.duration | default: p.period %}
{% assign funder = p.detail.funding | default: p.funder %}
{% assign has_detail = false %}
{% if p.detail.description or p.detail.investigators or p.detail.team %}{% assign has_detail = true %}{% endif %}

{% if has_detail %}
<details class="project{% if p.featured %} is-featured{% endif %}" id="{{ p.name | slugify }}">
  <summary>
    <h3 class="project__name no_toc">{{ p.name }}</h3>
    {% if p.tagline %}<span class="project__tagline">{{ p.tagline }}</span>{% endif %}
    <span class="project__summary">{{ p.summary }}</span>
    {% if funder or period %}
    <span class="project__meta">
      {%- if funder %}{{ funder }}{% endif -%}
      {%- if funder and period %} · {% endif -%}
      {%- if period %}{{ period }}{% endif -%}
    </span>
    {% endif %}
  </summary>
  <div class="project__detail">
    {% for para in p.detail.description %}<p>{{ para }}</p>{% endfor %}

    {% if p.detail.investigators or p.detail.team or p.detail.collaborators %}
    <dl class="project__people">
      {% if p.detail.investigators %}<dt>Principal investigators</dt><dd>{{ p.detail.investigators }}</dd>{% endif %}
      {% if p.detail.team %}<dt>Team</dt><dd>{{ p.detail.team }}</dd>{% endif %}
      {% if p.detail.collaborators %}<dt>Collaborators</dt><dd>{{ p.detail.collaborators }}</dd>{% endif %}
    </dl>
    {% endif %}

    {% if p.detail.publications %}
    <p class="project__pubs-label">Key publications</p>
    <ul class="project__pubs">
      {% for ref in p.detail.publications %}<li>{{ ref }}</li>{% endfor %}
    </ul>
    {% endif %}
  </div>
</details>
{% else %}
<div class="project{% if p.featured %} is-featured{% endif %}" id="{{ p.name | slugify }}">
  <h3 class="project__name no_toc">{{ p.name }}</h3>
  {% if p.tagline %}<p class="project__tagline">{{ p.tagline }}</p>{% endif %}
  <p class="project__summary">{{ p.summary }}</p>
  {% if funder or period %}
  <p class="project__meta">
    {%- if funder %}{{ funder }}{% endif -%}
    {%- if funder and period %} · {% endif -%}
    {%- if period %}{{ period }}{% endif -%}
  </p>
  {% endif %}
</div>
{% endif %}
{% endfor %}
{% endfor %}

<script>
// Open a project when linked to directly — from a team member's project chip,
// or from a shared link. Browsers scroll to a <details> by id but do not expand
// it, so do that here. Progressive enhancement: without JS the anchor still
// scrolls to the right project, it just stays collapsed.
(function () {
  function openTarget() {
    var id = decodeURIComponent(window.location.hash.slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (el && el.tagName === 'DETAILS' && !el.open) {
      el.open = true;
      el.scrollIntoView({ block: 'start' });
    }
  }
  window.addEventListener('hashchange', openTarget);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', openTarget);
  } else {
    openTarget();
  }
})();
</script>

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
