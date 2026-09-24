from datetime import UTC, datetime, timedelta
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ServiceInfo(BaseModel):
    name: str
    version: str
    environment: str
    documentation: str


class HealthResponse(BaseModel):
    status: Literal["healthy"]
    service: str
    version: str


DeviceIdentifier = Annotated[str, Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")]
PatientIdentifier = Annotated[str, Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")]


class SensorReadingCreate(BaseModel):
    """Versioned contract accepted from a prototype device or simulator."""

    schema_version: Literal["1.0"] = "1.0"
    event_id: UUID
    device_id: DeviceIdentifier
    patient_id: PatientIdentifier
    blood_viscosity_cp: float = Field(gt=0.1, le=20.0)
    temperature_c: float = Field(ge=30.0, le=45.0)
    battery_percent: int = Field(ge=0, le=100)
    signal_quality: Literal["good", "fair", "poor"]
    device_status: Literal["active", "charging", "maintenance"]
    measured_at: datetime

    @field_validator("measured_at")
    @classmethod
    def validate_measured_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("measured_at must include a timezone")
        normalized = value.astimezone(UTC)
        if normalized > datetime.now(UTC) + timedelta(minutes=5):
            raise ValueError("measured_at cannot be more than five minutes in the future")
        return normalized


class SensorReadingResponse(SensorReadingCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    received_at: datetime


class DeviceSummary(BaseModel):
    device_id: str
    reading_count: int
    latest_measured_at: datetime
    average_viscosity_cp: float
    minimum_viscosity_cp: float
    maximum_viscosity_cp: float
    latest_battery_percent: int
    latest_signal_quality: str
