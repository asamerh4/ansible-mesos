ansible-mesos
=============
playbooks and roles for mesos & alluxio deployment on Open Telekom Cloud (OTC)

##  what you get
- mesos cluster with one master (multi-master HA setup coming soon) and private agents within an autoscaling group (private IPs)
- distributed alluxio inMemory-FS accross agents (useable via alluxio-proxy REST API at `localhost:39999` on every cluster-node)
- alluxio underFS configured for S3 (OBS)
- readonly ssl enabled webUI & dashboards of `mesos` and `alluxio`
- chached nginx proxy for otc-instance metadata endpoints accessible at every node at  `localhost/user-data`
- jenkins instance for static processing pipelines (deactivated by default)

## why you want this
- for running batch-processing workloads on mesos from and to S3 optionally using an InMemory cache for intermediate data or results
- doing processing on `fast` InMemory-data with mesos-frameworks like `spark` or `mesos-batch` inside docker containers
- to run analytics on selected datasets from S3

## what you need
- ansible control host with internet access (preferably linuxOS)
- python, pip, ansible, awscli (for interaction with S3 and boto-dependency) installed
  ```sh
  # e.g. for centos...
  yum -y update
  yum -y install epel-release
  yum -y update
  yum -y install python-pip jq
  pip install --upgrade pip
  pip install awscli certifi
  ```
- OTC privileged account (admin-role)
- proper `clouds.yml` config in ~/.config/openstack/clouds.yml
  * Example of clouds.yml:
    ```yaml
    clouds:
      otc:
        auth:
          auth_url: https://iam.eu-de.otc.t-systems.com:443/v3
          username: -your-otc-privileged-username-
          password: -your-otc-privileged-username-password-
          project_name: eu-de
          project_domain_name: -your-domain-id- (e.g.8834sdfec3cc84120aac157xyz1234)
          user_domain_name: -your-domain-name- (e.g. OTC-EU-DE-0000000000xxxxxx)
        region_name: eu-de
    ```
- OTC Access keys with read/write permissions for S3
user-access keys consist of `access_key_id` and  `secret_access_key` and must be generated within the OTC web-console. It's recommanded to generate a seperate user with read/write permissions to OBS (S3) 
- OTC-static conf needed:
    - existing ssh-key
       - ansible expects ssh-key under ~/mesos130.pem -> change this in `scripts/otc_deploy.py`
    - existing VPC (VPC-ID)
       - deafult settings
    - existing subnet within VPC (subnet-ID)
       - subnet-cidr: 192.168.0.0/24
    - OTC Machine-Image (Image-ID)
       - centos7.2-docker1.17-mesos1.4.0-jenkins2.79-alluxio1.6-https
       - centos7.2 with docker engine 1.17, mesos 1.4.0, alluxio 1.6 jenkins 2.7, awscli, nginx (public readonly sites via ssl), no firewalld, no selinux, some network tweaks, iptables service, ip forwarding, all mentioned core services are disabled by default
       - shared with public `on request`