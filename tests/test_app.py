import asyncio
import pytest
from main import hello, test1, test2

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

@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
         pytest.param("This is a message from test1.", id="Test message for test1"),
        ],
)
async def test1_Call(expected):
    assert await test1() == expected
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from test2.", id="Test message for test1"),
        ],
)
async def test2_Call(expected):
    assert await test2() == expected 