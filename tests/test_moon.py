import pytest
from datetime import datetime
from apis.moon import get_moon_phase


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date, expected",
        [
            pytest.param(datetime(2024, 1, 1), 'First Quarter, First Quarter, First Quarter, First Quarter, Waxing Crescent, Waxing Crescent, Waxing Crescent'),
            pytest.param(datetime(2024, 1, 8), 'Waxing Crescent, Waxing Crescent, Waxing Crescent, Waxing Crescent, Waxing Crescent, Waxing Crescent, Waxing Crescent'),
            pytest.param(datetime(2024, 1, 15), 'Waxing Crescent, Waxing Crescent, Waxing Crescent, Waxing Crescent, First Quarter, First Quarter, First Quarter'),
            pytest.param(datetime(2024, 1, 22), 'First Quarter, First Quarter, First Quarter, First Quarter, First Quarter, First Quarter, First Quarter'),
        ],
)
async def test_get_moon_phase(date, expected):
    result = await get_moon_phase(date)

    assert result == expected
