import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import warnings
warnings.filterwarnings('ignore')

class FertilizerRecommendationModel:
    def __init__(self):
        self.dt_classifier = DecisionTreeClassifier(
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        self.encoders = {
            'label': LabelEncoder(),
            'Soil Type': LabelEncoder(),
            'target': LabelEncoder()
        }
        self.features = ['N', 'P', 'K', 'label', 'Soil Type']
        self.optimal_ranges = {}
        self.fertilizer_options = {
            'N': {'Urea': 0.46, 'Ammonium Nitrate': 0.34},
            'P': {'DAP': 0.46, 'SSP': 0.16},
            'K': {'MOP': 0.60, 'Potassium Sulfate': 0.50}
        }

    def calculate_optimal_ranges(self, df):
        optimal_ranges = {}
        for crop in df['label'].unique():
            crop_data = df[df['label'] == crop]
            optimal_ranges[crop] = {
                'N': (crop_data['N'].quantile(0.25), crop_data['N'].quantile(0.75)),
                'P': (crop_data['P'].quantile(0.25), crop_data['P'].quantile(0.75)),
                'K': (crop_data['K'].quantile(0.25), crop_data['K'].quantile(0.75))
            }
        return optimal_ranges

    def create_fertilizer_recommendation(self, n, p, k, crop):
        if crop not in self.optimal_ranges:
            return "Unknown crop"
        
        recommendation = []
        n_min, n_max = self.optimal_ranges[crop]['N']
        p_min, p_max = self.optimal_ranges[crop]['P']
        k_min, k_max = self.optimal_ranges[crop]['K']
        
        # Nitrogen
        if n < n_min:
            for fert, n_content in self.fertilizer_options['N'].items():
                amount = (n_min - n) / n_content
                recommendation.append(f"Add {fert}: {round(amount)} kg/acre")
                break  # Use first available fertilizer
        
        # Phosphorus
        if p < p_min:
            for fert, p_content in self.fertilizer_options['P'].items():
                amount = (p_min - p) / p_content
                recommendation.append(f"Add {fert}: {round(amount)} kg/acre")
                break
        
        # Potassium
        if k < k_min:
            for fert, k_content in self.fertilizer_options['K'].items():
                amount = (k_min - k) / k_content
                recommendation.append(f"Add {fert}: {round(amount)} kg/acre")
                break
        
        return "; ".join(recommendation) if recommendation else "No fertilizer needed"

    def train(self, df):
        # Calculate optimal ranges
        self.optimal_ranges = self.calculate_optimal_ranges(df)
        
        # Create fertilizer recommendations
        df['Fertilizer_Recommendation'] = df.apply(
            lambda row: self.create_fertilizer_recommendation(
                row['N'], row['P'], row['K'], row['label']
            ), axis=1
        )
        
        # Prepare features and target
        X = df[self.features]
        y = df['Fertilizer_Recommendation']
        
        # Encode categorical variables
        X['label'] = self.encoders['label'].fit_transform(X['label'])
        X['Soil Type'] = self.encoders['Soil Type'].fit_transform(X['Soil Type'])
        y = self.encoders['target'].fit_transform(y)
        
        # Train model
        self.dt_classifier.fit(X, y)
        print("✅ Trained Fertilizer Recommendation Model")
        
        # Store valid categories
        self.valid_crops = list(self.encoders['label'].classes_)
        self.valid_soils = list(self.encoders['Soil Type'].classes_)

    def predict(self, input_data):
        try:
            if isinstance(input_data, dict):
                input_df = pd.DataFrame([input_data])
            else:
                input_df = input_data.copy()
            
            # Check if the crop is known
            if 'label' not in input_df.columns:
                return "Error: No crop (label) specified"
                
            crop = input_df['label'].iloc[0]
            if crop not in self.valid_crops:
                return f"Error: Unknown crop '{crop}'. Valid crops are: {', '.join(self.valid_crops)}"
                
            # Direct fertilizer recommendation based on crop and NPK values
            # This is more reliable than classification for new/unseen values
            n = input_df['N'].iloc[0]
            p = input_df['P'].iloc[0]
            k = input_df['K'].iloc[0]
            
            recommendation = self.create_fertilizer_recommendation(n, p, k, crop)
            
            return f"\n🌿 Fertilizer Recommendation:\n{recommendation}"
            
        except Exception as e:
            return f"Error: {str(e)}"

# Main script
if __name__ == "__main__":
    try:
        # Load data
        data = pd.read_csv("Crop_recommendation_enriched.csv")
        
        # Create and train model
        model = FertilizerRecommendationModel()
        model.train(data)
        
        # User input interface
        print("\n=== Fertilizer Recommendation System ===")
        print("Enter the following details:")
        
        user_input = {}
        user_input['N'] = float(input("Nitrogen content (N): "))
        user_input['P'] = float(input("Phosphorus content (P): "))
        user_input['K'] = float(input("Potassium content (K): "))
        
        # Show valid crop options
        print(f"\nValid options for Crop: {', '.join(model.valid_crops)}")
        while True:
            value = input("Crop: ")
            if value in model.valid_crops:
                user_input['label'] = value
                break
            else:
                print(f"Invalid input. Choose from: {', '.join(model.valid_crops)}")
        
        # Show valid soil type options
        print(f"\nValid options for Soil Type: {', '.join(model.valid_soils)}")
        while True:
            value = input("Soil Type: ")
            if value in model.valid_soils:
                user_input['Soil Type'] = value
                break
            else:
                print(f"Invalid input. Choose from: {', '.join(model.valid_soils)}")
        
        # Get prediction
        result = model.predict(user_input)
        print(result)
        
    except FileNotFoundError:
        print("Error: 'Crop_recommendation_enriched.csv' not found.")
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Unexpected Error: {e}")