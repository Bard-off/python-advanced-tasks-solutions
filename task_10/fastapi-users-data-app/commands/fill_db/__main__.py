import asyncio
import logging

from commands.fill_db.load_and_save_data import fill_db
from core.config import settings


def main() -> None:
    logging.basicConfig(
        level=logging.getLevelNamesMapping()[settings.logging.log_level],
        format=settings.logging.log_format,
    )
    asyncio.run(fill_db())


if __name__ == "__main__":
    main()
