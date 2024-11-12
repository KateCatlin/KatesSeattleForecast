import requests
import json
from datetime import datetime
import pytz
from datetime import datetime, timedelta
import os

def fetch_sunset_data():
    # Seattle coordinates
    SEATTLE_LAT = "47.6062"
    SEATTLE_LNG = "-122.3321"
    
    url = f"https://api.sunrisesunset.io/json?lat={SEATTLE_LAT}&lng={SEATTLE_LNG}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Format sunset time to remove seconds
        if data.get('results', {}).get('sunset'):
            # Parse the sunset time
            sunset_time = datetime.strptime(data['results']['sunset'], '%I:%M:%S %p')
            
            # Get current time in Seattle
            seattle_tz = pytz.timezone('America/Los_Angeles')
            current_time = datetime.now(seattle_tz)
            
            # Set sunset time to today's date
            sunset_datetime = current_time.replace(
                hour=sunset_time.hour,
                minute=sunset_time.minute,
                second=0,
                microsecond=0
            )
            
            # Format sunset time (HH:MM)
            data['results']['sunset'] = sunset_time.strftime('%I:%M %p')
            
            # Calculate time until sunset
            if current_time < sunset_datetime:
                time_diff = sunset_datetime - current_time
                hours = time_diff.seconds // 3600
                minutes = (time_diff.seconds % 3600) // 60
                time_until = f"{hours} hours and {minutes} minutes until sunset"
                data['results']['time_until_sunset'] = time_until
            else:
                data['results']['time_until_sunset'] = 'after_sunset'
        
        # Save to a JSON file
        with open('sunset.json', 'w') as f:
            json.dump(data, f)
            
        return data
        
    except Exception as e:
        print(f"Error fetching sunset data: {e}")
        return None

if __name__ == "__main__":
    fetch_sunset_data()