---
title: "PLSR (regression)"
permalink: /docs/mvpa-plsr/
excerpt: "Partial Least Squares Regression for continuous outcomes, with repeated nested cross-validation and Freedman-Lane permutation testing."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> LaBGAS</span>
  <span><strong>Folder</strong> <code>secondlevel/</code></span>
  <span><strong>Guides</strong> README_PLSR_neuroimaging_pipeline.md, README_PLSR_plotting.md</span>
</div>

`PLSR_neuroimaging_pipeline` is the continuous-outcome counterpart to
[PLS-DA]({{ '/docs/mvpa-plsda/' | relative_url }}). Use it to predict a continuous variable —
symptom severity, a rating, a hormone level — from imaging features. It handles subjects ×
features matrices from fMRI, PET, cortical thickness or connectivity data.

## Inputs and outputs

**Inputs**

- `X` — `[n × p]` feature matrix, subjects × features
- `Y` — `[n × 1]` continuous outcome vector
- `opts.covariates` — optional `[n × nCov]` numeric covariate matrix

**Output** — a `results` structure.

## What the pipeline does

1. **Outer CV** — split into `outerK` folds, train on K−1, test on the held-out fold
2. **Inner CV** — within each training fold, evaluate `LV = 1…maxLV`; select the LV count with
   the highest inner-CV Q²
3. **Repeat** the outer procedure `nRepeats` times
4. **Preprocessing** — residualise covariates fold-wise, then z-score, at every resampling stage
5. **Permutation testing** using the **Freedman-Lane** scheme
6. **Bootstrap** out-of-bag confidence intervals across `nBoot` resamples
7. **Learning curves** across `learningSteps` subsample sizes

Freedman-Lane matters when covariates are in the model: it permutes the residuals of the
outcome after regressing out nuisance variables, rather than permuting the outcome itself, which
keeps the null distribution valid in the presence of covariates.

## Options and defaults

| Option | Default |
|---|---|
| `opts.outerK` | `5` |
| `opts.innerK` | `4` |
| `opts.nRepeats` | `50` |
| `opts.maxLV` | `4` |
| `opts.nPerm` | `1000` |
| `opts.nBoot` | `500` |
| `opts.learningSteps` | `6` |
| `opts.scale` | `'zscore'` |
| `opts.covariates` | `[]` |
| `opts.residualizeY` | `false` |
| `opts.seed` | `1` |

## Reading the results structure

**Performance** — `results.Q2` (primary), `results.MSE`, `results.RMSE`, `results.MAE`,
`results.Corr`, with fold-level `results.allQ2`, `results.allMSE`. Compare against
`results.Q2_global_cv`, the cross-validated baseline.

Q² is the cross-validated analogue of R². A negative Q² means the model predicts held-out data
worse than the training mean does — a real and reportable outcome, not a bug.

**Predictions** — `results.cvObserved`, `results.cvPredicted`, `results.cvRepeatID`,
`results.cvSubjectID`. These are what you plot observed against predicted from, and the repeat
and subject IDs let you show the spread across repeats honestly rather than collapsing it.

**Model selection** — `results.selectedLV`, `results.betaStore`, `results.featureWeights`,
`results.meanFeatureWeight`.

**Feature importance** — `results.VIP`, `results.meanBeta`, `results.sdBeta`,
`results.stabilityZ`, `results.signStability`.

**Inference** — `results.allpermQ2`, `results.permutation_p`; bootstrap `results.allbootQ2`,
`results.Q2_CI`.

**Learning** — `results.learningSizes`, `results.learningQ2`.

**Final model, for interpretation only** — `results.finalLV`, `results.betaFinal`,
`results.varExplainedX`, `results.varExplainedY`, `results.finalXLoadings`,
`results.finalYLoadings`, `results.finalXScores`, `results.finalYScores`. As with PLS-DA, the
final model is fitted on all data and its fit is not a generalisation estimate.

## Plotting

`README_PLSR_plotting.md` covers observed-versus-predicted plots, permutation nulls, bootstrap
intervals, VIP and stability maps, and learning curves. Brain rendering of weight maps uses the
CANlab [visualisation tools](https://canlab.github.io/walkthroughs/).

---

**Next:** [Elastic Net]({{ '/docs/mvpa-enet/' | relative_url }})
[Source: `secondlevel/`](https://github.com/labgas/LaBGAScore/tree/main/secondlevel){: .btn .btn--inverse}
[Usage guide](https://github.com/labgas/LaBGAScore/blob/main/secondlevel/README_PLSR_neuroimaging_pipeline.md){: .btn .btn--inverse}
