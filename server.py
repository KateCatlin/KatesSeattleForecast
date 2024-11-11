from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import os
import pytz

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather.json')
def weather_json():
    try:
        # Updated URL to include precipitation data
        url = "https://api.open-meteo.com/v1/forecast?latitude=47.6062&longitude=-122.3321&current=temperature_2m,precipitation&temperature_unit=fahrenheit"
        response = requests.get(url)
        data = response.json()
        
        # Get current time in Seattle
        seattle_tz = pytz.timezone('America/Los_Angeles')
        seattle_time = datetime.now(seattle_tz)
        
        temp = data['current']['temperature_2m']
        is_raining = data['current']['precipitation'] > 0
        
        # Determine clothing recommendation
        if is_raining:
            clothing = "Hey pal, wear a rain jacket! It's raining!"
        elif temp > 70:
            clothing = "Go with a tee-shirt, so hot right now!"
        elif temp > 50:
            clothing = "It's a little chilly but you're a tough Seattleite, you can handle it. Go for a sweatshirt."
        else:
            clothing = "The weather outside is frightful. Stop being impractical and wear a coat."
            
        weather_data = {
            "current_time": seattle_time.isoformat(),
            "timezone": "America/Los_Angeles",
            "current_temperature": temp,
            "is_raining": is_raining,
            "clothing_recommendation": clothing
        }
        
        return jsonify(weather_data)
        
    except Exception as e:
        print("Error fetching weather:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)