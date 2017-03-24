```
gluster pool list
```

```
gluster peer status
```

```
gluster volume status vol-name
```

```
gluster volume info vol-name
```

https://gluster.readthedocs.io/en/latest/Administrator%20Guide/Managing%20Volumes/#tuning-options
```
gluster volume set vol-name key value
```

```
cat /proc/mounts
```

```
gluster volume list
```

# Reset config volume
```
gluster volume reset vol-name
```

# Stop/start volume
```
gluster volume stop vol-name
gluster volume start vol-name
```

# Check status remove-brick
```
gluster volume remove-brick vol-name removed-brick status
```
