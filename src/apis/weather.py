import httpx
import json
import asyncio
from datetime import datetime, timedelta
import ephem

open_meteo_url = "https://api.open-meteo.com/v1/forecast"

ipinfo_url = "http://ipinfo.io/json"

async def get_user_location(): # getting the user's longitude and latitude
    async with httpx.AsyncClient() as client:
        response = await client.get(ipinfo_url)
        
        if response.status_code == 200:
            location_data = response.json()
            # Parse latitude and longitude from IPInfo location data
            loc = location_data.get("loc", "").split(",")
            if len(loc) == 2:
                latitude = loc[0]
                longitude = loc[1]
                return latitude, longitude
            else:
                print("Unable to determine latitude and longitude.")
                return None, None
        else:
            print("Unable to fetch location data.")
            return None, None

async def get_moon_phase(date): # getting the moon phase for specific dates
    moon = ephem.Moon(date)
    moon_phase = moon.phase

    # Moon phase names and their corresponding values
    phases = [
        (0, "New Moon"),
        (50, "Waxing Crescent"),
        (100, "First Quarter"),
        (150, "Waxing Gibbous"),
        (200, "Full Moon"),
        (250, "Waning Gibbous"),
        (300, "Last Quarter"),
        (350, "Waning Crescent"),
    ]
    
    for phase_value, phase_name in phases:
        if moon_phase < phase_value:
            return phase_name
    return "Waning Crescent"  # Default to Waning Crescent if phase is not found

async def fetch_weather():
    # Getting the user's location
    latitude, longitude = await get_user_location()
    # Parameters for the Open Meteo API request
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",  # Getting hourly temperature data
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",  # Getting max and min temps of the day
        "timezone": "auto"  # Setting the timezone automatically
    }
    # Request to the Open Meteo API
    async with httpx.AsyncClient() as client:
        response = await client.get(open_meteo_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parsing hourly weather data to be more readable
            print("Hourly Weather Forecast for the next seven days:")
            hourly_data = data.get("hourly", {})
            if hourly_data:
                for time, temp in zip(hourly_data.get("time", []), hourly_data.get("temperature_2m", [])):
                    # Format time as MM/DD/YYYY HH:MM
                    timestamp = datetime.fromisoformat(time)
                    formatted_time = timestamp.strftime("%m/%d/%Y %H:%M")
                    print(f"{formatted_time} {temp}°C")

            # Parsing daily weather data to be more readable
            print("\nDaily Weather Forecast with Moon Phases:")
            daily_data = data.get("daily", {})
            if daily_data:
                today = datetime.utcnow()  # Current date for moon phase calculation
                for i, (date, max_temp, min_temp, precip) in enumerate(zip(daily_data.get("time", []), 
                                                                            daily_data.get("temperature_2m_max", []), 
                                                                            daily_data.get("temperature_2m_min", []), 
                                                                            daily_data.get("precipitation_sum", []))):
                    # Format date as MM/DD/YYYY
                    date_str = datetime.fromisoformat(date).strftime("%m/%d/%Y")
                    future_date = today + timedelta(days=i)
                    moon_phase = await get_moon_phase(future_date)
                    
                    # Print weather data with moon phase
                    print(f"{date_str} High: {max_temp}°C, Low: {min_temp}°C, Precipitation: {precip}mm, Moon Phase: {moon_phase}")
            
        else:
            print(f"Error: Unable to fetch weather data. Status code: {response.status_code}")


asyncio.run(fetch_weather())
