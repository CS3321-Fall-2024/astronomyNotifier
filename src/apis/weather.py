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

    
    return ", ".join(phases)

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
        
    
import httpx
import json
import asyncio
from datetime import datetime, timedelta
import ephem  # For astronomical calculations

# Function to fetch geomagnetic storms from NASA DONKI API
async def fetch_geomagnetic_storms(start_date, end_date, api_key):
    url = "https://api.nasa.gov/DONKI/GST"
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "api_key": api_key
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        print(f"Request URL: {response.url}")  # Debugging: Show full request URL
        print(f"Status Code: {response.status_code}")  # Debugging: Show status code
        if response.status_code == 200:
            data = response.json()
            print(f"Response Data: {len(data)} events found.")  # Debugging: Number of events
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

# Function to determine nighttime visibility
def calculate_visibility(event, latitude, longitude):
    observer = ephem.Observer()
    observer.lat, observer.lon = str(latitude), str(longitude)

    # Convert ISO 8601 date to 'YYYY/MM/DD HH:MM:SS' format
    iso_date = event["startTime"]
    try:
        parsed_date = datetime.strptime(iso_date, "%Y-%m-%dT%H:%MZ")
        observer.date = parsed_date.strftime("%Y/%m/%d %H:%M:%S")
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return False  # Assume not visible if there's an error

    # Check the sun's altitude to determine nighttime
    sun = ephem.Sun()
    sun.compute(observer)
    return sun.alt < 0  # True if it's nighttime

async def get_aurora_data(api_key, latitude, longitude):
    today = datetime.utcnow()
    start_date = (today - timedelta(days=60)).strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=60)).strftime("%Y-%m-%d")
    
    # Fetch data
    storm_data = await fetch_geomagnetic_storms(start_date, end_date, api_key)
    if not storm_data:
        print("No geomagnetic storm data available for the specified range.")
        return []
    
    # Prepare the results string
    aurora_string = ""
    for event in storm_data:
        visibility = calculate_visibility(event, latitude, longitude)
        
        # Format Kp Index: List of Kp Index values -> Average Kp Index for simplicity
        kp_values = event.get('allKpIndex', [])
        if kp_values:
            avg_kp = sum(k['kpIndex'] for k in kp_values) / len(kp_values)
            kp_info = f"Average Kp Index: {avg_kp:.2f}"
        else:
            kp_info = "Kp Index: N/A"
        
        # Format the event details
        aurora_string += (
            f"Start Time: {datetime.fromisoformat(event['startTime']).strftime('%b %d, %Y %I:%M %p UTC')}\n"
            f"{kp_info}\n"
            f"Visibility: {'Visible' if visibility else 'Not Visible'}\n"
            f"{'-' * 40}\n"
        )
    
    return aurora_string