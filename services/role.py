from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from models import Role, Action, PrincipalRoleBinding
from schemas import RoleCreateRequest, RoleCreateResponse, RoleResponse, Permission, RoleUserAttachResponse, RoleUserAttachDetachRequest, Binding
from core.constants import StatusConstants

async def create_role(data: RoleCreateRequest, db: AsyncSession) -> RoleCreateResponse:
    if data.tenant_id:
        tenant_cond = Role.tenant_id == data.tenant_id
    else:
        tenant_cond = Role.tenant_id.is_(None)

    stmt = select(Role).where(tenant_cond, Role.role_code == data.role_code )
    existing = await db.execute(stmt)

    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Role role_code: {data.role_code} exists for tenant_id: {data.tenant_id if data.tenant_id else 'Global'}."
        )

    # Fetch action_ids
    action_stmt = select(Action).where(Action.id.in_(data.action_ids))
    result = await db.execute(action_stmt)
    action_objs = result.scalars().all()

    if len(action_objs) != len(set(data.action_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more provided action_ids are invalid or do not exist."
        )

    role = Role(
        role_code=data.role_code,
        tenant_id=data.tenant_id,
        name=data.name,
        actions=action_objs
    )

    db.add(role)
    await db.commit()
    await db.refresh(role)

    return RoleCreateResponse(
        status=StatusConstants.SUCCESS,
        role_code=role.role_code,
        role_id=role.id,
        tenant_id=role.tenant_id
    )


async def get_role_permission(role_id: str, db: AsyncSession) -> RoleResponse:
    stmt = select(Role).options(selectinload(Role.actions).selectinload(Action.resource)).where(Role.id == role_id)
    role = await db.execute(stmt)
    role = role.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID '{role_id}' not found."
        )
    permissions = []
    for action in role.actions:
        permissions.append(Permission(
            resource_key=action.resource.key,
            action_name=action.name,
            is_public=action.is_public
        ))

    return RoleResponse(
        id=role.id,
        role_code=role.role_code,
        name=role.name,
        tenant_id=role.tenant_id,
        permissions=permissions
    )


async def attach_role(data: RoleUserAttachDetachRequest, db: AsyncSession) -> RoleUserAttachResponse:
    role_stmt = select(Role).where(Role.id == data.role_id)
    existing = await db.execute(role_stmt)
    role = existing.scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id: {data.role_id} not found"
        )

    stmt = select(PrincipalRoleBinding).where(
        PrincipalRoleBinding.principal_id == data.principal_id,
        PrincipalRoleBinding.tenant_id == data.tenant_id,
        PrincipalRoleBinding.role_id == data.role_id
    )

    existing = await db.execute(stmt)

    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Principal principal_id: {data.principal_id} exists for tenant_id: {data.tenant_id} and role_id: {data.role_id}."
        )

    principal_role_binding = PrincipalRoleBinding(
        principal_id=data.principal_id,
        tenant_id=data.tenant_id,
        role_id=data.role_id
    )

    db.add(principal_role_binding)
    await db.commit()
    await db.refresh(principal_role_binding)

    binding = Binding(
        id=principal_role_binding.id,
        principal_id=principal_role_binding.principal_id,
        tenant_id=principal_role_binding.tenant_id,
        role_id=principal_role_binding.role_id
    )

    return RoleUserAttachResponse(
        message="Role attached successfully",
        binding=binding
    )


async def detach_role(data: RoleUserAttachDetachRequest, db: AsyncSession):
    stmt = select(PrincipalRoleBinding).where(
        PrincipalRoleBinding.principal_id == data.principal_id,
        PrincipalRoleBinding.tenant_id == data.tenant_id,
        PrincipalRoleBinding.role_id == data.role_id
    )

    principal_role_binding = await db.execute(stmt)
    principal_role_binding = principal_role_binding.scalar_one_or_none()

    if not principal_role_binding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No biniding found for principal_id: {data.principal_id}, role_id: {data.role_id}, tenant_id: {data.tenant_id}"
        )

    await db.delete(principal_role_binding)
    await db.commit()
    return True