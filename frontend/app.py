import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Title
st.title("SuperKart Store Sales Forecasting")

# -----------------------------
# SECTION 1: ONLINE PREDICTION
# -----------------------------
st.subheader("Online Prediction")

# Collect user input for product + store features
product_id = st.text_input("Product ID (e.g., FD123)")
product_weight = st.number_input("Product Weight", min_value=0.0, step=0.1)
product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
product_area = st.number_input("Product Allocated Area Ratio", min_value=0.0, max_value=1.0, step=0.01)
product_type = st.selectbox(
    "Product Type",
    ["Meat", "Snack Foods", "Hard Drinks", "Dairy", "Canned", "Soft Drinks",
     "Health and Hygiene", "Baking Goods", "Bread", "Breakfast", "Frozen Foods",
     "Fruits and Vegetables", "Household", "Seafood", "Starchy Foods", "Others"]
)
product_mrp = st.number_input("Product MRP", min_value=0.0, step=0.5)

store_id = st.text_input("Store ID (e.g., S001)")
store_year = st.number_input("Store Establishment Year", min_value=1900, max_value=2025, step=1)
store_size = st.selectbox("Store Size", ["High", "Medium", "Low"])
store_city = st.selectbox("Store City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox(
    "Store Type",
    ["Departmental Store", "Supermarket Type 1", "Supermarket Type 2", "Food Mart"]
)

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    "Product_Id": product_id,
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar,
    "Product_Allocated_Area": product_area,
    "Product_Type": product_type,
    "Product_MRP": product_mrp,
    "Store_Id": store_id,
    "Store_Establishment_Year": store_year,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_city,
    "Store_Type": store_type
}])

# Predict button
if st.button("Predict", type="primary"):
    response = requests.post(
        f"{BACKEND_URL}/v1/sales",
        json=input_data.to_dict(orient="records")[0]
    )
    if response.status_code == 200:
        prediction = response.json()["Predicted_Sales_Total"]
        st.success(f"Predicted Sales Revenue: {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# -----------------------------
# SECTION 2: BATCH PREDICTION
# -----------------------------
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(
            f"{BACKEND_URL}/v1/salesbatch",
            files={"file": uploaded_file}
        )
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)
        else:
            st.error("Unable to connect to the prediction API.")
