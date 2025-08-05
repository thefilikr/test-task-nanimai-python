from typing import Any, Optional
from uuid import UUID
from app.transaction.service import TransactionService
from app.transaction.models import TransactionStatus
from .interface import IBalanceService, IBalanceRepository

class BalanceService(IBalanceService):
    def __init__(self, repository: IBalanceRepository, transaction_service: TransactionService):
        self.repository = repository
        self.transaction_service = transaction_service

    async def get_balance(self, user_id: UUID) -> Any:
        return await self.repository.get_by_user_id(user_id)

    async def open_balance_transaction(
        self, user_id: UUID, amount: float, operation_type: str, initiator_id: Optional[UUID] = None
    ):
        """
        Открыть транзакцию на блокировку средств (pending).
        Проверяет, что достаточно доступных средств, и блокирует их.
        """
        balance = await self.repository.get_by_user_id(user_id)
        if not balance:
            return None

        # Сумма всех pending транзакций пользователя
        locked = await self.transaction_service.get_locked_amount(user_id)
        available = float(balance.amount) - locked

        if amount > available or amount <= 0:
            # Вообще, я обычно пишу тект ошибки исключительно на английском. 
            # Но тут решил для скорости и удобства отойти от этой привычки. 
            return {"error": "Недостаточно доступных средств или некорректная сумма"}

        # Создать транзакцию (pending)
        transaction = await self.transaction_service.open_transaction(
            user_id=user_id,
            amount=amount,
            operation_type=operation_type,
            initiator_id=initiator_id
        )
        return transaction

    async def confirm_balance_transaction(self, transaction_id: UUID) -> Any:
        """
        Подтвердить транзакцию: списать средства и изменить статус транзакции на confirmed.
        """
        transaction = await self.transaction_service.get_by_id(transaction_id)
        if not transaction or transaction.status != TransactionStatus.pending:
            return {"error": "Транзакция не найдена или уже обработана"}

        # Проверка таймаута
        if await self.transaction_service.is_timeout(transaction):
            await self.transaction_service.cancel_transaction(transaction_id)
            return {"error": "Транзакция просрочена и отменена"}

        # Списать средства и подтвердить транзакцию атомарно
        async with self.repository.session.begin():
            await self.repository.session.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
            balance = await self.repository.get_by_user_id(transaction.user_id)
            locked = await self.transaction_service.get_locked_amount(transaction.user_id, exclude_id=transaction_id)
            available = float(balance.amount) - locked

            if transaction.amount > available or balance is None:
                await self.transaction_service.cancel_transaction(transaction_id)
                return {"error": "Недостаточно средств для подтверждения транзакции"}

            balance.amount -= transaction.amount
            await self.repository.session.flush()
            await self.transaction_service.confirm_transaction(transaction_id)
        return balance

    async def cancel_balance_transaction(self, transaction_id: UUID) -> Any:
        """
        Отменить транзакцию: разблокировать средства.
        """
        transaction = await self.transaction_service.get_by_id(transaction_id)
        if not transaction or transaction.status != TransactionStatus.pending:
            return {"error": "Транзакция не найдена или уже обработана"}
        await self.transaction_service.cancel_transaction(transaction_id)
        return {"result": "Транзакция отменена"}

    async def change_limit(self, user_id: UUID, new_limit: float) -> Any:
        """
        Изменить лимит баланса. Проверяет, что лимит >= текущий баланс + заблокированные средства.
        """
        balance = await self.repository.get_by_user_id(user_id)
        if not balance:
            return None

        locked = await self.transaction_service.get_locked_amount(user_id)
        if new_limit < float(balance.amount) + locked or new_limit < 0:
            return {"error": "Лимит не может быть меньше суммы текущего баланса и заблокированных средств"}

        balance.limit = new_limit
        await self.repository.session.flush()
        return balance

    async def change_balance_direct(self, user_id: UUID, amount: float) -> Any:
        """
        Атомарное изменение баланса (без транзакции, только для внутренних нужд или тестов).
        """
        balance = await self.repository.get_by_user_id(user_id)
        if not balance:
            return None
        locked = await self.transaction_service.get_locked_amount(user_id)
        if amount < 0 or amount + locked > float(balance.limit):
            return {"error": "Баланс не может быть меньше нуля или превышать лимит с учетом блокировок"}
        balance.amount = amount
        await self.repository.session.flush()
        return balance