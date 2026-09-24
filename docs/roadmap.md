# Development roadmap

Each milestone is designed to become one meaningful, testable commit.

## Foundation

Suggested commit: `chore: initialize Visco-Sensor monorepo`

- Establish web and API applications.
- Add Docker Compose services.
- Add health checks and automated quality gates.
- Document product, architecture, roadmap, and safety boundaries.

## Sensor ingestion pipeline

Suggested commit: `feat: add sensor data ingestion pipeline`

- Generate deterministic synthetic readings.
- Validate versioned events and reject malformed data.
- Persist observations in PostgreSQL.
- Expose recent-reading and device-summary queries.
- Add simulator configuration, retry handling, and unit tests.

## Asynchronous ingestion

Suggested commit: `feat: build telemetry ingestion pipeline`

- Consume MQTT events.
- Validate schemas and timestamps.
- Record accepted and rejected event metrics.

## Data transformations

Suggested commit: `feat: persist and transform sensor data`

- Add migrations and relational models.
- Preserve raw events and derived observations.
- Build daily and weekly transformations.

## Patient monitoring

Suggested commit: `feat: add real-time patient dashboard`

- Stream validated readings with WebSockets.
- Visualize synthetic trends and device state.
- Add accessible alert presentation.

## Clinician workflow

Suggested commit: `feat: implement alert review workflow`

- Add review queues and acknowledgement state.
- Record a traceable audit history.
- Present longitudinal summaries.

## Reliability

Suggested commit: `test: add end-to-end pipeline validation`

- Test simulator-to-dashboard flow.
- Expand failure-path coverage.
- Add operational metrics and final documentation.
