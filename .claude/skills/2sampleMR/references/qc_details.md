# GWAS Quality Control (QC) Details for Mendelian Randomization

A rigorous Quality Control (QC) process is essential for reliable GWAS results, which in turn are the foundation for Mendelian Randomization (MR) analysis. The following steps, typically performed using **PLINK**, ensure data quality.

| Step | PLINK Command | Function | Recommended Thresholds | Rationale for MR |
| :--- | :--- | :--- | :--- | :--- |
| **1. Missingness** | `--geno` (SNP) | Excludes SNPs with a high proportion of missing genotype data. | `< 0.02` (SNP missingness) | High missingness can lead to biased effect estimates. |
| | `--mind` (Individual) | Excludes individuals with a high proportion of missing genotype data. | `< 0.05` (Individual missingness) | Ensures high-quality samples are used, reducing noise. |
| **2. Sex Discrepancy** | `--check-sex` | Checks for inconsistencies between recorded sex and genetically determined sex (based on X chromosome heterozygosity). | `F statistic` outside of expected range (e.g., `F > 0.8` for males, `F < 0.2` for females). | Incorrect sex assignment can bias X-chromosome analyses and lead to sample mix-ups. |
| **3. Minor Allele Frequency (MAF)** | `--maf` | Excludes SNPs where the minor allele is rare in the study population. | `< 0.01` (MAF) | Low MAF variants have low statistical power and their effect estimates are highly unstable, which is detrimental for MR. |
| **4. Hardy-Weinberg Equilibrium (HWE)** | `--hwe` | Excludes SNPs that significantly deviate from HWE expectations in controls (or all samples for quantitative traits). | `p < 1e-6` (HWE p-value) | Significant deviation often indicates genotyping errors, which can bias effect estimates. |
| **5. Heterozygosity** | `--het` | Identifies individuals with unusually high or low rates of heterozygosity. | `±3 Standard Deviations (SD)` from the mean F-statistic. | Outliers may indicate sample contamination (high) or inbreeding/population structure (low). |
| **6. Relatedness** | `--genome` and `--min` | Calculates Identity-By-Descent (IBD) and excludes one individual from related pairs. | `pi-hat > 0.2` (e.g., second-degree relatives) | Related individuals violate the assumption of independence between samples, leading to inflated test statistics. |
| **7. Population Stratification** | `--pca` (with external tools like EIGENSOFT) | Identifies and controls for population structure using Principal Component Analysis (PCA). | Outliers on PCA plots (e.g., >6 SD from mean of first 2 PCs) should be removed. | Population structure is a major source of confounding in GWAS and MR. Controlling for it is crucial to satisfy the MR assumption of no confounding. |

*Note: For two-sample MR, the QC steps are typically performed on the original GWAS data before summary statistics are generated. When working with publicly available summary statistics, the focus shifts to ensuring the data format is correct and that LD clumping is performed.*
