import requests
import json
from datetime import datetime

def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=47.6062&longitude=-122.3321&current=temperature_2m,is_day&temperature_unit=fahrenheit"
    response = requests.get(url)
    data = response.json()
    
    weather_data = {
        "current_time": datetime.utcnow().isoformat(),
        "current_temperature": data['current']['temperature_2m']
    }
    
    with open('weather.json', 'w') as f:
        json.dump(weather_data, f)

if __name__ == "__main__":
    fetch_weather()
