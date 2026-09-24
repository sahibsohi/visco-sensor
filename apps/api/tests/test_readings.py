from collections.abc import Generator
from datetime import UTC, datetime, timedelta

import pytest
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(bind=test_engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator[Session, None, None]:
        with testing_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def reading_payload(event_id: str, measured_at: datetime | None = None) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "event_id": event_id,
        "device_id": "VS-001",
        "patient_id": "patient-demo-001",
        "blood_viscosity_cp": 4.38,
        "temperature_c": 36.8,
        "battery_percent": 92,
        "signal_quality": "good",
        "device_status": "active",
        "measured_at": (measured_at or datetime.now(UTC)).isoformat(),
    }


def test_ingests_and_retrieves_reading(client: TestClient) -> None:
    payload = reading_payload("a293f783-2687-5ea3-9afa-6706a854e508")

    created = client.post("/api/v1/readings", json=payload)
    latest = client.get("/api/v1/readings/latest/VS-001")

    assert created.status_code == 201
    assert created.json()["event_id"] == payload["event_id"]
    assert latest.status_code == 200
    assert latest.json()["blood_viscosity_cp"] == 4.38


def test_rejects_duplicate_event(client: TestClient) -> None:
    payload = reading_payload("f5403496-c35c-5ae9-9a38-cdd88dc2f624")

    assert client.post("/api/v1/readings", json=payload).status_code == 201
    duplicate = client.post("/api/v1/readings", json=payload)

    assert duplicate.status_code == 409
    assert "already exists" in duplicate.json()["detail"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("battery_percent", 101),
        ("signal_quality", "unknown"),
        ("temperature_c", 52.0),
        ("blood_viscosity_cp", -1.0),
    ],
)
def test_rejects_invalid_measurements(
    client: TestClient, field: str, value: object
) -> None:
    payload = reading_payload("c6ec47c3-c2f9-5a13-8708-384cb90d431f")
    payload[field] = value

    response = client.post("/api/v1/readings", json=payload)

    assert response.status_code == 422


def test_rejects_future_timestamp(client: TestClient) -> None:
    payload = reading_payload(
        "4d3285d6-e357-54ac-936c-a274ca8828d3",
        datetime.now(UTC) + timedelta(minutes=10),
    )

    response = client.post("/api/v1/readings", json=payload)

    assert response.status_code == 422


def test_returns_device_summary(client: TestClient) -> None:
    now = datetime.now(UTC)
    first = reading_payload("182f959e-8f54-5f6d-8571-2dd62247a29d", now - timedelta(minutes=1))
    second = reading_payload("8b095d1b-9f60-50d7-858f-91f866560ca2", now)
    first["blood_viscosity_cp"] = 4.0
    second["blood_viscosity_cp"] = 5.0
    second["battery_percent"] = 89
    client.post("/api/v1/readings", json=first)
    client.post("/api/v1/readings", json=second)

    response = client.get("/api/v1/devices/VS-001/summary")

    assert response.status_code == 200
    assert response.json()["reading_count"] == 2
    assert response.json()["average_viscosity_cp"] == 4.5
    assert response.json()["latest_battery_percent"] == 89
