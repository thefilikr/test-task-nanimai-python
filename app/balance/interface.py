from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class IBalanceRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Any:
        pass

    @abstractmethod
    async def update_amount(self, user_id: UUID, amount: float) -> Any:
        pass

    @abstractmethod
    async def update_limit(self, user_id: UUID, limit: float) -> Any:
        pass

class IBalanceService(ABC):
    @abstractmethod
    async def get_balance(self, user_id: UUID) -> Any:
        pass

    @abstractmethod
    async def change_balance(self, user_id: UUID, amount: float) -> Any:
        pass

    @abstractmethod
    async def change_limit(self, user_id: UUID, limit: float) -> Any:
        pass