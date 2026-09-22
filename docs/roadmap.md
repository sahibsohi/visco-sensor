# Development roadmap

Each milestone is designed to become one meaningful, testable commit.

## Day 1 - Foundation

Suggested commit: `chore: initialize Visco-Sensor monorepo`

- Establish web and API applications.
- Add Docker Compose services.
- Add health checks and automated quality gates.
- Document product, architecture, roadmap, and safety boundaries.

## Day 2 - Device telemetry

Suggested commit: `feat: add simulated device telemetry`

- Generate deterministic viscosity scenarios.
- Publish versioned MQTT events.
- Add simulator configuration and unit tests.

## Day 3 - Ingestion

Suggested commit: `feat: build telemetry ingestion pipeline`

- Consume MQTT events.
- Validate schemas and timestamps.
- Record accepted and rejected event metrics.

## Day 4 - Data platform

Suggested commit: `feat: persist and transform sensor data`

- Add migrations and relational models.
- Preserve raw events and derived observations.
- Build daily and weekly transformations.

## Day 5 - Patient monitoring

Suggested commit: `feat: add real-time patient dashboard`

- Stream validated readings with WebSockets.
- Visualize synthetic trends and device state.
- Add accessible alert presentation.

## Day 6 - Clinician workflow

Suggested commit: `feat: implement alert review workflow`

- Add review queues and acknowledgement state.
- Record a traceable audit history.
- Present longitudinal summaries.

## Day 7 - Reliability

Suggested commit: `test: add end-to-end pipeline validation`

- Test simulator-to-dashboard flow.
- Expand failure-path coverage.
- Add operational metrics and final documentation.
