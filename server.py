from flask import Flask, render_template, send_from_directory
import requests
import os
import json

app = Flask(__name__)

def get_seattle_forecast():
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=47.6062&longitude=-122.3321&current_weather=true")
    if response.status_code == 200:
        data = response.json()
        current_weather = data.get("current_weather", {})
        with open("weather.json", "w") as file:
            json.dump(current_weather, file)
        return current_weather
    else:
        return None

@app.route("/")
def index():
    weather = get_seattle_forecast()
    return render_template("index.html", weather=weather)

@app.route("/weather.json")
def weather_json():
    return send_from_directory(os.getcwd(), "weather.json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))