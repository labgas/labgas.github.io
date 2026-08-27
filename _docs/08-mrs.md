---
title: "MR spectroscopy"
permalink: /docs/mrs/
excerpt: "MRS processing built on Osprey, for quantifying neurometabolites such as glutamate and GABA."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> LaBGAS</span>
  <span><strong>Folder</strong> <code>mrs/</code></span>
  <span><strong>Depends on</strong> Osprey</span>
</div>

Magnetic resonance spectroscopy quantifies neurometabolite concentrations — glutamate, GABA,
glutamine, NAA and others — within a defined voxel. It answers a different question from fMRI:
not where activity changes, but what the local neurochemistry is.

The `mrs/` workflows are built on [**Osprey**](https://github.com/schorschinho/osprey), an open
MRS analysis toolbox, which must be installed separately and added to the MATLAB path.

## The workflow in outline

1. **Load** raw spectroscopy data and the associated structural scan
2. **Process** — coil combination, frequency and phase correction, eddy-current correction,
   averaging
3. **Fit** the spectrum to a basis set to estimate metabolite concentrations
4. **Segment and co-register** the voxel against the structural image, so tissue composition is
   known
5. **Quantify**, correcting for the grey matter, white matter and CSF fractions within the voxel
6. **Export** to a table for statistical analysis

Step 5 is not optional. A voxel containing more CSF has less tissue to generate signal, so
uncorrected concentrations partly reflect voxel placement rather than neurochemistry — and voxel
placement varies systematically with brain morphology, which can differ between the groups being
compared.

## Quality control

Osprey reports linewidth, signal-to-noise ratio and fit residuals. Set exclusion criteria in
advance and apply them uniformly. Spectral quality varies more between subjects than fMRI data
quality does, and deciding what to exclude after seeing the group results is not a decision you
can defend.

## Downstream

MRS output is typically a small table of metabolite concentrations per subject and voxel, which
goes into conventional statistical models rather than the imaging pipelines. Where MRS is
combined with fMRI or PET in the same study, the metabolite measure usually enters as a
predictor or covariate.

{: .notice--info}
Consult [Osprey's own documentation](https://schorschinho.github.io/osprey/) for the processing
and fitting detail; the `mrs/` scripts handle our study conventions around it.

---

**Next:** [Connectivity & RSA]({{ '/docs/connectivity-rsa/' | relative_url }})
[Source: `mrs/`](https://github.com/labgas/LaBGAScore/tree/main/mrs){: .btn .btn--inverse}
