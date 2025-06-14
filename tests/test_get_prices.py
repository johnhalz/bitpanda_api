import pytest

from bitpanda_api.api.default import get_ticker


def test_get_prices(client):
    response = get_ticker.sync(client=client)

    assert response is not None, "Response should not be None"


@pytest.mark.asyncio
async def test_get_prices_async(client):
    response = await get_ticker.asyncio(client=client)

    assert response is not None, "Response should not be None"
