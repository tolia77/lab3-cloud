from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestFootballRouter:
    """Tests for Football API router."""

    def test_countries_endpoint_success(self, client, mock_football_client):
        """Test countries endpoint returns data successfully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "get": "countries",
            "parameters": {},
            "errors": [],
            "results": 1,
            "paging": {"current": 1, "total": 1},
            "response": [{"name": "Ukraine", "code": "UA", "flag": "https://example.com/ua.png"}],
        }
        mock_football_client.get_countries.return_value = mock_response

        with patch("app.routers.football_router.get_cache", new_callable=AsyncMock) as mock_cache:
            mock_cache.return_value = None
            with patch("app.routers.football_router.set_cache", new_callable=AsyncMock):
                response = client.get("/football/countries")

        assert response.status_code == 200

    def test_countries_endpoint_with_cache(self, client):
        """Test countries endpoint returns cached data."""
        cached_data = {
            "get": "countries",
            "parameters": {},
            "errors": [],
            "results": 1,
            "paging": {"current": 1, "total": 1},
            "response": [{"name": "Ukraine", "code": "UA", "flag": "https://example.com/ua.png"}],
        }

        with patch("app.routers.football_router.get_cache", new_callable=AsyncMock) as mock_cache:
            mock_cache.return_value = cached_data
            response = client.get("/football/countries")

        assert response.status_code == 200

    def test_countries_endpoint_with_name_param(self, client, mock_football_client):
        """Test countries endpoint with name parameter."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "get": "countries",
            "parameters": {"name": "Ukraine"},
            "errors": [],
            "results": 1,
            "paging": {"current": 1, "total": 1},
            "response": [{"name": "Ukraine", "code": "UA", "flag": "https://example.com/ua.png"}],
        }
        mock_football_client.get_countries.return_value = mock_response

        with patch("app.routers.football_router.get_cache", new_callable=AsyncMock) as mock_cache:
            mock_cache.return_value = None
            with patch("app.routers.football_router.set_cache", new_callable=AsyncMock):
                response = client.get("/football/countries?name=Ukraine")

        assert response.status_code == 200

    def test_teams_endpoint_success(self, client, mock_football_client):
        """Test teams endpoint returns data successfully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "get": "teams",
            "parameters": {"id": "33"},
            "errors": [],
            "results": 1,
            "paging": {"current": 1, "total": 1},
            "response": [
                {
                    "team": {"id": 33, "name": "Manchester United", "code": "MUN"},
                    "venue": {"id": 556, "name": "Old Trafford"},
                }
            ],
        }
        mock_football_client.get_teams.return_value = mock_response

        with patch("app.routers.football_router.get_cache", new_callable=AsyncMock) as mock_cache:
            mock_cache.return_value = None
            with patch("app.routers.football_router.set_cache", new_callable=AsyncMock):
                response = client.get("/football/teams?id=33")

        assert response.status_code == 200

    def test_teams_endpoint_with_cache(self, client):
        """Test teams endpoint returns cached data."""
        cached_data = {
            "get": "teams",
            "parameters": {"id": "33"},
            "errors": [],
            "results": 1,
            "paging": {"current": 1, "total": 1},
            "response": [
                {
                    "team": {"id": 33, "name": "Manchester United", "code": "MUN"},
                    "venue": {"id": 556, "name": "Old Trafford"},
                }
            ],
        }

        with patch("app.routers.football_router.get_cache", new_callable=AsyncMock) as mock_cache:
            mock_cache.return_value = cached_data
            response = client.get("/football/teams?id=33")

        assert response.status_code == 200

    def test_leagues_endpoint_success(self, client, mock_football_client):
        """Test leagues endpoint returns data successfully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "get": "leagues",
            "parameters": {},
            "errors": [],
            "results": 1,
            "paging": {"current": 1, "total": 1},
            "response": [
                {
                    "league": {"id": 39, "name": "Premier League", "type": "League"},
                    "country": {"name": "England", "code": "GB"},
                    "seasons": [],
                }
            ],
        }
        mock_football_client.get_leagues.return_value = mock_response

        with patch("app.routers.football_router.get_cache", new_callable=AsyncMock) as mock_cache:
            mock_cache.return_value = None
            with patch("app.routers.football_router.set_cache", new_callable=AsyncMock):
                response = client.get("/football/leagues")

        assert response.status_code == 200

    def test_teams_seasons_endpoint_success(self, client, mock_football_client):
        """Test teams seasons endpoint returns data successfully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "get": "teams/seasons",
            "parameters": {"team": "33"},
            "errors": [],
            "results": 5,
            "response": [2020, 2021, 2022, 2023, 2024],
        }
        mock_football_client.get_team_seasons.return_value = mock_response

        with patch("app.routers.football_router.get_cache", new_callable=AsyncMock) as mock_cache:
            mock_cache.return_value = None
            with patch("app.routers.football_router.set_cache", new_callable=AsyncMock):
                response = client.get("/football/teams/seasons?team=33")

        assert response.status_code == 200

    def test_players_squads_endpoint_success(self, client, mock_football_client):
        """Test players squads endpoint returns data successfully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "get": "players/squads",
            "parameters": {"team": "33"},
            "errors": [],
            "results": 1,
            "paging": {"current": 1, "total": 1},
            "response": [
                {
                    "team": {"id": 33, "name": "Manchester United"},
                    "players": [{"id": 1, "name": "Player 1", "number": 10}],
                }
            ],
        }
        mock_football_client.get_players_squads.return_value = mock_response

        with patch("app.routers.football_router.get_cache", new_callable=AsyncMock) as mock_cache:
            mock_cache.return_value = None
            with patch("app.routers.football_router.set_cache", new_callable=AsyncMock):
                response = client.get("/football/players/squads?team=33")

        assert response.status_code == 200

    def test_root_search_endpoint_success(self, client, mock_football_client):
        """Test root search endpoint returns data successfully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "get": "teams",
            "parameters": {"search": "United"},
            "errors": [],
            "results": 1,
            "paging": {"current": 1, "total": 1},
            "response": [{"team": {"id": 33, "name": "Manchester United"}}],
        }
        mock_football_client.get_root.return_value = mock_response

        with patch("app.routers.football_router.get_cache", new_callable=AsyncMock) as mock_cache:
            mock_cache.return_value = None
            with patch("app.routers.football_router.set_cache", new_callable=AsyncMock):
                response = client.get("/football/?search=United")

        assert response.status_code == 200

    def test_countries_endpoint_api_error(self, client, mock_football_client):
        """Test countries endpoint handles API errors."""
        mock_football_client.get_countries.side_effect = Exception("API Error")

        with patch("app.routers.football_router.get_cache", new_callable=AsyncMock) as mock_cache:
            mock_cache.return_value = None
            response = client.get("/football/countries")

        assert response.status_code == 500

    def test_teams_endpoint_missing_required_param(self, client):
        """Test teams/seasons endpoint without required team param."""
        response = client.get("/football/teams/seasons")
        assert response.status_code == 422  # Validation error
