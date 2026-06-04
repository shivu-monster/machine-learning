import streamlit as st
import pandas as pd
import joblib
import os

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Funding Prediction",
    page_icon="🔮",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🔮 Startup Funding Prediction")

st.markdown("""
Predict the expected funding amount for a startup using a
Machine Learning model trained on historical startup funding data.
""")

# --------------------------------------------------
# Load Model
# --------------------------------------------------

MODEL_PATH = "models/funding_model.pkl"

if not os.path.exists(MODEL_PATH):
    st.error(
        "Model file not found. Please train the model first."
    )
    st.stop()

try:
    saved_model = joblib.load(MODEL_PATH)

    model = saved_model["model"]
    industry_map = saved_model["industry_map"]
    city_map = saved_model["city_map"]
    investment_map = saved_model["investment_map"]

except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --------------------------------------------------
# User Inputs
# --------------------------------------------------

st.header("📋 Startup Information")

col1, col2 = st.columns(2)

with col1:

    startup_name = st.text_input(
        "Startup Name",
        placeholder="Enter startup name"
    )

    industry = st.selectbox(
        "Industry",
        sorted(list(industry_map.keys()))
    )

with col2:

    city = st.selectbox(
        "City",
        sorted(list(city_map.keys()))
    )

    investment_type = st.selectbox(
        "Investment Type",
        sorted(list(investment_map.keys()))
    )

# --------------------------------------------------
# Prediction
# --------------------------------------------------

if st.button("🚀 Predict Funding"):

    try:

        input_data = pd.DataFrame({
            "Industry": [
                industry_map[industry]
            ],
            "City": [
                city_map[city]
            ],
            "Investment": [
                investment_map[investment_type]
            ]
        })

        prediction = model.predict(
            input_data
        )[0]

        st.success(
            "Prediction generated successfully!"
        )

        st.metric(
            "Estimated Funding Amount",
            f"${prediction:,.0f}"
        )

        st.subheader("📊 Prediction Summary")

        st.write(
            f"""
            Startup Name: **{startup_name if startup_name else 'N/A'}**

            Industry: **{industry}**

            City: **{city}**

            Investment Type: **{investment_type}**

            Predicted Funding: **${prediction:,.0f}**
            """
        )

    except Exception as e:

        st.error(
            f"Prediction failed: {e}"
        )

# --------------------------------------------------
# Information Section
# --------------------------------------------------

st.markdown("---")

st.header("ℹ️ About the Model")

st.info("""
This prediction is generated using a Random Forest Regressor
trained on historical startup funding data.

Features used:

• Industry

• City Location

• Investment Type

The prediction should be treated as an estimate and not
as financial advice.
""")

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Funding Prediction | Top Funding Startups in India"
)
