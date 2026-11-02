from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import uuid

from core.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    key = Column(String(64), nullable=False, unique=True, index=True)
    name = Column(String(128), nullable=False)

    actions = relationship("Action", back_populates="resource", cascade="all, delete-orphan")
