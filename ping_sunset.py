import requests
import pytz
from datetime import datetime

def fetch_sunset_data():
    url = "https://api.sunrise-sunset.org/json?lat=47.6062&lng=-122.3321&formatted=0"
    response = requests.get(url)
    data = response.json()

    seattle_tz = pytz.timezone('America/Los_Angeles')
    current_time = datetime.now(seattle_tz)
    
    sunrise_time = datetime.fromisoformat(data['results']['sunrise']).astimezone(seattle_tz)
    sunset_time = datetime.fromisoformat(data['results']['sunset']).astimezone(seattle_tz)
    
    minutes_until_sunset = (sunset_time - current_time).total_seconds() / 60
    minutes_until_sunrise = (sunrise_time - current_time).total_seconds() / 60
    
    return {
        "results": {
            "sunrise_time": sunrise_time.strftime("%I:%M %p"),
            "sunset_time": sunset_time.strftime("%I:%M %p"),
            "time_until_sunset": "before_sunset" if minutes_until_sunset > 0 else "after_sunset",
            "minutes_until_sunset": max(0, minutes_until_sunset),
            "time_until_sunrise": "before_sunrise" if minutes_until_sunrise > 0 else "after_sunrise",
            "minutes_until_sunrise": max(0, minutes_until_sunrise)
        }
    }

if __name__ == "__main__":
    fetch_sunset_data()