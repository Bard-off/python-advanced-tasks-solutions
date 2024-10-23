from pydantic import BaseModel, ConfigDict

from .user_address import UserAddressRead


class UserBase(BaseModel):
    id: int
    name: str


class UserMinimalDetailsBase(UserBase):
    """
    User details for anon access
    """


class UserMinimalDetails(UserMinimalDetailsBase):
    model_config = ConfigDict(
        from_attributes=True,
    )


class UserPublicDetailsBase(UserBase):
    """
    User details for authorized access
    """

    username: str


class UserPublicDetails(UserPublicDetailsBase):
    model_config = ConfigDict(
        from_attributes=True,
    )


class UserPrivateDetailsBase(UserPublicDetailsBase):
    """
    User details for self access
    """

    email: str


class UserPrivateDetails(UserPrivateDetailsBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    address: UserAddressRead
