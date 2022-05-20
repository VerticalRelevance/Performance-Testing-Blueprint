#!/bin/sh

template=templates/pipeline.yml
stack_name=PerformanceTestingBlueprintPipelineStack

echo Preparing to deploy eks template

echo Linting...
cfn-lint "$template"

echo Deploying...
aws cloudformation deploy \
    --template-file "$template" \
    --stack-name "$stack_name" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
      PipelineName=PerformanceTestingBlueprintPipeline \
      S3BucketName=performance-testing-blueprint-pipeline-899456967600
