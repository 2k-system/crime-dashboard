**⚖️ Judicial Workload & Backlog Analytics Report (2022)**

📌 Project Overview
This project provides a comprehensive analysis of the National Crime Records Bureau (NCRB) 2022 dataset. While raw crime volumes often dominate public discourse, this analysis shifts the focus toward Judicial Efficiency—specifically the gap between case registration (Total Crimes) and case processing (Chargesheeting).

By quantifying the "Pending" volume, we identify administrative bottlenecks and pressure points within the Indian legal system across various States and Union Territories.

🛠️ Key Methodologies Applied
1. Data Engineering & Cleaning
Aggregate Removal: Stripped national and regional totals to ensure statistical averages were not skewed by double-counting.

Feature Engineering: Created the Pending_Cases_2022 metric by calculating the inverse of the Chargesheeting Rate against total volume.

2. Machine Learning Segmentation (K-Means)
Used K-Means Clustering to categorize regions into three distinct risk profiles:

High Intensity: High crime volume but high efficiency.

Efficiency Gap: Moderate crime with rising backlogs.

Stable: Low growth and manageable workloads.

3. Safety Indexing (Weighted SPI)
Developed a custom Safety Performance Index (SPI) using a weighted formula:

40% Efficiency (Chargesheet Rate)

30% Risk Mitigation (Inverse of Crime Rate)

30% Growth Control (Inverse of Year-over-Year Growth)

💡 Final Conclusions
The Volume Paradox: High crime volume does not always equate to poor performance. For instance, Uttar Pradesh manages a higher volume than Delhi but maintains a significantly lower backlog, indicating a more robust investigative "output."

The Efficiency Gap: Jurisdictions like Delhi and Rajasthan are facing a "Critical Overload" where the volume of pending cases exceeds or nears the volume of processed cases. This suggests a need for increased judicial resources and investigative officers.

Administrative Bottlenecks: The backlog analysis confirms that population size is not the only driver of crime; rather, the Resolution Ratio (Chargesheeted vs. Pending) is the true indicator of a state's ability to maintain law and order.

Policy Recommendation: Resource allocation should be prioritized toward "High Growth/Low Efficiency" zones to prevent a permanent judicial backlog that could take years to clear.

🚀 How to Run the Analysis
This project is available in both Python (Pandas/Plotly) and R (Tidyverse/ggplot2).

Ensure you have the NCRB_Table_1A.1.csv file in the root directory.

Install dependencies:

Python: pip install pandas plotly scikit-learn

R: install.packages(c("tidyverse", "plotly", "cluster"))

Execute the respective .ipynb or .R script to generate the interactive visualizations and ML clusters.
