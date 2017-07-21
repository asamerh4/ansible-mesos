#!/bin/bash
set -e
set -x
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name agents --output json