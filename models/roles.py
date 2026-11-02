from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship
import uuid

from core.database import Base
from .role_action import role_actions

class Role(Base):
    __tablename__ = "roles"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Logical role code (e.g., "role_editor", "viewer")
    role_code = Column(String(64), nullable=False)

    # NULL indicates a Global Default Role created by a Service Admin
    tenant_id = Column(String(64), nullable=True, index=True)
    name = Column(String(128), nullable=False)

    actions = relationship("Action", secondary=role_actions)

    __table_args__ = (
        UniqueConstraint("tenant_id", "role_code", name="uq_tenant_role_code"),
    )


