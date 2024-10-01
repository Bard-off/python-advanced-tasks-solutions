import logging

from aiohttp import web

from app import app
from core.config import CACHE_DIR, configure_logging

log = logging.getLogger(__name__)


def main() -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    configure_logging()
    web.run_app(app)


if __name__ == "__main__":
    main()
