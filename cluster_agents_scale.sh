#!/bin/bash
set -e
set -x
aws autoscaling set-desired-capacity --auto-scaling-group-name agents --desired-capacity $1 --output json