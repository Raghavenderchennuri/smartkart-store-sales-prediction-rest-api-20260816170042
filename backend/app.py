# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
rental_price_predictor_api = Flask("Retail Stores Price Predictor")

# Load the trained machine learning model
model = joblib.load("super_kart_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@rental_price_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Decision Platform API!"

# Define an endpoint for single property prediction (POST request)
@rental_price_predictor_api.post('/v1/store_sales')
def predict_rental_price():
    """
    This function handles POST requests to the '/v1/store_sales' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted store_sales price as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Store_Type': property_data['Store_Type'],
        'Store_Location_City_Type': property_data['Store_Location_City_Type'],
        'Store_Size': property_data['Store_Size'],
        'Product_Type': property_data['Product_Type']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get log_price)
    predicted_log_price = model.predict(input_data)[0]

    # Calculate actual price
    predicted_price = np.exp(predicted_log_price)

    # Convert predicted_price to Python float
    predicted_price = round(float(predicted_price), 2)
    # The conversion above is needed as we convert the model prediction (log price) to actual price using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Price (in dollars)': predicted_price})


# Define an endpoint for batch prediction (POST request)
@rental_price_predictor_api.post('/v1/store_salesbatch')
def predict_store_sales_price_batch():
    """
    This function handles POST requests to the '/v1/store_salesbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted store_sales prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_log_prices = model.predict(input_data).tolist()

    # Calculate actual prices
    predicted_prices = [round(float(np.exp(Product_Store_Sales_Total)), 2) for Product_Store_Sales_Total in predict_store_sales_price_batch]

    # Create a dictionary of predictions with property IDs as keys
    property_ids = input_data['id'].tolist()  # Assuming 'id' is the property ID column
    output_dict = dict(zip(property_ids, predicted_prices))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    rental_price_predictor_api.run(debug=True)
