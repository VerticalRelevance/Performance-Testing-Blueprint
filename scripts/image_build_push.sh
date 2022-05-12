#!/bin/sh

echo Removing existing locust image
docker image rm locust:latest

echo Building fresh locust image
docker build -t locust ..

echo Tagging image
docker tag locust:latest "$LOCUST_ECR_URI":latest

echo Logging in to aws ECR
aws ecr get-login-password --region "$AWS_REGION" \
    | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID".dkr.ecr."$AWS_REGION".amazonaws.com

echo Pushing image to ECR
docker push "$LOCUST_ECR_URI":latest
