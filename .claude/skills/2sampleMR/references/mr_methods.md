# Mendelian Randomization (MR) Methods and Assumptions

Mendelian Randomization (MR) is a method for estimating the causal effect of an exposure on an outcome using genetic variants (typically Single Nucleotide Polymorphisms or SNPs) as instrumental variables (IVs).

## Core Assumptions of Mendelian Randomization

For a genetic variant (IV) to be a valid instrument, it must satisfy three core assumptions:

1.  **Relevance (IV1)**: The IV must be reliably associated with the exposure.
2.  **Independence (IV2)**: The IV must not be associated with any confounders of the exposure-outcome relationship.
3.  **Exclusion Restriction (IV3)**: The IV must affect the outcome only through the exposure (i.e., no pleiotropy).

## Common Two-Sample MR Methods (TwoSampleMR R Package)

Two-sample MR uses summary statistics from two separate GWAS: one for the exposure and one for the outcome.

| Method | Primary Assumption | Sensitivity to Pleiotropy | Use Case |
| :--- | :--- | :--- | :--- |
| **Inverse Variance Weighted (IVW)** | All instruments are valid (no pleiotropy or balanced pleiotropy). | Highly sensitive. Provides the most precise estimate if assumptions hold. | Primary analysis method. |
| **MR-Egger** | Pleiotropy is independent of the instrument-exposure association (InSIDE assumption). | Robust to *directional* pleiotropy. The intercept tests for *overall* pleiotropy. | Sensitivity analysis for directional pleiotropy. |
| **Weighted Median** | At least 50% of the weight in the analysis comes from valid instruments. | Robust to up to 50% invalid instruments. | Sensitivity analysis for widespread, non-directional pleiotropy. |
| **Weighted Mode** | The largest cluster of instruments gives a consistent causal estimate. | Robust to a high proportion of invalid instruments, provided a large cluster of valid instruments exists. | Sensitivity analysis, especially when many instruments are used. |

## Sensitivity Analyses

To check the validity of the MR assumptions, several sensitivity analyses are performed:

1.  **Heterogeneity**: Assesses whether the causal estimates from individual SNPs are consistent. High heterogeneity suggests pleiotropy or violation of the IVW assumption.
    *   **Test**: Cochran's Q statistic (available in IVW and MR-Egger).
2.  **Pleiotropy**: Assesses whether the genetic instruments affect the outcome through pathways other than the exposure.
    *   **Test**: MR-Egger intercept test. A non-zero intercept suggests directional pleiotropy.
3.  **Leave-One-Out Analysis**: Sequentially removes one SNP at a time to see if the overall causal estimate is driven by a single outlier SNP.
4.  **Funnel Plot**: A visual tool to assess pleiotropy and heterogeneity. Asymmetry suggests directional pleiotropy.
5.  **Scatter Plot**: Visualizes the association of the SNP-exposure effect against the SNP-outcome effect, with the slope representing the causal estimate.
