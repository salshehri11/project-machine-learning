import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(
    page_title="Hotel Reservation Analysis",
    page_icon="🏨",
    layout="wide"
)

st.title("🏨 Hotel Reservation Analysis Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Hotel Reservations.csv")
    return df

df = load_data()

# Sidebar
st.sidebar.header("Dashboard Menu")

page = st.sidebar.radio(
    "Select Section",
    ["Dataset Overview", "Statistics", "Visualizations", "Insights"]
)

# -------------------------------
# Dataset Overview
# -------------------------------
if page == "Dataset Overview":

    st.subheader("Dataset Shape")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    st.subheader("First 5 Rows")
    st.dataframe(df.head())

# -------------------------------
# Statistics
# -------------------------------
elif page == "Statistics":

    st.subheader("Summary Statistics")
    st.dataframe(df.describe())

    st.subheader("Missing Values")
    st.dataframe(df.isnull().sum().reset_index())

# -------------------------------
# Visualizations
# -------------------------------
elif page == "Visualizations":

    st.subheader("Booking Status Distribution")

    fig, ax = plt.subplots()
    df["booking_status"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )
    ax.set_ylabel("")
    st.pyplot(fig)

    st.subheader("Lead Time vs Booking Status")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(
        data=df,
        x="booking_status",
        y="lead_time",
        ax=ax
    )
    st.pyplot(fig)

    st.subheader("Room Price vs Booking Status")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(
        data=df,
        x="booking_status",
        y="avg_price_per_room",
        ax=ax
    )
    st.pyplot(fig)

# -------------------------------
# Insights
# -------------------------------
else:

    st.subheader("Key Insights")

    st.markdown("""
    - Customers with longer lead times are more likely to cancel.
    - Higher room prices tend to have higher cancellation rates.
    - Longer stays generate more revenue.
    - Repeated guests are more reliable.
    - Booking behavior changes by season.
    - Different market segments show different booking patterns.
    """)