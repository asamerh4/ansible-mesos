#!/bin/bash

set -ex

BUILD=$(git rev-parse --short HEAD)
CLUSTER_NAME="analytics"
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e ${YELLOW}"**building cluster $CLUSTER_NAME"-"$BUILD"${NC}

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
 $CLUSTER_NAME"-"$BUILD \
 provision
