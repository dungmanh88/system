# Detect new size of existing block device
```
echo 1 > /sys/block/sdc/device/rescan
```

# Detect new block device
```
echo "- - -" >/sys/class/scsi_host/host0/scan
echo "- - -" >/sys/class/scsi_host/host1/scan
echo "- - -" >/sys/class/scsi_host/host2/scan
```

# Labeling block device
```
e2label /dev/sde1 TEST
```

# Show block device
```
lsblk
```
```
lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT
```
```
blkid
```

# format as ext4 fs
```
mkfs.ext4 /dev/sde1
```

# Check filesystem
```
e2fsck /dev/sde1
```

# Resize fs
```
resize2fs /dev/sde1
```

# Mount
```
mount -L TEST /test
or
mount /dev/sde1 /test
```

# Auto mount
vi /etc/fstab
```
LABEL=TEST                /data                   ext4 defaults 1 2
```

# View what process is keeping mountpoint
```
lsof <mountpoint>
```
