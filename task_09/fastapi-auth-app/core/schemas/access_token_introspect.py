from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccessTokenIntrospect(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    created_at: datetime
    user_id: int
    username: str
