from pathlib import Path
import streamlit as st
import pandas as pd

st.set_page_config(page_title="", layout="wide")
st.title("")

@st.cache_data
def load_data():
   data_path = Path(r"C:\Users\athul\Documents\trae_projects\carbonfootprint\indian_city_carbon_dataset (1).csv")
   return pd.read_csv(data_path, encoding="utf-8")

data = None
data_load_error = None
try:
    data = load_data()
except Exception as e:
    data_load_error = str(e)

search_city = st.text_input("Search City", placeholder="Enter city name")

if data_load_error:
    st.error(f"Failed to load dataset: {data_load_error}")
elif data is None or data.empty:
    st.warning("Dataset is empty or unavailable.")
else:
    required_cols = [
        "City",
        "Avg_Electricity_kWh",
        "Avg_Transport_Fuel_L",
        "Avg_Cooking_LPG_kg",
        "Avg_Waste_kg",
        "Avg_Air_Travel_km",
    ]
    if not all(col in data.columns for col in required_cols):
        st.error("Dataset is missing one or more required columns.")
    else:
        if search_city:
            city_match = data[
                data["City"].astype(str).str.strip().str.casefold()
                == search_city.strip().casefold()
            ]
            if city_match.empty:
                st.info("City not found in dataset.")
            else:
                row = city_match.iloc[0]
                electricity = float(row["Avg_Electricity_kWh"]) * 0.82
                transport = float(row["Avg_Transport_Fuel_L"]) * 2.31
                cooking = float(row["Avg_Cooking_LPG_kg"]) * 3
                waste = float(row["Avg_Waste_kg"]) * 0.57
                air = float(row["Avg_Air_Travel_km"]) * 0.115
                total = electricity + transport + cooking + waste + air

                cols = st.columns(5)
                labels = ["Electricity", "Transport", "Cooking LPG", "Waste", "Air Travel"]
                values = [electricity, transport, cooking, waste, air]
                for col, label, value in zip(cols, labels, values):
                    col.metric(label=label, value=f"{value:.2f} kg CO₂e")

                st.metric(label="Total Carbon Emission", value=f"{total:.2f} kg CO₂e")

                if total < 300:
                    st.success("Allow travel")
                elif 300 <= total <= 400:
                    st.warning("Moderate warning")
                else:
                    st.error("Suggest avoiding travel")
