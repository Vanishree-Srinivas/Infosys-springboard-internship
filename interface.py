import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Ecommerce Sales Forecast Analysis")

# User Inputs
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
indicators = st.multiselect(
    "Select Indicators",
    ["Customer Behavior", "Market Trends", "Seasonal Fluctuations", 
     "Product Availability", "Customer Demographics", 
     "Website Traffic", "Engagement Rate", "Sales Forecast"]
)

# Fetch Data Button
if st.button("Fetch Data"):
    payload = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "indicators": indicators,
    }
    response = requests.post("http://127.0.0.1:8000/filter-market-data", json=payload)
    data = response.json()
    if data:
        df = pd.DataFrame(data)

        # Display the raw data
        st.subheader("Filtered Data")
        st.dataframe(df)

        # Generate charts
        st.subheader("Market Trends Visualization")

        # Line Chart for Time Series Data
        for indicator in indicators:
            if indicator in df.columns:
                st.line_chart(df[indicator])

        # Correlation Heatmap
        if st.checkbox("Show Correlation Heatmap"):
            correlation = df.corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

    else:
        st.error("No data available for the selected range!")

# Generate Predictions Button
if st.button("Generate Predictions"):
    response = requests.get("http://127.0.0.1:8000/predict-trend-chart")
    if response.status_code == 200:
        chart_path = response.json()["chart_path"]
        st.subheader("Sales Forecast Prediction Chart")
        st.image(chart_path)
    else:
        st.error("Failed to generate prediction chart!")
