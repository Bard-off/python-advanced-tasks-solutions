from pydantic import BaseModel, ConfigDict


class UserAddressBase(BaseModel):
    id: int
    user_id: int
    street: str
    suite: str
    city: str
    zipcode: str


class UserAddressRead(UserAddressBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
