import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import TypeVar

from app import config
from app.models import User, UserAddress, Post

log = logging.getLogger(__name__)

T = TypeVar("T", User, UserAddress, Post)


@dataclass
class DataSaver[T]:
    data_dir: Path
    filename_pattern: str
    filename_data_key: str = "id"

    dump_ensure_ascii: bool = False
    dump_indent: int | None = 2
    dump_sort_keys: bool = True

    def __post_init__(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save(self, item: T) -> None:
        filename = self.filename_pattern.format(
            **{
                self.filename_data_key: getattr(item, self.filename_data_key),
            },
        )
        filepath = self.data_dir / filename
        log.info("Write data to %s/%s", self.data_dir.name, filename)
        with filepath.open(mode="w") as file:
            json.dump(
                asdict(item),
                file,
                ensure_ascii=self.dump_ensure_ascii,
                indent=self.dump_indent,
                sort_keys=self.dump_sort_keys,
            )

        log.info("Saved data to %s/%s", self.data_dir.name, filename)


user_saver = DataSaver[User](
    data_dir=config.USERS_DATA_DIR,
    filename_pattern="user-{id:02d}.json",
)
address_saver = DataSaver[UserAddress](
    data_dir=config.ADDRESSES_DATA_DIR,
    filename_pattern="address-user-{user_id:02d}.json",
    filename_data_key="user_id",
)
post_saver = DataSaver[Post](
    data_dir=config.POSTS_DATA_DIR,
    filename_pattern="post-{id:03d}.json",
)
