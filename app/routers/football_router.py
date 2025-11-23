from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, Dict, Any

from app.football_client import FootballClient
from app.schemas.football_schemas import (
    ApiResponse,
    TeamsResponse,
    CountriesResponse,
    LeaguesResponse,
    PlayersSquadsResponse,
)
from app.redis_client import get_cache, set_cache

router = APIRouter()


def get_client() -> FootballClient:
    return FootballClient()


def _clean_params(**kwargs) -> Dict[str, Any]:
    return {k: v for k, v in sorted(kwargs.items()) if v is not None}


def _extract_json(resp):
    if hasattr(resp, "json") and callable(getattr(resp, "json")):
        return resp.json()
    return resp


# Допоміжна функція для генерації ключа
def generate_cache_key(prefix: str, params: Dict[str, Any]) -> str:
    # Перетворюємо dict в рядок, наприклад: "countries:code=UA:name=Ukraine"
    param_str = ":".join([f"{k}={v}" for k, v in params.items()])
    return f"football:{prefix}:{param_str}"


@router.get("/countries", response_model=CountriesResponse)
async def countries(
        name: Optional[str] = Query(None),
        code: Optional[str] = Query(None),
        search: Optional[str] = Query(None),
        client: FootballClient = Depends(get_client),
):
    params = _clean_params(name=name, code=code, search=search)
    cache_key = generate_cache_key("countries", params)

    # 1. Спроба отримати з кешу
    cached_data = await get_cache(cache_key)
    if cached_data:
        return cached_data

    # 2. Якщо немає в кеші - робимо запит
    try:
        resp = client.get_countries(**params)
        data = _extract_json(resp)

        # 3. Зберігаємо в кеш (якщо немає помилок в даних)
        if isinstance(data, dict) and not data.get("errors"):
            await set_cache(cache_key, data)

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=ApiResponse[Dict[str, Any]])
async def root_search(
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
    cache_key = generate_cache_key("root", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        return cached_data

    try:
        resp = client.get_root(**params)
        data = _extract_json(resp)
        if isinstance(data, dict) and not data.get("errors"):
            await set_cache(cache_key, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams/seasons")
async def teams_seasons(
        team: int = Query(..., description="team id"),
        client: FootballClient = Depends(get_client),
):
    params = _clean_params(team=team)
    cache_key = generate_cache_key("teams_seasons", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        return cached_data

    try:
        resp = client.get_team_seasons(team=team)
        data = _extract_json(resp)
        await set_cache(cache_key, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/players/squads", response_model=PlayersSquadsResponse)
async def players_squads(
        team: Optional[int] = Query(None),
        player: Optional[int] = Query(None),
        client: FootballClient = Depends(get_client),
):
    params = _clean_params(team=team, player=player)
    cache_key = generate_cache_key("squads", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        return cached_data

    try:
        resp = client.get_players_squads(**params)
        data = _extract_json(resp)
        if isinstance(data, dict) and not data.get("errors"):
            await set_cache(cache_key, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams", response_model=TeamsResponse)
async def teams(
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
    cache_key = generate_cache_key("teams", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        return cached_data

    try:
        resp = client.get_teams(**params)
        data = _extract_json(resp)
        if isinstance(data, dict) and not data.get("errors"):
            await set_cache(cache_key, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leagues", response_model=LeaguesResponse)
async def leagues(
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
    cache_key = generate_cache_key("leagues", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        return cached_data

    try:
        resp = client.get_leagues(**params)
        data = _extract_json(resp)
        if isinstance(data, dict) and not data.get("errors"):
            await set_cache(cache_key, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))