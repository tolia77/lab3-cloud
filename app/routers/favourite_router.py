from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from app.database import get_db
from app.models import FavoriteTeam
from app.schemas import FavoriteTeamCreate, FavoriteTeamResponse, FavoriteTeamUpdate

router = APIRouter(tags=["Favorites"])


@router.post("/", response_model=FavoriteTeamResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite_team(
        team_data: FavoriteTeamCreate,
        db: AsyncSession = Depends(get_db)
):
    # Перевірка чи команда вже існує
    query = select(FavoriteTeam).where(FavoriteTeam.api_team_id == team_data.api_team_id)
    result = await db.execute(query)
    existing_team = result.scalar_one_or_none()

    if existing_team:
        raise HTTPException(status_code=400, detail="Team already in favorites")

    new_team = FavoriteTeam(**team_data.dict())
    db.add(new_team)
    await db.commit()
    await db.refresh(new_team)
    return new_team


@router.get("/", response_model=List[FavoriteTeamResponse])
async def get_favorites(db: AsyncSession = Depends(get_db)):
    query = select(FavoriteTeam).order_by(FavoriteTeam.created_at.desc())
    result = await db.execute(query)
    teams = result.scalars().all()
    return teams


@router.delete("/{api_team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(api_team_id: int, db: AsyncSession = Depends(get_db)):
    query = delete(FavoriteTeam).where(FavoriteTeam.api_team_id == api_team_id)
    await db.execute(query)
    await db.commit()