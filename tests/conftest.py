import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import os

os.environ["TESTING"] = "1"

from app.main import app
from app.database import get_db


@pytest.fixture(scope="session")
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_db_session():
    """Create mock database session."""
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    session.close = AsyncMock()
    return session


@pytest.fixture
def client_with_db(mock_db_session):
    """Create test client with mocked database."""
    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client, mock_db_session
    app.dependency_overrides.clear()


@pytest.fixture
def mock_football_client():
    """Mock FootballClient for testing without external API calls."""
    with patch("app.routers.football_router.FootballClient") as mock:
        client_instance = MagicMock()
        mock.return_value = client_instance
        yield client_instance
