from quart import Quart, jsonify
from apis.weatherQueries import *

app = Quart(__name__)


@app.route("/")
async def hello():

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


@app.route("/test1")
async def test1():
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


@app.route("/test2")
async def test2():
    lat, lon = await get_current_location()
    if lat is None or lon is None:
        print("Unable to fetch location")
        return

    # Get the next 5 ISS passes within the next 7 days
    passes = get_next_iss_pass(lat, lon, p=5, d=7)
    if passes:
        result = "Upcoming ISS Passes:<br>\n"
        for idx, pass_time in enumerate(passes, 1):
            result += f"Pass {idx}: {pass_time}<br>\n"
        return result
    else:
        return f"No passes found within the provided days."
    
@app.route("/test3")
async def test3():
    lat, lon = await get_current_location()
    distance, lat_iss, lon_iss = await get_distance_to_iss(lat, lon)
    result = f"The ISS is approximately {distance:.2f} kilometers away from your location.<br>"
    result += f"The ISS is currently at latitude {lat_iss:.2f} and longitude {lon_iss:.2f}.<br>"
    return result

@app.route("/test4")
async def test4():
    api_key = "cyA6A9N1vmADe8FxrOi7gg5jqs5EhGJCKC9Bclt1"
    result = await get_nasa_picture_of_the_day(api_key)
    return result
    


if __name__ == "__main__":
    app.run()
