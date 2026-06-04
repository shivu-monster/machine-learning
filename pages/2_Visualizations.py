import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/startup_funding.csv")

    if "AmountInUSD" in df.columns:
        df["AmountInUSD"] = (
            df["AmountInUSD"]
            .astype(str)
            .str.replace(",", "", regex=False)
        )

        df["AmountInUSD"] = pd.to_numeric(
            df["AmountInUSD"],
            errors="coerce"
        )

    return df


df = load_data()

# Remove invalid funding rows
df = df.dropna(subset=["AmountInUSD"])

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📈 Startup Funding Visualizations")

st.markdown(
    """
Interactive visualizations to explore startup funding trends,
investors, industries, and funding hotspots across India.
"""
)

# --------------------------------------------------
# Top Funded Startups
# --------------------------------------------------

st.header("🏆 Top 10 Funded Startups")

if "StartupName" in df.columns:

    top_startups = (
        df.groupby("StartupName")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_startups,
        x="StartupName",
        y="AmountInUSD",
        title="Top 10 Funded Startups",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Startup",
        yaxis_title="Funding (USD)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# City-wise Funding
# --------------------------------------------------

st.header("🏙️ Funding by City")

if "CityLocation" in df.columns:

    city_funding = (
        df.groupby("CityLocation")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.pie(
        city_funding,
        names="CityLocation",
        values="AmountInUSD",
        title="Top Funding Cities"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Industry-wise Funding
# --------------------------------------------------

st.header("🏭 Industry-wise Funding")

if "IndustryVertical" in df.columns:

    industry_funding = (
        df.groupby("IndustryVertical")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        industry_funding,
        x="IndustryVertical",
        y="AmountInUSD",
        title="Top Industries by Funding",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Industry",
        yaxis_title="Funding (USD)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Investment Type Distribution
# --------------------------------------------------

st.header("💰 Investment Type Distribution")

if "InvestmentType" in df.columns:

    investment_count = (
        df["InvestmentType"]
        .value_counts()
        .reset_index()
    )

    investment_count.columns = [
        "InvestmentType",
        "Count"
    ]

    fig = px.pie(
        investment_count,
        names="InvestmentType",
        values="Count",
        title="Investment Type Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Top Investors
# --------------------------------------------------

st.header("🤝 Top Investors")

if "InvestorsName" in df.columns:

    investor_count = (
        df["InvestorsName"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    investor_count.columns = [
        "Investor",
        "Investments"
    ]

    fig = px.bar(
        investor_count,
        x="Investor",
        y="Investments",
        title="Top 10 Investors",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Funding Trend
# --------------------------------------------------

st.header("📅 Funding Trend Over Time")

if "Date" in df.columns:

    try:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

        trend = (
            df.groupby(
                df["Date"].dt.year
            )["AmountInUSD"]
            .sum()
            .reset_index()
        )

        trend.columns = [
            "Year",
            "Funding"
        ]

        fig = px.line(
            trend,
            x="Year",
            y="Funding",
            markers=True,
            title="Funding Trend Over Years"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"Unable to process Date column: {e}"
        )

# --------------------------------------------------
# Funding Heatmap
# --------------------------------------------------

st.header("🔥 Industry vs City Funding Heatmap")

if (
    "IndustryVertical" in df.columns
    and
    "CityLocation" in df.columns
):

    heatmap_data = (
        df.pivot_table(
            values="AmountInUSD",
            index="IndustryVertical",
            columns="CityLocation",
            aggfunc="sum",
            fill_value=0
        )
    )

    fig = px.imshow(
        heatmap_data,
        aspect="auto",
        title="Funding Heatmap"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Visualizations | Top Funding Startups in India"
)
