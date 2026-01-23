import pytest

from clients.public.public_client import PublicClient, get_public_client, PublicSession, get_public_session


@pytest.fixture(scope='function')
def public_client() -> PublicClient:
    return get_public_client()


@pytest.fixture(scope='function')
def public_session() -> PublicSession:
    return get_public_session()