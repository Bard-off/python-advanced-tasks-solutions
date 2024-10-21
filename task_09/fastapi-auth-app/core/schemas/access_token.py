from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccessTokenBase(BaseModel):
    token: str
    created_at: datetime


class AccessTokenRead(AccessTokenBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
