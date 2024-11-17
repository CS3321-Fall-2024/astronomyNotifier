import httpx
import astronomy
from datetime import datetime
import time
import math
from geopy.geocoders import Nominatim
from skyfield.api import Topos, load

async def get_asteroids(api_key):

    url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={api_key}"
    asteroids = []

    async with httpx.AsyncClient() as client:
        while url:
            try:
                response = await client.get(url)
                response.raise_for_status()  
                data = response.json()
                asteroids.extend(data.get('near_earth_objects', []))
                url = data.get('links', {}).get('next')
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                break  
            except httpx.RequestError as e:
                print(f"Request error occurred: {e}")
                break  

    return asteroids

async def get_next_eclipse(lat, lon):
    
    location = astronomy.Observer(latitude=lat, longitude=lon)
    
    time_instance = astronomy.Time(datetime.now().strftime('%Y-%m-%d'))
    
    next_eclipse = astronomy.SearchLocalSolarEclipse(time_instance, location)
    
    return next_eclipse

def get_next_iss_pass(lat, lon, p, d):
    stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
    satellites = load.tle_file(stations_url)
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name['ISS (ZARYA)']

    location = Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    ts = load.timescale()
    t0 = ts.now()

    # Find ISS passes within the next d days
    t, events = satellite.find_events(location, t0, t0 + d)

    passes = []
    for ti, event in zip(t, events):
        if event == 0:  
            passes.append(ti.utc_iso())
            if len(passes) >= p:
                break

    if passes:
        return passes
    else:
        return f"No passes found within the next {d} days."

async def get_current_location():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://ipinfo.io")
            data = response.json()
        
        location_str = data['loc']  
        latitude, longitude = map(float, location_str.split(','))
        
        return latitude, longitude
    except Exception as e:
        print("Error fetching location:")
    
async def get_distance_to_iss(lat, lon):
    satellites = load.tle_file('http://www.celestrak.com/NORAD/elements/stations.txt')
    sat = [sat for sat in satellites if sat.name == 'ISS (ZARYA)'][0]
    
    observer = Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    ts = load.timescale()
    t = ts.now()
    
    # Calculate the position of the ISS
    astrometric = sat.at(t)
    
    # Get the observer's position (your position on Earth)
    observer_position = astrometric.position.au - observer.at(t).position.au
    
    distance = math.sqrt(observer_position[0]**2 + observer_position[1]**2 + observer_position[2]**2) * 149597870.7  # AU to km
    lat_iss, lon_iss = astrometric.subpoint().latitude.degrees, astrometric.subpoint().longitude.degrees
    
    return distance, lat_iss, lon_iss

async def get_nasa_picture_of_the_day(api_key):
    url = 'https://api.nasa.gov/planetary/apod'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={'api_key': api_key})
        response.raise_for_status()  # Ensure the request was successful

        data = response.json()  

        # Extract the title, URL, and explanation from the response
        title = data.get('title', 'No title available')
        explanation = data.get('explanation', 'No explanation available')
        image_url = data.get('url', 'No image available')

        return f"Title: {title}<br>Explanation: {explanation}<br><img src='{image_url}' alt='{title}' />"