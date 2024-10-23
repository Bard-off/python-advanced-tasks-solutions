from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.config import settings
from core.models import Post
from core.schemas.post import PostRead
from crud.user_details.get_all_posts_service import GetAllPostsService
from crud.user_details.get_post_details_service import GetPostDetailsService

router = APIRouter(
    prefix=settings.api.v1.posts,
)


@router.get("", response_model=list[PostRead])
async def get_posts_view(
    get_posts: Annotated[
        GetAllPostsService,
        Depends(GetAllPostsService),
    ],
) -> list[Post]:
    return await get_posts()


@router.get("/{id}", response_model=PostRead)
async def get_post_details_view(
    get_post: Annotated[
        GetPostDetailsService,
        Depends(GetPostDetailsService),
    ],
) -> Post:
    post = await get_post()
    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post #{get_post.object_id} not found",
    )
