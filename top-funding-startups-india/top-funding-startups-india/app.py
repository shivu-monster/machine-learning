import streamlit as st

st.set_page_config(
    page_title="Top Funding Startups in India",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
.main {
    padding-top: 0rem;
}

.metric-card{
    background-color:#0E1117;
    padding:20px;
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

st.image("assets/banner.png", use_container_width=True)

st.title("🚀 Top Funding Startups in India")

st.markdown("""
### Deep Analytics Platform for Indian Startup Ecosystem

Analyze:

- Startup Funding Trends
- Investor Activity
- Industry Growth
- Geographic Distribution
- Funding Predictions
- Market Intelligence
""")

st.info("Use the left sidebar to navigate through analytics modules.")
