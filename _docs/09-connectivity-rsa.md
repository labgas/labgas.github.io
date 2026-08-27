---
title: "Connectivity & RSA"
permalink: /docs/connectivity-rsa/
excerpt: "Representational similarity analysis, decoding accuracy, graph-theoretical connectivity and receptor-spatial correlation."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> LaBGAS</span>
  <span><strong>Folders</strong> <code>cosmomvpa/</code> <code>decoding_toolbox/</code> <code>graphvar/</code> <code>juspace/</code></span>
</div>

Four folders in LaBGAScore wrap external toolboxes, each answering a question the core pipeline
does not. All four dependencies are installed separately.

## Representational similarity analysis — `cosmomvpa/`

Built on [**CoSMoMVPA**](https://www.cosmomvpa.org/). RSA asks whether the *geometry* of neural
responses matches a hypothesised structure: are conditions that are conceptually similar also
represented similarly in the brain?

Rather than testing whether a region responds more to A than B, RSA compares the full pattern of
pairwise dissimilarities against candidate models. This suits questions about how classes of
sensation relate to one another — for instance whether visceral and somatic stimulation share a
representational structure, or whether interoceptive signals from different organs converge.

Searchlight analyses map representational structure across the brain rather than testing
predefined regions.

## Decoding accuracy — `decoding_toolbox/`

Built on [**The Decoding Toolbox**](https://sites.google.com/site/tdtdecodingtoolbox/) (TDT).
Where our [PLS-DA]({{ '/docs/mvpa-plsda/' | relative_url }}) and
[Elastic Net]({{ '/docs/mvpa-enet/' | relative_url }}) pipelines are built for whole-brain
prediction with full inference machinery, TDT is oriented toward classification accuracy maps —
particularly searchlight decoding, where a classifier is trained at every location.

Use TDT when the question is *where* information is present; use the LaBGAScore pipelines when
the question is whether a distributed pattern predicts an outcome, and how reliably.

## Graph-theoretical connectivity — `graphvar/`

Generates inputs for [**GraphVar**](https://www.nitrc.org/projects/graphvar/), which computes
graph-theoretical measures on brain connectivity data — degree, clustering coefficient, path
length, modularity and related metrics.

Two choices dominate the results and should be made and reported explicitly: the **parcellation**
defining the nodes, and the **thresholding** applied to the connectivity matrix. Both change the
graph metrics substantially.

This pipeline produced the analyses in
[`proj-IBS-somatization`](https://github.com/labgas/proj-IBS-somatization).

## Receptor-spatial correlation — `juspace/`

Built on [**JuSpace**](https://github.com/juryxy/JuSpace). Tests whether a spatial brain map —
a group difference, a multivariate weight map, a PET parametric image — correlates with the
distribution of specific neurotransmitter receptors and transporters, derived from independent
PET atlases.

This is a way to give a spatial result a neurochemical interpretation: if a pattern tracks
serotonergic or dopaminergic receptor density, that constrains what mechanism might produce it.
Because brain maps are spatially autocorrelated, the null model matters — spatial
autocorrelation-preserving nulls, rather than naive permutation of voxels.

<div class="canlab-note" markdown="1">
**Overlap with CANlab tools.** CanlabCore provides `atlas` objects, region-based extraction and
connectivity utilities, plus the multivariate signatures in
[Neuroimaging_Pattern_Masks](https://github.com/canlab/Neuroimaging_Pattern_Masks). For many
questions the CANlab machinery is sufficient and better integrated with the rest of the
pipeline — see the [object docs](https://canlab.github.io/docs/). Reach for these external
toolboxes when you need something they specifically provide.
</div>

---

**Next:** [Atlases & masks]({{ '/docs/atlases-masks/' | relative_url }})
[Source on GitHub](https://github.com/labgas/LaBGAScore){: .btn .btn--inverse}
