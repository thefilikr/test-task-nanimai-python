from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal

class BalanceRead(BaseModel):
    id: UUID
    user_id: UUID
    amount: Decimal
    limit: Decimal

    class Config:
        orm_mode = True

class BalanceAmountUpdate(BaseModel):
    amount: Decimal

class BalanceLimitUpdate(BaseModel):
    limit: Decimal