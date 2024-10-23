from core.models import User
from crud.user_details.get_object_details_service import GetObjectDetailsService


class GetUserDetailsService(GetObjectDetailsService[User]):
    model = User
