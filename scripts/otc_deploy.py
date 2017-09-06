import argparse
from subprocess import call

parser = argparse.ArgumentParser(description = 'Deploy and manage a Mesos cluster on OTC.')

parser.add_argument("region",
                    choices = ["eu-de"],
                    help = "The OTC region to search and deploy Mesos into")

parser.add_argument('cluster-id',
                    help = 'A unique identifier per OTC region for your Mesos cluster')

parser.add_argument('action', choices = ["provision"],
                    help = 'The action to perform on the cluster')

parser.add_argument("-n", "--n-instances", dest = 'n', type = int,
                    help = "The number of instances to provision")

parser.add_argument("-z", "--zookeeper", dest = 'zookeeper', action = 'store_true',
                    help = "Provision these machines with ZooKeeper installed")

parser.add_argument("-m", "--mesos-master", dest = 'mesos_master', action = 'store_true',
                    help = "Provision these machines with a Mesos master installed")





parser.add_argument("-f", "--ansible-vault-password-file", dest = 'password_file',
                    help = "The location of the file containing the Ansible Vault password")

args = parser.parse_args()
arg_vars = vars(args)

ansible_prompt = "--ask-vault-pass"
if arg_vars["password_file"]:
  ansible_prompt = "--vault-password-file={}".format(args.password_file)


if args.action == "provision":
  if not args.zookeeper and not args.mesos_master:
    print parser.error("Provisioning requires at least one role to be set (e.g. ZooKeeper, Mesos Master, etc)")
  elif not args.n:
    print parser.error("Provision machines requires --n-instances to be set to a positive integer")
  else:
    call(["ansible-playbook",
          ansible_prompt,
          "--private-key=~/mesos130.pem",
          "-e", "remote_user=linux",
          "-e", "mesos_cluster_id={}".format(arg_vars["cluster-id"]),
          "-e", "otc_provision=True",
          "-e", "n_vms={}".format(arg_vars["n"]),
          "-e", "mesos_zookeeper={}".format(arg_vars["zookeeper"]),
          "-e", "mesos_master={}".format(arg_vars["mesos_master"]),
          "-e", "mesos_otc_master=160.44.205.74",		  
          "-i", ",",
          "tasks/otc.yml"])
