import plotly.express as px

def perform_visual_analysis(df):
    # 1. 3-Year Trend Line Plot
    df_melted_3 = df.melt(id_vars='State_UT', value_vars=['Crimes_2020', 'Crimes_2021', 'Crimes_2022'], 
                                var_name='Year', value_name='Crime_Count')
    df_melted_3['Year'] = df_melted_3['Year'].str.extract('(\d+)')
    fig_line = px.line(df_melted_3, x="State_UT", y="Crime_Count", color="Year", markers=True,
                       title="<b>Trajectory Analysis:</b> Crime Trends by State (2020-2022)")
    fig_line.update_layout(xaxis={'categoryorder':'total descending'})

    # 2. Lockdown vs Recovery Bar Chart
    df_melted_2 = df.melt(id_vars='State_UT', value_vars=['Crimes_2020', 'Crimes_2022'], 
                                var_name='Year', value_name='Crime_Count')
    df_melted_2['Year'] = df_melted_2['Year'].str.extract('(\d+)')
    fig_bar = px.bar(df_melted_2, x="State_UT", y="Crime_Count", color="Year", barmode="group",
                     title="<b>Impact Analysis:</b> Crime Volume Comparison (2020 vs 2022)")

    # 3. Efficiency Bubble Chart
    fig_bubble = px.scatter(df, x="Crime_Rate_2022", y="Chargesheet_Rate_2022",
                            size="Crimes_2022", color="State_UT", hover_name="State_UT",
                            title="<b>Strategic Matrix:</b> Crime Rate vs. Chargesheet Efficiency",
                            labels={"Crime_Rate_2022": "Crime Rate", "Chargesheet_Rate_2022": "Efficiency (%)"})
    
    return fig_line, fig_bar, fig_bubble