#!/bin/sh

./deploy_cloudformation.sh
./build_load_test_image.sh
./run_load_tests.sh