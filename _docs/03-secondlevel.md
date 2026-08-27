---
title: "3 · Second-level analysis"
permalink: /docs/secondlevel/
excerpt: "Group inference with the CANlab batch pipeline: contrasts, signature responses, multivariate prediction, and date-stamped HTML reports."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> CANlab, extended by LaBGAS</span>
  <span><strong>Repository</strong> CANlab_help_examples (fork)</span>
  <span><strong>Folder</strong> <code>Second_level_analysis_template_scripts/</code></span>
</div>

Group-level analysis runs on the CANlab batch system, in our
[fork of CANlab_help_examples](https://github.com/labgas/CANlab_help_examples). The
multivariate pipelines that sit alongside it — PLS-DA, PLSR, Elastic Net — are ours and live in
[LaBGAScore `secondlevel/`](https://github.com/labgas/LaBGAScore/tree/main/secondlevel).

<div class="canlab-note" markdown="1">
**This stage is mostly CANlab's.** The batch system, the object model and the report machinery
are documented at [canlab.github.io/batch](https://canlab.github.io/batch/) and
[canlab.github.io/docs](https://canlab.github.io/docs/). Read those alongside this page — what
follows is an orientation, not a replacement.
</div>

## The philosophy, briefly

The design goals behind the batch system explain why it looks the way it does:

- **Interactive analysis** with reusable, well-vetted code rather than one-off scripts
- **Simple, readable scripts** that a reviewer or a future lab member can follow
- **Date-stamped HTML reports** carrying the figures, statistics and the code that produced
  them, archived as a durable record

That last point is the one that matters most in practice. A result from eighteen months ago can
be inspected without re-running anything, and the report says exactly what was run.

## The five steps

**1 · Create the analysis folder and run setup.** Establishes the standard directory structure
the later scripts expect.

**2 · Edit the study configuration.** Study metadata, paths, behavioural data, condition names
and contrast definitions. This is where nearly all study-specific work happens — the rest of
the pipeline is designed to need no editing.

**3 · Prepare the data.** The `prep_*` scripts load first-level contrast images into
`fmri_data` objects, attach behavioural data, compute contrasts, and optionally apply published
signatures or run machine-learning analyses. Results are cached so later steps are fast.

**4 · Run results scripts on demand.** Lettered scripts (`c*`, `d*`, `f*`, `h*`, `k*`) produce
figures and tables — univariate maps, multivariate predictions, signature responses, network
decompositions. Each works independently once the data are prepared, so you can iterate on one
analysis without re-running everything.

**5 · Publish.** The `z_batch_*` scripts render the collection into date-stamped HTML.

## What comes out

Five families of report: contrasts, signature responses, support vector machine analyses,
network decomposition, and meta-analysis tests.

## Inference

Group inference uses threshold-free cluster enhancement with permutation testing, which avoids
committing to an arbitrary cluster-forming threshold. Published multivariate signatures from
[Neuroimaging_Pattern_Masks](https://github.com/canlab/Neuroimaging_Pattern_Masks) — NPS,
SIIPS, PINES and others — are applied as *a priori* measures, which is a considerably stronger
test than an exploratory whole-brain map.

## Our multivariate pipelines

Three pipelines in [LaBGAScore `secondlevel/`](https://github.com/labgas/LaBGAScore/tree/main/secondlevel),
each with its own usage guide in the repository and a page here:

| Pipeline | Use when | Page |
|---|---|---|
| **PLS-DA** | the outcome is categorical and you want a dense latent-variable solution | [PLS-DA]({{ '/docs/mvpa-plsda/' | relative_url }}) |
| **PLSR** | the outcome is continuous — symptom severity, ratings, hormone levels | [PLSR]({{ '/docs/mvpa-plsr/' | relative_url }}) |
| **Elastic Net** | the outcome is categorical and you want a sparse, feature-selecting solution | [Elastic Net]({{ '/docs/mvpa-enet/' | relative_url }}) |

All three share the same design: repeated nested cross-validation, fold-wise covariate
residualisation to avoid leakage, permutation testing, bootstrap confidence intervals, stability
metrics and learning curves. A paired variant of PLS-DA handles within-subject designs.

The repository organises these into `classes/`, `functions/` and `scripts/`, with README guides
covering both the neuroimaging pipeline and the plotting for each method.

---

**Next:** [PLS-DA]({{ '/docs/mvpa-plsda/' | relative_url }})
[Batch scripts](https://github.com/labgas/CANlab_help_examples){: .btn .btn--inverse}
[CANlab batch docs](https://canlab.github.io/batch/){: .btn .btn--inverse}
