# Performance-Testing-Blueprint
Blueprint for performance testing foundation.

## Framework (Locust) Details

[Locust](locust.io) is the performance testing tool chosen for this blueprint. While this blueprint will focus on implementing the performance tests regardless of the tool, this section will cover some things specific to Locust to get those out of the way, so that the rest of the sections can focus on implementing the recommendations found in the playbook.

__This can go in a running locally section.__
Locust docs describe creating something called a locust file. This file is used as an entrypoint into the Locust framework. To see a simple example open `locustfiles/simple_locust_file.py`. To run locust with the webUI, then run from the cli: `locust -f locustfiles/simple_locust_file.py`. See `requirements.txt` for the things that pip will need to install in your environment. Note, see the pipeline scripts for an example of a headless run using Locust.

## Repo structure

This repo has the following directories based on the recommendations in the playbook.

`components` These are the files that make the calls to each service. Separated here by resources. Imagine each of the components here having its own prod repo and pipeline associated with it.

`locustfiles` These are the entrypoints into the performance test framework; here it is locust.

`pipeline` These are the scripts that would run in the pipeline of the prod code (system under test.)

`utils` Performance testing utils.

`website` This is where workflows through the website are defined. Note how these tests consume the component tests.

## Pipeline Tests

These (component) tests run in the pipeline of the service being tested. The goal here is to have a baseline of tests that must pass in order to prevent performance regressions. **_These things_** cover the pipeline tests. The pipeline tests implement a shell script runner. This shell script is responsible for calling initiating Locust, capturing the configuration, and collecting the reports. See the `pipeline` folder for examples.

## Characterization Tests

These are the longer running tests. That characterize the system under test using the types of performance tests mentioned in the playbook. **_These things_** cover the characterization tests. Currently, WIP.

## FAQs

### There are many things going on here. Where to I start building this out on a project?


