"""
Based on https://github.com/tough-dev-school/education-backend/blob/master/src/core/services.py
"""

from abc import ABC, abstractmethod
from collections.abc import (
    Callable,
    Coroutine,
    Sequence,
)
from typing import (
    Generic,
    TypeVar,
)

ReturnType = TypeVar("ReturnType")


class BaseService(ABC, Generic[ReturnType]):
    """
    This is a template of a base service.
    All services in the app should follow this rules:
      * Input variables should be done at the __init__ phase
      * Service should implement a single entrypoint without arguments

    Usage example:
    @dataclass
    class UserCreator(BaseService):
        first_name: str
        last_name: str | None

        def act(self) -> User:
            return User.objects.create(first_name=self.first_name, last_name=self.last_name)

    user_creator = UserCreator(first_name="Ivan", last_name="Petrov")
    user = user_creator()


    This is not ok, such usage is prohibited:
    class UserCreator:
        def __call__(self, first_name: str, last_name: str | None) -> User:
            return User.objects.create(first_name=self.first_name, last_name=self.last_name)

    ---

    Example for get_validators usage:

    @dataclass
    class UserUpdater(BaseService):
        ...

        def validate_username(self): ...
        def validate_email(self): ...

        def get_validators(self) -> list:
            return [
                self.validate_username,
                self.validate_email,
            ]

    """

    # noinspection PyMethodMayBeStatic
    def get_validators(self) -> Sequence[Callable[[], Coroutine[None, None, None]]]:
        return []

    async def __call__(self) -> ReturnType:
        await self.validate()
        return await self.act()

    async def validate(self) -> None:
        for validator in self.get_validators():
            await validator()

    @abstractmethod
    async def act(self) -> ReturnType:
        raise NotImplementedError("Please implement act method in your service class")
