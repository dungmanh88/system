# Start
```
parted /dev/sdc
```
You should choose a raw disk instead of a partition

# Select device or partition
```
(parted) select /dev/sdb
or
(parted) select /dev/sdb1
```

# List partition table
```
(parted) print
(parted) print all
```

# Make label
```
(parted) mklabel msdos
or
(parted) mklabel gpt
```

# Make a partition
```
(parted) mkpart primary 0% 100%
```

# Remove a partition
```
(parted) rm 1 ## partition id is 1
```

# Change partition flag
```
(parted) set 1 lvm on ## set flag lvm for partition id = 1
```
