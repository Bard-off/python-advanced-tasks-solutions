from core.models import User
from crud.user_details.get_all_objects_base_service import GetAllObjectsBaseService


class GetAllUsersService(GetAllObjectsBaseService[User]):
    model = User
