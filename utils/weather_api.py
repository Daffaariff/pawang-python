# utils/weather_api.py
import requests
from datetime import datetime

def get_weather_forecast(city: str):
    """
    Get 3-day weather forecast from OpenWeatherMap API by city name.
    Returns a dict with city name, forecast list (with date, temp, icon, desc)
    """
    api_key = "7b004d96d027735ee31526f062b71d52"  # your active key
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        # Validate API response
        if str(data.get("cod")) != "200" or "list" not in data:
            print("Error or unexpected data:", data)
            return None

        forecast = []
        seen_dates = set()

        for item in data["list"]:
            date_txt = item["dt_txt"].split(" ")[0]
            if date_txt not in seen_dates:
                temp_day = item["main"]["temp_max"]
                temp_night = item["main"]["temp_min"]
                description = item["weather"][0]["description"].title()
                icon = item["weather"][0]["icon"]
                icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

                formatted_date = datetime.strptime(date_txt, "%Y-%m-%d").strftime("%A, %d %B %Y")


                forecast.append({
                    "date": formatted_date,
                    "temp_day": round(temp_day, 1),
                    "temp_night": round(temp_night, 1),
                    "description": description,
                    "icon": icon_url
                })
                seen_dates.add(date_txt)

            if len(forecast) >= 3:
                break

        return {"city": city.title(), "forecast": forecast}

    except Exception as e:
        print("Weather API Error:", e)
        return None


# Test run (standalone)
if __name__ == "__main__":
    forecast = get_weather_forecast("Jakarta")
    if forecast:
        print(f"Weather in {forecast['city']}:")
        for day in forecast["forecast"]:
            print(f"{day['date']}: {day['description']} "
                  f"({day['temp_day']}°C / {day['temp_night']}°C)")
    else:
        print("Failed to get weather data.")
