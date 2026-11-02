from sqlalchemy import Column, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
import uuid

class PrincipalRoleBinding(Base):
    __tablename__ = "principal_role_bindings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    principal_id = Column(String(64), nullable=False, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    role_id = Column(String(36), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    role = relationship("Role")

    __table_args__ = (
        UniqueConstraint("principal_id", "tenant_id", "role_id", name="uq_principal_tenant_role"),
    )
