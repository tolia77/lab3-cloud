from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.database import get_db
from app.main import app


class TestFavouriteRouter:
    """Tests for Favorites router."""

    def test_get_favorites_empty(self):
        """Test getting favorites when list is empty."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.close = AsyncMock()

        async def override_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = override_get_db
        from fastapi.testclient import TestClient

        client = TestClient(app)

        response = client.get("/favorites/")
        app.dependency_overrides.clear()

        assert response.status_code == 200
        assert response.json() == []

    def test_get_favorites_with_data(self):
        """Test getting favorites when data exists."""
        mock_team = MagicMock()
        mock_team.id = 1
        mock_team.api_team_id = 33
        mock_team.name = "Manchester United"
        mock_team.country = "England"
        mock_team.logo_url = "https://example.com/logo.png"
        mock_team.notes = None
        mock_team.created_at = datetime(2024, 1, 1, 12, 0, 0)
        mock_team.updated_at = datetime(2024, 1, 1, 12, 0, 0)

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_team]

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.close = AsyncMock()

        async def override_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = override_get_db
        from fastapi.testclient import TestClient

        client = TestClient(app)

        response = client.get("/favorites/")
        app.dependency_overrides.clear()

        assert response.status_code == 200

    def test_add_favorite_team_success(self):
        """Test adding a new favorite team."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.commit = AsyncMock()
        mock_session.add = MagicMock()
        mock_session.close = AsyncMock()

        async def mock_refresh(obj):
            obj.id = 1
            obj.created_at = datetime(2024, 1, 1, 12, 0, 0)
            obj.updated_at = datetime(2024, 1, 1, 12, 0, 0)

        mock_session.refresh = mock_refresh

        async def override_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = override_get_db
        from fastapi.testclient import TestClient

        client = TestClient(app)

        response = client.post(
            "/favorites/",
            json={
                "api_team_id": 33,
                "name": "Manchester United",
                "country": "England",
                "logo_url": "https://example.com/logo.png",
            },
        )
        app.dependency_overrides.clear()

        assert response.status_code == 201

    def test_add_favorite_team_already_exists(self):
        """Test adding team that already exists returns 400."""
        mock_existing_team = MagicMock()
        mock_existing_team.id = 1
        mock_existing_team.api_team_id = 33

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_existing_team

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.close = AsyncMock()

        async def override_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = override_get_db
        from fastapi.testclient import TestClient

        client = TestClient(app)

        response = client.post(
            "/favorites/",
            json={
                "api_team_id": 33,
                "name": "Manchester United",
                "country": "England",
                "logo_url": "https://example.com/logo.png",
            },
        )
        app.dependency_overrides.clear()

        assert response.status_code == 400
        assert "already in favorites" in response.json()["detail"]

    def test_delete_favorite_team_success(self):
        """Test deleting a favorite team."""
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock()
        mock_session.commit = AsyncMock()
        mock_session.close = AsyncMock()

        async def override_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = override_get_db
        from fastapi.testclient import TestClient

        client = TestClient(app)

        response = client.delete("/favorites/33")
        app.dependency_overrides.clear()

        assert response.status_code == 204

    def test_add_favorite_team_invalid_data(self, client):
        """Test adding team with invalid data returns 422."""
        response = client.post("/favorites/", json={"api_team_id": "not_a_number", "name": "Manchester United"})
        assert response.status_code == 422

    def test_add_favorite_team_missing_required_field(self, client):
        """Test adding team without required fields returns 422."""
        response = client.post(
            "/favorites/",
            json={
                "name": "Manchester United"
                # Missing api_team_id
            },
        )
        assert response.status_code == 422

    def test_delete_favorite_wrong_method(self, client):
        """Test that POST to delete endpoint returns 405."""
        response = client.post("/favorites/33")
        assert response.status_code == 405

    def test_get_favorites_wrong_method(self, client):
        """Test that DELETE to get favorites returns 405."""
        response = client.delete("/favorites/")
        assert response.status_code == 405
