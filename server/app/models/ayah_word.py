from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class AyahWord(Base):
    __tablename__ = "ayah_words"

    id: Mapped[int] = mapped_column(primary_key=True)

    ayah_id: Mapped[int] = mapped_column(
        ForeignKey("ayahs.id"),
        nullable=False,
    )

    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id"),
        nullable=False,
    )

    position: Mapped[int] = mapped_column(
        nullable=False,
    )

    ayah: Mapped["Ayah"] = relationship(
        back_populates="words",
    )

    word: Mapped["Word"] = relationship(
        back_populates="ayah_words",
    )

    timings: Mapped[list["Timing"]] = relationship(
        back_populates="ayah_word",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "uq_ayah_word_position",
            "ayah_id",
            "position",
            unique=True,
        ),
    )