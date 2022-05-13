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

`characterization` These are where the characterization locustfiles for the various types of performance tests live. These too are locustfiles.

`chart` This folder has the helm chart used to deploy to EKS. Using chart from [here](https://github.com/deliveryhero/helm-charts).

`components` These are the libraries that make the calls to each service. Separated here by resources. Imagine each of the components here having its own prod repo and pipeline associated with it.

`controls` These are libraries that implement the control logic to implement sophisticated load shapes.

`locustfiles` These are the entrypoints into the performance test framework; here it is locust. These are locust files geared more towards being examples.

`pipeline` These are the scripts that would run in the pipeline of the prod code (system under test.)

`scripts` These are scripts that are used to deploy infrastructure and distributed performance testing system components.

`utils` Performance testing utils.

`website` This is where workflows through the website are defined. Note how these tests consume the component tests.

## Pipeline Tests

These (component) tests run in the pipeline of the service being tested. The goal here is to have a baseline of tests that must pass in order to prevent performance regressions. **_These things_** cover the pipeline tests. The pipeline tests implement a shell script runner. This shell script is responsible for calling initiating Locust, capturing the configuration, and collecting the reports. See the `pipeline` folder for examples.

## Characterization Tests

These are the longer running tests. That characterize the system under test using the types of performance tests mentioned in the playbook.



## FAQs

### I am only here to better understand implementing performance tests regardless of tool. Where can I go to look at the different performance test types?
Take a look at the characterization and locustfile folders for details on the tests themselves.

### There are many things going on here. Where to I start building this out on a project?
To get started using Locust, go [here](https://docs.locust.io/en/stable/quickstart.html) to get Locust setup on your system. Try running one of the files in the locustfiles folder on your system. A good one to try is `simple_locust_file.py`. It has few dependencies and is a good example of the anatomy of a performance test in Locust. Then, copy this file and change it to test a component of your system. Once that is working, you have a basic component test. Congratulations!

### How can I organize my tests?
There are many ways to organize your tests. Here, we have a folder dedicated to locustfiles. These are the files that are passed into the CLI directly to start the tests. Libraries are separated into folders depending on their functionality: components, controls, etc.

### I want to set up a distributed performance testing system using Locust. How do I do this?
Have a look at the templates (IaC) and scripts folders. These folders do the things necessary to set up and run a distributed performance testing system.

### What are the tests in these examples running against?
These tests run against something called the Gatling demo store. It is a public target set up by Gatling for this kind of thing.
