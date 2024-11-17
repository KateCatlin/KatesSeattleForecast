from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import os
import pytz
import json
from ping_sunset import fetch_sunset_data
import cohere
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

# Add to server.py temporarily
print(f"GitHub token present: {'Yes' if os.getenv('GITHUB_TOKEN') else 'No'}")

def get_time_context():
    try:
        with open('sunset.json', 'r') as f:
            sunset_data = json.load(f)
            
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
Time of day: {time_context}

Generate a humorous, Seattle-specific clothing recommendation that considers the temperature, rain, and time of day. Keep it under 100 characters."""
    
    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful Seattle weather assistant who knows the local culture."),
            UserMessage(content=prompt),
        ],
        temperature=0.9,
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
    try:
        with open('sunset.json', 'r') as f:
            data = json.load(f)
            # Add debug prints
            seattle_tz = pytz.timezone('America/Los_Angeles')
            current_time = datetime.now(seattle_tz)
            print(f"Current time (Seattle): {current_time}")
            print(f"Sunset data: {json.dumps(data, indent=2)}")
            return jsonify(data)
    except FileNotFoundError:
        data = fetch_sunset_data()
        print(f"Fresh sunset data: {json.dumps(data, indent=2)}")
        return jsonify(data if data else {"error": "Unable to fetch sunset data"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Changed from 5000 to 5001
    app.run(host="0.0.0.0", port=port)
