dbm_: dbadmin
ma_: mariadb
ngx_: nginx
pfm_: php-fpm

change inventories/staging|production/all/vars.yaml
```
### For fresh servers
ansible_ssh_user: "{{ vault_default_ansible_ssh_user }}"
ansible_ssh_pass: "{{ vault_default_ansible_ssh_pass }}"

### For running servers
#ansible_ssh_user: "{{ vault_ansible_ssh_user }}"
#ansible_become_pass: "{{ vault_ansible_ssh_pass }}"
```

ansible -i inventories/staging|production/hosts.yaml group_name ping
