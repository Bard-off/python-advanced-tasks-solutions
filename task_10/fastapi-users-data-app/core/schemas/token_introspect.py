from datetime import datetime

from pydantic import BaseModel


class TokenIntrospect(BaseModel):
    created_at: datetime
    user_id: int
    username: str
