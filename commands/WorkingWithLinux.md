## SSH
### Copy public key
```
ssh-copy-id -i /path/to/public-key user@host
```

### Use key to commit code
If private key name is different
```
ssh-add ~/.ssh/id_rsa_xxx
git add -A; git commit -m "Add"; git push  -u origin master
git pull
```
or
```
ssh-agent bash -c 'ssh-add ~/.ssh/id_rsa_xxx; git add -A; git commit -m "Add"; git push  -u origin master'
ssh-agent bash -c 'ssh-add ~/.ssh/id_rsa_xxx; git pull'
```

## File
### Delete file in a path
```
find . -iname "*retry*" | xargs rm -f
```

### Check differences
Follow: https://askubuntu.com/questions/111495/how-to-diff-multiple-files-across-directories
```
diff -r dir1/ dir2/
```

### Create softlink
```
ln -s /path/to/origin/dir /path/to/symlink
```

## User management
### Get group and user
```
groups
cat /etc/passwd
```
