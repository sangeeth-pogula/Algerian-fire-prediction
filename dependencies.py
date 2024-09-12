import pickle
import pandas as pd
import numpy as np
import json
import logging
from logging.handlers import RotatingFileHandler


# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = 'app.log'

# Set up file handler with rotation
file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Set up console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# Get the root logger and configure handlers
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Load the saved bounds from the JSON file
try:
    with open('Preprocessors/outlier_bounds.json', 'r') as file:
        outlier_bounds = json.load(file)
except FileNotFoundError:
    logging.error("outlier_bounds.json file not found.")
    outlier_bounds = {}

def load_knn_imputer(model_path):
    try:
        with open(model_path, 'rb') as file:
            knn_model = pickle.load(file)
        return knn_model
    except FileNotFoundError:
        logging.error(f"KNN imputer model file not found at {model_path}.")
        raise
    except pickle.PickleError:
        logging.error(f"Failed to load KNN imputer model from {model_path}.")
        raise

def outliers_function(df, bounds_dict, knn_model, columns_to_handle):
    try:
        # Step 1: Replace out-of-bounds values with NaN
        for col in columns_to_handle:
            if col in bounds_dict:
                lower_bound = bounds_dict[col]['lower_bound']
                upper_bound = bounds_dict[col]['upper_bound']
                df[col] = df[col].apply(lambda x: x if lower_bound <= x <= upper_bound else np.nan)

        # Step 2: Apply KNN imputer if there are NaN values
        if df.isna().sum().sum() > 0:  # Check if there are any NaN values
            imputed_values = knn_model.transform(df[columns_to_handle])
            df[columns_to_handle] = pd.DataFrame(imputed_values, columns=columns_to_handle)

    except Exception as e:
        logging.error(f"Error in outliers_function: {e}")
        raise

    return df

def load_robust_scaler(model_path):
    try:
        with open(model_path, 'rb') as file:
            robust_scaler = pickle.load(file)
        return robust_scaler
    except FileNotFoundError:
        logging.error(f"RobustScaler model file not found at {model_path}.")
        raise
    except pickle.PickleError:
        logging.error(f"Failed to load RobustScaler model from {model_path}.")
        raise

def apply_robust_scaler(df, scaler, columns_to_handle):
    try:
        scaled_values = scaler.transform(df[columns_to_handle])
        df[columns_to_handle] = pd.DataFrame(scaled_values, columns=columns_to_handle)
    except Exception as e:
        logging.error(f"Error in apply_robust_scaler: {e}")
        raise

    return df

def data_transormer(data):
    try:
        columns_to_handle = [column for column in data.columns if column not in ["region", "Classes"]]
        with open('Preprocessors/outlier_bounds.json', 'r') as file:
            outlier_bounds = json.load(file)
        
        knn_model = load_knn_imputer('Preprocessors/KNNImputer.pkl')
        data = outliers_function(data, outlier_bounds, knn_model, columns_to_handle)
        
        scaler = load_robust_scaler('Preprocessors/RobustScalar.pkl')
        data = apply_robust_scaler(data, scaler, columns_to_handle)
        logging.info("Data transformation complete.")
        return data
    except Exception as e:
        logging.error(f"Error in data_transformer: {e}")
        raise

def predict_FWI(data):
    try:
         # Ensure the dtype of specific columns are float
        columns_to_float = ['Rain', 'FFMC', 'DMC', 'ISI']
        for col in columns_to_float:
            if col in data.columns:
                if not pd.api.types.is_float_dtype(data[col]):
                    data[col] = pd.to_numeric(data[col], errors='coerce')
        data = data_transformer(data)

        with open("Model/LassoCV.pkl", 'rb') as model_data:
            model = pickle.load(model_data)
        
        prediction = model.predict(data)
        logging.info(f"Prediction: {prediction[0]}")
        return round(prediction[0], 2)
    except Exception as e:
        logging.error(f"Error in predict_FWI: {e}")
        raise