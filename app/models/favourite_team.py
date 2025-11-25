from app.database import Base, UpdatedMix
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class FavoriteTeam(Base, UpdatedMix):
    __tablename__ = "favorite_teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    api_team_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    logo_url: Mapped[str] = mapped_column(String(500), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
