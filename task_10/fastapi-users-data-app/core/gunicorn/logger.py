from logging import Formatter

from gunicorn import config  # type: ignore[import-untyped]
from gunicorn.glogging import Logger  # type: ignore[import-untyped]

from core.config import settings


class GunicornLogger(Logger):  # type: ignore[misc]
    def setup(self, cfg: config.Config) -> None:
        super().setup(cfg)

        self._set_handler(
            log=self.access_log,
            output=cfg.accesslog,
            fmt=Formatter(fmt=settings.logging.log_format),
        )
        self._set_handler(
            log=self.error_log,
            output=cfg.errorlog,
            fmt=Formatter(fmt=settings.logging.log_format),
        )
