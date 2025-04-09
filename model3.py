import pandas as pd

class CropConditionModel:
    def __init__(self):
        self.valid_soil_types = []
        
    def train(self, df):
        """Extract valid categories from dataset"""
        self.valid_soil_types = list(df['Soil Type'].unique())
        print("✅ Trained Crop Condition Assessment Model")
        
    def classify(self, n, p, k, temperature, humidity, ph, rainfall, 
                 soil_moisture, water_requirement, soil_type):
        """Classify crop condition as Optimal or Suboptimal"""
        # Rule 1: Core conditions for "Optimal"
        if (70 <= n <= 100 and 
            40 <= p <= 60 and 
            35 <= k <= 50 and 
            20 <= temperature <= 30 and 
            70 <= humidity <= 90 and 
            5.5 <= ph <= 7.0 and 
            200 <= rainfall <= 300 and 
            soil_moisture >= 20):
            return "Optimal"
        
        # Rule 2: Soil type-specific conditions
        if soil_type == "Sandy" and soil_moisture < 15:
            return "Suboptimal"
        if soil_type == "Clay" and soil_moisture > 40:
            return "Suboptimal"
        
        # Rule 3: Water requirement conditions
        if water_requirement > 8 and rainfall < 200:
            return "Suboptimal"

        # Default fallback
        return "Suboptimal"
    
    def predict(self, input_data):
        """Make prediction based on input data"""
        try:
            result = self.classify(
                input_data['N'], 
                input_data['P'],
                input_data['K'],
                input_data['temperature'],
                input_data['humidity'],
                input_data['ph'],
                input_data['rainfall'],
                input_data['Soil Moisture (%)'],
                input_data['Water Requirement (mm/day)'],
                input_data['Soil Type']
            )
            
            return f"\n🌱 Crop Condition Assessment:\n{result}"
            
        except Exception as e:
            return f"Error: {str(e)}"

# Main execution
if __name__ == "__main__":
    try:
        # Load data from CSV
        data = pd.read_csv("Crop_recommendation_enriched.csv")
        
        # Create and train model
        model = CropConditionModel()
        model.train(data)
        
        print("\n=== Crop Condition Assessment System ===")
        print("Enter the following details:")
        
        # Get user input
        user_input = {}
        user_input['N'] = float(input("Nitrogen content (N): "))
        user_input['P'] = float(input("Phosphorus content (P): "))
        user_input['K'] = float(input("Potassium content (K): "))
        user_input['temperature'] = float(input("Temperature (°C): "))
        user_input['humidity'] = float(input("Humidity (%): "))
        user_input['ph'] = float(input("pH value: "))
        user_input['rainfall'] = float(input("Rainfall (mm): "))
        user_input['Soil Moisture (%)'] = float(input("Soil Moisture (%): "))
        user_input['Water Requirement (mm/day)'] = float(input("Water Requirement (mm/day): "))
        
        # Get soil type with validation
        print(f"\nValid options for Soil Type: {', '.join(model.valid_soil_types)}")
        while True:
            value = input("Soil Type: ")
            if value in model.valid_soil_types:
                user_input['Soil Type'] = value
                break
            else:
                print(f"Invalid input. Choose from: {', '.join(model.valid_soil_types)}")
        
        # Get prediction
        result = model.predict(user_input)
        print(result)
        
    except FileNotFoundError:
        print("Error: 'Crop_recommendation_enriched.csv' not found.")
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
