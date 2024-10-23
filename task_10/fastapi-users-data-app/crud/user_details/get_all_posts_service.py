from core.models import Post
from crud.user_details.get_all_objects_base_service import GetAllObjectsBaseService


class GetAllPostsService(GetAllObjectsBaseService[Post]):
    model = Post
