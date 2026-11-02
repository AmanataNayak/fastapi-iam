from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from models import Resource, Action
from schemas import ResourceCreateRequest, ResourceCreateResponse, ResourceSchema
from core.constants import StatusConstants

async def create_resource(data: ResourceCreateRequest, db: AsyncSession) -> dict:
    # check if resource key already exists
    stmt = select(Resource).where(Resource.key == data.key)
    existing = await db.execute(stmt)

    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Resource key '{data.key}' already exists."
        )

    # Instantiate parent Resource
    res = Resource(
        name=data.name,
        key=data.key
    )
    db.add(res)
    await db.flush()

    action_objs = []

    for act in data.actions:
        action_obj = Action(
            resource_id=res.id,
            name=act.name,
            is_public=act.is_public
        )
        action_objs.append(action_obj)

    # Batch add all actions and flush once
    db.add_all(action_objs)
    await db.flush()
    await db.commit()

    return ResourceCreateResponse(
        resource_id=res.id,
        status=StatusConstants.SUCCESS,
        actions=[a.id for a in action_objs]
    ).model_dump()


async def get_resource(resource_id: str, db: AsyncSession) -> ResourceSchema:
    stmt = select(Resource).options(selectinload(Resource.actions)).where(Resource.id == resource_id)
    result = await db.execute(stmt)
    resource = result.scalar_one_or_none()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID '{resource_id}' not found."
        )

    return ResourceSchema.model_validate(resource, from_attributes=True)