---
title: "A new home for LaBGAS on the web"
date: 2026-08-27
categories:
  - lab
tags:
  - website
  - open science
excerpt: "One place for our research, our people and — for the first time — proper documentation of the analysis code we build."
---

This site brings together things that were previously scattered: a description of what the lab
actually works on, who is in it, and documentation for the analysis code we develop and release.

That last part is the reason for building it. The
[labgas GitHub organisation](https://github.com/labgas) holds two dozen repositories — two
carrying reusable methods, the rest study-specific code released alongside papers — with no index
and no entry point. Useful code that nobody outside the lab could find, and that new lab members
learned by asking someone.

The [pipeline documentation]({{ '/docs/' | relative_url }}) now walks through a study from raw
scanner output to archived result reports: BIDS conversion and prep, first-level modelling,
second-level analysis with the CANlab batch system, and our PLS-DA, PLSR and Elastic Net
pipelines, plus PET, MR spectroscopy, connectivity and atlas tooling.

Throughout, we have tried to be explicit about what is ours and what is not. Our neuroimaging
code sits on top of the toolset built by the
[Cognitive and Affective Neuroscience Lab](https://canlab.github.io/) — `CanlabCore`,
`Neuroimaging_Pattern_Masks`, and the second-level batch system. LaBGAScore is a layer, not a
replacement, and the docs link out to the CANlab material rather than restating it.

The [Tools page]({{ '/tools/' | relative_url }}) indexes every repository in the organisation,
and includes a table setting out which layer of the stack comes from where.

Corrections and additions are welcome at
[lukas.vanoudenhove@kuleuven.be](mailto:lukas.vanoudenhove@kuleuven.be).
