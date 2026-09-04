from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)

    glyph_text: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    simple_text: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    ayah_words: Mapped[list["AyahWord"]] = relationship(
        back_populates="word",
    )

    __table_args__ = (
        Index(
            "uq_words_glyph_simple",
            "glyph_text",
            "simple_text",
            unique=True,
        ),
    )