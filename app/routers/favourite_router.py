import logging
from typing import List

import sentry_sdk
from app.database import get_db
from app.models import FavoriteTeam
from app.schemas import FavoriteTeamCreate, FavoriteTeamResponse, FavoriteTeamUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Favorites"])

logger = logging.getLogger(__name__)


@router.post("/", response_model=FavoriteTeamResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite_team(team_data: FavoriteTeamCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"[FAVORITES][ADD] Adding favorite team api_team_id={team_data.api_team_id}")
    try:
        query = select(FavoriteTeam).where(FavoriteTeam.api_team_id == team_data.api_team_id)
        result = await db.execute(query)
        existing_team = result.scalar_one_or_none()

        if existing_team:
            logger.warning(f"[FAVORITES][ADD] Team already exists api_team_id={team_data.api_team_id}")
            raise HTTPException(status_code=400, detail="Team already in favorites")

        new_team = FavoriteTeam(**team_data.dict())
        db.add(new_team)
        await db.commit()
        await db.refresh(new_team)
        logger.info(f"[FAVORITES][ADD] Successfully added team id={new_team.id}")
        return new_team
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("[FAVORITES][ADD] Error adding favorite team")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[FavoriteTeamResponse])
async def get_favorites(db: AsyncSession = Depends(get_db)):
    logger.info("[FAVORITES][GET] Getting all favorite teams")
    try:
        query = select(FavoriteTeam).order_by(FavoriteTeam.created_at.desc())
        result = await db.execute(query)
        teams = result.scalars().all()
        logger.debug(f"[FAVORITES][GET] Found {len(teams)} favorite teams")
        return teams
    except Exception as e:
        logger.exception("[FAVORITES][GET] Error fetching favorite teams")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{api_team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(api_team_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"[FAVORITES][DELETE] Removing favorite team api_team_id={api_team_id}")
    try:
        query = delete(FavoriteTeam).where(FavoriteTeam.api_team_id == api_team_id)
        await db.execute(query)
        await db.commit()
        logger.info(f"[FAVORITES][DELETE] Successfully removed team api_team_id={api_team_id}")
    except Exception as e:
        logger.exception("[FAVORITES][DELETE] Error removing favorite team")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail=str(e))
