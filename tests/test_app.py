import pytest
from src import app

@pytest.mark.parametrize(
    "expected",
    [
        pytest.param("Pocatello", id="Getting the city name"), 
        ],
)


def test_get_current_city(expected):
    assert app.get_current_city() == expected


