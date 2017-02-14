## Get version
```
ansible --version
```

## ping
```
ansible lab -m ping
```

## Using limit
```
ansible-playbook --limit lab  -s playbooks/common.yaml
```

## Using tag
```
ansible-playbook --limit lab -s playbooks/common.yaml --tags "test"
```

## Debug
```
ansible-playbook --limit lab -s playbooks/common.yaml --step
ansible-playbook --limit lab -s playbooks/common.yaml --start-at-task "taskname"
```
