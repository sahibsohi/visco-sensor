from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import Base, engine, get_db
from app.entities import SensorReadingRecord
from app.models import (
    DeviceSummary,
    HealthResponse,
    SensorReadingCreate,
    SensorReadingResponse,
    ServiceInfo,
)

settings = get_settings()
DatabaseSession = Annotated[Session, Depends(get_db)]
ReadingLimit = Annotated[int, Query(ge=1, le=500)]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize local persistence before the service accepts traffic."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description="Application API for the Visco-Sensor software demonstration.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
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


@app.post(
    "/api/v1/readings",
    response_model=SensorReadingResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["readings"],
)
def create_reading(
    reading: SensorReadingCreate,
    db: DatabaseSession,
) -> SensorReadingRecord:
    """Validate and persist one synthetic prototype reading."""
    record = SensorReadingRecord(
        event_id=str(reading.event_id),
        device_id=reading.device_id,
        patient_id=reading.patient_id,
        blood_viscosity_cp=reading.blood_viscosity_cp,
        temperature_c=reading.temperature_c,
        battery_percent=reading.battery_percent,
        signal_quality=reading.signal_quality,
        device_status=reading.device_status,
        measured_at=reading.measured_at,
    )
    db.add(record)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A reading with this event_id already exists.",
        ) from error
    db.refresh(record)
    return record


@app.get(
    "/api/v1/readings",
    response_model=list[SensorReadingResponse],
    tags=["readings"],
)
def list_readings(
    db: DatabaseSession,
    device_id: str | None = None,
    limit: ReadingLimit = 100,
) -> list[SensorReadingRecord]:
    """Return recent readings, optionally filtered by device."""
    statement = select(SensorReadingRecord)
    if device_id:
        statement = statement.where(SensorReadingRecord.device_id == device_id)
    statement = statement.order_by(SensorReadingRecord.measured_at.desc()).limit(limit)
    return list(db.scalars(statement))


@app.get(
    "/api/v1/readings/latest/{device_id}",
    response_model=SensorReadingResponse,
    tags=["readings"],
)
def latest_reading(device_id: str, db: DatabaseSession) -> SensorReadingRecord:
    """Return the latest observation reported by one device."""
    statement = (
        select(SensorReadingRecord)
        .where(SensorReadingRecord.device_id == device_id)
        .order_by(SensorReadingRecord.measured_at.desc())
        .limit(1)
    )
    record = db.scalar(statement)
    if record is None:
        raise HTTPException(status_code=404, detail="No readings found for this device.")
    return record


@app.get(
    "/api/v1/devices/{device_id}/summary",
    response_model=DeviceSummary,
    tags=["devices"],
)
def device_summary(device_id: str, db: DatabaseSession) -> DeviceSummary:
    """Compute a compact aggregate from one device's persisted readings."""
    aggregate = db.execute(
        select(
            func.count(SensorReadingRecord.id),
            func.avg(SensorReadingRecord.blood_viscosity_cp),
            func.min(SensorReadingRecord.blood_viscosity_cp),
            func.max(SensorReadingRecord.blood_viscosity_cp),
        ).where(SensorReadingRecord.device_id == device_id)
    ).one()
    if aggregate[0] == 0:
        raise HTTPException(status_code=404, detail="No readings found for this device.")

    latest = db.scalar(
        select(SensorReadingRecord)
        .where(SensorReadingRecord.device_id == device_id)
        .order_by(SensorReadingRecord.measured_at.desc())
        .limit(1)
    )
    if latest is None:  # Defensive guard for concurrent deletion.
        raise HTTPException(status_code=404, detail="No readings found for this device.")

    return DeviceSummary(
        device_id=device_id,
        reading_count=aggregate[0],
        latest_measured_at=latest.measured_at,
        average_viscosity_cp=round(float(aggregate[1]), 3),
        minimum_viscosity_cp=float(aggregate[2]),
        maximum_viscosity_cp=float(aggregate[3]),
        latest_battery_percent=latest.battery_percent,
        latest_signal_quality=latest.signal_quality,
    )
