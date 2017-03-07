List key
```
etcdctl ls
etcdctl ls /coreos.com/
```

Get key (leaf)
```
etcdctl get /coreos.com/network/config
{"Network":"10.2.0.0/16","Backend":{"Type":"vxlan"}}
```

Check health
```
etcdctl cluster-health
cluster is healthy
```
