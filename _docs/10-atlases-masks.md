---
title: "Atlases & masks"
permalink: /docs/atlases-masks/
excerpt: "Atlas and mask generation, ready-made brain templates, and the CANlab pattern masks that underpin signature analyses."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> LaBGAS + CANlab</span>
  <span><strong>Folder</strong> <code>atlas_mask_tools/</code></span>
  <span><strong>Depends on</strong> Neuroimaging_Pattern_Masks</span>
</div>

`atlas_mask_tools/` holds atlas and mask generation utilities together with ready-made brain
templates for the regions we return to repeatedly.

<div class="canlab-note" markdown="1">
**Most of what you need is already in CANlab.**
[Neuroimaging_Pattern_Masks](https://github.com/canlab/Neuroimaging_Pattern_Masks) is a large,
curated collection of parcellations, region masks and published multivariate signatures, and
CanlabCore's `atlas` object provides the methods for working with them — selecting regions,
combining atlases, extracting data. The
[CANlab atlas documentation](https://canlab.github.io/docs/) is the reference. Build a custom
mask only when nothing suitable exists.
</div>

## What we build on top

The tooling here covers the cases our work needs that a general atlas does not supply:

- **Study-specific ROI masks**, particularly for brainstem and hypothalamic regions central to
  gut-brain signalling — the nucleus of the solitary tract, for example, which is small enough
  that atlas choice materially affects whether an effect is detectable
- **Combining or restricting atlases** — intersecting a parcellation with a group-level mask so
  that regions with poor coverage do not silently contribute
- **Templates** for repeated use across studies, so the same anatomical definition is applied
  consistently rather than redrawn per project

## Coverage matters here

Ventral brain regions suffer signal dropout in EPI, and those are exactly the regions our
research lines care about. Two practical consequences:

- Check the **group coverage mask** before interpreting any ROI result. A region can appear
  null simply because half the subjects have no usable signal there.
- Restrict analyses to voxels with adequate coverage across subjects, and report the
  restriction.

## Signatures

Published multivariate signatures — NPS, SIIPS, PINES and others in
[Neuroimaging_Pattern_Masks](https://github.com/canlab/Neuroimaging_Pattern_Masks) — are applied
as *a priori* measures during
[second-level analysis]({{ '/docs/secondlevel/' | relative_url }}). Applying an established
signature is a far stronger test than an exploratory whole-brain search, because the pattern and
its interpretation were fixed before your data existed.

The batch pipeline produces a dedicated signature response report. See
[the CANlab batch documentation](https://canlab.github.io/batch/).

---

[Source: `atlas_mask_tools/`](https://github.com/labgas/LaBGAScore/tree/main/atlas_mask_tools){: .btn .btn--inverse}
[CANlab pattern masks](https://github.com/canlab/Neuroimaging_Pattern_Masks){: .btn .btn--inverse}
