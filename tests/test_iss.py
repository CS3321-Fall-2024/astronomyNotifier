import pytest
import httpx
from apis.iss import get_next_iss_pass, get_distance_to_iss, get_nasa_picture_of_the_day
import datetime

@pytest.mark.asyncio
async def test_next_iss_pass():
    result = get_next_iss_pass(0, 0, 1, 5, True)
    assert isinstance(result, list) and len(result) > 0
    assert all(isinstance(pass_time, str) for pass_time in result)



@pytest.mark.asyncio
async def test_get_distance_to_iss():
    distance, lat_iss, lon_iss = await get_distance_to_iss(0, 0, True)
    assert isinstance(distance, float) and distance > 0
    assert isinstance(lat_iss, float) and -90 <= lat_iss <= 90
    assert isinstance(lon_iss, float) and -180 <= lon_iss <= 180
    distance_no_fixed, lat_iss_no_fixed, lon_iss_no_fixed = await get_distance_to_iss(0, 0, False)
    assert isinstance(distance_no_fixed, float) and distance_no_fixed > 0
    assert isinstance(lat_iss_no_fixed, float) and -90 <= lat_iss_no_fixed <= 90
    assert isinstance(lon_iss_no_fixed, float) and -180 <= lon_iss_no_fixed <= 180

    assert 0 < distance < 500000 

    

class empty_response:
    called = 0
    def raise_for_status(self):
        self.called += 1
    def json(self):
        class data:
            def get(self, prop, none):
                if prop == "title":
                    return "TITLE"
                elif prop == "explanation":
                    return "EXPLANATION"
                elif prop == "url":
                    return "URL"
        return data()


@pytest.mark.asyncio
async def test_get_nasa_picture_of_the_day(mocker):
    mocker_return = empty_response()
    mock_client = mocker.patch.object(httpx.AsyncClient, "get", return_value=mocker_return)

    result = await get_nasa_picture_of_the_day("API_KEY")

    assert result == "Title: TITLE\nExplanation: EXPLANATION\nimg url = URL description = TITLE"

    args, kwargs = mock_client.call_args
    assert args[0] == 'https://api.nasa.gov/planetary/apod'
    assert kwargs["params"]["api_key"] == "API_KEY"

    assert mocker_return.called > 0