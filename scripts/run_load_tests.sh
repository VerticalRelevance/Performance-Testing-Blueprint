#!/bin/sh

local_reports_directory=/tmp/reports

echo Run load tests...
docker run --rm -v /$local_reports_directory:/hostVolume gatling
echo --------------------------------------------------------------------
echo

echo Contents of the local report directory:
ls -la $local_reports_directory
aws s3 sync $local_reports_directory s3://"$GATLING_REPORT_S3_BUCKET"
echo --------------------------------------------------------------------
echo
