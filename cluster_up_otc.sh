rm -rf ~/.ansible
python scripts/otc_deploy.py --zookeeper --n-instances 1 --mesos-master eu-de s2preproc provision
