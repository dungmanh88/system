make sure that you turn off selinux on ansible server and servers in inventory

mkdir -p /etc/.ssh
copy private key to /etc/.ssh
ansible -i inventory all -m ping
make sure that you are able to ssh with key from ansible server to server in inventory.

ansible-playbook -i inventory -s common.yml
ansible-playbook -i inventory/dbservers -s dbservers.yml

not yet:
ansible script for centos 7
ansible script for bacula backup agent
add route and nameserver for ansible script
ansible for service zone
