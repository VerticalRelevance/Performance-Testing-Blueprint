#!/bin/sh

echo Packaging helm chart
cd ..
success_message="$(helm package chart)"
chart_path="$(echo "$success_message" | cut -f 2 -d ":" | xargs)"
chart="$(basename "$chart_path")"

echo Pushing chart "$chart"
echo Logging in to ecr
aws ecr get-login-password \
  --region "$AWS_REGION" \
  | helm registry login \
  --username AWS \
  --password-stdin "$AWS_ACCOUNT_ID".dkr.ecr."$AWS_REGION".amazonaws.com \
  || exit
echo successfully logged in to aws ecr

echo Pushing the chart
helm push "$chart" oci://"$AWS_ACCOUNT_ID".dkr.ecr."$AWS_REGION".amazonaws.com/
echo Push succedded

cd scripts || exit
