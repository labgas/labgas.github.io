---
title: "PLS-DA (classification)"
permalink: /docs/mvpa-plsda/
excerpt: "Partial Least Squares Discriminant Analysis for categorical outcomes, with nested cross-validation, permutation testing and bootstrap confidence intervals."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> LaBGAS</span>
  <span><strong>Folder</strong> <code>secondlevel/</code></span>
  <span><strong>Guides</strong> README_PLSDA_neuroimaging_pipeline.md, README_PLSDA_paired_neuroimaging_pipeline.md, README_PLSDA_plotting.md</span>
</div>

`PLSDA_neuroimaging_pipeline` applies Partial Least Squares Discriminant Analysis to
neuroimaging data — the case where features are strongly correlated and the sample is small,
which describes most of our studies. Use it when the outcome is **categorical**: patients versus
controls, condition A versus condition B.

## Inputs and outputs

**Inputs**

- `X` — `[n × p]` feature matrix, subjects × features
- `Y` — `[n × 1]` outcome vector, converted to binary; the maximum label becomes the positive
  class
- `opts.covariates` — optional `[n × nCov]` nuisance matrix

**Output** — a single `results` structure holding performance, model selection, feature
importance and inference (detailed below).

## What the pipeline does

The design goal is **leakage-free estimation**. Every preprocessing step that learns anything
from the data happens inside the cross-validation folds, never on the full sample.

1. **Outer CV split** into `outerK` folds for generalisation testing
2. **Inner CV tuning** — within each training fold, evaluate `LV = 1…maxLV` and select the best
3. **Preprocessing** — residualise covariates, then scale (z-score by default), all within folds
4. **Model training** on the outer training folds
5. **Evaluation** on the held-out fold
6. **Repeat** the whole outer CV `nRepeats` times
7. **Bootstrap** resampling for out-of-bag confidence intervals
8. **Permutation testing** — shuffle labels and re-run to get a null distribution
9. **Learning curves** across subsample sizes

Steps 7–9 are what make a result interpretable rather than merely reported. A cross-validated
AUC means little without the permutation null and the confidence interval beside it.

## Options and defaults

| Option | Default | Meaning |
|---|---|---|
| `outerK` | `5` | Outer CV folds |
| `innerK` | `4` | Inner CV folds for tuning |
| `nRepeats` | `50` | Repeats of the outer CV |
| `maxLV` | `4` | Maximum latent variables considered |
| `nPerm` | `1000` | Permutations |
| `nBoot` | `500` | Bootstrap resamples |
| `learningSteps` | `6` | Points on the learning curve |
| `opts.scale` | `'zscore'` | Feature scaling |
| `opts.seed` | `1` | Random seed |
| `opts.covariates` | `[]` | Nuisance matrix |

## Reading the results structure

**Performance** — `results.AUC` (primary), `results.AUC_PR`, `results.ACC`, `results.SENS`,
`results.SPEC`, `results.ACC_balanced`, with fold-level counterparts (`results.allAUC` and
friends).

**Model selection** — `results.selectedLV`, `results.betaStore`, `results.featureWeights`,
`results.meanFeatureWeight`.

**Final model, for interpretation only** — `results.finalLV`, `results.betaFinal`,
`results.varExplainedX`, `results.varExplainedY`, `results.finalXLoadings`,
`results.finalYLoadings`. Note *for interpretation only*: the final model is fitted on all the
data, so its apparent performance is not an estimate of generalisation. The cross-validated
metrics are.

**Feature importance** — `results.VIP`, `results.meanBeta`, `results.sdBeta`,
`results.stabilityZ`, `results.signStability`.

**Inference** — `results.permutation_p`, `results.permutation_p_PR`, `results.permAUC`;
bootstrap `results.AUC_CI`, `results.bootAUC`.

**Baseline** — `results.AUC_global_cv`, `results.AUC_PR_global_cv`, a cross-validated global
model to compare against.

**Learning** — `results.learningSizes`, `results.learningAUC`.

## Paired designs

For within-subject designs where observations are paired — the same participants under two
conditions — use the paired variant, documented in
`README_PLSDA_paired_neuroimaging_pipeline.md`. Cross-validation must split by *subject* rather
than by observation; splitting a pair across training and test folds leaks the subject's data
into its own prediction and inflates performance.

## Plotting

`README_PLSDA_plotting.md` covers the figures: performance distributions across repeats,
permutation nulls, bootstrap intervals, feature weight maps and learning curves.

For rendering weight maps on brains, use the CANlab visualisation methods — see the
[visualisation walkthroughs](https://canlab.github.io/walkthroughs/) and the
[object docs](https://canlab.github.io/docs/).

<div class="canlab-note" markdown="1">
**Compared with the CANlab predictive framework.** CanlabCore has its own predictive modelling
API — `predict` on `fmri_data`, SVM and LASSO-PCR among others — documented at
[canlab.github.io/docs](https://canlab.github.io/docs/), with a five-part
[SVM tutorial series](https://canlab.github.io/walkthroughs/). These LaBGAScore pipelines are
complementary: they add nested CV with fold-wise covariate residualisation, permutation and
bootstrap inference, and stability metrics as a single packaged workflow.
</div>

---

**Next:** [PLSR]({{ '/docs/mvpa-plsr/' | relative_url }})
[Source: `secondlevel/`](https://github.com/labgas/LaBGAScore/tree/main/secondlevel){: .btn .btn--inverse}
[Usage guide](https://github.com/labgas/LaBGAScore/blob/main/secondlevel/README_PLSDA_neuroimaging_pipeline.md){: .btn .btn--inverse}
