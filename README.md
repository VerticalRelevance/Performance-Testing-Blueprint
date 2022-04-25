# Performance-Testing-Blueprint
Blueprint for performance testing foundation.

## Technical Details

Locust is the performance testing tool chosen for this blueprint. While this blueprint will focus on implementing the performance tests regardless of the tool chosen, this section will cover some things specific to Locust to get those out of the way, so that the rest of the sections can focus on implementing the recommendations found in the playbook.

## Pipeline Tests

These (component) tests run in the pipeline of the service being tested. The goal here is to have a baseline of tests that must pass in order to prevent performance regressions. **_These things_** cover the pipeline tests.

## Characterization Tests

These are the longer running tests. That characterize the system under test using the types of performance tests mentioned in the playbook. **_These things_** cover the characterization tests.
