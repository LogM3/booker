from app.core.repos import BaseRepo
from app.users.models import User


class UserRepo(BaseRepo[User]):
    model = User

    @classmethod
    async def get_user_by_email(cls, email: str) -> User | None:
        return await cls.get_one_or_none(email=email)
