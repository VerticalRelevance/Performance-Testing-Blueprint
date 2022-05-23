# Performance-Testing-Blueprint

Blueprint for performance testing foundation. This blueprint uses Locust as the performance test framework. You can read more about it [here]().

## Installation guide

Clone this blueprint repo.

`git clone git@github.com:VerticalRelevance/Performance-Testing-Blueprint.git`

Check that you have python 3 installed on your machine. If you don't have it, you can get it [here](https://www.python.org/downloads/).

`python3 --version`

Ensure that you are in the root of the blueprint directory.

`cd Performance-Testing-Blueprint`

You are about to install several Python packages. These include Locust and its dependencies along with this project's dependencies. When working in Python, it is recommended to install these packages in something called a virtual environment. You can read more about this [here](https://docs.python.org/3/tutorial/venv.html).

Create the virtual environment. Here it is created in a folder called `venv`.

`python3 -m venv ./venv`

Once the virtual environment is created, activate the virtual environment.

`source venv/bin/activate`

Now it is time to use the virtual environment to install the packages needed for Locust and this project. Now that you are inside the virtual environment you created, you can install them with pip using the requirements.txt file that contains a list of the packages and their versions that are needed.

`pip3 install -r requirements.txt`

Once that finishes, all the things to run locust are now installed.

## Running a Performance Test

Once Locust and its dependencies are installed (see [Installation Guide](#installation-guide)), you run Locust via the command line by specifying a so-called locustfile. This file is the entrypoint into the Locust tool. Have a look at the `locustfiles/simple_locust_file.py` for an example of how to structure one of these files.

To run Locust using the `simple_locust_file` type the following into the terminal.

`locust -f locustfiles/simple_locust_file.py`

Open a browser at [http://localhost:8089](http://localhost:8089). Enter the number of users (concurrency), the spawn rate for the generation of new users and press Start swarming. This will start the locust load generator. As the test progresses, you can change the number of users and the spawn rate. Press the blue `Edit` link in the Locust toolbar at the top of the page to do this. In this way you can perform the various performance test types by changing the number of users. There are also more automated ways of doing this using Locust. Take a look at the characterization folder at the top of the page.

## Blueprint Overview
This blueprint is doing several things.
- Provide examples of what the different types of performance tests look like, regardless of tooling.
- Provide examples of performance tests at various levels of maturity, uses cases, and performance test types.
- Provide examples of how to run Locust locally as you begin to write tests and start the performance test journey.

## Repo structure

This repo has the following directories based on the recommendations in the playbook.

`characterization` These are where the characterization locustfiles for the various types of performance tests live. These too are locustfiles.

`components` These are the libraries that make the calls to each service. Separated here by resources. Imagine each of the components here having its own prod repo and pipeline associated with it.

`controls` These are libraries that implement the control logic to implement sophisticated load shapes.

`locustfiles` These are the entrypoints into the performance test framework; here it is locust. These are locust files geared more towards being examples.

`pipeline` These are the scripts that would run in the pipeline of the system under test. Notice that they don't use the Locust UI. More information on running Locust specifically as part of a CI/CD pipeline can be found [here](https://docs.locust.io/en/stable/running-without-web-ui.html).

`utils` Performance testing utils.

`website` This is where workflows through the website are defined. Note how these tests consume the component tests.

## CI/CD Pipeline Tests

These (component) tests run in the pipeline of the service being tested. The goal here is to have a baseline of tests that must pass in order to prevent performance regressions. **_These things_** cover the pipeline tests. The pipeline tests implement a shell script runner. This shell script is responsible for calling initiating Locust, capturing the configuration, and collecting the reports. See the `pipeline` folder for examples.

## Characterization Tests

These are the longer running tests. That characterize the system under test using the types of performance tests mentioned in the playbook. There are a couple ways to perform these tests. You can use the either a component locustfile or a user journey locustfile and perform these tests manually using the web UI. Alternatively, Locust, for example, provides a `LoadTestShape` class that can be used to create custom load profiles to automate these tests. 

## FAQs

### How can I get started running one of these examples quickly?
Assuming you have python3 already installed and are running on a mac. Run this in your command line:
```
git clone git@github.com:VerticalRelevance/Performance-Testing-Blueprint.git &&
cd Performance-Testing-Blueprint && 
python3 -m venv ./venv &&
. venv/bin/activate &&
pip3 install -r requirements.txt &&
locust -f locustfiles/simple_locust_file.py
```
Then open a browser at [http://localhost:8089](http://localhost:8089).
If you are running on another OS, the commands might be different to activate the python virtual environment (line 4.)

This downloads the project from GitHub, installs a Python virtual environment inside the project directory, then installs the project dependencies inside that environment, and finally launches Locust using `simple_locustfile.py`. All that is left is opening the browser at localhost to run Locust using the web UI.

### I am only here to better understand implementing performance tests regardless of tool. Where can I go to look at the different performance test types?
Take a look at the characterization and locustfile folders for details on the tests themselves.

### There are many things going on here. Where to I start building this out on a project?
To get started using Locust, go [here](https://docs.locust.io/en/stable/quickstart.html) to get Locust setup on your system. Try running one of the files in the locustfiles folder on your system. A good one to try is `simple_locust_file.py`. It has few dependencies and is a good example of the anatomy of a performance test in Locust. Then, copy this file and change it to test a component of your system. Once that is working, you have a basic component test. Congratulations!

### How can I organize my tests?
There are many ways to organize your tests. Here, we have a folder dedicated to locustfiles. These are the files that are passed into the CLI directly to start the tests. Libraries are separated into folders depending on their functionality: components, controls, etc.

### What are the tests in these examples running against?
These tests run against something called the Gatling demo store. It is a public target set up by Gatling for this kind of thing
