import importlib.util
import random
from datetime import UTC, datetime
from pathlib import Path


def load_simulator():
    module_path = Path(__file__).with_name("simulator.py")
    spec = importlib.util.spec_from_file_location("device_simulator", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load simulator module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generates_versioned_deterministic_payload() -> None:
    simulator = load_simulator()
    measured_at = datetime(2026, 1, 1, tzinfo=UTC)

    first = simulator.generate_reading(
        device_id="VS-TEST",
        patient_id="patient-test",
        sequence=4,
        rng=random.Random(7),
        measured_at=measured_at,
    )
    second = simulator.generate_reading(
        device_id="VS-TEST",
        patient_id="patient-test",
        sequence=4,
        rng=random.Random(7),
        measured_at=measured_at,
    )

    assert first == second
    assert first["schema_version"] == "1.0"
    assert 0.1 < first["blood_viscosity_cp"] <= 20
    assert 0 <= first["battery_percent"] <= 100
    assert first["measured_at"] == "2026-01-01T00:00:00+00:00"
