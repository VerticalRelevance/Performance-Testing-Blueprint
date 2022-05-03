#!/bin/sh

echo Preparing to deploy template.yml

echo Linting...
cfn-lint template.yml

echo Deploying...
aws cloudformation deploy \
    --template-file template.yml \
    --stack-name PerformanceTesting \
    --parameter-overrides \
        PerformanceReportsS3Bucket="$PERFORMANCE_REPORTS_S3_BUCKET" \
        LocustImageRepositoryName="$LOCUST_IMAGE_ECR_NAME" \
        PerformanceTestUserArn="$AWS_PERFORMANCE_TEST_USER_ARN"
