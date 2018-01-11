import argparse
from subprocess import call

parser = argparse.ArgumentParser(description = 'Deploy and manage a Mesos & Alluxio cluster on OTC.')

parser.add_argument("region",
                    choices = ["eu-de"],
                    help = "The OTC region to search and deploy Mesos into")

parser.add_argument('cluster-id',
                    help = 'A unique identifier per OTC region for your Mesos cluster')

parser.add_argument('action', choices = ["provision"],
                    help = 'The action to perform on the cluster')

parser.add_argument("-z", "--zookeeper", dest = 'zookeeper', action = 'store_true',
                    help = "Provision public ecs-instance with ZooKeeper installed")

parser.add_argument("-m", "--mesos-master", dest = 'mesos_master', action = 'store_true',
                    help = "Provision public ecs-instance with a Mesos master installed")

parser.add_argument("-s3", "--alluxio-s3-bucket", dest = 'alluxio-s3-bucket',type = str, 
                    help = "s3-bucket-url for alluxio underFS (s3a://bucket-name)")
	
parser.add_argument("-b", "--alluxio-block-size", dest = 'alluxio-block-size',type = int, 
                    help = "block size in MB for alluxio FS")

parser.add_argument("-k", "--ssh-key", dest = 'ssh-key', type = str,
                    help = "path to ssh-key (*.pem file)")

parser.add_argument("-ok", "--otc-ssh-key-name", dest = 'otc-ssh-key-name', type = str,
                    help = "name of keypair registered in OTC-ECS")

parser.add_argument("-u", "--remote-user", dest = 'remote-user', type = str,
                    help = "remote user for ECS instance (sudo)")

parser.add_argument("-f", "--ansible-vault-password-file", dest = 'password_file',
                    help = "The location of the file containing the Ansible Vault password")

args = parser.parse_args()
arg_vars = vars(args)

#ansible_prompt = "--ask-vault-pass"
#if arg_vars["password_file"]:
#  ansible_prompt = "--vault-password-file={}".format(args.password_file)


if args.action == "provision":
  if not args.zookeeper and not args.mesos_master:
    print parser.error("Provisioning requires at least one role to be set (e.g. ZooKeeper, Mesos Master, etc)")
  else:
    call(["ansible-playbook",
          #ansible_prompt,
          "--private-key={}".format(arg_vars["ssh-key"]),
		  "-e", "alluxio_block_size={}".format(str(arg_vars["alluxio-block-size"])+"MB"),
		  "-e", "alluxio_underfs_s3={}".format(arg_vars["alluxio-s3-bucket"]),
		  "-e", "remote_user={}".format(arg_vars["remote-user"]),
          "-e", "otc_ssh_key_name={}".format(arg_vars["otc-ssh-key-name"]),
          "-e", "cluster_id={}".format(arg_vars["cluster-id"]),
          "-e", "otc_provision=True",
          "-e", "n_vms=1",
          "-e", "mesos_zookeeper={}".format(arg_vars["zookeeper"]),
          "-e", "mesos_master={}".format(arg_vars["mesos_master"]),
          "-i", ",",
          "tasks/otc.yml"])
