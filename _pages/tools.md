---
layout: single
title: "Tools"
permalink: /tools/
author_profile: false
toc: true
toc_sticky: true
toc_label: "On this page"
---

Everything we use to analyse our data is developed in the open at
[github.com/labgas](https://github.com/labgas). Two repositories hold the reusable methods; the
rest are study-specific code released alongside papers.

<div class="canlab-note" markdown="1">
**Built on CANlab tools.** Our neuroimaging code is a layer *on top of* the toolset developed by
the [Cognitive and Affective Neuroscience Lab (CANlab)](https://canlab.github.io/), not a
replacement for it. Nothing here runs without
[CanlabCore](https://github.com/canlab/CanlabCore) and
[Neuroimaging_Pattern_Masks](https://github.com/canlab/Neuroimaging_Pattern_Masks) on the MATLAB
path, alongside [SPM12](https://www.fil.ion.ucl.ac.uk/spm/).

If you are new to this ecosystem, read the CANlab material first — the
[setup guide](https://canlab.github.io/setup/), the
[object-oriented analysis philosophy](https://canlab.github.io/objectoriented/), the
[object and method docs](https://canlab.github.io/docs/), and the
[walkthroughs](https://canlab.github.io/walkthroughs/). Our
[pipeline documentation]({{ '/docs/' | relative_url }}) assumes it.
</div>

## Who owns which layer

It is worth being explicit about where the boundary sits, because the two codebases are used
together constantly.

| Layer | Provided by | What it covers |
|---|---|---|
| Object model and core methods | **CANlab** — [CanlabCore](https://github.com/canlab/CanlabCore) | `fmri_data`, `statistic_image`, `atlas`, `fmri_model` and friends; plotting, thresholding, predictive modelling machinery |
| Brain masks, atlases, signatures | **CANlab** — [Neuroimaging_Pattern_Masks](https://github.com/canlab/Neuroimaging_Pattern_Masks) | Published multivariate signatures (NPS, SIIPS, PINES …), parcellations, region masks |
| Second-level batch pipeline & HTML reporting | **CANlab**, extended in our fork — [CANlab_help_examples](https://github.com/labgas/CANlab_help_examples) | `prep_*` and `z_batch_*` scripts, date-stamped report collections |
| Study initialisation, BIDS prep, first-level modelling | **LaBGAS** — [LaBGAScore](https://github.com/labgas/LaBGAScore) | Directory conventions, BIDS conversion, event timing, SPM first-level specification and diagnostics |
| PLS-DA / PLSR / Elastic Net neuroimaging pipelines | **LaBGAS** — [LaBGAScore](https://github.com/labgas/LaBGAScore) | `secondlevel/` classes, functions and scripts with their own usage guides |
| PET, MRS, connectivity, receptor mapping | **LaBGAS** — [LaBGAScore](https://github.com/labgas/LaBGAScore) | Wrappers around Osprey, CoSMoMVPA, The Decoding Toolbox, GraphVar, JuSpace |

## LaBGAScore

[**github.com/labgas/LaBGAScore**](https://github.com/labgas/LaBGAScore) · MATLAB · GPL-3.0

The core scripts — and templates for them — implementing our standard neuroimaging workflow.
The repository is deliberately **not** a toolbox you add to your path and call. The scripts are
canonical examples meant to be copied into a study-specific repository and adapted there, which
keeps every project's analysis code versioned with that project rather than drifting against a
shared library.

Scripts carry numbered prefixes (`s0`, `s1`, `s2` …) marking the order of the pipeline stages.

| Folder | Purpose |
|---|---|
| `prep/` | BIDS conversion, directory definition, event timing files, smoothing |
| `firstlevel/` | SPM + CANlab GLM specification, estimation, diagnostic reports |
| `secondlevel/` | Group statistics and the MVPA/machine-learning pipelines, with seven usage guides |
| `stats_tools/` | FDR correction and related helpers in `functions/`, plus `sas_macros/` — SAS macros for effect sizes on the fixed effects of a `PROC MIXED` model |
| `atlas_mask_tools/` | Atlas and mask generation, plus ready-made brain templates |
| `pet/` | PET workflows including kinetic modelling |
| `mrs/` | MR spectroscopy, built on [Osprey](https://github.com/schorschinho/osprey) |
| `cosmomvpa/` | Representational similarity analysis via [CoSMoMVPA](https://www.cosmomvpa.org/) |
| `decoding_toolbox/` | Classification accuracy via [The Decoding Toolbox](https://sites.google.com/site/tdtdecodingtoolbox/) |
| `graphvar/` | Connectivity analysis inputs for [GraphVar](https://www.nitrc.org/projects/graphvar/) |
| `juspace/` | Receptor–spatial correlation via [JuSpace](https://github.com/juryxy/JuSpace) |
| `power/` | Power analysis helpers |
| `figures/` | Plotting utilities |
| `clean/` | Housekeeping |

A static-analysis helper, `LaBGAScore_check_all_scripts.m`, runs MATLAB's Code Analyzer across
every file in the repository. It catches syntax problems, but not undefined variables or logic
errors — code review is still required.

[Pipeline documentation]({{ '/docs/' | relative_url }}){: .btn .btn--primary}

## CANlab_help_examples (LaBGAS fork)

[**github.com/labgas/CANlab_help_examples**](https://github.com/labgas/CANlab_help_examples) ·
forked from [canlab/CANlab_help_examples](https://github.com/canlab/CANlab_help_examples)

Carries the batch pipeline for second-level analysis, in
`Second_level_analysis_template_scripts/`. Its design philosophy is worth stating because it
shapes how we work: interactive analysis using well-vetted, readable code, producing
**date-stamped HTML reports** with figures and statistics that are archived as a durable record
of what was run and when.

The workflow runs in five steps: create the analysis folder and run setup → edit the study
configuration files (paths, conditions, contrasts, behavioural data) → load images into
`fmri_data` objects and compute contrasts → run on-demand results scripts → run the
`z_batch_*` publishing scripts to generate the report collection.

See the [second-level documentation]({{ '/docs/secondlevel/' | relative_url }}) and the
[CANlab batch system pages](https://canlab.github.io/batch/).

## Dependencies

Installed separately and added to the MATLAB path:

**Required** — [CanlabCore](https://github.com/canlab/CanlabCore),
[Neuroimaging_Pattern_Masks](https://github.com/canlab/Neuroimaging_Pattern_Masks),
[SPM12](https://www.fil.ion.ucl.ac.uk/spm/), MATLAB with the Statistics and Machine Learning and
Signal Processing toolboxes.

**Per-domain** — [CoSMoMVPA](https://www.cosmomvpa.org/),
[The Decoding Toolbox](https://sites.google.com/site/tdtdecodingtoolbox/),
[GraphVar](https://www.nitrc.org/projects/graphvar/),
[JuSpace](https://github.com/juryxy/JuSpace),
[Osprey](https://github.com/schorschinho/osprey).

**Preprocessing and data management** — [fMRIPrep](https://fmriprep.org/),
[BIDS](https://bids.neuroimaging.io/), [DataLad](https://www.datalad.org/) with
[GIN](https://gin.g-node.org/) for data hosting.

Start with [Setup & dependencies]({{ '/docs/setup/' | relative_url }}).

## All repositories

{% assign methods = site.data.repos.repos | where: "category", "methods" %}
{% assign studies = site.data.repos.repos | where: "category", "study" %}

### Methods

<table class="repo-table">
<thead><tr><th>Repository</th><th>Language</th><th>Description</th></tr></thead>
<tbody>
{% for r in methods %}
<tr>
  <td><a href="https://github.com/labgas/{{ r.name }}"><code>{{ r.name }}</code></a></td>
  <td>{% if r.lang %}<span class="lang-tag">{{ r.lang }}</span>{% endif %}</td>
  <td>{{ r.desc }}</td>
</tr>
{% endfor %}
</tbody>
</table>

### Study code

Code — and in some cases data — released alongside specific projects and papers.

<table class="repo-table">
<thead><tr><th>Repository</th><th>Language</th><th>Description</th></tr></thead>
<tbody>
{% for r in studies %}
<tr>
  <td><a href="https://github.com/labgas/{{ r.name }}"><code>{{ r.name }}</code></a></td>
  <td>{% if r.lang %}<span class="lang-tag">{{ r.lang }}</span>{% endif %}</td>
  <td>{{ r.desc }}</td>
</tr>
{% endfor %}
</tbody>
</table>

{: .notice--info}
This index was compiled on {{ site.data.repos.compiled }}. The organisation page at
[github.com/labgas](https://github.com/labgas) is always authoritative.
