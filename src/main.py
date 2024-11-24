from quart import Quart, jsonify
from apis.weatherQueries import *
from datetime import datetime

app = Quart(__name__)

def write_to_file(data):
    with open('example.txt', 'a') as f:
        f.write(f"{data}\n")

@app.route("/get_asteroids")
async def test1():
    api_key = "cyA6A9N1vmADe8FxrOi7gg5jqs5EhGJCKC9Bclt1"
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

@app.route("/get_next_eclipse")
async def test2():
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
async def test3():
    lat, lon = await get_current_location()
    if lat is None or lon is None:
        print("Unable to fetch location")
        return

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
async def test4():
    lat, lon = await get_current_location()
    distance, lat_iss, lon_iss = await get_distance_to_iss(lat, lon)
    result = f"The ISS is approximately {distance:.2f} kilometers away from your location.\n"
    result += f"The ISS is currently at latitude {lat_iss:.2f} and longitude {lon_iss:.2f}.\n"
    
    result += "\n^\n"
    write_to_file(result)
    return result

@app.route("/get_nasa_picture_of_the_day")
async def test5():
    api_key = "cyA6A9N1vmADe8FxrOi7gg5jqs5EhGJCKC9Bclt1"
    result = await get_nasa_picture_of_the_day(api_key)
    
    result += "\n^\n"
    write_to_file(result)
    return result

if __name__ == "__main__":
    app.run()