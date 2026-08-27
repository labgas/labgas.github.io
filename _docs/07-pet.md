---
title: "PET"
permalink: /docs/pet/
excerpt: "PET-specific workflows including kinetic modelling, for receptor imaging and simultaneous PET-MR studies."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> LaBGAS</span>
  <span><strong>Folder</strong> <code>pet/</code></span>
  <span><strong>Repository</strong> LaBGAScore</span>
</div>

PET is central to our [appetite and food reward line]({{ '/research/#appetite-food-intake--reward' | relative_url }}),
where we image neurotransmitter systems — dopamine, opioid and endocannabinoid — that fMRI
cannot address. The `pet/` folder holds the PET-specific workflows, including kinetic modelling.

## Where PET differs from the fMRI pipeline

PET data need their own handling before they reach anything resembling the second-level stage:

- **Kinetic modelling** to derive the parameter of interest — binding potential, volume of
  distribution — from the dynamic time-activity data, rather than fitting a GLM to a BOLD time
  series
- **Input functions**, whether arterial or reference-region based
- **Attenuation correction and motion correction** over acquisitions long enough that subject
  movement is a certainty
- **Partial volume effects**, which matter more at PET's resolution than at fMRI's

The output is a parametric image per subject. From that point the second-level machinery
applies as it does for fMRI: the images become `fmri_data` objects and go through the same
group inference and multivariate pipelines.

## Simultaneous PET-MR

For simultaneous PET-MR acquisitions, the two modalities are preprocessed on their own terms and
then brought into a common space, allowing the receptor measure and the BOLD response to be
related within the same session and the same participant.

## Multivariate analysis of PET data

The [PLSR]({{ '/docs/mvpa-plsr/' | relative_url }}) pipeline explicitly supports PET feature
matrices — its usage guide names PET alongside fMRI, cortical thickness and connectivity as
input types. Parametric PET images are well suited to it: strongly correlated features, modest
sample sizes.

For relating spatial patterns to receptor distributions, see
[JuSpace]({{ '/docs/connectivity-rsa/' | relative_url }}).

{: .notice--info}
This page is an orientation rather than a manual. Scripts, exact model implementations and their
options are in the repository, which is the source of truth.

---

**Next:** [MR spectroscopy]({{ '/docs/mrs/' | relative_url }})
[Source: `pet/`](https://github.com/labgas/LaBGAScore/tree/main/pet){: .btn .btn--inverse}
