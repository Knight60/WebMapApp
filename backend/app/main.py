from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import imagery


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    if settings.ee_service_account_email:
        from app.ee_session import init_ee

        init_ee(settings)
    yield


app = FastAPI(title="WebMapApp API", lifespan=lifespan)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)


app.include_router(imagery.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
