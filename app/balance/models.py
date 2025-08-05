from sqlalchemy import Column, ForeignKey, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

class Balance(Base):
    __tablename__ = "balances"

    # Везде прописал UUID вместо числовых id, т.к. подразумевается, что это один из микросервисов. 
    # А в таикх случаях лучшен использовать UUID для более удобной стыковки данных
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Numeric(18, 2), nullable=False, default=0)
    limit = Column(Numeric(18, 2), nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="balances")