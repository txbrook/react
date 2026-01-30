# run_mr_analysis.py
# A template Python script for performing Two-Sample Mendelian Randomization analysis
# using the 'TwoSampleMR' R package via rpy2.

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import pandas as pd
import os

# Activate R to Python data conversion
pandas2ri.activate()

# Load the TwoSampleMR R package
try:
    TwoSampleMR = importr('TwoSampleMR')
    print("TwoSampleMR R package loaded successfully.")
except Exception as e:
    print(f"Error loading TwoSampleMR: {e}")
    print("Please ensure the TwoSampleMR R package is installed in your R environment.")
    exit()

def run_two_sample_mr(exposure_gwas_id, outcome_gwas_id, p_value_threshold=5e-8, clump_kb=10000, clump_r2=0.001):
    """
    Performs a standard two-sample MR analysis using the TwoSampleMR R package.

    Args:
        exposure_gwas_id (str): The ID of the exposure GWAS in the IEU OpenGWAS database (e.g., "ieu-a-2").
        outcome_gwas_id (str): The ID of the outcome GWAS in the IEU OpenGWAS database (e.g., "ieu-a-7").
        p_value_threshold (float): P-value threshold for instrument selection (default: 5e-8).
        clump_kb (int): Clumping window size in kilobases (default: 10000 kb).
        clump_r2 (float): Clumping R2 threshold (default: 0.001).

    Returns:
        tuple: (mr_results_df, sensitivity_results_df) as pandas DataFrames.
    """
    print(f"Starting MR analysis for Exposure: {exposure_gwas_id} and Outcome: {outcome_gwas_id}")

    # 1. Extract instruments for the exposure
    print("1. Extracting instruments...")
    exposure_dat_r = TwoSampleMR.extract_instruments(
        outcomes=ro.StrVector([exposure_gwas_id]),
        p1=p_value_threshold,
        clump=True,
        clump_kb=clump_kb,
        clump_r2=clump_r2,
        access_token=os.environ.get("IEUGWAS_API_KEY", "") # Use environment variable for API key if needed
    )
    exposure_dat = pandas2ri.rpy2py(exposure_dat_r)
    print(f"Found {len(exposure_dat)} instruments.")

    if exposure_dat.empty:
        print("No instruments found. Exiting.")
        return pd.DataFrame(), pd.DataFrame()

    # 2. Extract outcome data for the instruments
    print("2. Extracting outcome data...")
    outcome_dat_r = TwoSampleMR.extract_outcome_data(
        snps=ro.StrVector(exposure_dat['SNP'].tolist()),
        outcomes=ro.StrVector([outcome_gwas_id]),
        access_token=os.environ.get("IEUGWAS_API_KEY", "")
    )
    outcome_dat = pandas2ri.rpy2py(outcome_dat_r)
    print(f"Found outcome data for {len(outcome_dat)} SNPs.")

    # 3. Harmonise the exposure and outcome data
    print("3. Harmonising data...")
    dat_r = TwoSampleMR.harmonise_data(
        exposure_dat_r,
        outcome_dat_r,
        action=2 # Remove palindromic SNPs with intermediate allele frequencies
    )
    dat = pandas2ri.rpy2py(dat_r)
    print(f"Harmonised data for {len(dat)} SNPs.")

    # 4. Perform MR analysis
    print("4. Performing MR analysis (IVW, MR-Egger, Weighted Median)...")
    res_r = TwoSampleMR.mr(dat_r)
    res = pandas2ri.rpy2py(res_r)

    # 5. Perform Sensitivity Analysis (Heterogeneity and Pleiotropy)
    print("5. Performing sensitivity analysis...")
    het_r = TwoSampleMR.mr_heterogeneity(dat_r)
    het = pandas2ri.rpy2py(het_r)

    pleio_r = TwoSampleMR.mr_pleiotropy_test(dat_r)
    pleio = pandas2ri.rpy2py(pleio_r)

    # Combine results
    mr_results = res[['method', 'nsnp', 'b', 'se', 'pval', 'lo_ci', 'up_ci']]
    mr_results.columns = ['Method', 'SNPs', 'Effect_Estimate', 'SE', 'P_value', 'Lower_CI', 'Upper_CI']

    sensitivity_results = pd.merge(
        het[['method', 'Q', 'Q_pval']],
        pleio[['egger_intercept', 'pval']],
        on='method',
        how='outer'
    )
    sensitivity_results.columns = ['Method', 'Q_Statistic', 'Q_Pvalue', 'Egger_Intercept', 'Egger_Pvalue']

    print("MR analysis complete.")
    return mr_results, sensitivity_results

if __name__ == "__main__":
    # --- EXAMPLE USAGE ---
    # Example: Causal effect of Body Mass Index (BMI) on Coronary Heart Disease (CHD)
    # BMI GWAS ID: ieu-a-2
    # CHD GWAS ID: ieu-a-7
    
    # NOTE: You need to have the IEU OpenGWAS API key set as an environment variable 
    # or passed to the function if you are not using the default public access.
    # For simplicity, this example uses the public IDs.

    # Replace with your desired GWAS IDs
    EXPOSURE_ID = "ieu-a-2"
    OUTCOME_ID = "ieu-a-7"

    mr_res, sens_res = run_two_sample_mr(EXPOSURE_ID, OUTCOME_ID)

    print("\n--- MR Results ---")
    print(mr_res.to_markdown(index=False))

    print("\n--- Sensitivity Results ---")
    print(sens_res.to_markdown(index=False))

    # --- VISUALIZATION (Requires R plotting libraries) ---
    # To generate plots, you would typically use the R functions directly:
    # TwoSampleMR.mr_scatter_plot(res_r, dat_r)
    # TwoSampleMR.mr_funnel_plot(res_r, dat_r)
    # TwoSampleMR.mr_forest_plot(res_r, dat_r)
    # TwoSampleMR.mr_leaveoneout_plot(res_r, dat_r)
    
    # For a full report, you could use:
    # TwoSampleMR.mr_report(dat_r, output_path="mr_report.html")
    
    # Since we are in a Python environment, generating and saving R plots 
    # requires additional rpy2 and R setup which is complex. 
    # The user can be instructed to run the R commands in an R environment.
    pass
