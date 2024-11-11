from quart import Quart
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
    next_solar = await get_next_eclipse()

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
    return "test2"


if __name__ == "__main__":
    app.run()
