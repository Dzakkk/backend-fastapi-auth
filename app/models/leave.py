import uuid
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from ..config.connection_db import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from .user import User
class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    reason = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String, default="Pending")

    user = relationship("User", back_populates="leave_requests")