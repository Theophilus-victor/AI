import requests
import datetime
import time

# Your OpenWeather API key
API_KEY = "409acf13939ff8c90c9d06b165c4a2d1"  # Updated with your key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

def get_current_weather(city):
    """Fetch current weather data for a given city"""
    params = {
        "q": city,
        "appid": '409acf13939ff8c90c9d06b165c4a2d1',  # API key used here
        "units": "metric"  # Use 'imperial' for Fahrenheit
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current weather: {e}")
        return None

def get_forecast(city):
    """Fetch 5-day forecast data for a given city"""
    params = {
        "q": city,
        "appid": '409acf13939ff8c90c9d06b165c4a2d1',  # API key used here
        "units": "metric"
    }
    
    try:
        response = requests.get(FORECAST_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast: {e}")
        return None

def check_weather_alerts(current_data, forecast_data):
    """Analyze weather data and generate alerts with advice"""
    alerts = []
    
    if not current_data or not forecast_data:
        return alerts
    
    # Current weather conditions
    current_temp = current_data['main']['temp']
    current_weather = current_data['weather'][0]['main'].lower()
    wind_speed = current_data['wind']['speed']  # m/s
    
    # Check current conditions
    if "rain" in current_weather:
        alerts.append("🌧 Current Rain Alert: Avoid outdoor activities and protect equipment.")
    
    if current_temp > 35:
        alerts.append("☀️ Heatwave Alert: Stay hydrated and avoid strenuous outdoor work.")
    
    if wind_speed > 15:  # Approx 33 mph
        alerts.append("💨 Wind Storm Alert: Secure loose objects and avoid high structures.")
    
    # Check forecast for next 48 hours (16 entries at 3-hour intervals)
    for forecast in forecast_data['list'][:16]:
        timestamp = forecast['dt']
        forecast_time = datetime.datetime.fromtimestamp(timestamp)
        temp = forecast['main']['temp']
        weather = forecast['weather'][0]['main'].lower()
        wind = forecast['wind']['speed']
        
        time_diff = (forecast_time - datetime.datetime.now()).total_seconds() / 3600
        
        if time_diff <= 48:  # Within 48 hours
            if "rain" in weather:
                alerts.append(f"🌧 Rain expected in {int(time_diff)}h. Delay fertilizer application.")
            if temp > 35:
                alerts.append(f"☀️ Heatwave expected in {int(time_diff)}h. Plan indoor activities.")
            if wind > 15:
                alerts.append(f"💨 High winds expected in {int(time_diff)}h. Secure outdoor items.")
    
    return alerts

def display_weather_info(city):
    """Display current weather and alerts"""
    current_data = get_current_weather(city)
    forecast_data = get_forecast(city)
    
    if current_data and current_data.get('cod') == 200:
        temp = current_data['main']['temp']
        weather = current_data['weather'][0]['description']
        wind = current_data['wind']['speed']
        
        print(f"\nCurrent Weather in {city}:")
        print(f"Temperature: {temp}°C")
        print(f"Conditions: {weather}")
        print(f"Wind Speed: {wind} m/s")
        
        # Get and display alerts
        alerts = check_weather_alerts(current_data, forecast_data)
        if alerts:
            print("\nWeather Alerts:")
            for alert in alerts:
                print(f"- {alert}")
        else:
            print("\nNo significant weather alerts at this time.")
    else:
        print(f"Could not fetch weather data for {city}")

def main():
    print("Weather Alert System")
    city = input("Enter city name: ")
    
    while True:
        display_weather_info(city)
        print(f"\nLast updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(1800)  # Update every 30 minutes
        
if __name__ == "__main__":
    main()  # Run the program directly with your API key