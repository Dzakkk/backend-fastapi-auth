import uuid
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from ..config.connection_db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telephone = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer, unique=False, nullable=True)
    address = Column(Text, unique=False, nullable=True)