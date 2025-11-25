from typing import Any, Dict, Optional

from app.http_client import HttpClient


class FootballClient:
    def __init__(self, api_key: Optional[str] = None, api_host: Optional[str] = None, base_url: Optional[str] = None):
        self.http = HttpClient(base_url=base_url, api_key=api_key, api_host=api_host)

    def get_countries(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        p = params or {}
        p.update(kwargs)
        return self.http.get("/countries", params=p)

    def get_root(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        p = params or {}
        p.update(kwargs)
        return self.http.get("/", params=p)

    def get_team_seasons(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        p = params or {}
        p.update(kwargs)
        return self.http.get("/teams/seasons", params=p)

    def get_players_squads(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        p = params or {}
        p.update(kwargs)
        return self.http.get("/players/squads", params=p)

    def get_teams(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        p = params or {}
        p.update(kwargs)
        return self.http.get("/teams", params=p)

    def get_leagues(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        p = params or {}
        p.update(kwargs)
        return self.http.get("/leagues", params=p)
