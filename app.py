from flask import Flask, render_template, request, jsonify
from integrated_model import IntegratedFarmingSystem
import datetime
import io
import sys
import re

app = Flask(__name__)

# Function to capture print output
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout

@app.route('/')
def home():
    return render_template('admin_home.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get form data
        form_data = request.form
        
        # Convert form data to the format expected by the model
        user_inputs = {
            'city': form_data['city'],
            'N': float(form_data['N']),
            'P': float(form_data['P']),
            'K': float(form_data['K']),
            'temperature': float(form_data['temperature']),
            'humidity': float(form_data['humidity']),
            'ph': float(form_data['ph']),
            'rainfall': float(form_data['rainfall']),
            'Wind Speed (km/h)': float(form_data['wind_speed']),
            'Soil Moisture (%)': float(form_data['soil_moisture']),
            'Water Requirement (mm/day)': float(form_data['water_requirement']),
            'Area (sqm)': float(form_data['area']),
            'Soil Type': form_data['soil_type'],
            'Region/State': form_data['region'],
            'Last Irrigation Date': form_data['last_irrigation_date'],
            'Last Fertilization Date': form_data['last_fertilization_date']
        }
        
        # Initialize the integrated system
        system = IntegratedFarmingSystem()
        
        # Capture the output from the model
        with Capturing() as output:
            system.run_all_models(user_inputs)
        
        # Process the output into sections
        sections = []
        current_section = []
        
        for line in output:
            if line.strip():  # Only process non-empty lines
                if line.startswith('=' * 50):  # Section separator
                    if current_section:
                        sections.append(current_section)
                        current_section = []
                else:
                    current_section.append(line)
        
        if current_section:
            sections.append(current_section)
        
        # Return success response with the formatted output
        return jsonify({
            'status': 'success',
            'message': 'Analysis completed successfully',
            'output': sections
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True) 