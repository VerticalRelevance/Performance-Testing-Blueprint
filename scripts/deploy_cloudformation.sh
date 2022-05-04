#!/bin/sh

echo Deploying cloud formation templates

bash deploy_images_cfn.sh
bash deploy_reports_cfn.sh
