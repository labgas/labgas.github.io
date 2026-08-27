---
layout: single
title: "Pipeline documentation"
permalink: /docs/
author_profile: false
sidebar:
  nav: "docs"
toc: true
toc_sticky: true
toc_label: "On this page"
---

How a LaBGAS neuroimaging study goes from raw scanner output to a set of archived, date-stamped
result reports. Each page below covers one stage: what it is for, what it consumes and produces,
the canonical scripts involved, and where to read further.

<div class="canlab-note" markdown="1">
**Read the CANlab documentation first.** These pages describe *our* layer. The object model,
the methods, and most of the underlying machinery are CANlab's, and are documented far more
thoroughly at [canlab.github.io](https://canlab.github.io/):
[Setup](https://canlab.github.io/setup/) ·
[Interactive fMRI philosophy](https://canlab.github.io/objectoriented/) ·
[Object & method docs](https://canlab.github.io/docs/) ·
[Walkthroughs](https://canlab.github.io/walkthroughs/) ·
[Batch system](https://canlab.github.io/batch/)

Where a CANlab walkthrough already covers something, we link to it rather than restate it.
</div>

## How the pipeline fits together

```
raw DICOM
   │
   ├─ prep/          BIDS conversion → fMRIPrep → event timing files → smoothing
   │
   ├─ firstlevel/    SPM + CANlab GLM per subject → contrast images → diagnostics
   │
   └─ secondlevel/   group inference, MVPA, signature responses
                     │
                     └─ CANlab batch system → date-stamped HTML reports
```

Everything upstream of `secondlevel/` is owned by
[LaBGAScore](https://github.com/labgas/LaBGAScore). Second-level analysis is a mix: the batch
machinery and reporting come from the
[CANlab_help_examples fork](https://github.com/labgas/CANlab_help_examples), while the
multivariate pipelines (PLS-DA, PLSR, Elastic Net) are ours.

## Working principles

A few conventions shape all of the below, and are worth knowing before you start.

**Scripts are templates, not a library.** LaBGAScore is copied into a study repository and
adapted. Numbered prefixes (`s0`, `s1`, `s2` …) mark pipeline order. This keeps analysis code
versioned with the study it belongs to.

**Reports are the deliverable.** Analyses end in date-stamped HTML containing the figures,
statistics and the code that produced them. The point is that a result can be traced back months
later without re-running anything.

**Data lives under version control.** [DataLad](https://www.datalad.org/) — built on git and
git-annex — tracks both code and data, with code pushed to GitHub and data to
[GIN](https://gin.g-node.org/).

**Analyses run on a shared Linux server**, not on laptops.

## Pages

| Stage | Page |
|---|---|
| Prerequisites, paths, conventions | [Setup & dependencies]({{ '/docs/setup/' | relative_url }}) |
| 1 · Raw data → BIDS → prepared inputs | [BIDS conversion & prep]({{ '/docs/prep-bids/' | relative_url }}) |
| 2 · Subject-level GLM | [First-level models]({{ '/docs/firstlevel/' | relative_url }}) |
| 3 · Group inference & reporting | [Second-level analysis]({{ '/docs/secondlevel/' | relative_url }}) |
| Classification | [PLS-DA]({{ '/docs/mvpa-plsda/' | relative_url }}) |
| Continuous prediction | [PLSR]({{ '/docs/mvpa-plsr/' | relative_url }}) |
| Regularised regression | [Elastic Net]({{ '/docs/mvpa-enet/' | relative_url }}) |
| Receptor and kinetic imaging | [PET]({{ '/docs/pet/' | relative_url }}) |
| Metabolite quantification | [MR spectroscopy]({{ '/docs/mrs/' | relative_url }}) |
| Networks and representational similarity | [Connectivity & RSA]({{ '/docs/connectivity-rsa/' | relative_url }}) |
| Parcellations, masks, signatures | [Atlases & masks]({{ '/docs/atlases-masks/' | relative_url }}) |

{: .notice--warning}
These pages summarise the repository as it stood when they were written. For anything
operational — exact arguments, current script names — treat
[the repository](https://github.com/labgas/LaBGAScore) as the source of truth.
