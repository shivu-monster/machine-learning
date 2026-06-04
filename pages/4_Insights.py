import streamlit as st
import pandas as pd

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Insights",
    page_icon="📋",
    layout="wide"
)

# --------------------------------------------------
# Load Dataset
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

# Remove invalid funding values
df = df.dropna(subset=["AmountInUSD"])

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📋 Startup Funding Insights")

st.markdown("""
Business intelligence and strategic insights derived from
Indian startup funding data.
""")

# --------------------------------------------------
# Key Metrics
# --------------------------------------------------

st.header("📊 Key Metrics")

total_funding = df["AmountInUSD"].sum()
average_funding = df["AmountInUSD"].mean()

total_startups = (
    df["StartupName"].nunique()
    if "StartupName" in df.columns
    else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Funding",
        f"${total_funding:,.0f}"
    )

with col2:
    st.metric(
        "Average Funding",
        f"${average_funding:,.0f}"
    )

with col3:
    st.metric(
        "Total Startups",
        total_startups
    )

# --------------------------------------------------
# Top Funded Startup
# --------------------------------------------------

st.header("🏆 Top Funded Startup")

if "StartupName" in df.columns:

    top_startup = (
        df.groupby("StartupName")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
    )

    if not top_startup.empty:

        st.success(
            f"Most Funded Startup: "
            f"{top_startup.index[0]} "
            f"(${top_startup.iloc[0]:,.0f})"
        )

# --------------------------------------------------
# Funding Hotspot
# --------------------------------------------------

st.header("🏙️ Startup Funding Hotspot")

if "CityLocation" in df.columns:

    city_funding = (
        df.groupby("CityLocation")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
    )

    if not city_funding.empty:

        st.info(
            f"Highest Funded City: "
            f"{city_funding.index[0]} "
            f"(${city_funding.iloc[0]:,.0f})"
        )

# --------------------------------------------------
# Leading Industry
# --------------------------------------------------

st.header("🏭 Leading Industry")

if "IndustryVertical" in df.columns:

    industry_funding = (
        df.groupby("IndustryVertical")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
    )

    if not industry_funding.empty:

        st.success(
            f"Top Industry: "
            f"{industry_funding.index[0]} "
            f"(${industry_funding.iloc[0]:,.0f})"
        )

# --------------------------------------------------
# Most Active Investor
# --------------------------------------------------

st.header("🤝 Most Active Investor")

if "InvestorsName" in df.columns:

    investor_count = (
        df["InvestorsName"]
        .dropna()
        .value_counts()
    )

    if not investor_count.empty:

        st.info(
            f"Most Active Investor: "
            f"{investor_count.index[0]} "
            f"({investor_count.iloc[0]} investments)"
        )

# --------------------------------------------------
# Business Insights
# --------------------------------------------------

st.header("💡 Strategic Insights")

insights = []

if "CityLocation" in df.columns and not city_funding.empty:
    insights.append(
        f"📍 {city_funding.index[0]} attracts the highest startup funding in India."
    )

if "IndustryVertical" in df.columns and not industry_funding.empty:
    insights.append(
        f"🏭 {industry_funding.index[0]} is currently the most funded industry sector."
    )

if "StartupName" in df.columns and not top_startup.empty:
    insights.append(
        f"🚀 {top_startup.index[0]} has received the highest overall funding."
    )

if average_funding > 0:
    insights.append(
        f"💰 Average funding per startup is approximately ${average_funding:,.0f}."
    )

for item in insights:
    st.write(item)

# --------------------------------------------------
# Recommendations
# --------------------------------------------------

st.header("🚀 Investment Recommendations")

st.markdown("""
### Recommended Areas of Focus

1. Invest in high-growth sectors such as:
   - FinTech
   - AI & Machine Learning
   - EdTech
   - HealthTech

2. Monitor startup hubs:
   - Bengaluru
   - Mumbai
   - Delhi NCR
   - Hyderabad

3. Follow active investors to identify funding trends.

4. Study top-funded startups to understand successful business models.

5. Track industry funding patterns before making investment decisions.
""")

# --------------------------------------------------
# Funding Concentration Analysis
# --------------------------------------------------

st.header("📈 Funding Concentration")

if "StartupName" in df.columns:

    startup_funding = (
        df.groupby("StartupName")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
    )

    top_10_funding = startup_funding.head(10).sum()

    concentration = (
        (top_10_funding / total_funding) * 100
        if total_funding > 0
        else 0
    )

    st.metric(
        "Top 10 Startups Funding Share",
        f"{concentration:.2f}%"
    )

# --------------------------------------------------
# Dataset Viewer
# --------------------------------------------------

with st.expander("📂 View Complete Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Insights | Top Funding Startups in India"
)
