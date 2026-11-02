from sqlalchemy import Table, Column, ForeignKey, String
from core.database import Base


# Many-to-Many link between roles & actions
role_actions = Table(
    "role_actions",
    Base.metadata,
    Column("role_id", String(36), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("action_id", String(36), ForeignKey("actions.id", ondelete="CASCADE"), primary_key=True)
)

