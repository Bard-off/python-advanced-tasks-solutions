import logging
from typing import Any

from app.models import Post, User, UserAddress

log = logging.getLogger(__name__)


def prepare_posts_models(posts_data: list[dict[str, Any]]) -> list[Post]:
    log.info("Preparing posts from data: %s", posts_data)
    posts = [
        # just take values
        Post(
            id=post["id"],
            user_id=post["userId"],
            title=post["title"],
            body=post["body"],
        )
        # for each
        for post in posts_data
    ]
    log.info("Prepared posts: %s", posts)
    return posts


def prepare_users_and_addresses(
    users_data: list[dict[str, Any]]
) -> tuple[list[User], list[UserAddress]]:
    log.info("Preparing users and addresses from data: %s", users_data)
    users: list[User] = []
    addresses: list[UserAddress] = []

    for user in users_data:
        users.append(
            User(
                id=user["id"],
                name=user["name"],
                username=user["username"],
                email=user["email"],
            )
        )
        address = user["address"]
        addresses.append(
            UserAddress(
                user_id=user["id"],
                street=address["street"],
                suite=address["suite"],
                city=address["city"],
                zipcode=address["zipcode"],
            )
        )

    log.info("Prepared users: %s", users)
    log.info("Prepared addresses: %s", addresses)

    return users, addresses
