import argparse
from subprocess import call

parser = argparse.ArgumentParser(description = 'Deploy and manage a Mesos & Alluxio cluster on OTC.')

parser.add_argument("region",
                    choices = ["eu-de"],
                    help = "The OTC region to search and deploy Mesos into")

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

ansible_prompt = "--ask-vault-pass"
if arg_vars["password_file"]:
  ansible_prompt = "--vault-password-file={}".format(args.password_file)


call(["ansible-playbook",
          ansible_prompt,
          "--private-key={}".format(arg_vars["ssh-key"]),
		  
		  "-e", "remote_user={}".format(arg_vars["remote-user"]),
          "-e", "otc_ssh_key_name={}".format(arg_vars["otc-ssh-key-name"]),
          "-i", ",",
          "tasks/machineImage.yml"])
