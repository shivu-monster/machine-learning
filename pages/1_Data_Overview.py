import streamlit as st
import pandas as pd

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Data Overview",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/startup_funding.csv")

    # Clean AmountInUSD
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

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📊 Data Overview")

st.markdown(
    """
Explore the startup funding dataset, understand its structure,
data quality, and funding statistics.
"""
)

# --------------------------------------------------
# Dataset Metrics
# --------------------------------------------------

st.header("📌 Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

with col3:
    st.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

with col4:
    st.metric(
        "Duplicates",
        int(df.duplicated().sum())
    )

# --------------------------------------------------
# Dataset Preview
# --------------------------------------------------

st.header("🔍 Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)

# --------------------------------------------------
# Column Information
# --------------------------------------------------

st.header("📋 Column Information")

column_info = pd.DataFrame({
    "Column Name": df.columns,
    "Data Type": df.dtypes.astype(str)
})

st.dataframe(
    column_info,
    use_container_width=True
)

# --------------------------------------------------
# Missing Values
# --------------------------------------------------

st.header("⚠️ Missing Values")

missing_values = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values
})

st.dataframe(
    missing_values,
    use_container_width=True
)

# --------------------------------------------------
# Statistical Summary
# --------------------------------------------------

st.header("📈 Statistical Summary")

st.dataframe(
    df.describe(include="all"),
    use_container_width=True
)

# --------------------------------------------------
# Unique Values
# --------------------------------------------------

st.header("🔢 Unique Values Count")

unique_values = pd.DataFrame({
    "Column": df.columns,
    "Unique Values": [
        df[col].nunique()
        for col in df.columns
    ]
})

st.dataframe(
    unique_values,
    use_container_width=True
)

# --------------------------------------------------
# Funding Statistics
# --------------------------------------------------

if "AmountInUSD" in df.columns:

    st.header("💰 Funding Statistics")

    total_funding = df["AmountInUSD"].sum()
    average_funding = df["AmountInUSD"].mean()
    maximum_funding = df["AmountInUSD"].max()
    minimum_funding = df["AmountInUSD"].min()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Funding",
            f"${total_funding:,.0f}"
        )

        st.metric(
            "Average Funding",
            f"${average_funding:,.0f}"
        )

    with col2:
        st.metric(
            "Maximum Funding",
            f"${maximum_funding:,.0f}"
        )

        st.metric(
            "Minimum Funding",
            f"${minimum_funding:,.0f}"
        )

# --------------------------------------------------
# Download Dataset
# --------------------------------------------------

st.header("⬇️ Download Dataset")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="startup_funding.csv",
    mime="text/csv"
)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Data Overview | Top Funding Startups in India"
)
