from typing import Optional
from fastapi import FastAPI, APIRouter
import redis.asyncio as aioredis
from models import *
from routers import resources_router, roles_routers
from core.database import Base, engine

app = FastAPI()
iam_router = APIRouter(prefix='/iam')
REDIS_URL = "redis://localhost:6379/0"
INVALIDATION_CHANNEL = "iam_role_invalidations"
redis_client: Optional[aioredis.Redis] = None


@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    if redis_client:
        await redis_client.close()


iam_router.include_router(resources_router, tags=['Resources'])
iam_router.include_router(roles_routers, tags=['Roles'])
app.include_router(iam_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
