import pandas as pd

# --------------------------------------------------
# Load and Clean Dataset
# --------------------------------------------------

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load startup funding dataset and perform basic cleaning.
    """

    df = pd.read_csv(file_path)

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing values (safe for dashboard)
    df = df.fillna("Unknown")

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

        df["AmountInUSD"] = df["AmountInUSD"].fillna(0)

    # Convert Date column if exists
    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    return df


# --------------------------------------------------
# Basic Dataset Statistics
# --------------------------------------------------

def get_basic_stats(df: pd.DataFrame) -> dict:
    """
    Returns dataset summary statistics.
    """

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum())
    }


# --------------------------------------------------
# Top Funded Startups
# --------------------------------------------------

def top_funded_startups(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Returns top funded startups.
    """

    if "StartupName" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("StartupName")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


# --------------------------------------------------
# Top Cities
# --------------------------------------------------

def top_cities(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Returns top funding cities.
    """

    if "CityLocation" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("CityLocation")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


# --------------------------------------------------
# Top Industries
# --------------------------------------------------

def top_industries(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Returns top funded industries.
    """

    if "IndustryVertical" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("IndustryVertical")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


# --------------------------------------------------
# Top Investors
# --------------------------------------------------

def top_investors(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Returns most active investors.
    """

    if "InvestorsName" not in df.columns:
        return pd.DataFrame()

    return (
        df["InvestorsName"]
        .value_counts()
        .head(n)
        .reset_index()
        .rename(columns={
            "index": "Investor",
            "InvestorsName": "Investments"
        })
    )


# --------------------------------------------------
# Funding Trend
# --------------------------------------------------

def funding_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns yearly funding trend.
    """

    if "Date" not in df.columns:
        return pd.DataFrame()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    trend = (
        df.groupby(df["Date"].dt.year)["AmountInUSD"]
        .sum()
        .reset_index()
    )

    trend.columns = ["Year", "Funding"]

    return trend
