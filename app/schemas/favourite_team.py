from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Базова схема для створення/оновлення
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

# Схема для відображення (включаючи ID з БД та дати)
class FavoriteTeamResponse(FavoriteTeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True