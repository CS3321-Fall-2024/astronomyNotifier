import httpx
import astronomy
from datetime import datetime, timezone
import python_weather

async def get_asteroids(api_key):

    url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={api_key}"
    asteroids = []

    async with httpx.AsyncClient() as client:
        while url:
            try:
                response = await client.get(url)
                response.raise_for_status()  # Raise an error for bad responses
                data = response.json()
                asteroids.extend(data.get('near_earth_objects', []))
                url = data.get('links', {}).get('next')
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                break  # Exit the loop on HTTP error
            except httpx.RequestError as e:
                print(f"Request error occurred: {e}")
                break  # Exit the loop on request error

    return asteroids

async def get_next_eclipse():
    latitude = 42.8713
    longitude = -112.4455
    
    location = astronomy.Observer(latitude=latitude, longitude=longitude)
    time_instance = astronomy.Time('2024-11-10')
    
    next_eclipse = astronomy.SearchLocalSolarEclipse(time_instance, location)
    
    return next_eclipse
