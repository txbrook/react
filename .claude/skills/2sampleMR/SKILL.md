---
name: gwas-mr-analysis
description: "Guide for performing Mendelian Randomization (MR) analysis using GWAS summary statistics. Use for: two-sample MR, instrument selection, data harmonization, and sensitivity analysis."
license: Complete terms in LICENSE.txt
---

# GWAS and Mendelian Randomization (MR) Analysis Skill

This skill provides a structured workflow and reusable resources for conducting Mendelian Randomization (MR) analysis, primarily focusing on the widely-used two-sample MR approach with GWAS summary statistics.

## Core Workflow

The analysis follows a four-stage process:

1.  **Data Preparation**: Ensure GWAS summary statistics are available and properly formatted.
2.  **Quality Control (QC)**: Apply rigorous QC to the underlying GWAS data (if raw data is available) or ensure the summary statistics meet quality standards.
3.  **Instrument Selection**: Select and clump genetic variants (SNPs) to serve as valid instrumental variables (IVs).
4.  **MR Analysis and Sensitivity**: Perform the MR estimation and conduct sensitivity analyses to test core MR assumptions.

## 1. Data Quality Control (QC)

If working with raw GWAS data (e.g., PLINK files), perform the following QC steps before generating summary statistics. If using publicly available summary statistics, assume the original authors performed these steps, but be aware of potential issues.

**Action**: Read the `references/gwas_qc_details.md` file for a detailed table of recommended QC steps, PLINK commands, and thresholds.

## 2. Instrument Selection and Harmonization

The core of two-sample MR is the selection of valid IVs and the harmonization of data.

1.  **Instrument Selection**: Select SNPs associated with the exposure at a genome-wide significance level (typically $P < 5 \times 10^{-8}$).
2.  **Linkage Disequilibrium (LD) Clumping**: Ensure the selected SNPs are independent by clumping them based on a reference panel (e.g., 1000 Genomes). A common setting is $r^2 < 0.001$ and a window of $10,000$ kb.
3.  **Harmonization**: Align the effect alleles and effect sizes for the exposure and outcome data to prevent spurious results.

## 3. Performing Mendelian Randomization

The primary analysis should use multiple MR methods to check for consistency and robustness.

**Action**: Read the `references/mr_methods.md` file for a comparison of the Inverse Variance Weighted (IVW), MR-Egger, and Weighted Median methods, along with their underlying assumptions.

### Reusable Script: `run_mr_analysis.py`

Use the provided Python script to execute a standard two-sample MR analysis using the **TwoSampleMR** R package via `rpy2`. This script handles instrument extraction, clumping, harmonization, and the main MR methods.

**Usage**:

```bash
python /home/ubuntu/skills/gwas-mr-analysis/scripts/run_mr_analysis.py
```

**Note**: The script requires the `rpy2` Python package and the `TwoSampleMR` R package to be installed. It is configured to use the IEU OpenGWAS database for summary statistics, requiring the GWAS IDs (e.g., `ieu-a-2` for BMI).

## 4. Interpretation and Reporting

After running the analysis, interpret the results:

*   **Causal Estimate**: The primary result from the IVW method.
*   **Pleiotropy**: Check the MR-Egger intercept. A P-value $> 0.05$ suggests no directional pleiotropy.
*   **Heterogeneity**: Check Cochran's Q statistic. A high Q-statistic (low P-value) suggests heterogeneity, indicating potential pleiotropy or violation of the IVW assumption.

If the IVW, MR-Egger (slope), and Weighted Median estimates are consistent, the causal inference is more robust. If they diverge, prioritize the methods that are more robust to the detected violations (e.g., Weighted Median or MR-Egger).
