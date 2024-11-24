import asyncio
import pytest
from main import test1, test2, test3, test4, test5

pytest_plugins = ("pytest_asyncio",)

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
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from test2.", id="Test message for test1"),
        ],
)
async def test3_Call(expected):
    assert await test3() == expected 
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from test2.", id="Test message for test1"),
        ],
)
async def test4_Call(expected):
    assert await test4() == expected 
    
@pytest.mark.asyncio
@pytest.mark.parametrize(
        "expected",
        [
            pytest.param("This is a message from test2.", id="Test message for test1"),
        ],
)
async def test5_Call(expected):
    assert await test5() == expected 