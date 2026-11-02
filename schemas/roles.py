from typing import Optional, List
from pydantic import BaseModel, Field


class RoleCreateRequest(BaseModel):
    role_code: str = Field(description="code of role")
    tenant_id: Optional[str] = Field(default=None, description="Provide tenant id to configure tenant specific roles.")
    name: str = Field(description="Name of the role")
    action_ids: List[str] = Field(description="List of action id that the role can do")

class RoleCreateResponse(BaseModel):
    status: str = Field(description="Status of the request")
    role_id: str = Field(description="Id of the new role")
    role_code: str = Field(description="Code of the new role")
    tenant_id: Optional[str] = Field(description="Tenant ID if the role is tenant specific")

class Permission(BaseModel):
    resource_key: str
    action_name: str
    is_public: bool

class RoleResponse(BaseModel):
    id: str
    role_code: str
    name: str
    tenant_id: str
    permissions: List[Permission]


class RoleUserAttachDetachRequest(BaseModel):
    principal_id: str
    tenant_id: str
    role_id: str

class Binding(BaseModel):
    id: str
    principal_id: str
    tenant_id: str
    role_id: str


class RoleUserAttachResponse(BaseModel):
    message: str
    binding: Binding

class RoleUserDetachResponse(BaseModel):
    message: str
