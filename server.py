from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import os
import pytz
import json
from ping_sunset import fetch_sunset_data
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from functools import lru_cache
import time

load_dotenv()

app = Flask(__name__)
endpoint = "https://models.inference.ai.azure.com"
model_name = "Cohere-command-r-plus"
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(os.getenv('GITHUB_TOKEN')),
)

@lru_cache(maxsize=1)
def get_cached_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=47.6062&longitude=-122.3321&current=temperature_2m,precipitation&temperature_unit=fahrenheit"
    response = requests.get(url)
    return response.json()

@lru_cache(maxsize=1)
def get_cached_sunset():
    return fetch_sunset_data()

def get_weather_with_cache():
    current_time = int(time.time() / 300)  # Changes every 5 minutes
    return get_cached_weather()

def get_time_context():
    try:
        sunset_data = get_cached_sunset()  # Get fresh data

        time_until_sunset = sunset_data.get('results', {}).get('time_until_sunset')
        minutes_until_sunset = sunset_data.get('results', {}).get('minutes_until_sunset')
        time_until_sunrise = sunset_data.get('results', {}).get('time_until_sunrise')
        minutes_until_sunrise = sunset_data.get('results', {}).get('minutes_until_sunrise')
        
        if time_until_sunset == 'after_sunset':
            return "after sunset"
        elif minutes_until_sunset and minutes_until_sunset <= 30:
            return "near sunset"
        elif time_until_sunrise == 'before_sunrise':
            return "before sunrise"
        else:
            return "during daylight"
    except:
        return "during daylight"  # default fallback

def generate_weather_description(temp, is_raining):
    # Cache key components
    cache_key = f"{temp}_{is_raining}_{get_time_context()}"
    
    @lru_cache(maxsize=32)
    def get_cached_description(key):
        prompt = f"""Context: Seattle weather conditions
Temperature: {temp}°F
Raining: {'Yes' if is_raining else 'No'}
Lighting: {get_time_context()}

Generate ONE casual clothing recommendation for a Seattleite that:
- Considers temperature, rain, and whether it's dark out
- References Seattle-specific clothing
- If relevant, includes appropriate lighting gear (headlamp/reflective gear for dark, sunglasses or a hat for a not-rainy day)
- Is humorous and locally relevant
- Stays under 100 characters"""
    
        response = client.complete(
            messages=[
                SystemMessage(content="You are a Seattle local who gives practical and witty weather advice, always considering safety and visibility."),
                UserMessage(content=prompt),
            ],
            temperature=1.0,  # Controls randomness
            top_p=0.9,       # Controls diversity of word choice
            max_tokens=60,
            model=model_name
        )
        return response.choices[0].message.content
    
    return get_cached_description(cache_key)

@app.route('/')
def index():
    return render_template('index.html')

# Add no-cache headers to weather_json route
@app.route('/weather.json')
def weather_json():
    try:
        # Pre-warm cache
        data = get_weather_with_cache()
        sunset_data = get_cached_sunset()
        
        # Rest of your code
        # Get current time in Seattle
        seattle_tz = pytz.timezone('America/Los_Angeles')
        seattle_time = datetime.now(seattle_tz)
        
        temp = data['current']['temperature_2m']
        is_raining = data['current']['precipitation'] > 0
        
        # Get the AI clothing recommendation without modifications
        clothing = generate_weather_description(temp, is_raining)
            
        weather_data = {
            "current_time": seattle_time.isoformat(),
            "timezone": "America/Los_Angeles",
            "current_temperature": temp,
            "is_raining": is_raining,
            "clothing_recommendation": clothing
        }
        
        response = jsonify(weather_data)
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        return response
        
    except Exception as e:
        return jsonify({"error": "Loading data..."}), 202  # 202 Accepted

# In server.py, add debug prints
@app.route('/sunset.json')
def get_sunset():
    data = get_cached_sunset()  # Get fresh data every time
    return jsonify(data if data else {"error": "Unable to fetch sunset data"})

@app.errorhandler(Exception)
def handle_error(error):
    if "azure.ai.inference" in str(error):
        return jsonify({
            "error": "AI service temporarily unavailable",
            "fallback_suggestion": "Layer up, it's Seattle after all!"
        }), 503

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Changed from 5000 to 5001
    app.run(host="0.0.0.0", port=port)
