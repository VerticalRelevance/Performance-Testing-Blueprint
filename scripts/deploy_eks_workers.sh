#!/bin/sh

template=../templates/eks_workers.yml
stack_name=PerformanceTestingEKSWorkers

# things from the control plane stack
control_plane_stack_name=PerformanceTestingEKSControlPlane
cluster_name=PerformanceTestingControlPlane
cluster_control_plane_security_group=sg-05134c68fb6c4a287
key_name=EKSWorkersKey
desired_capacity=1
max_capacity=3
min_capacity=1
worker_node_group_name=PerformanceTestWorkers
node_instance_type=t3.micro
node_volume_size=8
subnets=subnet-06131d9b35c5e3eec,subnet-08710858dcf04c97a,subnet-0fc6f3f75ff5d142e,subnet-0faa75694a234d0e0
vpc_id=vpc-0065967fbb6fba9ba

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
      ClusterControlPlaneSecurityGroup="$cluster_control_plane_security_group" \
      KeyName="$key_name" \
      NodeAutoScalingGroupDesiredCapacity="$desired_capacity" \
      NodeAutoScalingGroupMaxSize="$max_capacity" \
      NoteAutoScalingGroupMinSize="$min_capacity" \
      NodeGroupName="$worker_node_group_name" \
      NodeInstanceType="$node_instance_type" \
      NodeVolumeSize="$node_volume_size" \
      Subnets="$subnets" \
      VpcId="$vpc_id" \
