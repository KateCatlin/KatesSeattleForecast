from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import os
import pytz
import json
from ping_sunset import fetch_sunset_data
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_weather_description(temp, is_raining):
    prompt = f"""Generate a casual, friendly one-sentence clothing recommendation for Seattle weather.
    Current temperature: {temp}°F
    Is it raining: {'Yes' if is_raining else 'No'}
    Make it somewhat humorous and very specific to Seattle culture.
    Keep it under 100 characters."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating AI description: {e}")
        # Fallback to basic recommendation
        return "Dress for typical Seattle weather!" 

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
        
        # Replace the static clothing recommendations with AI-generated ones
        clothing = generate_weather_description(temp, is_raining)
            
        # Get sunset data
        try:
            with open('sunset.json', 'r') as f:
                sunset_data = json.load(f)
                
            # Add lighting recommendation based on sunset
            if sunset_data.get('results', {}).get('time_until_sunset') == 'after_sunset':
                clothing += " Also it's dark, bring a headlamp."
            elif sunset_data.get('results', {}).get('minutes_until_sunset', float('inf')) <= 30:
                clothing += " Also, it's getting dark out, you may want to bring a headlamp."
            elif not is_raining:
                clothing += " Wear your sunglasses."
                
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # If sunset data isn't available, skip the lighting recommendation
            
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

@app.route('/sunset.json')
def get_sunset():
    try:
        with open('sunset.json', 'r') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        data = fetch_sunset_data()
        return jsonify(data if data else {"error": "Unable to fetch sunset data"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Changed from 5000 to 5001
    app.run(host="0.0.0.0", port=port)
