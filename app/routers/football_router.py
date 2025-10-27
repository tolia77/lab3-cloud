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
    id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    code: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    season: Optional[int] = Query(None),
    current: Optional[int] = Query(None),
    team: Optional[int] = Query(None),
    type: Optional[str] = Query(None),
    last: Optional[int] = Query(None),
    client: FootballClient = Depends(get_client),
):
    params = _clean_params(id=id, name=name, code=code, search=search, country=country,
                           season=season, current=current, team=team, type=type, last=last)
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

