#!/bin/bash

# More info on running Locust in CI/CD here: https://docs.locust.io/en/stable/running-without-web-ui.html

# --headless flag to run Locust without the web UI.
# -r to specify spawn rate
# -u to specify the number of users
# -t to specify the length of the run
# --html to specify where to store the results as an html file

timestamp=$(date '+%Y-%m-%d.%H-%M-%S')
. venv/bin/activate
locust -f locustfiles/category_locust_file.py --headless -r 2 -u 10 -t 30s --html pipeline-report-"$timestamp".html