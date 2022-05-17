#!/bin/sh

control_plane_stack_name=PerformanceTestingEKSControlPlane

template=../templates/eks_workers.yml
stack_name=PerformanceTestingEKSWorkers

# things from the control plane stack
cluster_name=PerformanceTestingControlPlane
key_name=PerformanceTestEKSWorkersKey
desired_capacity=1
max_capacity=3
min_capacity=1
worker_node_group_name=PerformanceTestWorkers
node_instance_type=t3.medium
node_volume_size=8
# These three come from control plan

echo Preparing to deploy eks template

echo Linting...
cfn-lint "$template"

echo Deploying...
aws cloudformation deploy \
    --template-file "$template" \
    --stack-name "$stack_name" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
      ClusterName="$cluster_name" \
      KeyName="$key_name" \
      NodeAutoScalingGroupDesiredCapacity="$desired_capacity" \
      NodeAutoScalingGroupMaxSize="$max_capacity" \
      NoteAutoScalingGroupMinSize="$min_capacity" \
      NodeGroupName="$worker_node_group_name" \
      NodeInstanceType="$node_instance_type" \
      NodeVolumeSize="$node_volume_size" \
      ControlPlaneStackName="$control_plane_stack_name"
