import joblib
import numpy as np
import os

# Get correct path to model
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, '../models/model.pkl')

# Load model once (important for performance)
model = joblib.load(model_path)


def predict_status(temperature, flow_rate, water_level):
    try:
        # Convert input into proper format
        data = np.array([[temperature, flow_rate, water_level]])

        # Make prediction
        prediction = model.predict(data)[0]

        # Convert numeric output to label
        if prediction == 0:
            return "normal"
        else:
            return "blockage"

    except Exception as e:
        print("Prediction Error:", e)
        return "error"