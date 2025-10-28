from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, Dict, Any

# import your client (adjust if your import path differs)
from app.football_client import FootballClient


router = APIRouter()


def get_client() -> FootballClient:
    return FootballClient()


def _clean_params(**kwargs) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def _extract_json(resp):
    # support both requests.Response and direct dict returns
    if hasattr(resp, "json") and callable(getattr(resp, "json")):
        return resp.json()
    return resp


@router.get("/countries")
def countries(
    name: Optional[str] = Query(None),
    code: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    client: FootballClient = Depends(get_client),
):
    # only name, code, search are accepted for /countries
    params = _clean_params(name=name, code=code, search=search)
    try:
        resp = client.get_countries(**params)
        return _extract_json(resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def root_search(
    id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    code: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    league: Optional[int] = Query(None),
    season: Optional[int] = Query(None),
    venue: Optional[str] = Query(None),
    client: FootballClient = Depends(get_client),
):
    params = _clean_params(id=id, name=name, code=code, search=search, country=country,
                           league=league, season=season, venue=venue)
    try:
        resp = client.get_root(**params)
        return _extract_json(resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams/statistics")
def teams_statistics(
    league: Optional[int] = Query(None),
    season: Optional[int] = Query(None),
    team: Optional[int] = Query(None),
    date: Optional[str] = Query(None),
    client: FootballClient = Depends(get_client),
):
    params = _clean_params(league=league, season=season, team=team, date=date)
    try:
        resp = client.get_team_statistics(**params)
        return _extract_json(resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams/seasons")
def teams_seasons(
    team: int = Query(..., description="team id"),
    client: FootballClient = Depends(get_client),
):
    try:
        resp = client.get_team_seasons(team=team)
        return _extract_json(resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/players/squads")
def players_squads(
    team: Optional[int] = Query(None),
    player: Optional[int] = Query(None),
    client: FootballClient = Depends(get_client),
):
    params = _clean_params(team=team, player=player)
    try:
        resp = client.get_players_squads(**params)
        return _extract_json(resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams")
def teams(
    id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    code: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    league: Optional[int] = Query(None),
    season: Optional[int] = Query(None),
    venue: Optional[str] = Query(None),
    client: FootballClient = Depends(get_client),
):
    params = _clean_params(id=id, name=name, code=code, search=search, country=country,
                           league=league, season=season, venue=venue)
    try:
        resp = client.get_teams(**params)
        return _extract_json(resp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET /countries/{name}/teams — combine country info + teams for that country
@router.get("/countries/{name}/teams")
def country_with_teams(
    name: str,
    client: FootballClient = Depends(get_client),
):
    try:
        country_resp = client.get_countries(name=name)
        teams_resp = client.get_teams(country=name)

        country_data = _extract_json(country_resp)
        teams_data = _extract_json(teams_resp)

        country_item = None
        if isinstance(country_data, dict) and "response" in country_data:
            resp_list = country_data.get("response")
            country_item = resp_list[0] if isinstance(resp_list, list) and resp_list else None
        else:
            country_item = country_data

        return {"country": country_item, "teams": teams_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
