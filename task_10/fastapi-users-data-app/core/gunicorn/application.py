from typing import Any

from fastapi import FastAPI
from gunicorn.app.base import BaseApplication  # type: ignore[import-untyped]


class Application(BaseApplication):  # type: ignore[misc]
    def __init__(
        self,
        application: FastAPI,
        options: dict[str, Any] | None = None,
    ) -> None:
        self.options = options or {}
        self.application = application
        super().__init__()

    def load(self) -> FastAPI:
        return self.application

    @property
    def config_options(self) -> dict[str, Any]:
        return {
            # pair
            k: v
            # for each option
            for k, v in self.options.items()
            # not empty key / value
            if k in self.cfg.settings and v is not None
        }

    def load_config(self) -> None:
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)
