```
swapoff -a
swapon -a
```

Free page cache
```
echo 1 > /proc/sys/vm/drop_caches
```
Free dentries and inode
```
echo 2 > /proc/sys/vm/drop_caches
```
Free page cache, dentries and inode
```
echo 3 > /proc/sys/vm/drop_caches
```

```
smem -u
```

```
smem -m
```
