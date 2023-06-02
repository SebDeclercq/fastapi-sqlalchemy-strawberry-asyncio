"""
MAINLY DEVELOPED BY CHATGPT (WHILE TESTING THE TOOL)
"""

import random
from random import randint
from faker import Faker
from rich.progress import track
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)
from .._private.types import AsyncSessionMaker
from ..db.models import Base, File, FileFormat, FileLanguage, Standard

__all__: list[str] = ["random_populate"]


async def _random_populate(
    async_session: AsyncSessionMaker, amount: int, fake: Faker
) -> None:
    async with async_session() as session:
        inserted: int = 0
        for _ in track(range(amount), description="Inserting..."):
            try:
                standard = Standard(
                    numdos=fake.random_letter().upper()
                    + fake.random_letter().upper()
                    + str(random.randint(1, 999999))
                )
                session.add(standard)
                for _ in range(randint(1, 5)):
                    try:
                        file = File(
                            name=fake.file_name(),
                            numdosvl=standard.numdos[0]
                            + random.choice([standard.numdos[1], "E"])
                            + standard.numdos[2:],
                            numdos=standard.numdos,
                            format=random.choice(list(FileFormat)),
                            language=random.choice(list(FileLanguage)),
                        )
                        standard.files.append(file)
                    except:
                        continue
                inserted += 1
                await session.flush()  # Flush to generate primary key IDs
            except:
                continue

        await session.commit()
        count_in_db: int = (
            await session.execute(select(func.count()).select_from(Standard))
        ).scalar() or 0
        print(
            f"{inserted} inserted Standards ({inserted / count_in_db * 100:.2f}% new)."
        )


async def random_populate(db_url: str, amount: int = 10) -> None:
    # Create the async engine and sessionmaker
    engine: AsyncEngine = create_async_engine(db_url)
    async_session: AsyncSessionMaker = async_sessionmaker(engine, class_=AsyncSession)

    # Create an instance of Faker
    fake = Faker()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await _random_populate(async_session, amount, fake)
