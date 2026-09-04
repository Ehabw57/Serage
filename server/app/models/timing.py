from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Timing(Base):
    __tablename__ = "timings"

    id: Mapped[int] = mapped_column(primary_key=True)

    start_time: Mapped[float] = mapped_column(
        nullable=False,
    )

    end_time: Mapped[float] = mapped_column(
        nullable=False,
    )

    reciter_id: Mapped[int] = mapped_column(
        ForeignKey("reciters.id"),
        nullable=False,
    )

    ayah_word_id: Mapped[int] = mapped_column(
        ForeignKey("ayah_words.id"),
        nullable=False,
    )

    reciter: Mapped["Reciter"] = relationship(
        back_populates="timings",
    )

    ayah_word: Mapped["AyahWord"] = relationship(
        back_populates="timings",
    )

    __table_args__ = (
        Index(
            "uq_timing_reciter_word",
            "reciter_id",
            "ayah_word_id",
            unique=True,
        ),
    )