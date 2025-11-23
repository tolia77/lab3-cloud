from typing import Optional, Dict, Any, List, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class Paging(BaseModel):
    current: int
    total: int


class ApiResponse(GenericModel, Generic[T]):
    get: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    errors: List[Any] = []
    results: int
    paging: Paging
    response: List[T]


class TeamBasic(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    country: Optional[str] = None
    founded: Optional[int] = None
    national: Optional[bool] = None
    logo: Optional[str] = None


class Venue(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    capacity: Optional[int] = None
    surface: Optional[str] = None
    image: Optional[str] = None


class TeamVenueItem(BaseModel):
    team: TeamBasic
    venue: Optional[Venue] = None


class TeamsResponse(ApiResponse[TeamVenueItem]):
    pass


# Countries
class CountryItem(BaseModel):
    name: str
    code: Optional[str] = None
    flag: Optional[str] = None


class CountriesResponse(ApiResponse[CountryItem]):
    pass


# Leagues
class LeagueInfo(BaseModel):
    id: int
    name: str
    type: Optional[str] = None
    logo: Optional[str] = None


class CountryShort(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    flag: Optional[str] = None


class SeasonCoverage(BaseModel):
    fixtures: Optional[Dict[str, Any]] = None
    standings: Optional[Any] = None
    players: Optional[Any] = None
    top_scorers: Optional[Any] = None
    top_assists: Optional[Any] = None
    top_cards: Optional[Any] = None
    injuries: Optional[Any] = None
    predictions: Optional[Any] = None
    odds: Optional[Any] = None


class SeasonModel(BaseModel):
    year: int
    start: Optional[str] = None
    end: Optional[str] = None
    current: Optional[bool] = None
    coverage: Optional[Dict[str, Any]] = None


class LeagueItem(BaseModel):
    league: LeagueInfo
    country: CountryShort
    seasons: Optional[List[SeasonModel]] = None


class LeaguesResponse(ApiResponse[LeagueItem]):
    pass


# Players / squads
class PlayerModel(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    number: Optional[int] = None
    position: Optional[str] = None
    photo: Optional[str] = None


class PlayersSquadsItem(BaseModel):
    team: Optional[Dict[str, Any]] = None
    players: List[PlayerModel]


class PlayersSquadsResponse(ApiResponse[PlayersSquadsItem]):
    pass

