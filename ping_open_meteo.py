import requests
import json

def get_seattle_forecast():
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=47.6062&longitude=-122.3321&current_weather=true")
    if response.status_code == 200:
        data = response.json()
        current_weather = data.get("current_weather", {})
        with open("weather.json", "w") as file:
            json.dump(current_weather, file)
    else:
        print("Failed to get the weather data")

get_seattle_forecast()
