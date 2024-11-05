import asyncio
import pytest
from main import hello

pytest_plugins = ("pytest_asyncio",)

#@pytest.mark.parametrize(
#     "expected",
#     [
#         pytest.param("Pocatello", id="Getting the city name"), 
#         ],
# )
# 
# 
# def test_get_current_city(expected):
#     assert app.get_current_city() == expected

@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("hello world!", id="init test"),
            ],
)
async def test_hello(expected):
    assert await hello() == expected
