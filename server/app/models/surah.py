from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Surah(Base):
    __tablename__ = "surahs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    en_name: Mapped[str] = mapped_column(String(32), nullable=False)
    ayahs_count: Mapped[int] = mapped_column(nullable=False)

    ayahs: Mapped[list["Ayah"]] = relationship(
        back_populates="surah",
        cascade="all, delete-orphan",
    )
