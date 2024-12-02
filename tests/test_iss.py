import pytest
import httpx
from apis.iss import get_next_iss_pass, get_distance_to_iss, get_nasa_picture_of_the_day

def test_next_iss_pass():
    result = get_next_iss_pass(0,0,1,5, True)
    assert result == ['2024-01-01T18:56:19Z']

@pytest.mark.asyncio
async def test_get_distance_to_iss():
    result = await get_distance_to_iss(0, 0, True)
    result = (int(result[0]), int(result[1]), int(result[1]))
    assert result == (6414, 9, 9)

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