
# Import required libraries
# Import required libraries
# Import required libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests

# Backend URL for authentication
BACKEND_URL = "http://127.0.0.1:8000"

# Custom CSS for purple theme
st.markdown(
    """
    <style>
    body {
        background-color:#e6e6fa;
    }
    .main {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        border-radius: 15px;
        padding: 2rem;
        color: white;
    }
    input, button {
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    h1, h2 {
        text-align: center;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit App Title
st.title("Market Data Dashboard")

# Navigation options
page = st.sidebar.radio("Navigation", ["Login", "Signup", "Dashboard"])

if page == "Signup":
    st.header("User Registration")
    with st.form("registration_form"):
        username = st.text_input("Enter Username")
        password = st.text_input("Enter Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        signup_button = st.form_submit_button("Register")

        if signup_button:
            if password != confirm_password:
                st.error("Passwords do not match!")
            else:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/signup",
                        json={"username": username, "password": password},
                    )
                    if response.status_code == 200:
                        st.success("User registered successfully! Please log in.")
                    else:
                        st.error(response.json().get("detail", "Error during signup"))
                except Exception as e:
                    st.error(f"Error: {e}")

elif page == "Login":
    st.header("User Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/login",
                    json={"username": username, "password": password},
                )
                if response.status_code == 200:
                    st.success("Login successful! Navigate to the Dashboard.")
                    st.session_state["authenticated"] = True
                else:
                    st.error(response.json().get("detail", "Invalid credentials"))
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "Dashboard":
    if not st.session_state.get("authenticated", False):
        st.warning("Please log in to access the dashboard.")
    else:
        st.sidebar.title("Upload Your Data")

        # File upload section
        uploaded_file = st.sidebar.file_uploader(
            "Upload your Market Data CSV", type=["csv"]
        )

        if uploaded_file is not None:
            try:
                # Load the dataset
                market_data = pd.read_csv(uploaded_file)

                # Ensure necessary columns are present
                required_columns = [
                    "Date", "Store ID", "Product ID", "Category", "Region",
                    "Inventory Level", "Units Sold", "Units Ordered",
                    "Demand Forecast", "Price", "Discount", "Weather Condition",
                    "Holiday/Promotion", "Competitor Pricing", "Seasonality"
                ]
                missing_columns = [
                    col for col in required_columns if col not in market_data.columns
                ]

                if missing_columns:
                    st.error(
                        f"Missing required columns: {', '.join(missing_columns)}. Please upload a valid dataset."
                    )
                else:
                    # Convert Date column to datetime
                    market_data["Date"] = pd.to_datetime(
                        market_data["Date"], errors="coerce"
                    )
                    if market_data["Date"].isnull().all():
                        st.error(
                            "Invalid 'Date' column format. Please ensure dates are properly formatted."
                        )
                    else:
                        # Sidebar filter options
                        region = st.sidebar.selectbox(
                            "Select Region", market_data["Region"].unique()
                        )
                        filtered_data = market_data[
                            market_data["Region"] == region
                        ]

                        if filtered_data.empty:
                            st.warning(
                                f"No data available for the selected region: {region}."
                            )
                        else:
                            # Display raw and filtered data
                            st.subheader("Raw Data")
                            st.dataframe(market_data)

                            st.subheader(f"Filtered Data for Region: {region}")
                            st.dataframe(filtered_data)

                            # --- Visualization Section ---
                            st.header("Visualizations")

                            # 1. Line Chart - Units Sold Over Time
                            st.subheader("Line Chart - Units Sold Over Time")
                            line_chart_data = (
                                filtered_data.groupby("Date")
                                .sum(numeric_only=True)
                                .reset_index()
                            )
                            if "Units Sold" in line_chart_data.columns:
                                fig = px.line(
                                    line_chart_data,
                                    x="Date",
                                    y="Units Sold",
                                    title=f"Units Sold Trends in {region}",
                                )
                                st.plotly_chart(fig)
                            else:
                                st.warning(
                                    "The 'Units Sold' column is missing or not numeric. Cannot generate line chart."
                                )

                            # 2. Pie Chart - Category Distribution
                            st.subheader("Pie Chart - Category Distribution")
                            fig = px.pie(
                                filtered_data,
                                names="Category",
                                values="Units Sold",
                                title=f"Product Category Distribution in {region}",
                            )
                            st.plotly_chart(fig)

                            # 3. Heatmap - Correlation Matrix
                            st.subheader("Heatmap - Correlation Matrix")
                            correlation = filtered_data.corr(numeric_only=True)
                            if not correlation.empty:
                                fig, ax = plt.subplots(figsize=(10, 8))
                                sns.heatmap(
                                    correlation, annot=True, cmap="coolwarm", ax=ax
                                )
                                st.pyplot(fig)
                            else:
                                st.warning(
                                    "No numeric columns available for correlation matrix."
                                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.info("Please upload a CSV file to proceed.")

