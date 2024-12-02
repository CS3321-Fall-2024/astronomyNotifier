import pytest
from apis.asteroids import get_asteroids
import pytest
import httpx

asteroid_list = ["asteroid1", "asteroid2"]

class empty_response:
    called = 0
    def raise_for_status(self):
        self.called += 1
    def json(self):
        class empty_data:
            def get(data, string, lst):
                if string == "near_earth_objects":
                    return asteroid_list
                elif string == 'links':
                    class next:
                        def get(self, str):
                            return None
                    return next()
        return empty_data()

@pytest.mark.asyncio
async def test_get_asteroids(mocker):
    mocker_return = empty_response()
    mock_client = mocker.patch.object(httpx.AsyncClient, "get", return_value=mocker_return)

    result = await get_asteroids("API_KEY")

    for index, ast in enumerate(result):
        assert ast == asteroid_list[index]

    mock_client.assert_called_once_with("https://api.nasa.gov/neo/rest/v1/neo/browse?api_key=API_KEY")
    assert mocker_return.called > 0
