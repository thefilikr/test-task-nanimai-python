from fastapi import APIRouter, Depends, HTTPException, Request
from uuid import UUID
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import BalanceRepository
from .service import BalanceService
from .schemas import BalanceRead, BalanceAmountUpdate, BalanceLimitUpdate
from app.transaction.repository import TransactionRepository
from app.transaction.service import TransactionService
from app.utils.auth.depends import get_current_user

router = APIRouter(prefix="/balance", tags=["balance"])

def get_service(session: AsyncSession = Depends(get_async_session)):
    transaction_repo = TransactionRepository(session)
    transaction_service = TransactionService(transaction_repo)
    repo = BalanceRepository(session)
    return BalanceService(repo, transaction_service)

@router.get("/{user_id}", response_model=BalanceRead)
async def get_balance(
    user_id: UUID,
    service: BalanceService = Depends(get_service),
    current_user: dict = Depends(get_current_user)
):
    # Проверка доступа: хозяин или админ
    if str(current_user["id"]) != str(user_id) and not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Access denied")
    balance = await service.get_balance(user_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    return balance

@router.patch("/{user_id}/amount", response_model=BalanceRead)
async def update_balance_amount(
    user_id: UUID,
    data: BalanceAmountUpdate,
    service: BalanceService = Depends(get_service),
    current_user: dict = Depends(get_current_user)
):
    # Только хозяин может менять amount
    if str(current_user["id"]) != str(user_id):
        raise HTTPException(status_code=403, detail="Only owner can change amount")
    balance = await service.change_balance(user_id, data.amount)
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    if isinstance(balance, dict) and balance.get("error"):
        raise HTTPException(status_code=409, detail=balance["error"])
    return balance

@router.post("/{user_id}/transaction", response_model=dict)
async def open_balance_transaction(
    user_id: UUID,
    data: BalanceAmountUpdate,
    service: BalanceService = Depends(get_service)
):
    result = await service.open_balance_transaction(user_id, float(data.amount), operation_type="reserve")
    if not result or (isinstance(result, dict) and result.get("error")):
        raise HTTPException(status_code=409, detail=result.get("error", "Unknown error"))
    return {"transaction_id": str(result.id)}

@router.post("/transaction/{transaction_id}/confirm", response_model=BalanceRead)
async def confirm_balance_transaction(
    transaction_id: UUID,
    service: BalanceService = Depends(get_service)
):
    result = await service.confirm_balance_transaction(transaction_id)
    if not result or (isinstance(result, dict) and result.get("error")):
        raise HTTPException(status_code=409, detail=result.get("error", "Unknown error"))
    return result

@router.post("/transaction/{transaction_id}/cancel", response_model=dict)
async def cancel_balance_transaction(
    transaction_id: UUID,
    service: BalanceService = Depends(get_service)
):
    result = await service.cancel_balance_transaction(transaction_id)
    if not result or (isinstance(result, dict) and result.get("error")):
        raise HTTPException(status_code=409, detail=result.get("error", "Unknown error"))
    return result

@router.patch("/{user_id}/limit", response_model=BalanceRead)
async def update_balance_limit(
    user_id: UUID,
    data: BalanceLimitUpdate,
    service: BalanceService = Depends(get_service),
    current_user: dict = Depends(get_current_user)
):
    # Хозяин и админ могут менять лимит
    if str(current_user["id"]) != str(user_id) and not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Only owner or admin can change limit")
    balance = await service.change_limit(user_id, float(data.limit))
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    if isinstance(balance, dict) and balance.get("error"):
        raise HTTPException(status_code=409, detail=balance["error"])
    return balance