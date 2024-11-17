import requests
import json
from datetime import datetime
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

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

def get_clothing_suggestion(weather_data):
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "Meta-Llama-3-70B-Instruct"
    token = os.environ["GITHUB_TOKEN"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    prompt = f"Given Seattle weather with temperature {weather_data['temperature']}°C and {weather_data['precipitation']}mm precipitation, suggest appropriate clothing in a witty way that references Seattle culture. Keep it brief."

    response = client.complete(
        messages=[
            SystemMessage(content="You are a helpful assistant knowledgeable about Seattle weather and culture."),
            UserMessage(content=prompt),
        ],
        temperature=0.7,
        model=model_name
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    fetch_weather()
