from app.models.base import Base
from app.models.surah import Surah
from app.models.ayah import Ayah
from app.models.word import Word
from app.models.ayah_word import AyahWord
from app.models.reciter import Reciter
from app.models.timing import Timing

__all__ = [
    "Base",
    "Surah",
    "Ayah",
    "Word",
    "AyahWord",
    "Reciter",
    "Timing",
]