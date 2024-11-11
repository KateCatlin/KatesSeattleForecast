from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather.json')
def weather_json():
    try:
        # Fetch weather data directly from API
        url = "https://api.open-meteo.com/v1/forecast?latitude=47.6062&longitude=-122.3321&current=temperature_2m&temperature_unit=fahrenheit"
        response = requests.get(url)
        data = response.json()
        
        # Format the response data
        weather_data = {
            "current_time": datetime.now().isoformat(),
            "current_temperature": data['current']['temperature_2m']
        }
        
        print("Serving weather data:", weather_data)  # Debug log
        return jsonify(weather_data)
        
    except Exception as e:
        print("Error fetching weather:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)