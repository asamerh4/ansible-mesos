#!/bin/bash
set -e

#get jenkins server IPs from autoscaling-group "gateway"
ec2_id=\
$(\
  aws autoscaling describe-auto-scaling-groups \
    --auto-scaling-group-name gateway \
    --output json \
    | jq .AutoScalingGroups[].Instances[].InstanceId \
    | sed -e 's/^"//' -e 's/"$//'\
)

ec2_ip=\
$(\
  aws ec2 describe-instances \
    --instance-ids $ec2_id \
    --output json \
    | jq .Reservations[].Instances[].PublicIpAddress \
    | sed -e 's/^"//' -e 's/"$//'\
)

#run jenkins-playbook
ansible-playbook \
--private-key=~/mesos120.pem \
-e jenkins_host=$ec2_ip \
-e remote_user=centos \
tasks/jenkins.yml
