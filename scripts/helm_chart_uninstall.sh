#!/bin/sh

release_name=$1

echo Deleting locustfile configmap...
kubectl delete configmap blueprint-locustfile

echo Uninstalling...
helm uninstall "$release_name"
