import pytest
import datetime
from apis.eclipse import get_next_eclipse
from unittest.mock import patch


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "lat, long, expected",
    [
        pytest.param(10,10, "Partial"),
        pytest.param(10,20, "Partial"),
    ]
)
async def test_get_next_eclipse(mocker, lat, long, expected):
    with patch('datetime.datetime') as mock_date:
        mock_date.today.return_value = datetime.date(2024, 1, 8)
        result = await get_next_eclipse(lat, long)
        assert result.kind.name == expected