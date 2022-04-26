data_tag=$1

number_of_users=10
spawn_rate=2
run_time=1m

# capture configurations
# TODO: logic here to capture some things

# run the tests
locust -f locustfiles/category_locust_file.py -u "$number_of_users" -r "$spawn_rate" -t "$run_time" \
 --headless --csv "$data_tag"

# present the results
#  TODO: logic here to analyze results for pass/fail exit code