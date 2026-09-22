# Contributing

Visco-Sensor is being developed in focused milestones so each change remains reviewable and testable.

## Workflow

1. Create a branch from `main`, such as `feat/device-simulator`.
2. Keep each commit limited to one coherent change.
3. Run `make lint`, `make test`, and `make build` before opening a pull request.
4. Explain the user or engineering value of the change in the pull request.
5. Never commit secrets, real patient information, or identifiable health data.

## Commit style

Use short, imperative Conventional Commit messages:

```text
feat: add simulated device telemetry
fix: reject malformed sensor timestamps
test: cover API readiness response
docs: explain telemetry event schema
```

## Safety expectations

- Use synthetic data only.
- Label simulated outputs clearly.
- Do not implement real medication recommendations or dosing logic.
- Document assumptions and limitations alongside health-related functionality.
