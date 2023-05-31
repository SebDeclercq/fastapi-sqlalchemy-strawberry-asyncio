"""
MAINLY DEVELOPED BY CHATGPT (WHILE TESTING THE TOOL)
"""

import asyncio
import os
import random
import sys
from random import randint
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import selectinload
from standards.db.models import Base, Standard, File


async def populate_data(async_session: AsyncSession, fake: Faker) -> None:
    async with async_session() as session:
        # Create 10 standards
        for _ in range(10):
            standard = Standard(
                numdos=fake.unique.random_letter().upper()
                + fake.unique.random_letter().upper()
                + str(random.randint(1, 999999))
            )
            session.add(standard)

        await session.flush()  # Flush to generate primary key IDs

        # Create files associated with each standard
        standards = await session.execute(
            select(Standard).options(selectinload(Standard.files)).filter()
        )
        for standard in standards.scalars():
            num_files = randint(1, 5)
            for _ in range(num_files):
                file = File(
                    name=fake.file_name(),
                    numdosvl=standard.numdos[0]
                    + str(fake.random_number(digits=6))
                    + standard.numdos[2:],
                    numdos=standard.numdos,
                )
                standard.files.append(file)

        await session.commit()


async def main():
    # Configure your database URL
    try:
        database_url: str = sys.argv[1]
    except IndexError:
        database_url = os.getenv("DB_URL", "sqlite+aiosqlite://")

    # Create the async engine and sessionmaker
    engine = create_async_engine(database_url)
    async_session = async_sessionmaker(engine, class_=AsyncSession)

    # Create an instance of Faker
    fake = Faker()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await populate_data(async_session, fake)


# Run the async script
if __name__ == "__main__":
    asyncio.run(main())
