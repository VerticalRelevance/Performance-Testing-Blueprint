# Performance-Testing-Blueprint
Blueprint for performance testing foundation.

## Blueprint Overview
This blueprint is trying to do several things. Hopefully well:
- Provide examples of what the different types of performance tests look like, regardless of tooling.
- Provide examples of performance tests at various levels of maturity, uses cases, and performance test types.
- Provide examples of how to run Locust locally as you begin to write tests and start the performance test journey.
- Provide an example of how to use Locust to setup a distributed performance tester in AWS with a master and many workers.

## Repo structure

This repo has the following directories based on the recommendations in the playbook.

`characterization` These are where the characterization code for the various types of performance tests live.

`chart` This folder has the helm chart used to deploy to EKS. Using chart from [here](https://github.com/deliveryhero/helm-charts).

`components` These are the files that make the calls to each service. Separated here by resources. Imagine each of the components here having its own prod repo and pipeline associated with it.

`locustfiles` These are the entrypoints into the performance test framework; here it is locust.

`pipeline` These are the scripts that would run in the pipeline of the prod code (system under test.)

`scripts` These are scripts that are used to deploy infrastructure and distributed performance testing system components.

`utils` Performance testing utils.

`website` This is where workflows through the website are defined. Note how these tests consume the component tests.

`controls` This is where control logic lives, e.g. automated load shaping.

## Pipeline Tests

These (component) tests run in the pipeline of the service being tested. The goal here is to have a baseline of tests that must pass in order to prevent performance regressions. **_These things_** cover the pipeline tests. The pipeline tests implement a shell script runner. This shell script is responsible for calling initiating Locust, capturing the configuration, and collecting the reports. See the `pipeline` folder for examples.

## Characterization Tests

These are the longer running tests. That characterize the system under test using the types of performance tests mentioned in the playbook. **_These things_** cover the characterization tests. Currently, WIP.

## FAQs

### There are many things going on here. Where to I start building this out on a project?
I assume you are using locust. Go [here](https://docs.locust.io/en/stable/quickstart.html) to get Locust setup on your system.

### I am only here to better understand implementing performance tests regardless of tool. Where can I go to look at the different performance test types?
Take a look at the characterization and locustfile folders for details on the tests themselves.
