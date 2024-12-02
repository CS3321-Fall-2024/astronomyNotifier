import pytest
import httpx
import datetime
from apis.aurora import fetch_geomagnetic_storms, calculate_visibility, get_aurora_data

class fake_response:
    def __init__(self, ret, code):
        self.url = "URL"
        self.status_code = code
        self.ret = ret
        self.text = "TEXT"
    def json(self):
        return self.ret

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response",
    [
        pytest.param(fake_response(["storm1", "storm2"], 200), id="ok response"),
        pytest.param(fake_response([], 300), id="bad response")
    ]
)
async def test_fetch_geomagnetic_storms(mocker, response):
    mock_client = mocker.patch.object(httpx.AsyncClient, "get", return_value=response)

    result = await fetch_geomagnetic_storms("START_DATE", "END_DATE", "API_KEY")

    for index, ast in enumerate(result):
        assert ast == response.ret[index]
    assert len(result) == len(response.ret)

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "event, lat, long, expected",
    [
        pytest.param({"startTime" : "2024-01-01T00:00Z"}, 30, 40, True),
        pytest.param({"startTime" : "2024-01-01T06:00Z"}, 30, 40, False),
        pytest.param({"startTime" : "2024-01-01T12:00Z"}, 30, 40, False),
        pytest.param({"startTime" : "2024-01-01T18:00Z"}, 30, 40, True),
    ]
)
async def test_calculate_visibility(event, lat, long, expected):
    result = calculate_visibility(event, lat, long)
    assert result == expected

class fake_event:
    def __init__(self):
        pass
    def get(self, str, lst):
        assert str == 'allKpIndex'
        return None
    def __getitem__(self, key):
        assert key == "startTime"
        return "2024-01-01T00:00Z"

@pytest.mark.asyncio
async def test_get_aurora_data(mocker):
    mocker.patch("apis.aurora.fetch_geomagnetic_storms", return_value=[fake_event()])
    mocker.patch("apis.aurora.calculate_visibility", return_value=True)
    result = await get_aurora_data("API_KEY", 30, 40)
    assert result == "Start Time: Jan 01, 2024 12:00 AM UTC\nKp Index: N/A\nVisibility: Visible\n----------------------------------------\n"
