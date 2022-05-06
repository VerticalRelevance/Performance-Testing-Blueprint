#!/bin/sh

template=../templates/ecr.yml
stack_name=PerformanceTestingHelmRepo
repo_name=locust-chart-performance-test
user_arn="$AWS_PERFORMANCE_TEST_USER_ARN"


echo Preparing to deploy images template

echo Linting...
cfn-lint "$template"

echo Deploying...
aws cloudformation deploy \
    --template-file "$template" \
    --stack-name "$stack_name" \
    --parameter-overrides \
        RepositoryName="$repo_name" \
        PerformanceTestUserArn="$user_arn"
