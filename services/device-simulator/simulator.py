"""Generate and transmit synthetic Visco-Sensor prototype readings."""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import random
import time
from datetime import UTC, datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import NAMESPACE_URL, uuid5

LOGGER = logging.getLogger("visco-sensor-simulator")


def generate_reading(
    *,
    device_id: str,
    patient_id: str,
    sequence: int,
    rng: random.Random,
    measured_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a deterministic, synthetic observation suitable for API ingestion."""
    timestamp = measured_at or datetime.now(UTC)
    viscosity = 4.4 + 0.35 * math.sin(sequence / 4) + rng.uniform(-0.08, 0.08)
    temperature = 36.7 + rng.uniform(-0.25, 0.25)
    battery = max(0, 100 - sequence // 12)
    signal_quality = rng.choices(["good", "fair", "poor"], weights=[85, 13, 2], k=1)[0]
    event_key = f"{device_id}:{sequence}:{timestamp.isoformat()}"

    return {
        "schema_version": "1.0",
        "event_id": str(uuid5(NAMESPACE_URL, event_key)),
        "device_id": device_id,
        "patient_id": patient_id,
        "blood_viscosity_cp": round(viscosity, 3),
        "temperature_c": round(temperature, 2),
        "battery_percent": battery,
        "signal_quality": signal_quality,
        "device_status": "charging" if battery < 15 else "active",
        "measured_at": timestamp.isoformat(),
    }


def send_reading(api_url: str, payload: dict[str, Any], retries: int = 3) -> bool:
    """Send one observation with bounded retries for transient failures."""
    endpoint = f"{api_url.rstrip('/')}/api/v1/readings"
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=5) as response:  # noqa: S310 - configured local API
                if response.status == 201:
                    return True
        except HTTPError as error:
            if 400 <= error.code < 500:
                LOGGER.error(
                    "Reading rejected with status %s: %s",
                    error.code,
                    error.read().decode(),
                )
                return False
            LOGGER.warning("API returned %s on attempt %s", error.code, attempt)
        except URLError as error:
            LOGGER.warning("API unavailable on attempt %s: %s", attempt, error.reason)
        if attempt < retries:
            time.sleep(2 ** (attempt - 1))
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-url", default=os.getenv("API_URL", "http://localhost:8000"))
    parser.add_argument("--device-id", default=os.getenv("DEVICE_ID", "VS-001"))
    parser.add_argument("--patient-id", default=os.getenv("PATIENT_ID", "patient-demo-001"))
    parser.add_argument("--interval", type=float, default=float(os.getenv("INTERVAL_SECONDS", "5")))
    parser.add_argument("--count", type=int, default=int(os.getenv("READING_COUNT", "0")))
    parser.add_argument("--seed", type=int, default=int(os.getenv("SIMULATOR_SEED", "42")))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    sequence = 0
    LOGGER.info("Starting synthetic device %s against %s", args.device_id, args.api_url)

    while args.count == 0 or sequence < args.count:
        payload = generate_reading(
            device_id=args.device_id,
            patient_id=args.patient_id,
            sequence=sequence,
            rng=rng,
        )
        accepted = send_reading(args.api_url, payload)
        LOGGER.info(
            "event=%s viscosity=%s accepted=%s",
            payload["event_id"],
            payload["blood_viscosity_cp"],
            accepted,
        )
        sequence += 1
        if args.count == 0 or sequence < args.count:
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
