import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city="Perth", country="AU"):
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    current_url = "https://api.openweathermap.org/data/2.5/weather"

    # Set up params
    params = {
        "q": f"{city},{country}",
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        # Get current weather for description
        current_resp = requests.get(current_url, params=params)
        current_data = current_resp.json()
        description = current_data["weather"][0]["description"].capitalize()

        # Get forecast for high/low
        forecast_resp = requests.get(forecast_url, params=params)
        forecast_data = forecast_resp.json()

        today = datetime.utcnow().date()
        temps_today = [
            (entry["main"]["temp_min"], entry["main"]["temp_max"])
            for entry in forecast_data["list"]
            if datetime.fromtimestamp(entry["dt"]).date() == today
        ]

        if not temps_today:
            return "🌤️ Could not get today's temperature range."

        lows = [t[0] for t in temps_today]
        highs = [t[1] for t in temps_today]

        low = min(lows)
        high = max(highs)

        return f"🌤️ {description}. Today's range: {low:.1f}°C to {high:.1f}°C."

    except Exception as e:
        return f"❌ Error getting weather: {str(e)}"
