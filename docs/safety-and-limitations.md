# Safety and limitations

Visco-Sensor is an educational prototype. It is not a medical device and must not be used for clinical decisions.

## Current limitations

- No physical sensor is connected to this repository.
- No clinical study has validated its outputs.
- Future device readings will be synthetic.
- Future risk classifications will be demonstration logic, not diagnoses.
- The platform does not prescribe or administer medication.
- The projected cost comparison is a feasibility estimate, not an observed outcome.

## Engineering safeguards

- Synthetic records will be visibly labelled.
- Incoming events will use versioned schemas and validation.
- Invalid events will be quarantined instead of silently accepted.
- Demonstration alerts will maintain an audit trail.
- No medication dosage logic will be implemented.
