import pytest
from src.app import app

@pytest.mark.parametrize(
    "expected",
    [
        pytest.param("Pocatello", id="Getting the city name"), 
        ],
)


def test_get_current_city(expected):
    """Tests the hypotenuse function"""
    assert app.get_current_city() == expected
    

@pytest.mark.parametrize(
    "expected",
    [
        pytest.param("Pocatello", id="Getting the city name"), 
        ],
)

