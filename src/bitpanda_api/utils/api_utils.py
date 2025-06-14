from bitpanda_api.client import Client
from bitpanda_api.utils import PRODUCTION_URL


def setup_client(base_url: str = PRODUCTION_URL) -> Client:
    """
    Set up a client.

    Args:
        base_url (str): The base URL of the API.

    Returns:
        Client: A client for the API.
    """
    return Client(base_url=base_url)
