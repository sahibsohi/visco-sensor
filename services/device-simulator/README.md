# Device simulator

The simulator generates deterministic synthetic readings and submits them to the FastAPI ingestion endpoint. It models the software boundary of a prototype device without representing clinical measurements.

Run a finite five-reading simulation against a locally running API:

```bash
python services/device-simulator/simulator.py --count 5 --interval 1
```

Configuration is available through command-line flags or the `API_URL`, `DEVICE_ID`, `PATIENT_ID`, `INTERVAL_SECONDS`, `READING_COUNT`, and `SIMULATOR_SEED` environment variables. A reading count of `0` runs continuously.
