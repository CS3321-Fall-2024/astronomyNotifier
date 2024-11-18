
from quart import Quart, jsonify
from apis.weather import *
from apis.weatherQueries import *
from datetime import datetime, timedelta

app = Quart(__name__)


@app.route("/get_asteroids")
async def get_asteroids_API():
   
    api_key = "cyA6A9N1vmADe8FxrOi7gg5jqs5EhGJCKC9Bclt1"
    asteroids = await get_asteroids(api_key)

    sorted_by_magnitude = sorted(asteroids, key=lambda a: a["absolute_magnitude_h"])

    sorted_by_distance = sorted(
        asteroids,
        key=lambda a: a["close_approach_data"][0]["miss_distance"]["kilometers"],
    )

    magnitude_response = "Asteroids sorted by magnitude:<br>"
    for asteroid in sorted_by_magnitude:
        magnitude = asteroid["absolute_magnitude_h"]
        name = asteroid["name"]
        magnitude_response += f"{name}: Magnitude {magnitude}<br>"

    distance_response = "Asteroids sorted by distance:<br>"
    for asteroid in sorted_by_distance:
        distance = asteroid["close_approach_data"][0]["miss_distance"]["kilometers"]
        name = asteroid["name"]
        distance_response += f"{name}: Distance {distance} km<br>"

    return magnitude_response + "<br>" + distance_response

@app.route('/get_moon_phase')
async def get_moon_phase_API():
    s = await get_moon_phase(datetime.utcnow())
    
    return "The moon phase forecast for the next 7 days is: " +str(s)
    

# takes long, lat as arg to return daily weather for the next 7 days
@app.route('/fetch_daily_weather')
async def fetch_dail_weather_API():
    s = await fetch_daily_weather(44.0682,-114.7420)
    return str(s)

# takes long, lat as arg to return hourly weather for the next 7 days
@app.route('/fetch_hourly_weather')
async def fetch_hourly_weather_API():
    s  = await fetch_hourly_weather(44.0682,-114.7420)
    return str(s)



@app.route("/get_next_eclipse")
async def get_next_eclipse_API():
    lat, lon = await get_current_location()
    next_solar = await get_next_eclipse(lat, lon)
    
    if next_solar:
        result = f"Next Solar Eclipse:<br>"
        result += f"Type: {next_solar.kind.name}<br>"
        result += f"Visibility: {next_solar.obscuration}<br>"
        result += f"Date: {datetime.fromisoformat(str(next_solar.peak.time)).strftime('%Y-%m-%d %H:%M:%S')}<br>"
    else:
        result = "No upcoming solar eclipses.<br>"

    return result


@app.route("/get_next_iss_pass")
async def get_next_iss_pass_API():
    lat, lon = await get_current_location()
    if lat is None or lon is None:
        print("Unable to fetch location")
        return

    # Get the next 5 ISS passes within the next 7 days
    passes = get_next_iss_pass_API(lat, lon, p=5, d=7)
    if passes:
        result = "Upcoming ISS Passes:<br>\n"
        for idx, pass_time in enumerate(passes, 1):
            result += f"Pass {idx}: {pass_time}<br>\n"
        return result
    else:
        return f"No passes found within the provided days."
    
@app.route("/get_distance_to_iss")
async def get_distance_to_iss_API():
    lat, lon = await get_current_location()
    distance, lat_iss, lon_iss = await get_distance_to_iss(lat, lon)
    result = f"The ISS is approximately {distance:.2f} kilometers away from your location.<br>"
    result += f"The ISS is currently at latitude {lat_iss:.2f} and longitude {lon_iss:.2f}.<br>"
    return result

@app.route("/get_nasa_picture_of_the_day")
async def get_nasa_picture_of_the_day_API():
    api_key = "cyA6A9N1vmADe8FxrOi7gg5jqs5EhGJCKC9Bclt1"
    result = await get_nasa_picture_of_the_day(api_key)
    return result


if __name__ == "__main__":
    app.run()
