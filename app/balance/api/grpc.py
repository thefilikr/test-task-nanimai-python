import grpc
from concurrent import futures
from uuid import UUID

from app.db.session import AsyncSessionLocal
from app.balance.repository import BalanceRepository
from app.balance.service import BalanceService
from app.transaction.repository import TransactionRepository
from app.transaction.service import TransactionService

import proto.balance_pb2 as pb2
import proto.balance_pb2_grpc as pb2_grpc

import asyncio

class BalanceServiceGRPC(pb2_grpc.BalanceServiceServicer):
    async def _get_service(self):
        session = AsyncSessionLocal()
        transaction_repo = TransactionRepository(session)
        transaction_service = TransactionService(transaction_repo)
        repo = BalanceRepository(session)
        return BalanceService(repo, transaction_service), session

    async def GetBalance(self, request, context):
        service, session = await self._get_service()
        try:
            balance = await service.get_balance(UUID(request.user_id))
            if not balance:
                return pb2.BalanceResponse(error="Balance not found")
            return pb2.BalanceResponse(
                id=str(balance.id),
                user_id=str(balance.user_id),
                amount=float(balance.amount),
                limit=float(balance.limit),
            )
        finally:
            await session.close()

    async def OpenBalanceTransaction(self, request, context):
        service, session = await self._get_service()
        try:
            result = await service.open_balance_transaction(
                UUID(request.user_id), request.amount, request.operation_type
            )
            if not result or (isinstance(result, dict) and result.get("error")):
                return pb2.TransactionResponse(error=result.get("error", "Unknown error"))
            return pb2.TransactionResponse(transaction_id=str(result.id))
        finally:
            await session.close()

    async def ConfirmBalanceTransaction(self, request, context):
        service, session = await self._get_service()
        try:
            result = await service.confirm_balance_transaction(UUID(request.transaction_id))
            if not result or (isinstance(result, dict) and result.get("error")):
                return pb2.BalanceResponse(error=result.get("error", "Unknown error"))
            return pb2.BalanceResponse(
                id=str(result.id),
                user_id=str(result.user_id),
                amount=float(result.amount),
                limit=float(result.limit),
            )
        finally:
            await session.close()

    async def CancelBalanceTransaction(self, request, context):
        service, session = await self._get_service()
        try:
            result = await service.cancel_balance_transaction(UUID(request.transaction_id))
            if not result or (isinstance(result, dict) and result.get("error")):
                return pb2.CancelResponse(error=result.get("error", "Unknown error"))
            return pb2.CancelResponse(result="Транзакция отменена")
        finally:
            await session.close()

    async def UpdateBalanceLimit(self, request, context):
        service, session = await self._get_service()
        try:
            balance = await service.change_limit(UUID(request.user_id), request.limit)
            if not balance:
                return pb2.BalanceResponse(error="Balance not found")
            if isinstance(balance, dict) and balance.get("error"):
                return pb2.BalanceResponse(error=balance["error"])
            return pb2.BalanceResponse(
                id=str(balance.id),
                user_id=str(balance.user_id),
                amount=float(balance.amount),
                limit=float(balance.limit),
            )
        finally:
            await session.close()

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_BalanceServiceServicer_to_server(BalanceServiceGRPC(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())