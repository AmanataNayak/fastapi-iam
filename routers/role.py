from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_

from core.database import get_db
from schemas import RoleCreateResponse, RoleCreateRequest, RoleResponse, RoleUserAttachResponse, RoleUserAttachDetachRequest, RoleUserDetachResponse
from services import create_role as service_create_role, get_role_permission, attach_role, detach_role

roles_routers = APIRouter(prefix='/roles')

@roles_routers.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RoleCreateResponse
)
async def create_role(request: RoleCreateRequest, db: AsyncSession = Depends(get_db)):
    return await service_create_role(request, db)


@roles_routers.get(
    '/{role_id}',
    status_code=status.HTTP_200_OK,
    response_model=RoleResponse
)
async def get_role(role_id: str, db: AsyncSession = Depends(get_db)):
    return await get_role_permission(role_id, db)

@roles_routers.post(
    '/attach',
    status_code=status.HTTP_201_CREATED,
    response_model=RoleUserAttachResponse
)
async def attach(request: RoleUserAttachDetachRequest, db: AsyncSession = Depends(get_db)):
    return await attach_role(request, db)


@roles_routers.delete(
    "/detach",
    status_code=status.HTTP_204_NO_CONTENT
)
async def detach(request: RoleUserAttachDetachRequest, db: AsyncSession = Depends(get_db)):
    return await detach_role(request, db)
