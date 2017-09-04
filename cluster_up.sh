rm -rf ~/.ansible
python scripts/aws_deploy.py --zookeeper --n-instances 1 --mesos-master eu-central-1 s2preproc provision
