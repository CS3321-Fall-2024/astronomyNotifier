import pytest
import httpx
from apis.weather import fetch_daily_weather, fetch_hourly_weather

class fake_response:
    def __init__(self):
        self.status_code = 200
    def json(self):
        class data:
            def get(self2, str, lst):
                if str == "daily":
                    return self2
                elif str == "time":
                    return ["2024-01-01"]
                elif str == "temperature_2m_max":
                    return ["83"]
                elif str == "temperature_2m_min":
                    return ["32"]
                elif str == "precipitation_sum":
                    return ["4"]
        return data()


@pytest.mark.asyncio
async def test_fetch_daily_weather(mocker):  
    mocker.patch.object(httpx.AsyncClient, "get", return_value = fake_response())
    result = await fetch_daily_weather(30, 40)
    assert result == "Date: 01/01/2024, High Temp: 83 F, Low Temp: 32 F, Precipitation: 4mm"