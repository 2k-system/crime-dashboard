import pandas as pd
from scipy.stats import pearsonr

def perform_statistical_analysis(df):
    # Metadata: Null values check
    null_info = df.isnull().sum()
    null_present = null_info.sum() > 0
    
    # Min/Max logic for 2022
    min_crime_state = df.loc[df['Crimes_2022'].idxmin(), 'State_UT']
    max_crime_state = df.loc[df['Crimes_2022'].idxmax(), 'State_UT']
    min_eff_state = df.loc[df['Chargesheet_Rate_2022'].idxmin(), 'State_UT']
    max_eff_state = df.loc[df['Chargesheet_Rate_2022'].idxmax(), 'State_UT']
    
    # Correlation Math
    pop_crime_corr, p_val = pearsonr(df["Population_Lakhs_2022"], df["Crimes_2022"])
    corr_matrix = df[["Population_Lakhs_2022", "Crimes_2022", "Chargesheet_Rate_2022", "Crime_Rate_2022"]].corr()
    
    return {
        "null_present": null_present,
        "null_details": null_info,
        "min_crime": min_crime_state,
        "max_crime": max_crime_state,
        "min_eff": min_eff_state,
        "max_eff": max_eff_state,
        "pop_crime_corr": pop_crime_corr,
        "p_value": p_val,
        "corr_matrix": corr_matrix
    }