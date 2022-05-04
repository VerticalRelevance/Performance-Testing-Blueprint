#!/bin/sh

template=../templates/images.yml
stack_name=PerformanceTestingImages
image_repo_name=locust-performance-test
user_arn="$AWS_PERFORMANCE_TEST_USER_ARN"


echo Preparing to deploy images template

echo Linting...
cfn-lint "$template"

echo Deploying...
aws cloudformation deploy \
    --template-file "$template" \
    --stack-name "$stack_name" \
    --parameter-overrides \
        LocustImageRepositoryName="$image_repo_name" \
        PerformanceTestUserArn="$user_arn"
