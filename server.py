from flask import Flask, render_template
import requests
import os  # Import the os module

app = Flask(__name__)

def get_seattle_forecast():
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=47.6062&longitude=-122.3321&current_weather=true")
    if response.status_code == 200:
        data = response.json()
        current_weather = data.get("current_weather", {})
        return current_weather
    else:
        return None

@app.route("/")
def index():
    weather = get_seattle_forecast()
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))