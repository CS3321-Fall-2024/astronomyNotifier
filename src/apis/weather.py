import httpx
import json
import asyncio
from datetime import datetime, timedelta
import ephem

open_meteo_url = "https://api.open-meteo.com/v1/forecast"

ipinfo_url = "http://ipinfo.io/json"

async def fetch_daily_weather(lat, lon):
    """
    Fetches daily weather data and returns it as a string.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "temperature_unit": "fahrenheit",
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

                result.append(f"Date: {datetime.fromisoformat(date).strftime('%m/%d/%Y')}, "
                              f"High Temp: {max_temp} F, Low Temp: {min_temp} F, "
                              f"Precipitation: {precip}mm, Moon Phase: {moon_phase}")
            
            # Return all weather data as a single concatenated string
            return "\n".join(result)
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
        "timezone": "auto",
        "temperature_unit": "fahrenheit",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.open-meteo.com/v1/forecast", params=params)

        if response.status_code == 200:
            data = response.json()
            hourly_data = data.get("hourly", {})
            result = []

            for time, temp in zip(hourly_data.get("time", []), hourly_data.get("temperature_2m", [])):
                timestamp = datetime.fromisoformat(time)
                result.append(f"Time: {timestamp.strftime('%m/%d/%Y %H:%M')}, Temperature: {temp} F")

            # Return all hourly weather data as a single formatted string
            return "\n".join(result)
        else:
            raise Exception(f"Failed to fetch hourly weather: {response.status_code}")
        
    