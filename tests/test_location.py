import pytest
import httpx
from apis.location import get_current_location

class fake_response:
    def __init__(self, loc):
         self.loc = loc
    def json(self):
        class data:
            def __getitem__(self2, key):
                assert key == 'loc'
                return self.loc 
        return data()

@pytest.mark.asyncio
@pytest.mark.parametrize(
        "resp, expected",
        [
            pytest.param(fake_response("20,20"), (20,20)),
            pytest.param(fake_response("0,0"), (0,0)),
            pytest.param(fake_response("120,-30"), (120,-30))
        ],
)
async def test_get_current_location(mocker, resp, expected):
    mock_client = mocker.patch.object(httpx.AsyncClient, "get", return_value=resp)

    result = await get_current_location()

    assert result == expected

    assert await mock_client.called_once()
