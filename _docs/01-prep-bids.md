---
title: "1 · BIDS conversion & prep"
permalink: /docs/prep-bids/
excerpt: "Raw scanner output to analysis-ready inputs: BIDS conversion, fMRIPrep, event timing files and smoothing."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> LaBGAS</span>
  <span><strong>Folder</strong> <code>prep/</code></span>
  <span><strong>Scripts</strong> s0 – s3</span>
</div>

The prep stage turns what came off the scanner into something the first-level pipeline can
consume: a BIDS dataset, fMRIPrep derivatives, event timing files matched to the imaging runs,
and — where the analysis calls for it — smoothed images.

## What this stage produces

- A valid [BIDS](https://bids.neuroimaging.io/) dataset under `BIDS/`
- fMRIPrep derivatives under `BIDS/derivatives/fmriprep/`
- Per-run **event timing files** (onsets, durations, conditions) in the format the first-level
  scripts expect
- Optionally, smoothed functional images

## Steps

### s0 · Define directories

`LaBGAScore_prep_s0_define_directories.m` — the entry point for the entire pipeline. Verifies
dependencies, resolves the study directory structure into variables, and configures the
environment. Adapt this for each study; everything downstream inherits from it.

See [Setup & dependencies]({{ '/docs/setup/' | relative_url }}) for the directory layout it
expects.

### s1 · BIDS conversion

Converts `sourcedata/` into a BIDS-compliant dataset. In practice this means resolving scanner
naming into BIDS entities (`sub-`, `ses-`, `task-`, `run-`), writing the sidecar JSON metadata,
and validating the result.

Validate before going further — fMRIPrep is unforgiving of malformed BIDS, and a problem caught
here costs minutes rather than a wasted preprocessing run.

### s2 · Event timing files

Behavioural output from the stimulus presentation software is converted into per-run event
files: onsets, durations and condition labels, aligned to the imaging runs.

This is the step most likely to need study-specific work, because it depends entirely on what
the paradigm logged. It is also the step where errors are most costly and least visible — a
misaligned onset produces a first-level model that runs perfectly and means nothing. Check a
subject's events against the raw log by hand before running the whole cohort.

### s3 · Smoothing

Applies spatial smoothing where the planned analysis requires it. Univariate group analyses
generally do; multivariate pattern analyses often deliberately do not, since smoothing discards
the fine-grained spatial information those methods exploit.

Keep smoothed and unsmoothed derivatives distinguishable, since later stages consume different
ones.

## Preprocessing with fMRIPrep

Preprocessing itself is [fMRIPrep](https://fmriprep.org/)'s job, run outside MATLAB on the
lab's Linux server. Its confound regressors are consumed at the
[first level]({{ '/docs/firstlevel/' | relative_url }}).

Read fMRIPrep's own [outputs documentation](https://fmriprep.org/en/stable/outputs.html) — which
confounds exist and what they mean is a modelling decision, not a detail.

<div class="canlab-note" markdown="1">
**Related CANlab material.** For loading and inspecting images once they exist, see the
[CANlab walkthroughs](https://canlab.github.io/walkthroughs/) and the
[object documentation](https://canlab.github.io/docs/) — particularly `fmri_data` and its
quality-control methods, which are worth running on prep output before modelling.
</div>

---

**Next:** [First-level models]({{ '/docs/firstlevel/' | relative_url }})
[Source: `prep/`](https://github.com/labgas/LaBGAScore/tree/main/prep){: .btn .btn--inverse}
