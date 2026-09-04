from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Reciter(Base):
    __tablename__ = "reciters"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    timings: Mapped[list["Timing"]] = relationship(
        back_populates="reciter",
        cascade="all, delete-orphan",
    )