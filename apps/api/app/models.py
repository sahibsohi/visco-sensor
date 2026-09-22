from typing import Literal

from pydantic import BaseModel


class ServiceInfo(BaseModel):
    name: str
    version: str
    environment: str
    documentation: str


class HealthResponse(BaseModel):
    status: Literal["healthy"]
    service: str
    version: str
