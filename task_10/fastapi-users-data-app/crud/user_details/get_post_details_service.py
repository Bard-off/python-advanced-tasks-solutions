from core.models import Post
from crud.user_details.get_object_details_service import GetObjectDetailsService


class GetPostDetailsService(GetObjectDetailsService[Post]):
    model = Post
