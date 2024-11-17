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

load_dotenv()

app = Flask(__name__)
endpoint = "https://models.inference.ai.azure.com"
model_name = "Cohere-command-r-plus"
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(os.getenv('GITHUB_TOKEN')),
)

def get_time_context():
    try:
        sunset_data = fetch_sunset_data()  # Get fresh data

        time_until_sunset = sunset_data.get('results', {}).get('time_until_sunset')
        minutes_until_sunset = sunset_data.get('results', {}).get('minutes_until_sunset')
        
        if time_until_sunset == 'after_sunset':
            return "after sunset"
        elif minutes_until_sunset and minutes_until_sunset <= 30:
            return "near sunset"
        else:
            return "during daylight"
    except:
        return "during daylight"  # default fallback

def generate_weather_description(temp, is_raining):
    time_context = get_time_context()
    
    prompt = f"""Context: Seattle weather conditions
Temperature: {temp}°F
Raining: {'Yes' if is_raining else 'No'}
Lighting: {time_context}

Generate ONE casual clothing recommendation for a Seattleite that:
- Considers temperature, rain, and whether it's dark out
- References Seattle-specific clothing like:
  * Puffy jackets (when cold)
  * Ski jackets (when super cold)
  * Rain shells (when raining)
  * Fleece layers
  * Flannel shirts
  * Rain boots/hiking boots/winter boots/birkenstocks/running shoes
  * Gore-tex gear
  * Technical outdoor wear
  * Beanies/caps
  * Running shorts 
- Includes appropriate lighting gear (headlamp/reflective gear for dark, sunglasses for day)
- Is humorous and locally relevant
- Stays under 100 characters
- Incorporates the lighting gear naturally into the suggestion"""
    
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

@app.route('/')
def index():
    return render_template('index.html')

# Add no-cache headers to weather_json route
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
        print("Error fetching weather:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500

# In server.py, add debug prints
@app.route('/sunset.json')
def get_sunset():
    data = fetch_sunset_data()  # Get fresh data every time
    return jsonify(data if data else {"error": "Unable to fetch sunset data"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Changed from 5000 to 5001
    app.run(host="0.0.0.0", port=port)
