from typing import Any, Dict, Optional
from app.http_client import HttpClient


class FootballClient:
    def __init__(self, api_key: Optional[str] = None, api_host: Optional[str] = None, base_url: Optional[str] = None):
        self.http = HttpClient(base_url=base_url, api_key=api_key, api_host=api_host)

    # GET /countries
    def get_countries(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        # accepted params: id, name, code, search, country, season, current, team, type, last
        p = params or {}
        p.update(kwargs)
        return self.http.get("/countries", params=p)

    # GET / (root) — use as generic lookup for endpoints under base url with query params
    def get_root(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        p = params or {}
        p.update(kwargs)
        return self.http.get("/", params=p)

    # GET /teams/statistics
    def get_team_statistics(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        # accepted params: league, season, team, date
        p = params or {}
        p.update(kwargs)
        return self.http.get("/teams/statistics", params=p)

    # GET /teams/seasons
    def get_team_seasons(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        # accepted params: team
        p = params or {}
        p.update(kwargs)
        return self.http.get("/teams/seasons", params=p)

    # GET /players/squads
    def get_players_squads(self, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        # accepted params: team, player
        p = params or {}
        p.update(kwargs)
        return self.http.get("/players/squads", params=p)

