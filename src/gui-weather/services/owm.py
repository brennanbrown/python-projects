"""OpenWeatherMap service wrapper."""

from __future__ import annotations

import json
import urllib.parse
from datetime import datetime
from urllib.request import Request, urlopen

USER_AGENT = "python-projects/ci (github.com/brennanbrown)"


def get_open_weather_data(city: str, api_key: str, timeout: int = 10) -> dict[str, str]:
    city_q = urllib.parse.quote(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_q}&appid={api_key}"
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        data = resp.read().decode()
    json_data = json.loads(data)

    def kelvin_to_celsius(temp_k: float) -> str:
        return f"{(temp_k - 273.15):.1f}"

    def kelvin_to_fahrenheit(temp_k: float) -> str:
        return f"{((temp_k - 273.15) * 1.8 + 32):.1f}"

    def unix_to_datetime(unix_time: int) -> str:
        return datetime.fromtimestamp(int(unix_time)).strftime("%Y-%m-%d %H:%M:%S")

    def meter_to_miles(meter: float) -> str:
        return f"{(meter * 0.00062137):.2f}"

    lastupdate_unix = json_data["dt"]
    humidity = json_data["main"]["humidity"]
    pressure = json_data["main"]["pressure"]
    temp_kelvin = json_data["main"]["temp"]
    city_name = json_data["name"]
    city_country = json_data["sys"]["country"]
    sunrise_unix = json_data["sys"]["sunrise"]
    sunset_unix = json_data["sys"]["sunset"]
    owm_weather = json_data["weather"][0]["description"]
    weather_icon = json_data["weather"][0]["icon"]
    wind_deg = json_data["wind"].get("deg", 0)
    wind_speed_meter_sec = json_data["wind"]["speed"]
    visibility_meter = json_data.get("visibility", None)

    visibility_miles = "N/A" if visibility_meter is None else meter_to_miles(visibility_meter)

    return {
        "lastupdate": unix_to_datetime(lastupdate_unix),
        "humidity": f"{humidity} %",
        "pressure": f"{pressure} hPa",
        "temp_f": kelvin_to_fahrenheit(temp_kelvin),
        "temp_c": kelvin_to_celsius(temp_kelvin),
        "location": f"{city_name}, {city_country}",
        "weather": owm_weather,
        "weather_icon": weather_icon,
        "wind": f"{wind_deg} degrees at {wind_speed_meter_sec * 2.23693629:.1f} MPH",
        "visibility": f"{visibility_miles} miles",
        "sunrise": unix_to_datetime(sunrise_unix),
        "sunset": unix_to_datetime(sunset_unix),
    }
