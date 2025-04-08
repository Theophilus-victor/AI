import pandas as pd
import datetime
from model1 import CropRecommendationModel
from model2 import FertilizerRecommendationModel
from model3 import CropConditionModel
import model4
import random

class IntegratedFarmingSystem:
    def __init__(self):
        self.crop_model = CropRecommendationModel()
        self.fertilizer_model = FertilizerRecommendationModel()
        self.condition_model = CropConditionModel()
        
        # Load dataset for training and valid values
        try:
            self.data = pd.read_csv("Crop_recommendation_enriched.csv")
            print("✅ Dataset loaded successfully")
        except FileNotFoundError:
            print("Error: 'Crop_recommendation_enriched.csv' not found.")
            exit(1)
            
        # Train all models
        self.train_models()
        
    def train_models(self):
        """Train all models with the dataset"""
        self.crop_model.train(self.data)
        self.fertilizer_model.train(self.data)
        self.condition_model.train(self.data)
        
    def collect_inputs(self):
        """Collect all required inputs from user"""
        print("\n=== Integrated Farming Advisory System ===")
        print("Please enter the following details once:")
        
        user_inputs = {}
        
        # Get city for weather information
        user_inputs['city'] = input("City name (for weather forecast): ")
        
        # Get numerical inputs
        user_inputs['N'] = float(input("Nitrogen content (N): "))
        user_inputs['P'] = float(input("Phosphorus content (P): "))
        user_inputs['K'] = float(input("Potassium content (K): "))
        user_inputs['temperature'] = float(input("Temperature (°C): "))
        user_inputs['humidity'] = float(input("Humidity (%): "))
        user_inputs['ph'] = float(input("pH value: "))
        user_inputs['rainfall'] = float(input("Rainfall (mm): "))
        user_inputs['Wind Speed (km/h)'] = float(input("Wind Speed (km/h): "))
        user_inputs['Soil Moisture (%)'] = float(input("Soil Moisture (%): "))
        user_inputs['Water Requirement (mm/day)'] = float(input("Water Requirement (mm/day): "))
        user_inputs['Area (sqm)'] = float(input("Area (sqm): "))
        
        # Categorical inputs with validation
        # Soil Type
        print(f"\nValid options for Soil Type: {', '.join(self.crop_model.valid_categories['Soil Type'])}")
        while True:
            value = input("Soil Type: ")
            if value in self.crop_model.valid_categories['Soil Type']:
                user_inputs['Soil Type'] = value
                break
            else:
                print(f"Invalid input. Choose from: {', '.join(self.crop_model.valid_categories['Soil Type'])}")
        
        # Region/State
        print(f"\nValid options for Region/State: {', '.join(self.crop_model.valid_categories['Region/State'])}")
        while True:
            value = input("Region/State: ")
            if value in self.crop_model.valid_categories['Region/State']:
                user_inputs['Region/State'] = value
                break
            else:
                print(f"Invalid input. Choose from: {', '.join(self.crop_model.valid_categories['Region/State'])}")
        
        # Dates
        print("\nEnter the following dates (DD-MM-YYYY):")
        user_inputs['Last Irrigation Date'] = input("Last Irrigation Date: ")
        user_inputs['Last Fertilization Date'] = input("Last Fertilization Date: ")
        
        return user_inputs
    
    def run_all_models(self, user_inputs):
        """Run all models with collected inputs"""
        print("\n" + "="*50)
        print("RUNNING ALL ADVISORY MODULES")
        print("="*50)
        
        # 1. Display weather information and alerts
        print("\n[MODULE 1: WEATHER ALERTS]")
        model4.display_weather_info(user_inputs['city'])
        
        # 2. Get crop recommendation
        print("\n" + "="*50)
        print("[MODULE 2: CROP RECOMMENDATION]")
        crop_result = self.crop_model.predict(user_inputs)
        print(crop_result)
        
        # Extract recommended crop to use as 'label' for model2
        recommended_crop = None
        
        result_lines = crop_result.split('\n')
        
        # Loop through each line to find the crop
        for i, line in enumerate(result_lines):
            # Try multiple patterns to be more robust
            if "Recommended Crop" in line:
                # Look for crop name in the next few lines
                for j in range(i+1, min(i+5, len(result_lines))):
                    next_line = result_lines[j]
                    
                    # Try different patterns
                    if next_line.strip().startswith('   - '):
                        recommended_crop = next_line.strip()[5:].strip()
                        break
                
                if recommended_crop:
                    break
        
        # Fallback: If we couldn't extract the crop, use a random fallback crop
        if not recommended_crop:
            fallback_crops = ['rice', 'maize', 'chickpea', 'pigeonpeas']
            recommended_crop = random.choice(fallback_crops)
        
        # 3. Get fertilizer recommendation
        print("\n" + "="*50)
        print("[MODULE 3: FERTILIZER RECOMMENDATION]")
        if recommended_crop:
            # Create a separate input dict with just the fields needed for fertilizer model
            fertilizer_inputs = {
                'N': user_inputs['N'],
                'P': user_inputs['P'],
                'K': user_inputs['K'],
                'label': recommended_crop,
                'Soil Type': user_inputs['Soil Type']
            }
            fertilizer_result = self.fertilizer_model.predict(fertilizer_inputs)
            print(fertilizer_result)
        else:
            print("Error: Could not extract crop recommendation for fertilizer module")
            print("Try running the fertilizer model separately")
        
        # 4. Get crop condition assessment
        print("\n" + "="*50)
        print("[MODULE 4: CROP CONDITION ASSESSMENT]")
        condition_result = self.condition_model.predict(user_inputs)
        print(condition_result)
        
        print("\n" + "="*50)
        print("All advisory modules completed successfully!")
        print("="*50)

def main():
    try:
        # Create integrated system
        system = IntegratedFarmingSystem()
        
        # Collect inputs once
        inputs = system.collect_inputs()
        
        # Run all models
        system.run_all_models(inputs)
        
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main() 