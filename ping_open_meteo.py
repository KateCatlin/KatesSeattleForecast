import requests
import schedule
import time

def get_seattle_forecast():
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=47.6062&longitude=-122.3321&current_weather=true")
    if response.status_code == 200:
        data = response.json()
        current_weather = data.get("current_weather", {})
        print(f"Current weather in Seattle: {current_weather}")
    else:
        print("Failed to get the weather data")

schedule.every().hour.do(get_seattle_forecast)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
