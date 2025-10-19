# routes/weather_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.weather_api import get_weather_forecast

weather_bp = Blueprint("weather", __name__, url_prefix="/weather")

@weather_bp.route("/get", methods=["POST"])
def get_weather():
    city = request.form.get("city")

    if not city:
        flash("Please enter a city name.", "error")
        return redirect(url_for("home"))

    weather = get_weather_forecast(city)
    if not weather:
        flash("Could not retrieve weather data. Try again.", "error")
        return redirect(url_for("home"))

    # Re-render homepage with weather info
    return render_template("index.html", weather=weather)
