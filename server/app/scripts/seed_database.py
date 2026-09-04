import asyncio
import gzip
import json
from pathlib import Path

from sqlalchemy import select

from app.core.database import AsyncSessionLocal, engine
from app.models import (
    Base,
    Surah,
    Ayah,
    Word,
    AyahWord,
)


DATA_DIR = Path(__file__).resolve().parents[1] / "data"

CHAPTERS_FILE = DATA_DIR / "hafsChapters_v3-0.json.gz"
VERSES_FILE = DATA_DIR / "hafsVerses_v3.0.json.gz"


def load_json_gz(path: Path) -> list[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"{path.name} must contain a JSON list")

    return data


async def reset_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def seed_database():
    print("Loading Quran data...")

    chapters = load_json_gz(CHAPTERS_FILE)
    verses = load_json_gz(VERSES_FILE)

    print(f"Loaded {len(chapters)} surahs")
    print(f"Loaded {len(verses)} ayahs")

    print("Resetting database...")

    await reset_database()

    async with AsyncSessionLocal() as session:

        # --------------------------------
        # 1. Surahs
        # --------------------------------

        surahs = [
            Surah(
                id=chapter["id"],
                name=chapter["name"],
                en_name=chapter["en_name"],
                ayahs_count=chapter["ayahs_count"],
            )
            for chapter in chapters
        ]

        session.add_all(surahs)

        await session.flush()

        print(f"Inserted {len(surahs)} surahs")

        # --------------------------------
        # 2. Ayahs
        # --------------------------------

        ayahs = []

        for verse in verses:
            text_words = verse["text"]
            simple_words = verse["simple_text"]

            if len(text_words) != len(simple_words):
                raise ValueError(
                    f"Ayah {verse['id']} has different " f"text/simple_text word counts"
                )

            ayah = Ayah(
                id=verse["id"],
                surah_id=verse["surah_id"],
                number=verse["number"],
                page=verse["page"],
                juz=verse["juz"],
                glyph_no=verse["glyph_no"],
                text=" ".join(text_words),
                simple_text=" ".join(simple_words),
            )

            ayahs.append(ayah)

        session.add_all(ayahs)

        await session.flush()

        print(f"Inserted {len(ayahs)} ayahs")

        # --------------------------------
        # 3. Words
        # --------------------------------

        word_map: dict[tuple[str, str], Word] = {}

        for verse in verses:
            text_words = verse["text"]
            simple_words = verse["simple_text"]

            for glyph_text, simple_text in zip(
                text_words,
                simple_words,
            ):
                key = (glyph_text, simple_text)

                if key not in word_map:
                    word_map[key] = Word(
                        glyph_text=glyph_text,
                        simple_text=simple_text,
                    )

        session.add_all(word_map.values())

        await session.flush()

        print(f"Inserted {len(word_map)} unique words")

        # --------------------------------
        # 4. AyahWord
        # --------------------------------

        ayah_words = []

        for verse in verses:
            ayah_id = verse["id"]

            for position, (glyph_text, simple_text) in enumerate(
                zip(
                    verse["text"],
                    verse["simple_text"],
                ),
                start=1,
            ):
                word = word_map[(glyph_text, simple_text)]

                ayah_word = AyahWord(
                    ayah_id=ayah_id,
                    word_id=word.id,
                    position=position,
                )

                ayah_words.append(ayah_word)

        session.add_all(ayah_words)

        await session.flush()

        print(f"Inserted {len(ayah_words)} ayah-word relations")

        # --------------------------------
        # Commit
        # --------------------------------

        await session.commit()

    print()
    print("Database seeding completed successfully.")


async def main():
    await seed_database()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
