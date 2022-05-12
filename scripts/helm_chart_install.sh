#!/bin/sh

release_name=$1

echo Creating locustfile configmap...
kubectl create configmap blueprint-locustfile --from-file ../locustfiles/blueprint.py

echo Installing...
helm install "$release_name" deliveryhero/locust \
  --set loadtest.name=blueprint \
  --set loadtest.locust_locustfile_configmap=blueprint-locustfile \
  --set loadtest.locust_lib_configmap=example-lib \
  -f ../chart/values.yaml