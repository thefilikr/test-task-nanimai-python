from celery import Celery
from app.db.session import AsyncSessionLocal
from app.transaction.models import Transaction, TransactionStatus
from app.transaction.repository import TransactionRepository
from app.transaction.service import TransactionService
from sqlalchemy.future import select
from datetime import datetime, timedelta

celery_app = Celery("tasks", broker="redis://localhost:6379/0")

@celery_app.task
def process_balance_timeouts():
    import asyncio

    async def _process():
        async with AsyncSessionLocal() as session:
            repo = TransactionRepository(session)
            service = TransactionService(repo)
            await service.process_timeouts(session=session, timeout_minutes=10)

    asyncio.run(_process())