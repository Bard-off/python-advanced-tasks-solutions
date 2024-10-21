from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserRegister(UserBase):
    password: str


class UserLogin(UserRegister):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
