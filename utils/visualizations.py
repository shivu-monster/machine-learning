import plotly.express as px
import pandas as pd

# --------------------------------------------------
# Top Funded Startups
# --------------------------------------------------

def plot_top_startups(df: pd.DataFrame, top_n: int = 10):
    """
    Bar chart of top funded startups.
    """

    data = (
        df.groupby("StartupName")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        data,
        x="StartupName",
        y="AmountInUSD",
        title=f"Top {top_n} Funded Startups",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Startup",
        yaxis_title="Funding (USD)"
    )

    return fig


# --------------------------------------------------
# Top Cities
# --------------------------------------------------

def plot_top_cities(df: pd.DataFrame, top_n: int = 10):
    """
    Pie chart of funding by city.
    """

    data = (
        df.groupby("CityLocation")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.pie(
        data,
        names="CityLocation",
        values="AmountInUSD",
        title="Funding Distribution by City"
    )

    return fig


# --------------------------------------------------
# Top Industries
# --------------------------------------------------

def plot_top_industries(df: pd.DataFrame, top_n: int = 10):
    """
    Bar chart for industry-wise funding.
    """

    data = (
        df.groupby("IndustryVertical")["AmountInUSD"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        data,
        x="IndustryVertical",
        y="AmountInUSD",
        title="Top Industries by Funding",
        text_auto=".2s"
    )

    fig.update_layout(
        xaxis_title="Industry",
        yaxis_title="Funding (USD)"
    )

    return fig


# --------------------------------------------------
# Top Investors
# --------------------------------------------------

def plot_top_investors(df: pd.DataFrame, top_n: int = 10):
    """
    Bar chart for most active investors.
    """

    data = (
        df["InvestorsName"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    data.columns = ["Investor", "Investments"]

    fig = px.bar(
        data,
        x="Investor",
        y="Investments",
        title="Top Investors",
        text_auto=True
    )

    return fig


# --------------------------------------------------
# Funding Trend Over Time
# --------------------------------------------------

def plot_funding_trend(df: pd.DataFrame):
    """
    Line chart for funding over years.
    """

    df = df.copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    trend = (
        df.groupby(df["Date"].dt.year)["AmountInUSD"]
        .sum()
        .reset_index()
    )

    trend.columns = ["Year", "Funding"]

    fig = px.line(
        trend,
        x="Year",
        y="Funding",
        markers=True,
        title="Funding Trend Over Years"
    )

    return fig


# --------------------------------------------------
# Investment Type Distribution
# --------------------------------------------------

def plot_investment_type(df: pd.DataFrame):
    """
    Pie chart for investment types.
    """

    data = (
        df["InvestmentType"]
        .value_counts()
        .reset_index()
    )

    data.columns = ["InvestmentType", "Count"]

    fig = px.pie(
        data,
        names="InvestmentType",
        values="Count",
        title="Investment Type Distribution"
    )

    return fig
