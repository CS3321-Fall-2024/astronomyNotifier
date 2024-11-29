import asyncio
import pytest
import main

pytest_plugins = ("pytest_asyncio",)

@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
         pytest.param("This is a message from get_asteroids_API.", id="Test message for get_asteroids_API"),
        ],
)
async def test_get_asteroids_API_Call(expected):
    assert await main.get_asteroids_API() == expected
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from get_next_eclipse_API.", id="Test message for get_next_eclipse_API"),
        ],
)
async def test_get_next_eclipse_API_Call(expected):
    assert main.get_next_eclipse_API() == expected 
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from get_next_iss_pass_API.", id="Test message for get_next_iss_pass_API"),
        ],
)
async def test_get_next_iss_pass_API_Call(expected):
    assert await main.get_next_iss_pass_API() == expected 
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from get_distance_to_iss_API.", id="Test message for get_distance_to_iss_API"),
        ],
)
async def test_get_distance_to_iss_API_Call(expected):
    assert await main.get_distance_to_iss_API() == expected 
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from get_nasa_picture_of_the_day_API.", id="Test message for get_nasa_picture_of_the_day_API"),
        ],
)

async def test_get_nasa_picture_of_the_day_API_Call(expected):
    assert await main.get_nasa_picture_of_the_day_API() == expected 

@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from get_aurora_API.", id="Test message for get_aurora_API"),
        ],
)

async def test_get_aurora_API_Call(expected):
    assert await main.get_aurora_API() == expected 
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from fetch_hourly_weather_API.", id="Test message for fetch_hourly_weather_API"),
        ],
)

async def test_fetch_hourly_weather_API_Call(expected):
    assert await main.fetch_hourly_weather_API() == expected 

@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from fetch_daily_weather_API.", id="Test message for fetch_daily_weather_API"),
        ],
)

async def test_fetch_daily_weather_API_Call(expected):
    assert await main.fetch_daily_weather_API() == expected 
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from get_moon_phase_API.", id="Test message for get_moon_phase_API"),
        ],
)

async def test_get_moon_phase_API_Call(expected):
    assert await main.get_moon_phase_API() == expected 