---
title: "2 · First-level models"
permalink: /docs/firstlevel/
excerpt: "Subject-level GLM with SPM and CANlab: design specification, estimation, contrasts and diagnostic reports."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> LaBGAS</span>
  <span><strong>Folder</strong> <code>firstlevel/</code></span>
  <span><strong>Depends on</strong> SPM12, CanlabCore</span>
</div>

The first level fits a general linear model to each subject's preprocessed time series, and
produces the contrast images that group analysis consumes.

## What this stage produces

- A specified and estimated SPM design per subject and model
- Contrast images, one set per subject, named consistently across the cohort
- Diagnostic reports for quality control before anything reaches the group level

## Design specification

The design is built from the event timing files created during
[prep]({{ '/docs/prep-bids/' | relative_url }}) together with fMRIPrep's confound regressors.
Decisions that matter here:

- **Which conditions are modelled**, and which are collapsed
- **Which confounds enter the model** — motion parameters, aCompCor components, framewise
  displacement, cosine drift terms. fMRIPrep offers far more than any single model should use;
  choose a defensible strategy and apply it uniformly across subjects
- **High-pass filtering and autocorrelation modelling**
- **Whether runs are concatenated** or modelled separately with run regressors

The model definition is study-specific, so this is expected to be adapted. Keep it in the
study's own repository so the choices are versioned alongside the results they produced.

## Estimation

Estimation is SPM's, driven from the LaBGAScore scripts so that the same model can be applied
across the cohort without hand-editing batch files per subject.

Contrasts are specified once, centrally, and applied to every subject — consistent contrast
naming is what makes the second-level scripts able to find images automatically. Renaming a
contrast midway through a cohort is a reliable way to lose an afternoon.

## Diagnostics

Run diagnostics before group analysis, not after a result looks odd. Worth inspecting:

- **Design matrix** — collinearity between regressors, particularly between conditions of
  interest and motion
- **Model fit** — residual structure, variance explained
- **Motion** — per-subject summaries, and an explicit, pre-registered exclusion rule applied
  uniformly
- **Contrast images** — visual inspection for coverage dropout, especially in ventral regions,
  which matters for the gut-brain circuitry we study

CanlabCore's `fmri_data` methods are useful here — see the
[CANlab object documentation](https://canlab.github.io/docs/) and the quality-control material
in the [walkthroughs](https://canlab.github.io/walkthroughs/).

<div class="canlab-note" markdown="1">
**CANlab equivalents.** CanlabCore has its own first-level machinery, including the `fmri_model`
object and `canlab_glm_*` batch tools, documented at
[canlab.github.io/docs](https://canlab.github.io/docs/). LaBGAScore's first-level scripts wrap
SPM directly to fit our BIDS/fMRIPrep conventions, then hand off to CANlab objects from the
second level onward.
</div>

## Handing off to the group level

The second-level scripts expect to find contrast images in a predictable location with
predictable names. Getting that right at the first level is what makes
[second-level analysis]({{ '/docs/secondlevel/' | relative_url }}) close to configuration-only.

---

**Next:** [Second-level analysis]({{ '/docs/secondlevel/' | relative_url }})
[Source: `firstlevel/`](https://github.com/labgas/LaBGAScore/tree/main/firstlevel){: .btn .btn--inverse}
