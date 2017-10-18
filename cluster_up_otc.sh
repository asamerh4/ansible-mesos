#!/bin/bash

set -ex

rm -rf ~/.ansible
python scripts/otc_deploy.py \
  -z \
  -m \
  -s3 "s3a://alluxio-tests/tests" \
  -b 4 \
  -k "~/mesos130-api.pem" \
  -ok mesos130-api \
  -u linux \
 eu-de \
 mesos-analytics123 \
 provision