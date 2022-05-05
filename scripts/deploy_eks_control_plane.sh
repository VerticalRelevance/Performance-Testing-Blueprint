#!/bin/sh

template=../templates/eks_control_plane.yml
stack_name=PerformanceTestingEKSControlPlane

echo Preparing to deploy eks template

echo Linting...
cfn-lint "$template"

echo Deploying...
aws cloudformation deploy \
    --template-file "$template" \
    --stack-name "$stack_name" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
      EKSIAMRoleName=EKSServiceRole \
      EKSClusterName=PerformanceTestingControlPlane
