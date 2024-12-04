from quart import Quart, jsonify
from apis.asteroids import *
from apis.aurora import *
from apis.eclipse import *
from apis.iss import *
from apis.location import *
from apis.moon import *
from apis.weather import *
from datetime import datetime, timedelta
import os

app = Quart(__name__)
api_key = os.getenv("NASA_API")

@app.route("/get_asteroids")
async def get_asteroids_API():
    asteroidsList = await get_asteroids(api_key)
    asteroids = [asteroid for asteroid in asteroidsList if asteroid["close_approach_data"]]
    sorted_by_magnitude = sorted(asteroids, key=lambda a: a["absolute_magnitude_h"])
    sorted_by_distance = sorted(
        asteroids,
        key=lambda a: a["close_approach_data"][0]["miss_distance"]["kilometers"],
    )

    magnitude_response = "Asteroids sorted by magnitude:\n"
    for asteroid in sorted_by_magnitude:
        magnitude = asteroid["absolute_magnitude_h"]
        name = asteroid["name"]
        magnitude_response += f"{name}: Magnitude {magnitude}\n"
        

    distance_response = "Asteroids sorted by distance:\n"
    for asteroid in sorted_by_distance:
        distance = asteroid["close_approach_data"][0]["miss_distance"]["kilometers"]
        name = asteroid["name"]
        distance_response += f"{name}: Distance {distance} km\n"

    result = magnitude_response + "\n~\n\n" + distance_response
    result += "\n^\n"
    write_to_file(result)
    return result

@app.route('/get_moon_phase')
async def get_moon_phase_API():
    s = await get_moon_phase(datetime.utcnow())
    
    write_to_file("The moon phase forecast for the next 7 days is: " +str(s) + "\n\n^\n")
    return "The moon phase forecast for the next 7 days is: " +str(s)
    

# takes long, lat as arg to return daily weather for the next 7 days
@app.route('/fetch_daily_weather')
async def fetch_daily_weather_API():
    lat, lon = await get_current_location()
    s = await fetch_daily_weather(lat,lon)
    
    write_to_file(str(s) + "\n\n^\n")
    return str(s)

# takes long, lat as arg to return hourly weather for the next 7 days
@app.route('/fetch_hourly_weather')
async def fetch_hourly_weather_API():
    lat, lon = await get_current_location()
    s  = await fetch_hourly_weather(lat,-lon)
    
    write_to_file(str(s) + "\n\n^\n")
    return str(s)


@app.route("/get_next_eclipse")
async def get_next_eclipse_API():
    lat, lon = await get_current_location()
    next_solar = await get_next_eclipse(lat, lon)
    
    if next_solar:
        result = f"Next Solar Eclipse:\n"
        result += f"Type: {next_solar.kind.name}\n"
        result += f"Visibility: {next_solar.obscuration}\n"
        result += f"Date: {datetime.fromisoformat(str(next_solar.peak.time)).strftime('%Y-%m-%d %H:%M:%S')}\n"
    else:
        result = "No upcoming solar eclipses.\n"

    result += "\n^\n"
    write_to_file(result)
    return result


@app.route("/get_next_iss_pass")
async def get_next_iss_pass_API():
    lat, lon = await get_current_location()
    if lat is None or lon is None:
        print("Unable to fetch location")
        return


    # Get the next 5 ISS passes within the next 7 days
    passes = get_next_iss_pass(lat, lon, p=5, d=7)
    if passes:
        result = "Upcoming ISS Passes:\n"
        for idx, pass_time in enumerate(passes, 1):
            result += f"Pass {idx}: {pass_time}\n"
    else:
        result = "No passes found within the provided days."

    result += "\n^\n"
    write_to_file(result)
    return result
    
@app.route("/get_distance_to_iss")
async def get_distance_to_iss_API():
    lat, lon = await get_current_location()
    distance, lat_iss, lon_iss = await get_distance_to_iss(lat, lon)
    result = f"The ISS is approximately {distance:.2f} kilometers away from your location.\n"
    result += f"The ISS is currently at latitude {lat_iss:.2f} and longitude {lon_iss:.2f}.\n"
    
    result += "\n^\n"
    write_to_file(result)
    return result

@app.route("/get_nasa_picture_of_the_day")
async def get_nasa_picture_of_the_day_API():
    result = await get_nasa_picture_of_the_day(api_key)
    
    result += "\n\n^\n"
    write_to_file(result)
    return result

# getting aurora events for 120 days(today-60 to today+60).
@app.route("/get_aurora")
async def get_aurora_API():
    lat, lon = await get_current_location() 
    result = await get_aurora_data(api_key, lat, lon)
    
    write_to_file(str(result) + "\n\n^\n")
    return str(result)


def write_to_file(data):
    with open('example.txt', 'a') as f:
        f.write(f"{data}\n")

if __name__ == "__main__":
    with open("example.txt", "w") as file:
        file.truncate(0)
    app.run(host='0.0.0.0', port=80)
