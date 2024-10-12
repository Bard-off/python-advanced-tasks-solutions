import logging
from concurrent.futures import ThreadPoolExecutor

import config
from app.prepare_models import (
    prepare_posts_models,
    prepare_users_and_addresses,
)
from app.save_data import (
    address_saver,
    post_saver,
    user_saver,
)
from fetch_data import (
    fetch_posts,
    fetch_users,
)

log = logging.getLogger(__name__)


def main():
    config.configure_logging()
    log.warning("Starting...")

    log.info("Fetch data from API")
    # IO-bound tasks: read API
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_posts_data = executor.submit(fetch_posts)
        future_users_data = executor.submit(fetch_users)

    log.info("Prepare models")
    # CPU-bound tasks: prepare models
    posts = prepare_posts_models(future_posts_data.result())
    users, addresses = prepare_users_and_addresses(future_users_data.result())

    log.info("Write data to disk")
    # IO-bound tasks: write data to disk
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(user_saver.save, users)
        executor.map(address_saver.save, addresses)
        executor.map(post_saver.save, posts)

    log.warning("Done. Bye!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
