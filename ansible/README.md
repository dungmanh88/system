dbm_: dbadmin
ma_: mariadb
ngx_: nginx
pfm_: php-fpm

Copy ansible production if you need

Use example_ as sample config in group_vars, inventories, playbooks

change inventories/staging|production/all/vars.yaml
```
### For fresh servers
ansible_ssh_user: "{{ vault_default_ansible_ssh_user }}"
ansible_ssh_pass: "{{ vault_default_ansible_ssh_pass }}"

### For running servers
#ansible_ssh_user: "{{ vault_ansible_ssh_user }}"
#ansible_become_pass: "{{ vault_ansible_ssh_pass }}"
```

ansible -i inventories/staging|production/hosts.yaml group_name -m ping

ansible-playbook -i inventories/staging|production/hosts.yaml --limit group_name -s roles/init/create_deployer.yaml

change inventories/staging|production/all/vars.yaml
```
### For fresh servers
#ansible_ssh_user: "{{ vault_default_ansible_ssh_user }}"
#ansible_ssh_pass: "{{ vault_default_ansible_ssh_pass }}"

### For running servers
ansible_ssh_user: "{{ vault_ansible_ssh_user }}"
ansible_become_pass: "{{ vault_ansible_ssh_pass }}"
```

ansible-playbook -i inventories/staging|production/hosts.yaml --limit group_name -s playbooks/staging|production/group_name.yaml
