#!/bin/sh

template=../templates/reports.yml
stack_name=PerformanceTestingReports
reports_s3_bucket_name=performance-test-reports-nchandlersmith

echo Preparing to deploy reports template

echo Linting...
cfn-lint "$template"

echo Deploying...
aws cloudformation deploy \
    --template-file "$template" \
    --stack-name "$stack_name" \
    --parameter-overrides \
        PerformanceReportsS3Bucket="$reports_s3_bucket_name"
