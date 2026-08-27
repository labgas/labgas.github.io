---
title: "Elastic Net (classification)"
permalink: /docs/mvpa-enet/
excerpt: "Elastic net regularised classification with automatic feature selection, fold-wise covariate residualisation and stability metrics."
---

<div class="step-meta" markdown="0">
  <span><strong>Owner</strong> LaBGAS</span>
  <span><strong>Folder</strong> <code>secondlevel/</code></span>
  <span><strong>Guides</strong> README_ENet_neuroimaging_pipeline.md, README_ENet_plotting.md</span>
</div>

`ENet_neuroimaging_pipeline` implements **elastic net regularised classification** for
small-to-moderate neuroimaging datasets, including the common case where features outnumber
subjects. Combining L1 (lasso) and L2 (ridge) penalties gives automatic feature selection while
controlling overfitting — L1 drives coefficients to zero, L2 keeps correlated features from
being arbitrarily discarded.

Use it when the outcome is categorical and you want a **sparse** solution. For a dense
latent-variable solution on the same kind of outcome, use
[PLS-DA]({{ '/docs/mvpa-plsda/' | relative_url }}) instead.

## Inputs and outputs

**Inputs**

- `X` — `[n × p]` feature matrix, subjects × features
- `Y` — `[n × 1]` outcome vector; the maximum label becomes the positive class
- `opts.covariates` — `[n × nCov]`, with `opts.covariateNames`

**Output** — a `results` structure.

## What the pipeline does

1. **Repeated nested cross-validation** — outer CV for generalisation, inner CV for
   hyperparameter tuning
2. **Feature preprocessing** — residualisation, then scaling, applied fold-wise
3. **Hyperparameter optimisation** across the alpha and lambda grids
4. **Training and evaluation** on held-out folds
5. **Permutation testing** for significance
6. **Bootstrap** out-of-bag confidence intervals
7. **Learning curves** across subsample sizes

<div class="notice--warning" markdown="1">
**Residualise covariates within each fold.** The usage guide is explicit about this: covariates
must be residualised inside every fold. Pre-residualising on the full sample leaks information
from the test fold into training and produces systematically biased performance estimates. This
is the single easiest way to get a result that will not replicate.
</div>

## Options and defaults

| Option | Default |
|---|---|
| `outerK` | `5` |
| `innerK` | `4` |
| `nRepeats` | `50` |
| `nPerm` | `1000` |
| `nBoot` | `500` |
| `learningSteps` | `6` |
| `alphaGrid` | `[0.05 0.1 0.25 0.5 0.75 0.9 1]` |
| `lambdaGrid` | `logspace(-3, 1, 25)` |
| `scale` | `'zscore'` — also `'center'`, `'none'` |
| `seed` | `1` |

`alpha = 1` is pure lasso; lower values mix in ridge. The grid spans that continuum so the
inner CV can choose.

## Reading the results structure

**Performance** — `results.AUC` (primary), `results.AUC_PR`, `results.ACC`, `results.SENS`,
`results.SPEC`, `results.ACC_balanced`, plus fold-level variants from `results.allAUC` through
`results.allACC_balanced`.

**Model** — `results.betaStore`, `results.interceptStore`, `results.featureWeights`,
`results.meanFeatureWeight`.

**Stability** — `results.featureStability`, `results.signStability`,
`results.selectionFrequency`, `results.selectionTopK`. The guide gives thresholds for reading
these:

| Value | Interpretation |
|---|---|
| `> 0.8` | Highly stable |
| `0.4 – 0.8` | Moderately stable |
| `< 0.4` | Unstable |

With a sparse model this matters more than the weight magnitudes. Which features get selected
can shift substantially between folds when predictors are correlated, and a feature that enters
the model in a third of folds should not be discussed as though it were a finding.

**Inference** — `results.permutation_p`, `results.permutation_p_PR`; bootstrap
`results.AUC_CI`; and `results.quickCV_observed`, a matched null distribution baseline.

**Baselines** — in-sample `results.AUC_global`, `results.AUC_PR_global`; cross-validated
`results.AUC_global_cv`, `results.AUC_PR_global_cv`, using the mean or median feature. Compare
against the cross-validated versions.

**Learning** — `results.learningSizes`, `results.learningAUC`.

## Plotting

`README_ENet_plotting.md` covers performance distributions, permutation nulls, bootstrap
intervals, selection-frequency and stability maps, and learning curves.

---

**Next:** [PET]({{ '/docs/pet/' | relative_url }})
[Source: `secondlevel/`](https://github.com/labgas/LaBGAScore/tree/main/secondlevel){: .btn .btn--inverse}
[Usage guide](https://github.com/labgas/LaBGAScore/blob/main/secondlevel/README_ENet_neuroimaging_pipeline.md){: .btn .btn--inverse}
