import logging
from typing import Any

from core.models import (
    Post,
    User,
    UserAddress,
)

log = logging.getLogger(__name__)


def prepare_users_and_addresses(
    users_data: list[dict[str, Any]],
) -> tuple[list[User], list[UserAddress], dict[int, User]]:
    log.info("Preparing users and addresses from data: %s", users_data)
    users: list[User] = []
    addresses: list[UserAddress] = []
    user_ids_to_users: dict[int, User] = {}

    for user_data in users_data:
        user = User(
            name=user_data["name"],
            username=user_data["username"],
            email=user_data["email"],
        )
        users.append(user)
        user_ids_to_users[user_data["id"]] = user
        address = user_data["address"]
        addresses.append(
            UserAddress(
                user=user,
                street=address["street"],
                suite=address["suite"],
                city=address["city"],
                zipcode=address["zipcode"],
            )
        )

    log.info("Prepared users: %s", users)
    log.info("Prepared addresses: %s", addresses)

    return users, addresses, user_ids_to_users


def prepare_posts_models(
    posts_data: list[dict[str, Any]],
    user_ids_to_users: dict[int, User],
) -> list[Post]:
    log.info("Preparing posts from data: %s", posts_data)
    posts = [
        # just take values
        Post(
            user=user_ids_to_users[post["userId"]],
            title=post["title"],
            body=post["body"],
        )
        # for each
        for post in posts_data
    ]
    log.info("Prepared posts: %s", posts)
    return posts
