import streamlit as st
import requests

st.title("Basic Income Simulator")

current_income = st.number_input(
    "Current monthly income (€)", min_value=0.0, value=1500.0
)
household_size = st.number_input("Household size", min_value=1, value=1)

if st.button("Calculate"):
    payload = {"current_income": current_income, "household_size": household_size}
    try:
        response = requests.post(
            "http://backend:8000/api/calculate_basic_income", json=payload
        )
        response.raise_for_status()
        data = response.json()
        st.success(f"Basic income calculated: {data['basic_income']:.2f} €")
    except requests.RequestException as e:
        st.error(f"Calculation failed: {e}")
