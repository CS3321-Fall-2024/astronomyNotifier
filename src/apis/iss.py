import httpx
import math
from skyfield.api import Topos, load


def get_next_iss_pass(lat, lon, p, d, fixed_time = False):
    stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
    satellites = load.tle_file(stations_url)
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name['ISS (ZARYA)']

    location = Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    ts = load.timescale()
    t0 = ts.now()

    if fixed_time:
        t0 = ts.tt(2024,1,1,12,0)

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

    
async def get_distance_to_iss(lat, lon, fixed_time = False):
    satellites = load.tle_file('http://www.celestrak.com/NORAD/elements/stations.txt')
    sat = [sat for sat in satellites if sat.name == 'ISS (ZARYA)'][0]
    
    observer = Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    ts = load.timescale()
    t = ts.now()

    if fixed_time:
        t = ts.tt(2024,1,1,12,0)
    
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


        return f"Title: {title}\nExplanation: {explanation}\nimg url = {image_url} description = {title}"
    