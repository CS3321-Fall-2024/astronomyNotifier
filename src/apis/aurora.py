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