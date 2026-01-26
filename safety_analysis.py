import pandas as pd
import plotly.express as px

def analyze_safety_status(df):
    df = df.copy()
    df['Crime_Intensity'] = df['Crimes_2022'] / df['Population_Lakhs_2022']
    
    # 1. Truly Safe Logic
    truly_safe = df[
        (df['Crime_Intensity'] < df['Crime_Intensity'].median()) & 
        (df['Chargesheet_Rate_2022'] > df['Chargesheet_Rate_2022'].median())
    ].sort_values(by='Crime_Intensity')

    # 2. Anomaly Logic
    anomalies = df[
        (df['Population_Lakhs_2022'] < df['Population_Lakhs_2022'].median()) & 
        (df['Crime_Intensity'] > df['Crime_Intensity'].mean())
    ]

    # 3. Under-Reporting Risk
    risk_states = df[
        (df['Crimes_2022'] < df['Crimes_2022'].median()) & 
        (df['Chargesheet_Rate_2022'] < df['Chargesheet_Rate_2022'].mean())
    ]

    # 4. Growth Plot for Visual
    df["Crime_Growth_Pct"] = ((df["Crimes_2022"] - df["Crimes_2020"]) / df["Crimes_2020"]) * 100
    top_growth = df.sort_values("Crime_Growth_Pct", ascending=False).head(10)
    fig_growth = px.bar(top_growth, x="Crime_Growth_Pct", y="State_UT", orientation='h',
                        color="Crime_Growth_Pct", color_continuous_scale='Reds',
                        title="<b>Alert List:</b> Top 10 States with Highest Crime Growth %")

    return {
        "safe_list": truly_safe['State_UT'].tolist()[:5],
        "anomaly_list": anomalies['State_UT'].tolist(),
        "risk_list": risk_states['State_UT'].tolist(),
        "growth_plot": fig_growth
    }