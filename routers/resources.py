from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas import ResourceCreateRequest, ResourceCreateResponse, ResourceSchema
from services import create_resource as create_resource_service, get_resource as get_resource_service

resources_router = APIRouter(prefix='/resources')

@resources_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResourceCreateResponse
)
async def create_resource(data: ResourceCreateRequest, db: AsyncSession = Depends(get_db)):
    return await create_resource_service(data, db)


@resources_router.get(
    "/{resource_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResourceSchema
)
async def get_resource(resource_id: str, db: AsyncSession = Depends(get_db)):
    return await get_resource_service(resource_id, db)