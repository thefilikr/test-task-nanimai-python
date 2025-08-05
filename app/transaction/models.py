from sqlalchemy import Column, ForeignKey, Numeric, DateTime, String, Enum, func, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base
import enum

class TransactionStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Numeric(18, 2), nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False, index=True)
    operation_type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="transactions")

    __table_args__ = (
        Index("ix_transactions_user_id_status", "user_id", "status"),
    )