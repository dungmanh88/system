mkdir -p /etc/.ssh
copy private key to /etc/.ssh
ansible -i inventory all -m ping
make sure that you are able to ssh with key from ansible server to server in inventory.
