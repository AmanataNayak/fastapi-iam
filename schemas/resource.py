from typing import List

from pydantic import BaseModel, Field

class ActionCreate(BaseModel):
    name: str = Field(description="Action name relative to resource")
    is_public: bool = Field(default=False, description="Whether action bypasses IAM role evaluation")

class ActionSchema(BaseModel):
     name: str = Field(description="Name of the action")
     is_public: bool = Field(description="Whether action bypasses IAM role evaluation")


class ResourceCreateRequest(BaseModel):
    name: str = Field(description="Human readable display title")
    key: str = Field(description="Machine identifier used in route matching")
    actions: List[ActionCreate]

class ResourceCreateResponse(BaseModel):
    status: str = Field(description="Status of the request")
    resource_id: str = Field(description="ID of the resource")
    actions: List[str] = Field(description="List of actions that are linked with it")


class ResourceSchema(BaseModel):
    id: str = Field(description="ID of the resource")
    name: str = Field(description="Name to show in the UI")
    key: str = Field(description="Raw value of name")
    actions: List[ActionSchema] = Field(description="Name of the actions that allowed here")
