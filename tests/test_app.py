import asyncio
import pytest
import astronomy
import datetime

from main import *

pytest_plugins = ("pytest_asyncio",)

#@pytest.mark.parametrize(
#     "expected",
#     [
#         pytest.param("Pocatello", id="Getting the city name"), 
#         ],
# )
# 
# 
# def test_get_current_city(expected):
#     assert app.get_current_city() == expected

@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("hello world!", id="init test"),
            ],
)
async def test_hello(expected):
    assert True


asteroids = [ 
    {
        "name" : "asteroid a",
        "absolute_magnitude_h" : 1,
        "close_approach_data" : [{"miss_distance" : {"kilometers" : 100}}]
    },
    {
        "name" : "asteroid b",
        "absolute_magnitude_h" : 2,
        "close_approach_data" : [{"miss_distance" : {"kilometers" : 50}}]
    },
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
        "asteroids",
        [
            pytest.param(asteroids, id="basic pretend asteroids")
        ],
)
async def test_get_asteroids_API(mocker, asteroids):
    mocker.patch("main.get_asteroids", return_value = asteroids)

    mag_sort = "Asteroids sorted by magnitude:<br>" + \
           f'{asteroids[0]["name"]}: Magnitude {asteroids[0]["absolute_magnitude_h"]}<br>' + \
           f'{asteroids[1]["name"]}: Magnitude {asteroids[1]["absolute_magnitude_h"]}<br>'

    dist_sort = "Asteroids sorted by distance:<br>" + \
           f'{asteroids[1]["name"]}: Distance {asteroids[1]["close_approach_data"][0]["miss_distance"]["kilometers"]} km<br>' + \
           f'{asteroids[0]["name"]}: Distance {asteroids[0]["close_approach_data"][0]["miss_distance"]["kilometers"]} km<br>'

    expected = mag_sort + "<br>" + dist_sort

    assert await get_asteroids_API() == expected

@pytest.mark.asyncio
async def test_get_next_eclipse_API(mocker):
    loc_patch = mocker.patch("main.get_current_location", return_value = (0,0))
    test_location = astronomy.Observer(latitude=0, longitude=0)
    test_time = astronomy.Time(datetime(2024, 6, 6).strftime('%Y-%m-%d'))
    next_eclipse = astronomy.SearchLocalSolarEclipse(test_time, test_location)
    ecplise_patch = mocker.patch("main.get_next_eclipse", return_value = next_eclipse)

    expected = f"Next Solar Eclipse:<br>"
    expected += f"Type: {next_eclipse.kind.name}<br>"
    expected += f"Visibility: {next_eclipse.obscuration}<br>"
    expected += f"Date: {datetime.fromisoformat(str(next_eclipse.peak.time)).strftime('%Y-%m-%d %H:%M:%S')}<br>"

    assert await get_next_eclipse_API() == expected
    loc_patch.assert_called_once()
    ecplise_patch.assert_called_once()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "times, expected",
    [
        pytest.param(["2024-5-5T21:40:48Z", "2024-5-5T22:41:30Z"], "Upcoming ISS Passes:<br>\nPass 1: 2024-5-5T21:40:48Z<br>\nPass 2: 2024-5-5T22:41:30Z<br>\n", id="non empty times"),
        pytest.param([], "No passes found within the provided days.", id="empty times")
    ]
)
async def test_get_next_iss_pass_API(mocker, times, expected):
    mocker.patch("main.get_current_location", return_value = (0,0))
    mocker.patch("main.get_next_iss_pass", return_value = times)
    assert await get_next_iss_pass_API() == expected

@pytest.mark.asyncio
async def test_get_disctance_to_iss_API(mocker):
    mocker.patch("main.get_current_location", return_value = (0,0))
    mocker.patch("main.get_distance_to_iss", return_value = (10000, 0, 130))
    expected = f"The ISS is approximately 10000.00 kilometers away from your location.<br>"
    expected += f"The ISS is currently at latitude 0.00 and longitude 130.00.<br>"
    
    assert await get_distance_to_iss_API() == expected


@pytest.mark.asyncio
async def test_get_aurora_API(mocker):
    loc_mock = mocker.patch("main.get_current_location", return_value = (120,40))
    aurora_dat_mock =mocker.patch("main.aurora_data_to_string", return_value = "AURORADAT")
    assert await get_aurora_API() == "AURORADAT"
    args, kwargs = aurora_dat_mock.call_args
    assert args[1] == 120
    assert args[2] == 40
