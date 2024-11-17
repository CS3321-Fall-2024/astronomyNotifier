import httpx
import json
import asyncio
from datetime import datetime, timedelta
import ephem

open_meteo_url = "https://api.open-meteo.com/v1/forecast"

ipinfo_url = "http://ipinfo.io/json"

async def get_moon_phase(current_date): # getting the moon phase for specific dates
    phases = []
    # Moon phase names and their corresponding values
    phase_names = [
        (0, "New Moon"),
        (50, "Waxing Crescent"),
        (100, "First Quarter"),
        (150, "Waxing Gibbous"),
        (200, "Full Moon"),
        (250, "Waning Gibbous"),
        (300, "Last Quarter"),
        (350, "Waning Crescent"),
    ]
    
    # Function to calculate the moon phase for a given date
    def get_phase_name(date):
        moon = ephem.Moon(date)
        moon_phase = moon.phase

        for phase_value, phase_name in phase_names:
            if moon_phase < phase_value:
                return phase_name
        return "Waning Crescent"  # Default to Waning Crescent if phase is not found

    # Calculate moon phases for the next 7 days
    for i in range(7):
        future_date = current_date + timedelta(days=i)
        phase_name = get_phase_name(future_date)
        phases.append(phase_name)

    
    return phases

async def fetch_daily_weather(lat, lon):
    """
    Fetches daily weather data and returns it as a list of dictionaries.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.open-meteo.com/v1/forecast", params=params)

        if response.status_code == 200:
            data = response.json()
            daily_data = data.get("daily", {})
            result = []
            today = datetime.utcnow()

            for i, (date, max_temp, min_temp, precip) in enumerate(zip(
                daily_data.get("time", []),
                daily_data.get("temperature_2m_max", []),
                daily_data.get("temperature_2m_min", []),
                daily_data.get("precipitation_sum", [])
            )):
                future_date = today + timedelta(days=i)
                moon_phase = await get_moon_phase(future_date)  # Assume this function exists

                result.append({
                    "date": datetime.fromisoformat(date).strftime("%m/%d/%Y"),
                    "high": max_temp,
                    "low": min_temp,
                    "precipitation": precip,
                })
            return result
        else:
            raise Exception(f"Failed to fetch daily weather: {response.status_code}")


async def fetch_hourly_weather(lat, lon):
    """
    Fetches hourly weather data and returns it as a list of dictionaries.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": "auto"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.open-meteo.com/v1/forecast", params=params)

        if response.status_code == 200:
            data = response.json()
            hourly_data = data.get("hourly", {})
            result = []

            for time, temp in zip(hourly_data.get("time", []), hourly_data.get("temperature_2m", [])):
                timestamp = datetime.fromisoformat(time)
                result.append({
                    "time": timestamp.strftime("%m/%d/%Y %H:%M"),
                    "temperature": temp
                })
            return result
        else:
            raise Exception(f"Failed to fetch hourly weather: {response.status_code}")
