# AI Farming Assistant

🌿 AI Farming Assistant is an AI-powered intelligent assistant designed to empower farmers with smarter decision-making through real-time environmental data, machine learning models, and crop intelligence. It offers a comprehensive dashboard for crop recommendations, fertilizer planning, irrigation scheduling, pest detection, and yield predictions.

---

## ✨ Features

- ✅ **Crop Recommendation**: Suggests optimal crops based on soil and weather data.
- ✅ **Smart Fertilizer Planning**: Provides tailored fertilizer recommendations.
- ✅ **Irrigation Schedule Advice**: Optimizes water usage with scheduling.
- ✅ **Pest & Disease Detection**: Analyzes images for pest and disease identification.
- ✅ **Real-time Weather Forecast Integration**: Leverages live weather updates.
- ✅ **Yield Prediction**: Estimates crop yield using historical and current data.
- ✅ **Soil Health Analysis**: Assesses soil conditions with improvement tips.
- ✅ **Admin Dashboard**: Offers monitoring, reports, and downloadable PDFs.

---

## 📥 Inputs

- **Soil Data**: N, P, K values, pH, moisture, soil type.
- **Weather**: Temperature, humidity, rainfall, wind speed.
- **Location**: Region/State.
- **Land Info**: Area, irrigation type.
- **Crop Type & Growth Stage**: Manual input or detected.
- **Images**: For pest/disease detection.
- **Historical Records**: Past yield, irrigation/fertilization logs.

---

## 📤 Outputs

- **Recommended Crop**: Top 3 crops with suitability scores.
- **Fertilizer Recommendations**: Quantities for Urea, DAP, NPK, etc.
- **Irrigation Advice**: Schedule and water amount.
- **Pest/Disease Risk Alerts**: Text and image-based classification.
- **Yield Prediction**: Based on inputs and history.
- **Weather-Based Notifications**: Alerts for rain, wind, heatwave.
- **Soil Health Report**: Insights with improvement tips.
- **Growth Stage Tips**: Actionable advice.
- **Admin View**: Comprehensive reports, usage stats, downloadable PDFs.

---

## 🛠️ Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Frontend    | React.js / Flutter / Next.js      |
| Backend     | FastAPI / Node.js / Flask         |
|Custom ML    | Rule-Based, Decision Tree,        |
|               Linear Regression,Threshold Rules |
|Models       | Scikit-learn, TensorFlow, Keras   |
| CV Models   | OpenCV, MobileNet, YOLOv8         |
| DB & Auth   | Firebase / PostgreSQL / MongoDB   |
| APIs        | OpenWeatherMap, SoilGrids, REST   |
| Deployment  | AWS / Render / HuggingFace        |

---

## 🧪 AI/ML Models Used

| Task                 | Model                        |
|----------------------|------------------------------|
| Crop Recommendation  | Random Forest / XGBoost      |
| Pest Detection       | CNN (MobileNet, YOLOv8)      |
| Yield Prediction     | Regression Models            |
| Fertilizer Planning  | Rule-based + ML Hybrid       |
| Irrigation Planning  | Time Series + Rule Engine    |

---

## 📦 Folder Structure

```
.
├── backend/
├── frontend/
├── models/
├── data/
│   └── Crop_recommendation_enriched.csv
├── utils/
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/Theophilus-victor/AI
cd agromind-ai-assistant
```

### Set Up the Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📸 Screenshots

### 1. Farming Advisory System Interface
![Farming Advisory System Interface](attachment://Farming_Advisory_System_Interface.png)  
*Description: The input form for farming parameters including city name, temperature, humidity, rainfall, and more.*

### 2. Crop Recommendation Analysis
![Crop Recommendation Analysis](attachment://Crop_Recommendation_Analysis.png)  
*Description: Sample output showing recommended crop (muskmelon), irrigation method (flood), water requirement (6.99 mm/day), and predicted yield (2.99 tons).*

### 3. Fertilizer Recommendation
![Fertilizer Recommendation](attachment://Fertilizer_Recommendation.png)  
*Description: Detailed fertilizer plan with quantities for Urea (15 kg/acre), DAP (39 kg/acre), and MOP (90 kg/acre).*

### 4. Weather Alerts
![Weather Alerts](attachment://Weather_Alerts.png)  
*Description: Real-time weather update for Coimbatore with temperature, wind speed, and rain alerts for the next 5 days.*

### 5. Analysis Results
![Analysis Results](attachment://Analysis_Results.png)  
*Description: Comprehensive analysis including weather alerts, crop recommendation (kidney beans), fertilizer recommendation, and crop condition assessment.*

### 6. Crop Condition Assessment
![Crop Condition Assessment](attachment://Crop_Condition_Assessment.png)  
*Description: Assessment indicating suboptimal crop conditions.* 
