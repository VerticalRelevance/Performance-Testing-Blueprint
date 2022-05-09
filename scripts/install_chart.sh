#!/bin/sh

echo Run a kubectl to check connection
kubectl get service

# enable experimental OCI support
export HELM_EXPERIMENTAL_OCI=1

echo Authenticating with AWS ECR...
aws ecr get-login-password \
  --region "$AWS_REGION" | helm registry login \
  --username AWS \
  --password-stdin "$AWS_ACCOUNT_ID".dkr.ecr."$AWS_REGION".amazonaws.com

echo Pull chart to local...
echo Pull Helm chart to local cache
helm pull oci://"$AWS_ACCOUNT_ID".dkr.ecr."$AWS_REGION".amazonaws.com/locust-chart-performance-test

echo Installing...
helm install locust-performance-tester ./locust-chart-performance-test-0.26.1.tgz
