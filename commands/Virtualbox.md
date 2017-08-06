Mount
```
mount -t vboxsf share_name /mnt
```
Get virtualbox version
```
VBoxManage --version
```
Load virtualbox linux kernel module
```
/sbin/vboxconfig
```
Get name and uuid of vm
```
VBoxManage list vms
```
Start a vms
```
VBoxManage startvm <UUID-of-vm>
```
Poweroff a vms
```
VBoxManage controlvm <UUID-of-vm> poweroff
