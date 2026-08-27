---
title: "Setup & dependencies"
permalink: /docs/setup/
excerpt: "What to install, how the MATLAB path is arranged, and the directory conventions every LaBGAScore script assumes."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> LaBGAS + CANlab</span>
  <span><strong>Repository</strong> LaBGAScore</span>
  <span><strong>Language</strong> MATLAB</span>
</div>

Before any pipeline stage will run, three things have to be true: the dependencies are installed
and on the MATLAB path, the study directory follows the expected layout, and the path-definition
script has been adapted for the study.

<div class="canlab-note" markdown="1">
**Install and read the CANlab tools first.** Follow the
[CANlab setup guide](https://canlab.github.io/setup/) — it covers cloning the repositories,
path configuration and the common pitfalls. Then read
[why interactive analysis](https://canlab.github.io/objectoriented/), which explains the object
model that everything below is written against.
</div>

## Required dependencies

| Dependency | Why |
|---|---|
| [MATLAB](https://mathworks.com/) with Statistics & Machine Learning and Signal Processing toolboxes | The pipelines are MATLAB throughout |
| [SPM12](https://www.fil.ion.ucl.ac.uk/spm/) | First-level model specification and estimation |
| [CanlabCore](https://github.com/canlab/CanlabCore) | The object model (`fmri_data`, `statistic_image`, `atlas`, …) and the analysis and plotting methods |
| [Neuroimaging_Pattern_Masks](https://github.com/canlab/Neuroimaging_Pattern_Masks) | Atlases, parcellations, and published multivariate signatures |
| [LaBGAScore](https://github.com/labgas/LaBGAScore) | Our scripts and templates |
| [CANlab_help_examples](https://github.com/labgas/CANlab_help_examples) | The second-level batch pipeline and reporting |

## Optional, per analysis domain

Install these only when the corresponding pipeline is used:
[CoSMoMVPA](https://www.cosmomvpa.org/) (RSA),
[The Decoding Toolbox](https://sites.google.com/site/tdtdecodingtoolbox/) (classification
accuracy), [GraphVar](https://www.nitrc.org/projects/graphvar/) (graph-theoretical connectivity),
[JuSpace](https://github.com/juryxy/JuSpace) (receptor–spatial correlation), and
[Osprey](https://github.com/schorschinho/osprey) (MR spectroscopy).

## Preprocessing and data management

Functional data are preprocessed with [fMRIPrep](https://fmriprep.org/) on
[BIDS](https://bids.neuroimaging.io/)-formatted input. Code and data are version-controlled with
[DataLad](https://www.datalad.org/), built on git and git-annex, with code pushed to GitHub and
data to [GIN](https://gin.g-node.org/).

Analyses run on the lab's shared Linux server rather than on individual machines.

## Directory conventions

LaBGAScore assumes a consistent layout so that path-definition happens once and every downstream
script inherits it. In outline:

```
<study_root>/
├── code/          study-specific copy of the adapted LaBGAScore scripts
├── sourcedata/    raw data as it came off the scanner
├── BIDS/          BIDS-converted data
│   └── derivatives/
│       └── fmriprep/
├── firstlevel/    per-model subject-level results
└── secondlevel/   group-level results and HTML reports
```

## Path definition

Each study starts from `LaBGAScore_prep_s0_define_directories.m`, adapted for that study. It
verifies the dependencies are present, resolves the directory structure above into variables,
and configures the environment. Every later script expects to be run after it.

This is the one script you should expect to edit for every new study.

## Getting the code

LaBGAScore is **copied into a study repository and adapted**, not added to the path and called.
The scripts are canonical templates; numbered prefixes (`s0`, `s1`, `s2` …) mark pipeline order.
This means each study's analysis code is versioned with that study, rather than silently
drifting against a shared library.

```bash
git clone https://github.com/labgas/LaBGAScore.git
git clone https://github.com/labgas/CANlab_help_examples.git
git clone https://github.com/canlab/CanlabCore.git
git clone https://github.com/canlab/Neuroimaging_Pattern_Masks.git
```

## Checking your scripts

`LaBGAScore_check_all_scripts.m` runs MATLAB's Code Analyzer over every script in the
repository. It catches syntax errors and style problems. It does **not** catch undefined
variables or logic errors, so it complements code review rather than replacing it.

---

**Next:** [BIDS conversion & prep]({{ '/docs/prep-bids/' | relative_url }})
[Source on GitHub](https://github.com/labgas/LaBGAScore){: .btn .btn--inverse}
