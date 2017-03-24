# Physical volume
## Scan block device used as physical volume
```
lvmdiskscan
```

## Display physical volume
```
pvdisplay
```
```
pvs
```
```
pvscan
```

## Prevent allocation extent on a specific physical volume
Disallow
```
pvchange -x n /dev/sdc1
```
Allow
```
pvchange -x y /dev/sdc1
```

## Remove
```
pvremove /dev/sdc1
```

## Resize
```
pvresize --setphysicalvolumesize 100G /dev/sdc1
```

# Volume group

## Adding physical volume
```
vgextent <vg-name> /dev/sdc1
```

## Reducing physical volume
```
vgreduce <vg-name> /dev/sdc1
```

## Display volume group
```
vgdisplay
```
```
vgs
```

## Scan physical volume
```
vgscan
```

## Active and deactive volume group
Deactive
```
vgchange -a n <vg-name>
```
Active
```
vgchange -a y <vg-name>
```

## Change maximum logical volume in a vg
```
vgchange -l 128 /dev/vg1 ## to 128 LV
```

## Rename
```
vgrename /dev/vg1 /dev/volgroup1
```

# Logical volume

## Display logical volume
```
lvs
```
```
lvs -a
```
```
lvdisplay
```
