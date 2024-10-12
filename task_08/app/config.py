import logging
from pathlib import Path

USERS_API = "https://jsonplaceholder.typicode.com/users"
POSTS_API = "https://jsonplaceholder.typicode.com/posts"


APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
USERS_DATA_DIR = DATA_DIR / "users"
ADDRESSES_DATA_DIR = DATA_DIR / "addresses"
POSTS_DATA_DIR = DATA_DIR / "posts"

DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)14s:%(lineno)d %(levelname)-8s - %(message)s"
)


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format=DEFAULT_FORMAT,
    )
