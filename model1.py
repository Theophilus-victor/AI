import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
import datetime

class CropRecommendationModel:
    def __init__(self):
        # Main crop recommendation classifier
        self.crop_model = RandomForestClassifier(n_estimators=100, random_state=42)
        # Irrigation method classifier
        self.irrigation_model = RandomForestClassifier(n_estimators=100, random_state=42)
        # Water requirement regressor
        self.water_model = RandomForestRegressor(n_estimators=100, random_state=42)
        # Yield regressor
        self.yield_model = RandomForestRegressor(n_estimators=100, random_state=42)

        self.label_encoders = {}
        self.feature_columns = [
            'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall',
            'Wind Speed (km/h)', 'Soil Moisture (%)', 'Area (sqm)'
        ]
        self.categorical_columns = ['Soil Type', 'Region/State']
        self.date_columns = ['Last Irrigation Date', 'Last Fertilization Date']
        self.valid_categories = {col: [] for col in self.categorical_columns}

    def preprocess_data(self, df):
        df_processed = df.copy()
        current_date = datetime.datetime(2025, 4, 5)
        
        # Convert date columns to days since today
        for date_col in self.date_columns:
            # Convert from DD-MM-YYYY to datetime
            df_processed[date_col] = pd.to_datetime(df_processed[date_col], errors='coerce', format='%d-%m-%Y')
            df_processed[date_col] = (current_date - df_processed[date_col]).dt.days.fillna(0)
        
        # Encode categorical variables
        for col in self.categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df_processed[col] = self.label_encoders[col].fit_transform(df_processed[col])
                self.valid_categories[col] = list(self.label_encoders[col].classes_)
            else:
                df_processed[col] = self.label_encoders[col].transform(df_processed[col])
        
        return df_processed

    def train(self, df):
        df_processed = self.preprocess_data(df)

        # Features for all models
        X = df_processed[self.feature_columns + self.categorical_columns + self.date_columns]

        # 1. Train crop recommendation model
        y_crop = df_processed['label']
        self.crop_model.fit(X, y_crop)
        print("✅ Trained Crop Recommendation Model")

        # 2. Train irrigation method model
        y_irrigation = df_processed['Irrigation Type']
        irrigation_encoder = LabelEncoder()
        y_irrigation_encoded = irrigation_encoder.fit_transform(y_irrigation)
        self.label_encoders['Irrigation Type'] = irrigation_encoder
        self.irrigation_model.fit(X, y_irrigation_encoded)
        print("✅ Trained Irrigation Method Model")

        # 3. Train water requirement model
        y_water = df_processed['Water Requirement (mm/day)']
        self.water_model.fit(X, y_water)
        print("✅ Trained Water Requirement Regressor")

        # 4. Train predicted yield model
        y_yield = df_processed['Past Yield (tons)']
        self.yield_model.fit(X, y_yield)
        print("✅ Trained Yield Prediction Regressor")

        self.all_crops = list(self.crop_model.classes_)

    def predict(self, input_data):
        if isinstance(input_data, dict):
            input_df = pd.DataFrame([input_data])
        else:
            input_df = input_data.copy()
            
        input_processed = self.preprocess_data(input_df)
        X = input_processed[self.feature_columns + self.categorical_columns + self.date_columns]

        # 1. Predict top crop
        probabilities = self.crop_model.predict_proba(X)[0]
        crop_prob_pairs = list(zip(self.all_crops, probabilities))
        top_crop = sorted(crop_prob_pairs, key=lambda x: x[1], reverse=True)[0]

        # 2. Predict irrigation type
        irrigation_pred = self.irrigation_model.predict(X)[0]
        irrigation_label = self.label_encoders['Irrigation Type'].inverse_transform([irrigation_pred])[0]

        # 3. Predict water requirement
        water_req = self.water_model.predict(X)[0]

        # 4. Predict yield
        predicted_yield = self.yield_model.predict(X)[0]

        # Format output
        result = "\n🌱 Crop Recommendation Analysis:\n"
        result += "\n1. ✅ Recommended Crop:\n"
        crop, prob = top_crop
        result += f"   - {crop}\n"
        result += f"\n2. 🚿 Predicted Irrigation Method: {irrigation_label}"
        result += f"\n3. 💧 Estimated Water Requirement (per square meter): {water_req:.2f} mm/day"
        result += f"\n4. 🌾 Predicted Yield: {predicted_yield:.2f} tons"
        
        return result

# === CLI Script ===
if __name__ == "__main__":
    try:
        data = pd.read_csv("Crop_recommendation_enriched.csv")
        model = CropRecommendationModel()
        model.train(data)

        print("\n=== Crop Recommendation System ===")
        print("Enter the following details for prediction:")

        user_input = {}
        user_input['N'] = float(input("Nitrogen content (N): "))
        user_input['P'] = float(input("Phosphorus content (P): "))
        user_input['K'] = float(input("Potassium content (K): "))
        user_input['temperature'] = float(input("Temperature (°C): "))
        user_input['humidity'] = float(input("Humidity (%): "))
        user_input['ph'] = float(input("pH value: "))
        user_input['rainfall'] = float(input("Rainfall (mm): "))
        user_input['Wind Speed (km/h)'] = float(input("Wind Speed (km/h): "))
        user_input['Soil Moisture (%)'] = float(input("Soil Moisture (%): "))
        user_input['Area (sqm)'] = float(input("Area (sqm): "))

        # Categorical inputs
        for field in ['Soil Type', 'Region/State']:
            valid_options = model.valid_categories[field]
            print(f"\nValid options for {field}: {', '.join(valid_options)}")
            while True:
                value = input(f"{field}: ")
                if value in valid_options:
                    user_input[field] = value
                    break
                else:
                    print(f"Invalid input. Choose from: {', '.join(valid_options)}")

        print("\nEnter the following dates (DD-MM-YYYY):")
        user_input['Last Irrigation Date'] = input("Last Irrigation Date: ")
        user_input['Last Fertilization Date'] = input("Last Fertilization Date: ")

        prediction = model.predict(user_input)
        print(prediction)

    except FileNotFoundError:
        print("Error: 'Crop_recommendation_enriched.csv' not found.")
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
