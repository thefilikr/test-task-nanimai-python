from typing import Any, Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Transaction, TransactionStatus
from .interface import ITransactionRepository

class TransactionRepository(ITransactionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, amount: float, operation_type: str, initiator_id: Optional[UUID] = None) -> Transaction:
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            status=TransactionStatus.pending,
            operation_type=operation_type,
            initiator_id=initiator_id
        )
        self.session.add(transaction)
        await self.session.flush()
        return transaction

    async def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        result = await self.session.execute(select(Transaction).where(Transaction.id == transaction_id))
        return result.scalar_one_or_none()

    async def update_status(self, transaction_id: UUID, status: TransactionStatus) -> Optional[Transaction]:
        transaction = await self.get_by_id(transaction_id)
        if transaction:
            transaction.status = status
            await self.session.flush()
        return transaction

    async def get_pending_by_user(self, user_id: UUID) -> List[Transaction]:
        result = await self.session.execute(
            select(Transaction).where(
                Transaction.user_id == user_id,
                Transaction.status == TransactionStatus.pending
            )
        )
        return result.scalars().all()