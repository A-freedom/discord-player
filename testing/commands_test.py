import pytest
import asyncio

# An asynchronous function that adds two numbers
async def async_add(a, b):
    await asyncio.sleep(1)  # Simulate some asynchronous work
    return a + b

# Use pytest.mark.asyncio to define asynchronous test functions
@pytest.mark.asyncio
async def test_async_add_positive_numbers():
    result = await async_add(3, 4)
    assert result == 7

@pytest.mark.asyncio
async def test_async_add_negative_numbers():
    result = await async_add(-2, -5)
    assert result == -7

@pytest.mark.asyncio
async def test_async_add_mixed_numbers():
    result = await async_add(10, -5)
    assert result == 5215
