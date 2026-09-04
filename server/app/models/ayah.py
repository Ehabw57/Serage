from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Ayah(Base):
    __tablename__ = "ayahs"

    id: Mapped[int] = mapped_column(primary_key=True)

    surah_id: Mapped[int] = mapped_column(
        ForeignKey("surahs.id"),
        nullable=False,
    )

    number: Mapped[int] = mapped_column(nullable=False)
    page: Mapped[int] = mapped_column(nullable=False)
    juz: Mapped[int] = mapped_column(nullable=False)

    glyph_no: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    simple_text: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    surah: Mapped["Surah"] = relationship(
        back_populates="ayahs",
    )

    words: Mapped[list["AyahWord"]] = relationship(
        back_populates="ayah",
        cascade="all, delete-orphan",
    )