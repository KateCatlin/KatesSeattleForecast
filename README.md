# Seattle Weather Web App

## Overview
This app provides Seattle weather updates alongside witty, AI-generated clothing suggestions tailored to the city’s unique vibe.

Here’s the kicker: I don’t know any Python! This was made entirely with GitHub Copilot and a model I handpicked from the GitHub Models marketplace. Hopefully, it shows that even without deep coding knowledge, you can create something fun and functional with Copilot as your... well... co-pilot!

---

## Core Features
- **Real-Time Weather Data:** Fetches live Seattle weather information, including temperature, rain status, and sunset timing, from the Open-Meteo API.
- **Clothing Recommendations:** Leverages Azure AI to generate clever and Seattle-appropriate clothing suggestions (think fleece jackets and Gore-Tex).
- **Dynamic Updates:** Refreshes data dynamically without requiring a full page reload.
- **Timezone Awareness:** Incorporates Seattle’s local timezone for accurate sunset calculations and time-specific recommendations.

---

## Technical Stack
- **Backend:** Flask, serving JSON endpoints.
- **Frontend:** Vanilla JavaScript for a lightweight and interactive user experience.
- **AI Integration:** Azure AI for generating culturally-relevant recommendations.
- **Timezone Handling:** PyTZ for managing Seattle’s timezone.
- **Caching:** LRU caching to optimize API performance and reduce latency.

---

## Key Components
1. **Weather Data Endpoint:**
   - `/weather.json`: Provides real-time weather data as JSON.

2. **Sunset Calculations:**
   - Computes sunset times specific to Seattle’s timezone for accurate, time-aware recommendations.

3. **AI-Powered Recommendations:**
   - Uses prompt engineering to generate culturally relevant and witty suggestions (e.g., "Don’t forget your Gore-Tex; drizzle doesn’t count as rain here!").

4. **Caching Layer:**
   - Implements LRU caching to minimize redundant API calls and ensure faster response times.

5. **Error Handling and Fallbacks:**
   - Robust error handling ensures the app gracefully degrades with default messages if external APIs are unavailable.

---

## Unique Features
- **Showcase of AI Tools:**
   - Developed entirely using GitHub Copilot, demonstrating its capabilities to generate a fully functional Python web app without any prior coding knowledge.

- **Witty Model Selection:**
   - The AI model chosen from the GitHub Models Marketplace was handpicked for its witty and culturally relevant tone after rigorous testing.

- **Seattle-Specific Recommendations:**
   - Tailored clothing suggestions accounting for Seattle’s rainy winters and mild summers.

- **Time-Aware Insights:**
   - Adjusts recommendations based on time of day (e.g., layering advice for chilly evenings).

- **Fresh Data Guaranteed:**
   - Employs no-cache headers to ensure users always receive the latest updates.

---

## Deployment
- **Hosting:**
   - Deployed on Heroku for scalable and reliable performance.

- **Environment Variables:**
   - Secures API keys for Open-Meteo and Azure AI using environment variables.

- **Error Handling:**
   - Production-grade error handling for smooth user experience under all conditions.

---

## How to Run Locally
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/seattle-weather-web-app.git
   cd seattle-weather-web-app
   ```

2. **Set Up Environment Variables:**
   - Create a `.env` file in the root directory with the following keys:
     ```
     OPEN_METEO_API_KEY=your_open_meteo_key
     AZURE_AI_API_KEY=your_azure_ai_key
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   flask run
   ```

5. **Access the App:**
   - Open your browser and navigate to `http://localhost:5000`.

---

## Future Enhancements
- Add localization for other cities with similar climates.
- Expand witty model testing to include even more cultural references.
- Support for mobile-friendly UI.
- Advanced user preferences for tailored suggestions.

---

## Contributing
We welcome contributions! Please fork the repository and submit a pull request with your changes.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.


