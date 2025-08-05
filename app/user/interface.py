from abc import ABC, abstractmethod
from typing import Protocol, Any
from uuid import UUID

class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Any:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Any:
        pass

    @abstractmethod
    async def create(self, email: str) -> Any:
        pass

class IUserService(ABC):
    @abstractmethod
    async def create_user(self, email: str) -> Any:
        pass

    @abstractmethod
    async def get_user(self, user_id: UUID) -> Any:
        pass