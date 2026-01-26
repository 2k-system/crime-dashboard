import streamlit as st
import pandas as pd
import plotly.express as px
from analysis.statistical_analysis import perform_statistical_analysis
from analysis.visual_analysis import perform_visual_analysis
from analysis.safety_analysis import analyze_safety_status

# Page Config
st.set_page_config(layout="wide", page_title="NCRB Analytics")

# --- HEADER ---
st.title("📊 NCRB Crime Data Analytics (2020-2022)")
st.markdown("Interactive analysis of Indian crime trends, police efficiency, and safety anomalies.")

# --- NAVIGATION ---
option = st.radio("Select Analysis Module:", 
                  ["Statistical Analysis", "Data Visualization", "Which State is Safe?"], 
                  horizontal=True)
st.markdown("---") # Visual divider line

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df = pd.read_csv("crime_data.csv")
    df.columns = ['Sr_No', 'State_UT', 'Crimes_2020', 'Crimes_2021', 'Crimes_2022', 
                  'Population_Lakhs_2022', 'Crime_Rate_2022', 'Chargesheet_Rate_2022']
    # Filter totals
    df = df[~df['Sr_No'].str.contains("Total", na=False)].copy()
    for col in df.columns[2:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Pre-calc for conclusion
    df["Pending_Cases_2022"] = df["Crimes_2022"] - (df["Crimes_2022"] * df["Chargesheet_Rate_2022"] / 100)
    df["Crime_Growth_Pct"] = ((df["Crimes_2022"] - df["Crimes_2020"]) / df["Crimes_2020"]) * 100
    return df.dropna()

df = load_data()

# --- MODULE 1: STATISTICAL ANALYSIS ---
if option == "Statistical Analysis":
    stats = perform_statistical_analysis(df)
    
    st.subheader("Statistical Observations")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Null Values Present:** {'Yes' if stats['null_present'] else 'No'}")
        st.write(f"**Max Crime (2022):** {stats['max_crime']}")
        st.write(f"**Min Crime (2022):** {stats['min_crime']}")
    with col2:
        st.write(f"**Pearson Correlation Factor:** {stats['pop_crime_corr']:.4f}")
        st.write(f"**Max Efficiency:** {stats['max_eff']}")
        st.write(f"**Min Efficiency:** {stats['min_eff']}")
    
    st.markdown("---")
    st.plotly_chart(px.imshow(stats['corr_matrix'], text_auto=True, color_continuous_scale='RdBu_r', 
                              title="<b>Correlation Heatmap:</b> Metric Interdependence"), use_container_width=True)
    
    # YOUR DYNAMIC CONCLUSION
    avg_growth = df["Crime_Growth_Pct"].mean()
    max_growth_state = df.loc[df["Crime_Growth_Pct"].idxmax(), "State_UT"]
    pop_crime_corr = stats['pop_crime_corr']

    st.subheader("--- ANALYSIS CONCLUSION ---")
    st.info(f"""
    1. **TREND:** The average crime growth across all states from 2020 to 2022 was {avg_growth:.2f}%. 
       The highest surge was observed in {max_growth_state}.
    2. **CORRELATION:** The correlation between Population and Crime Volume is {pop_crime_corr:.2f}. 
       This suggests a {'strong' if pop_crime_corr > 0.7 else 'moderate'} relationship between population size and reported crimes.
    3. **EFFICIENCY:** Out of the total recorded crimes in 2022, approximately {df['Pending_Cases_2022'].sum():,.0f} 
       cases remained pending (not chargesheeted) across the cleaned dataset.
    """)

# --- MODULE 2: DATA VISUALIZATION ---
elif option == "Data Visualization":
    fig_line, fig_bar, fig_bubble = perform_visual_analysis(df)
    
    st.subheader("Visual Exploration")
    st.plotly_chart(fig_line, use_container_width=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.plotly_chart(fig_bubble, use_container_width=True)

# --- MODULE 3: WHICH STATE IS SAFE? ---
elif option == "Which State is Safe?":
    safety = analyze_safety_status(df)
    
    st.subheader("Safety and Anomaly Observations")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.success("✅ **Truly Safe States**")
        for s in safety['safe_list']: st.write(f"- {s}")
    with c2:
        st.warning("⚠️ **Statistical Anomalies**")
        for s in safety['anomaly_list']: st.write(f"- {s}")
    with c3:
        st.error("🚩 **Reporting Risk**")
        for s in safety['risk_list']: st.write(f"- {s}")
    
    st.markdown("---")
    st.plotly_chart(safety['growth_plot'], use_container_width=True)
    
    st.subheader("Final Safety Conclusion")

    st.info("The safest states are determined by low Crime Intensity relative to population combined with a high Chargesheet Rate, ensuring that most reported crimes are effectively processed.")
