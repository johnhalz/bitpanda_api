import pytest

from bitpanda_api.utils.api_utils import setup_client


@pytest.fixture(scope="session")
def client():
    client = setup_client()

    return client
