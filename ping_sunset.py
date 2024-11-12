
import requests
import json
from datetime import datetime
import os

def fetch_sunset_data():
    # Seattle coordinates
    SEATTLE_LAT = "47.6062"
    SEATTLE_LNG = "-122.3321"
    
    url = f"https://api.sunrisesunset.io/json?lat={SEATTLE_LAT}&lng={SEATTLE_LNG}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Save to a JSON file
        with open('sunset.json', 'w') as f:
            json.dump(data, f)
            
        return data
        
    except Exception as e:
        print(f"Error fetching sunset data: {e}")
        return None

if __name__ == "__main__":
    fetch_sunset_data()