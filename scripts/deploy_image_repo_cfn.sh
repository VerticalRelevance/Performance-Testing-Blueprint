#!/bin/sh

template=../templates/ecr.yml
stack_name=PerformanceTestingImageRepo
repo_name=locust-image-performance-test


echo Preparing to deploy images template

echo Linting...
cfn-lint "$template"

echo Deploying...
aws cloudformation deploy \
    --template-file "$template" \
    --stack-name "$stack_name" \
    --parameter-overrides \
        RepositoryName="$repo_name"