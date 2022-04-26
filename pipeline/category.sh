data_tag=$1

# capture configurations
# TODO: logic here to capture some things

# run the tests
locust -f locustfiles/category_locust_file.py -u 10 -r 2 -t 1m --headless --csv "$data_tag"

# present the results
#  TODO: logic here to analyze results for pass/fail exit code