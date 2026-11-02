from sqlalchemy import Column, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import uuid

from core.database import Base

class Action(Base):
    __tablename__ = "actions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    resource_id = Column(String(36), ForeignKey("resources.id", ondelete="CASCADE"), nullable=False)

    # Action key relative to resource (e.g., "read", "write", "*")
    name = Column(String(64), nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)

    resource = relationship("Resource", back_populates="actions")

    __table_args__ = (
        UniqueConstraint("resource_id", "name", name="uq_resource_action"),
    )