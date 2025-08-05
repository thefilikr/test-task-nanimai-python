from typing import Any, Optional
from uuid import UUID
from .interface import IUserService, IUserRepository

class UserService(IUserService):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def create_user(self, email: str) -> Any:
        return await self.repository.create(email)

    async def get_user(self, user_id: UUID) -> Any:
        return await self.repository.get_by_id(user_id)