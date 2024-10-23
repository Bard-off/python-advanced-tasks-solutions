from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    id: int
    user_id: int
    title: str
    body: str


class PostRead(PostBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
