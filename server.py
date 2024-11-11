
from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/weather.json')
def weather():
    return send_from_directory('.', 'weather.json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)