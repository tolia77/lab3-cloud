from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FavoriteTeamBase(BaseModel):
    api_team_id: int
    name: str
    country: Optional[str] = None
    logo_url: Optional[str] = None
    notes: Optional[str] = None


class FavoriteTeamCreate(FavoriteTeamBase):
    pass


class FavoriteTeamUpdate(BaseModel):
    notes: Optional[str] = None


class FavoriteTeamResponse(FavoriteTeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
