from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models import HealthResponse, ServiceInfo

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description="Application API for the Visco-Sensor software demonstration.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", response_model=ServiceInfo, tags=["service"])
async def service_info() -> ServiceInfo:
    """Return discoverable service metadata."""
    return ServiceInfo(
        name=settings.app_name,
        version=settings.api_version,
        environment=settings.app_env,
        documentation="/docs",
    )


@app.get("/health", response_model=HealthResponse, tags=["service"])
async def health() -> HealthResponse:
    """Confirm that the API process is ready to receive requests."""
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.api_version,
    )
