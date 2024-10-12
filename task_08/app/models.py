from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    name: str
    username: str
    email: str


@dataclass(frozen=True)
class UserAddress:
    user_id: int
    street: str
    suite: str
    city: str
    zipcode: str


@dataclass(frozen=True)
class Post:
    id: int
    user_id: int
    title: str
    body: str
