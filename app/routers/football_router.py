import logging
from typing import Any, Dict, Optional

import sentry_sdk
from app.football_client import FootballClient
from app.redis_client import get_cache, set_cache
from app.schemas.football_schemas import (
    ApiResponse,
    CountriesResponse,
    LeaguesResponse,
    PlayersSquadsResponse,
    TeamsResponse,
)
from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()

logger = logging.getLogger(__name__)


def get_client() -> FootballClient:
    return FootballClient()


def _clean_params(**kwargs) -> Dict[str, Any]:
    return {k: v for k, v in sorted(kwargs.items()) if v is not None}


def _extract_json(resp):
    if hasattr(resp, "json") and callable(getattr(resp, "json")):
        return resp.json()
    return resp


def generate_cache_key(prefix: str, params: Dict[str, Any]) -> str:
    param_str = ":".join([f"{k}={v}" for k, v in params.items()])
    return f"football:{prefix}:{param_str}"


@router.get("/countries", response_model=CountriesResponse)
async def countries(
    name: Optional[str] = Query(None),
    code: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    client: FootballClient = Depends(get_client),
):
    logger.info(f"[FOOTBALL][COUNTRIES] Get countries name={name}, code={code}, search={search}")
    params = _clean_params(name=name, code=code, search=search)
    cache_key = generate_cache_key("countries", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        logger.debug(f"[FOOTBALL][COUNTRIES] Cache hit for key={cache_key}")
        return cached_data

    try:
        resp = client.get_countries(**params)
        data = _extract_json(resp)

        if isinstance(data, dict) and not data.get("errors"):
            await set_cache(cache_key, data)
            logger.debug(f"[FOOTBALL][COUNTRIES] Data cached for key={cache_key}")

        return data
    except Exception as e:
        logger.exception("[FOOTBALL][COUNTRIES] Error fetching countries")
        sentry_sdk.capture_exception(e)
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
    logger.info(f"[FOOTBALL][ROOT] Root search id={id}, name={name}")
    params = _clean_params(
        id=id, name=name, code=code, search=search, country=country, league=league, season=season, venue=venue
    )
    cache_key = generate_cache_key("root", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        logger.debug(f"[FOOTBALL][ROOT] Cache hit for key={cache_key}")
        return cached_data

    try:
        resp = client.get_root(**params)
        data = _extract_json(resp)
        if isinstance(data, dict) and not data.get("errors"):
            await set_cache(cache_key, data)
            logger.debug(f"[FOOTBALL][ROOT] Data cached for key={cache_key}")
        return data
    except Exception as e:
        logger.exception("[FOOTBALL][ROOT] Error in root search")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams/seasons")
async def teams_seasons(
    team: int = Query(..., description="team id"),
    client: FootballClient = Depends(get_client),
):
    logger.info(f"[FOOTBALL][TEAMS_SEASONS] Get team seasons team={team}")
    params = _clean_params(team=team)
    cache_key = generate_cache_key("teams_seasons", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        logger.debug(f"[FOOTBALL][TEAMS_SEASONS] Cache hit for key={cache_key}")
        return cached_data

    try:
        resp = client.get_team_seasons(team=team)
        data = _extract_json(resp)
        await set_cache(cache_key, data)
        logger.debug(f"[FOOTBALL][TEAMS_SEASONS] Data cached for key={cache_key}")
        return data
    except Exception as e:
        logger.exception("[FOOTBALL][TEAMS_SEASONS] Error fetching team seasons")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/players/squads", response_model=PlayersSquadsResponse)
async def players_squads(
    team: Optional[int] = Query(None),
    player: Optional[int] = Query(None),
    client: FootballClient = Depends(get_client),
):
    logger.info(f"[FOOTBALL][SQUADS] Get player squads team={team}, player={player}")
    params = _clean_params(team=team, player=player)
    cache_key = generate_cache_key("squads", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        logger.debug(f"[FOOTBALL][SQUADS] Cache hit for key={cache_key}")
        return cached_data

    try:
        resp = client.get_players_squads(**params)
        data = _extract_json(resp)
        if isinstance(data, dict) and not data.get("errors"):
            await set_cache(cache_key, data)
            logger.debug(f"[FOOTBALL][SQUADS] Data cached for key={cache_key}")
        return data
    except Exception as e:
        logger.exception("[FOOTBALL][SQUADS] Error fetching player squads")
        sentry_sdk.capture_exception(e)
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
    logger.info(f"[FOOTBALL][TEAMS] Get teams id={id}, name={name}, country={country}")
    params = _clean_params(
        id=id, name=name, code=code, search=search, country=country, league=league, season=season, venue=venue
    )
    cache_key = generate_cache_key("teams", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        logger.debug(f"[FOOTBALL][TEAMS] Cache hit for key={cache_key}")
        return cached_data

    try:
        resp = client.get_teams(**params)
        data = _extract_json(resp)
        if isinstance(data, dict) and not data.get("errors"):
            await set_cache(cache_key, data)
            logger.debug(f"[FOOTBALL][TEAMS] Data cached for key={cache_key}")
        return data
    except Exception as e:
        logger.exception("[FOOTBALL][TEAMS] Error fetching teams")
        sentry_sdk.capture_exception(e)
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
    logger.info(f"[FOOTBALL][LEAGUES] Get leagues id={id}, name={name}, country={country}")
    params = _clean_params(
        id=id,
        name=name,
        code=code,
        search=search,
        country=country,
        season=season,
        current=current,
        team=team,
        type=type,
        last=last,
    )
    cache_key = generate_cache_key("leagues", params)

    cached_data = await get_cache(cache_key)
    if cached_data:
        logger.debug(f"[FOOTBALL][LEAGUES] Cache hit for key={cache_key}")
        return cached_data

    try:
        resp = client.get_leagues(**params)
        data = _extract_json(resp)
        if isinstance(data, dict) and not data.get("errors"):
            await set_cache(cache_key, data)
            logger.debug(f"[FOOTBALL][LEAGUES] Data cached for key={cache_key}")
        return data
    except Exception as e:
        logger.exception("[FOOTBALL][LEAGUES] Error fetching leagues")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail=str(e))
