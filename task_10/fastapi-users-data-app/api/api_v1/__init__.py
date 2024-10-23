from fastapi import APIRouter

from core.config import settings

from .posts import router as posts_router
from .user_posts import router as user_posts_router
from .users import router as users_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(users_router, tags=["Users"])
router.include_router(posts_router, tags=["Posts"])
router.include_router(user_posts_router, tags=["Posts"])
