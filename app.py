
# ===============================
# STREAMLIT DASHBOARD APP
# Save as app.py
# ===============================

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hotel Reservation Dashboard",
                   page_icon="🏨",
                   layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Hotel Reservations.csv")

    df["total_guests"] = (
        df["no_of_adults"]
        + df["no_of_children"]
    )

    df["total_nights"] = (
        df["no_of_weekend_nights"]
        + df["no_of_week_nights"]
    )

    df["total_booking_value"] = (
        df["avg_price_per_room"]
        * df["total_nights"]
    )

    return df

df = load_data()

st.sidebar.header("Filters")

status = st.sidebar.multiselect(
    "Booking Status",
    df["booking_status"].unique(),
    default=df["booking_status"].unique()
)

segment = st.sidebar.multiselect(
    "Market Segment",
    df["market_segment_type"].unique(),
    default=df["market_segment_type"].unique()
)

filtered_df = df[
    (df["booking_status"].isin(status)) &
    (df["market_segment_type"].isin(segment))
]

st.title("🏨 Hotel Reservation Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Bookings", len(filtered_df))
c2.metric("Avg Price", round(filtered_df["avg_price_per_room"].mean(),2))
c3.metric("Avg Nights", round(filtered_df["total_nights"].mean(),2))
c4.metric("Revenue", f"{filtered_df['total_booking_value'].sum():,.0f}")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview","Cancellation","Revenue","Correlation"]
)

with tab1:

    fig = px.pie(
        filtered_df,
        names="booking_status",
        hole=0.5,
        title="Booking Status Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:

    fig = px.box(
        filtered_df,
        x="booking_status",
        y="lead_time",
        color="booking_status",
        title="Lead Time vs Booking Status"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab3:

    revenue = (
        filtered_df
        .groupby("market_segment_type")["total_booking_value"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        revenue,
        x="market_segment_type",
        y="total_booking_value",
        title="Revenue by Segment"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab4:

    corr = filtered_df.select_dtypes(include="number").corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered Data")
st.dataframe(filtered_df)

st.download_button(
    "Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_hotel_data.csv",
    "text/csv"
)


