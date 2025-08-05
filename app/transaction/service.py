from typing import Any, Optional
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.future import select
from .models import Transaction, TransactionStatus
from .interface import ITransactionService, ITransactionRepository

class TransactionService(ITransactionService):
    def __init__(self, repository: ITransactionRepository):
        self.repository = repository

    async def open_transaction(self, user_id: UUID, amount: float, operation_type: str, initiator_id: Optional[UUID] = None) -> Transaction:
        return await self.repository.create(user_id, amount, operation_type, initiator_id)

    async def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        return await self.repository.get_by_id(transaction_id)

    async def confirm_transaction(self, transaction_id: UUID) -> Any:
        return await self.repository.update_status(transaction_id, TransactionStatus.confirmed)

    async def cancel_transaction(self, transaction_id: UUID) -> Any:
        return await self.repository.update_status(transaction_id, TransactionStatus.canceled)

    async def get_locked_amount(self, user_id: UUID, exclude_id: Optional[UUID] = None) -> float:
        """
        Сумма всех pending транзакций пользователя (кроме exclude_id).
        """
        transactions = await self.repository.get_pending_by_user(user_id)
        total = 0.0
        for tx in transactions:
            if exclude_id and tx.id == exclude_id:
                continue
            total += float(tx.amount)
        return total

    async def is_timeout(self, transaction: Transaction, timeout_minutes: int = 60) -> bool:
        """
        Проверяет, истёк ли таймаут транзакции.
        """
        if not transaction.created_at:
            return True
        return (datetime.utcnow() - transaction.created_at) > timedelta(minutes=timeout_minutes)

    async def process_timeouts(self, session=None, timeout_minutes: int = 60) -> None:
        """
        Находит и отменяет все зависшие (pending и просроченные) транзакции.
        Может вызываться как из Celery, так и вручную.
        """
        # Если session не передан, используем self.repository.session (для ручного вызова)
        session = session or getattr(self.repository, "session", None)
        if session is None:
            raise RuntimeError("AsyncSession is required for processing timeouts")

        timeout_time = datetime.utcnow() - timedelta(minutes=timeout_minutes)
        result = await session.execute(
            select(Transaction).where(
                Transaction.status == TransactionStatus.pending,
                Transaction.created_at < timeout_time
            )
        )
        for tx in result.scalars():
            tx.status = TransactionStatus.canceled
        await session.commit()

