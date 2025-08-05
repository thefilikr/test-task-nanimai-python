from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class ITransactionRepository(ABC):
    @abstractmethod
    async def create(self, user_id: UUID, amount: float, operation_type: str) -> Any:
        pass

    @abstractmethod
    async def get_by_id(self, transaction_id: UUID) -> Any:
        pass

    @abstractmethod
    async def update_status(self, transaction_id: UUID, status: str) -> Any:
        pass

class ITransactionService(ABC):
    @abstractmethod
    async def open_transaction(self, user_id: UUID, amount: float, operation_type: str) -> Any:
        pass

    @abstractmethod
    async def confirm_transaction(self, transaction_id: UUID) -> Any:
        pass

    @abstractmethod
    async def cancel_transaction(self, transaction_id: UUID) -> Any:
        pass

    @abstractmethod
    async def process_timeouts(self) -> None:
        pass