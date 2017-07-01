1 - Run install_ansible.sh on ansible server

2 - Run install_basic.sh on monitored server

3 - Make sure inventories/group_vars/all/vars.yaml
```
### For running servers
ansible_ssh_user: "{{ vault_ansible_ssh_user }}"
ansible_become_pass: "{{ vault_ansible_ssh_pass }}"
```
4 - Set group and host_vars in inventories file
hostname must distinct.
```
[development_test]
test1 ansible_host=xx.xx.xx.xx hostname=test1

[staging_test]
test2 ansible_host=yy.yy.yy.yy hostname=test2

[production_test]
test3 ansible_host=zz.zz.zz.zz hostname=test3
```

5 - Create group, set vars.yaml and/or vault.yaml

6 - Create playbook
```
- hosts: development_test
  roles:
    - role: common

- hosts: staging_test
  roles:
    - role: common

- hosts: production_test
  roles:
    - role: common
```

7 - Test
ansible -i inventories/hosts.yaml group_name -m ping

8 - Do it
ansible-playbook -i inventories/hosts.yaml --limit group_name -s playbooks/group_name.yaml

```
ansible-playbook --limit development_test -s playbooks/test.yaml
ansible-playbook --limit staging_test -s playbooks/test.yaml
ansible-playbook --limit production_test -s playbooks/test.yaml
```

9 - Debug
```
ansible-playbook --limit development_test -s playbooks/test.yaml --step
ansible-playbook --limit development_test -s playbooks/test.yaml --start-at-task="task name"
```
