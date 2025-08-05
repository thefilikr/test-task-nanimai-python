from typing import Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Balance
from .interface import IBalanceRepository

class BalanceRepository(IBalanceRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: UUID) -> Optional[Balance]:
        result = await self.session.execute(select(Balance).where(Balance.user_id == user_id))
        return result.scalar_one_or_none()

    async def update_amount(self, user_id: UUID, amount: float) -> Optional[Balance]:
        balance = await self.get_by_user_id(user_id)
        if balance:
            balance.amount = amount
            await self.session.flush()
        return balance

    async def update_limit(self, user_id: UUID, limit: float) -> Optional[Balance]:
        balance = await self.get_by_user_id(user_id)
        if balance:
            balance.limit = limit
            await self.session.flush()
        return balance

    # С одной стороны класскное решение - сделать обёртку. Но не думаю, что рабочее. Т.к. в реале 
    # скорее всего логика изоляции будет прописываться отлдельно в каждом из запросов. Но здесь 
    # думаю это хорошее решение.
    async def safe_update(self, update_func, *args, isolation_level: str = "SERIALIZABLE", **kwargs):
        from sqlalchemy.exc import OperationalError
        try:
            async with self.session.begin():
                await self.session.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")
                return await update_func(*args, **kwargs)
        except OperationalError as e:
            # Здесь можно реализовать повтор попытки или возврат ошибки
            raise